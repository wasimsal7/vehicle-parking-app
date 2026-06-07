from flask import Flask
from .models import db, User
from .routes import main
import os

def create_app():
  app = Flask(__name__, 
              template_folder=os.path.join('..', 'templates'), 
              static_folder=os.path.join('..', 'static'),)
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
  app.config['SECRET_KEY'] = 'random-secret-key'
  
  db.init_app(app)
  app.register_blueprint(main)

  with app.app_context():
    db.create_all()
    if not User.query.filter_by(admin_status=True).first():
      admin = User(email='admin@gmail.com', fullname='admin', password='admin123', admin_status=True)
      db.session.add(admin)
      db.session.commit()
  
  return app