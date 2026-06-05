from flask import Flask
from models import db
from routes import main

def create_app():
  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
  app.config['SECRET_KEY'] = 'random-secret-key'
  
  db.init_app(app)
  app.register_blueprint(main)

  with app.app_context():
    db.create_all()
  
  return app

app = create_app()

if __name__ == '__main__':
  app.run(debug=True)