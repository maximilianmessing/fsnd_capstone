import os
from sqlalchemy import Column, String, Integer, create_engine, Date
from flask_sqlalchemy import SQLAlchemy
import json

# postgres://localhost:5432/casting

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Movie(db.Model):
  __tablename__ = 'movie'

  id = Column(Integer, primary_key=True)
  title = Column(String)
  release_date = Column(Date)
  artists = db.relationship('artist', backref='movie', lazy=True)

class Artist(db.Model):
  __tablename__ ='artist'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  gender =  Column(Integer)


