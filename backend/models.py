from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
  __tablename__ = 'user'
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String, nullable=False, unique=True)
  password = db.Column(db.String, nullable=False)
  fullname = db.Column(db.String, nullable=False)
  admin_status = db.Column(db.Boolean, nullable=False, default=False)

class ParkingLot(db.Model):
  __tablename__ = 'parkinglot'
  id = db.Column(db.Integer, primary_key=True)
  location = db.Column(db.String, nullable=False)
  price = db.Column(db.Float, nullable=False)
  address = db.Column(db.String, nullable=False, unique=True)
  pincode = db.Column(db.String, nullable=False)
  max_spots = db.Column(db.Integer, nullable=False)
  spots = db.relationship('ParkingSpot', backref='lot', cascade='all, delete')

class ParkingSpot(db.Model):
  __tablename__ = 'parkingspot'
  id = db.Column(db.Integer, primary_key=True)
  lot_id = db.Column(db.Integer, db.ForeignKey('parkinglot.id'))
  status = db.Column(db.String, nullable=False, default='A')
  spot_num = db.Column(db.Integer, nullable=False)
  bookings = db.relationship('Reserved', backref='spot')

class Reserved(db.Model):
  __tablename__ = 'reserved'
  id = db.Column(db.Integer, primary_key=True)
  spot_id = db.Column(db.Integer, db.ForeignKey('parkingspot.id'))
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  parking_timestamp = db.Column(db.DateTime, nullable=False)
  leaving_timestamp = db.Column(db.DateTime)
  parking_cost = db.Column(db.Float)
  vehicle_num = db.Column(db.String, nullable=False)
  user = db.relationship('User', backref='reserve')

class BookingHistory(db.Model):
  __tablename__ = 'bookinghistory'
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, nullable=False)
  lot_id = db.Column(db.Integer, nullable=False)
  location = db.Column(db.String, nullable=False)
  spot_id = db.Column(db.Integer, nullable=False)
  vehicle_num = db.Column(db.String, nullable=False)
  parking_timestamp = db.Column(db.DateTime, nullable=False)
  leaving_timestamp = db.Column(db.DateTime, nullable=False)
  parking_cost = db.Column(db.Float, nullable=False)