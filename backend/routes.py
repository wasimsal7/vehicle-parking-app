from flask import Blueprint, request, render_template, session, redirect, url_for
from .models import db, User

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
        return redirect(url_for('main.dashboard'))
      else:
        return redirect(url_for('main.dashboard'))
    else:
      return "Invalid credentials!"
  else:
    return render_template('/login.html')
  
@main.route('/dashboard') # test dashboard
def dashboard():
  return render_template('/dashboard.html')