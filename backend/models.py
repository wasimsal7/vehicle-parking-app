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

