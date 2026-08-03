from flask import Blueprint, request, render_template, session, redirect, url_for, current_app
from .models import db, User, ParkingLot, ParkingSpot, Reserved, BookingHistory
from datetime import datetime
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

main = Blueprint('main', __name__)

@main.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    email = request.form['email']
    fullname = request.form['fullname']
    password = request.form['password']
    user = User.query.filter_by(email=email).first()
    if user:
      return "Email already taken!"
    new_user = User(email=email, fullname=fullname, password=password)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('main.login'))
  else:
    return render_template('/register.html')

@main.route('/')
@main.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(email=email).first()
    if user and password == user.password:
      session['user_id'] = user.id
      session['user_email'] = user.email
      session['user_fullname'] = user.fullname
      session['admin_status'] = user.admin_status
      if session['admin_status']:
        return redirect(url_for('main.admin_dashboard'))
      else:
        return redirect(url_for('main.user_dashboard'))
    else:
      return "Invalid credentials!"
  else:
    return render_template('/login.html')
  
@main.route('/logout')
def logout():
  session.clear()
  return redirect(url_for('main.login'))

# admin

@main.route('/admin/dashboard')
def admin_dashboard():
  reserved = Reserved.query.all()
  return render_template('/admin/admin_dashboard.html', reserved=reserved)

@main.route('/admin/users')
def users():
  users = User.query.all()
  return render_template('/admin/users.html', users=users)

@main.route('/admin/add_lot', methods=['GET', 'POST'])
def add_lot():
  if request.method == 'POST':
    location = request.form['location']
    price = request.form['price']
    address = request.form['address']
    pincode = request.form['pincode']
    max_spots = int(request.form['max_spots'])
    lot = ParkingLot(location=location, price=price, address=address, pincode=pincode, max_spots=max_spots)
    db.session.add(lot)
    db.session.commit()

    for i in range(1, max_spots + 1):
      spot = ParkingSpot(lot_id=lot.id, spot_num=i)
      db.session.add(spot)
    db.session.commit()
    return redirect(url_for('main.admin_dashboard'))
  else:
    return render_template('/admin/add_lot.html')
  
@main.route('/admin/lots')
def lots():
  lots = ParkingLot.query.all()
  return render_template('/admin/lots.html', lots=lots)

@main.route('/admin/edit_lot/<int:lot_id>', methods=['GET', 'POST'])
def edit_lot(lot_id):
  lot = ParkingLot.query.get(lot_id)
  
  if request.method == 'POST':
    action = request.form.get('action')
    lot_id = request.form.get('lot_id')

    if action == 'update':
      new_maxspots = int(request.form['new_maxspots'])
      occupied_size = ParkingSpot.query.filter_by(lot_id=lot_id, status='O').count()

      if new_maxspots >= occupied_size:
        old_maxspots = lot.max_spots
        lot.max_spots = new_maxspots

        if new_maxspots > old_maxspots:
          for i in range(old_maxspots + 1, new_maxspots + 1):
            spot = ParkingSpot(lot_id=lot_id, spot_num=i)
            db.session.add(spot)
          db.session.commit()

        elif new_maxspots < old_maxspots:
          extra = ParkingSpot.query.filter(ParkingSpot.lot_id==lot_id, ParkingSpot.spot_num > new_maxspots).all()
          for spot in extra:
            db.session.delete(spot)
          db.session.commit()

      else:
        return "New spot count can't be less than occupied spot count!"
    
    elif action == 'delete':
      empty = True
      for spot in lot.spots:
        if spot.status == 'O':
          empty = False
          break
      if empty:
        db.session.delete(lot)
        db.session.commit()
        return redirect(url_for('main.lots'))
      else:
        return "Non-empty lots cannot be deleted!"
      
    return render_template('/admin/edit_lot.html', lot=lot)
      
  else:
    return render_template('/admin/edit_lot.html', lot=lot)

@main.route('/admin/reserved')
def reserved():
  reserved = Reserved.query.all()
  return render_template('/admin/reserved.html', reserved=reserved)

@main.route('/admin/history')
def history():
  history = BookingHistory.query.all()
  return render_template('/admin/history.html', history=history)

@main.route('/admin/spots')
def spots():
  spots = ParkingSpot.query.all()
  return render_template('/admin/spots.html', spots=spots)

