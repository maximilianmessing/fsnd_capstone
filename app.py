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
        if movies == []:
            abort(404)
        formatted_movies = [movie.format() for movie in movies]
        return jsonify({
            "success": True,
            "movies": formatted_movies
        })

    @app.route('/movies', methods=["POST"])
    def create_movie():
        body = request.get_json()

        new_title = body.get('title', None)
        new_release_date = body.get('release_date', None)
        new_actors = body.get('actors', None)

        try:
            movie = Movie(title=new_title,
                          release_date=new_release_date)
            movie.insert()
            movies = Movie.query.order_by(Movie.id).all()
            formatted_movies = [movie.format() for movie in movies]
            return jsonify({
                "success": True,
                "movies": formatted_movies
            })
        except Exception:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=["PATCH"])
    def edit_movie(movie_id):
        body = request.get_json()

        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)

        # try:
        movie.title = body.get('title', None)
        movie.release_date = body.get('release_date', None)
        movie.actors = Actor.query.filter(Actor.id.in_(
            body.get('actors', None))).all()
        movie.update()
        movies = Movie.query.order_by(Movie.id).all()
        formatted_movies = [movie.format() for movie in movies]
        return jsonify({
            "success": True,
            "movies": formatted_movies
            })
        # except Exception:
        #     abort(422)

    @app.route('/movies/<int:movie_id>', methods=["DELETE"])
    def delete_movie(movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)
        try:
            movie.delete()
            movies = Movie.query.order_by(Movie.id).all()
            formatted_movies = [movie.format() for movie in movies]
            return jsonify({
                "success": True,
                "movies": formatted_movies
            })
        except Exception:
            abort(422)

    @app.route('/actors')
    def get_actors():
        actors = Actor.query.order_by(Actor.id).all()
        if actors == []:
            abort(404)
        formatted_actors = [actor.format() for actor in actors]
        return jsonify({
            "success": True,
            "actors": formatted_actors
        })

    @app.route('/actors', methods=["POST"])
    def create_actor():
        body = request.get_json()

        new_name = body.get('name', None)
        new_gender = body.get('gender', None)
        new_age = body.get('age', None)

        try:
            actor = Actor(name=new_name,
                          gender=new_gender, age=new_age)
            actor.insert()
            actors = Actor.query.order_by(Actor.id).all()
            formatted_actors = [actor.format() for actor in actors]
            return jsonify({
                "success": True,
                "actors": formatted_actors
            })
        except Exception:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=["PATCH"])
    def edit_actor(actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)

        body = request.get_json()

        try:
            actor.name = body.get('name', None)
            actor.gender = body.get('gender', None)
            actor.age = body.get('age', None)
            actor.update()
            actors = Actor.query.order_by(Actor.id).all()
            formatted_actors = [actor.format() for actor in actors]
            return jsonify({
                "success": True,
                "actors": formatted_actors
            })
        except Exception:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=["DELETE"])
    def delete_actor(actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)
        try:
            actor.delete()
            actors = Actor.query.order_by(Actor.id).all()
            formatted_actors = [actor.format() for actor in actors]
            return jsonify({
                "success": True,
                "actors": formatted_actors
            })
        except Exception:
            abort(422)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            "error": 404,
            "message": "Resource was not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            "error": 422,
            "message": "Unprocessable Entity"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            "error": 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(405)
    def method_not_found(error):
        return jsonify({
            'success': False,
            "error": 405,
            "message": "Method not found"
        }), 405

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            "error": 500,
            "message": "Internal Server error"
        }), 500

    return app


app = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
