from flask import Blueprint, request, render_template, session, redirect, url_for
from .models import db, User, ParkingLot, ParkingSpot

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
  return render_template('/admin/admin_dashboard.html')

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

# user

@main.route('/user/dashboard')
def user_dashboard():
  return render_template('/user/user_dashboard.html')

