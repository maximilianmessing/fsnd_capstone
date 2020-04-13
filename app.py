from flask import Flask, request, abort, jsonify
from flask_cors import CORS

from models import setup_db, Movie, Actor

from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(token):
        movies = Movie.query.order_by(Movie.id).all()
        if movies == []:
            abort(404)
        formatted_movies = [movie.format() for movie in movies]
        return jsonify({
            "success": True,
            "movies": formatted_movies
        })

    @app.route('/movies', methods=["POST"])
    @requires_auth('post:movies')
    def create_movie(token):
        body = request.get_json()

        new_title = body.get('title', None)
        new_release_date = body.get('release_date', None)
        new_actors = Actor.query.filter(Actor.id.in_(
            body.get('actors', None))).all()

        try:
            movie = Movie(title=new_title,
                          release_date=new_release_date
                          )
            movie.actors = new_actors
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
    @requires_auth('patch:movies')
    def edit_movie(token, movie_id):
        body = request.get_json()

        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)

        try:
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
        except Exception:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=["DELETE"])
    @requires_auth('delete:movies')
    def delete_movie(token, movie_id):
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
    @requires_auth('get:actors')
    def get_actors(token):
        actors = Actor.query.order_by(Actor.id).all()
        if actors == []:
            abort(404)
        formatted_actors = [actor.format() for actor in actors]
        return jsonify({
            "success": True,
            "actors": formatted_actors
        })

    @app.route('/actors', methods=["POST"])
    @requires_auth('post:actors')
    def create_actor(token):
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
    @requires_auth('patch:actors')
    def edit_actor(token, actor_id):
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
    @requires_auth('delete:actors')
    def delete_actor(token, actor_id):
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

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    return app


app = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