@main.route('/admin/admin_summary')
def admin_summary():
  lots = ParkingLot.query.all()
  labels = []
  available_count = []
  occupied_count = []
  
  for lot in lots:
    labels.append("Lot " + str(lot.id))
    occupied = ParkingSpot.query.filter_by(lot_id=lot.id, status='O').count()
    available = ParkingSpot.query.filter_by(lot_id=lot.id, status='A').count()
    occupied_count.append(occupied)
    available_count.append(available)
  
  fig, ax = plt.subplots(figsize=(6, 5))
  x = range(len(labels))

  ax.bar(x, occupied_count, label='Occupied', color='red')

  ax.bar(x, available_count, bottom=occupied_count, label='Available', color='green')

  ax.set_ylabel('Number of Spots')
  ax.set_title('Parking Spot Status')
  ax.set_xticks(x)
  ax.set_xticklabels(labels)
  ax.legend()

  plt.tight_layout()

  images_dir = os.path.join(current_app.static_folder, 'images')
  os.makedirs(images_dir, exist_ok=True)
  chart_path = os.path.join(images_dir, 'summary_chart.png')
  plt.savefig(chart_path)
  plt.close()

  return render_template('/admin/admin_summary.html')

# user

@main.route('/user/dashboard', methods=['GET', 'POST'])
def user_dashboard():
  user_id = session.get('user_id')
  fullname = session.get('user_fullname')
  
  if request.method == 'POST':
    spot_id = request.form['release_spot']
    booking = Reserved.query.filter_by(user_id=user_id, spot_id=spot_id, leaving_timestamp=None).first()
    spot = ParkingSpot.query.get(spot_id)
    if booking and spot:
      spot.status = 'A'
      booking.leaving_timestamp = datetime.now()

      duration = booking.leaving_timestamp - booking.parking_timestamp
      seconds = duration.total_seconds()
      hours = seconds / 3600
      booking.parking_cost = round(booking.spot.lot.price * hours, 2)
      
      history = BookingHistory(user_id=booking.user_id, lot_id=booking.spot.lot_id, location=booking.spot.lot.location, spot_id=booking.spot_id, vehicle_num=booking.vehicle_num, parking_timestamp=booking.parking_timestamp, leaving_timestamp=booking.leaving_timestamp, parking_cost=booking.parking_cost)
      
      db.session.delete(booking)
      db.session.add(history)
      db.session.commit()
      return redirect(url_for('main.user_dashboard'))
  
  else:
    booking = Reserved.query.filter_by(user_id=user_id, leaving_timestamp=None).first()
  
    booking_history = BookingHistory.query.filter_by(user_id=user_id)
    
    return render_template('/user/user_dashboard.html', fullname=fullname, booking=booking, booking_history=booking_history)

@main.route('/user/booking')
def booking():
  lots = ParkingLot.query.all()
  for lot in lots:
    lot.available = False
    for spot in lot.spots:
      if spot.status == 'A':
        lot.available = True
        break
  return render_template('/user/booking.html', lots=lots)

@main.route('/user/book/<int:lot_id>', methods=['GET', 'POST'])
def book(lot_id):
  lot = ParkingLot.query.get(lot_id)
  
  if request.method == 'POST':
    user_id = session.get('user_id')
    if not user_id:
      return redirect(url_for('main.login'))
    
    booking = Reserved.query.filter_by(user_id=user_id, leaving_timestamp=None).first()
    if booking:
      return "You have already booked a spot. Release it first."
    
    lot_id = request.form['lot_id']
    vehicle_num = request.form['vehicle_num']
    spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='A').first()
    if not spot:
      return "No available spots in this lot."
    
    new_booking = Reserved(user_id=user_id, spot_id=spot.id, vehicle_num=vehicle_num, parking_timestamp=datetime.now())
    spot.status = 'O' 
    db.session.add(new_booking)
    db.session.commit()
    return redirect(url_for('main.user_dashboard'))
  
  else:
    return render_template('/user/book.html', lot=lot)

@main.route('/user/summary')
def user_summary():
  user_id = session.get('user_id')
  durations = []
  labels = []

  bookings = BookingHistory.query.filter_by(user_id=user_id).all()
  
  for booking in bookings:
    duration = (booking.leaving_timestamp - booking.parking_timestamp).total_seconds() / 60 
    durations.append(duration)

  n = len(durations)
  for i in range(1, n + 1) :
    labels.append("Booking " + str(i))

  fig, ax = plt.subplots(figsize=(6, 5))
  x = range(len(labels))

  ax.bar(x, durations, color='orange')
  ax.set_xticks(x)
  ax.set_xticklabels(labels)
  ax.set_ylabel('Time Spent (minutes)')
  ax.set_title('Time Spent in Each Booking')

  plt.tight_layout()

  images_dir = os.path.join(current_app.static_folder, 'images')
  os.makedirs(images_dir, exist_ok=True)
  chart_path = os.path.join(images_dir, 'user_booking_duration.png')
  plt.savefig(chart_path)
  plt.close()

  return render_template('/user/user_summary.html')
