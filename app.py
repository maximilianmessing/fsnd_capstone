import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Movie, Actor


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  @app.route('/movies')
  def get_movies():
    movies = Movie.query.order_by(Movie.id).all()
    formatted_movies = [movie.format() for movie in movies]
    return jsonify({
      "success":True,
      "movies": formatted_movies
    })

  @app.route('/actors')
  def get_actors():
    actors = Actor.query.order_by(Actor.id).all()
    formatted_actors = [actor.format() for actor in actors]
    return jsonify({
      "success":True,
      "actors": formatted_actors
    })


  return app

app = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)

