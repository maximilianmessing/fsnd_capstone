import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor


class CastingTestCase(unittest.TestCase):
    """This class represents the casting test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_actor = {'name': 'Maximilian Messing',
                          'age': 25,
                          'gender': 'female',
                          }
        self.new_invalid_actor = {'name': 'Maximilian Messing',
                                  'age': 'twenty five',
                                  'gender': 'female',
                                  }
        self.new_movie = {'title': 'Terminator',
                          'release_date': '2002-12-04',
                          'actors': [1],
                          }
        self.new_invalid_movie = {'name': 'Terminator',
                                  'release_date': "hey there",
                                  'actors': [1],
                                  }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_0_get_empty_movie_404(self):
        res = self.client().get('movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Resource was not found")

    def test_0_get_empty_actor_404(self):
        res = self.client().get('actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Resource was not found")

    def test_1_post_actors(self):
        res = self.client().post('actors', json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['actors']), 1)

    def test_post_invalid_actors_yield_422(self):
        res = self.client().post('actors', json=self.new_invalid_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unprocessable Entity")

    def test_1_post_movies(self):
        res = self.client().post('movies', json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['movies']), 1)

    def test_post_invalid_movies_yield_422(self):
        res = self.client().post('movies', json=self.new_invalid_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unprocessable Entity")

    def test_2_get_actors(self):
        res = self.client().get('actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['actors']), 1)

    def test_2_get_movies(self):
        res = self.client().get('movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['movies']), 1)

    def test_patch_non_existing_actor_yield_404(self):
        res = self.client().patch('actors/5', json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Resource was not found")

    def test_patch_non_existing_movie_yield_404(self):
        res = self.client().patch('movies/5', json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Resource was not found")

    def test_3_delete_movie(self):
        res = self.client().delete('movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['movies']), 0)

    def test_3_delete_actor(self):
        res = self.client().delete('actors/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['actors']), 0)

    def test_delete_non_existing_actor_yield_404(self):
        res = self.client().delete('actors/5')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Resource was not found")

    def test_delete_non_existing_movie_yield_404(self):
        res = self.client().delete('movies/5')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Resource was not found")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
