import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db

import requests

# testing user password database:
testingUsers = {
    'messing.maximilian+executive@gmail.com': 'executive123!',
    'messing.maximilian+director@gmail.com': 'director123!',
    'messing.maximilian+assistant@gmail.com': 'assistant123!',
}

# Taken from https://stackoverflow.com/questions/48552474/
# auth0-obtain-access-token-for-unit-tests-in-python/48554119#48554119


def getUserToken(userName):
    url = 'https://wcp.eu.auth0.com/oauth/token'
    headers = {'content-type': 'application/json'}
    client_secret =\
        "0L9AdpWZfeXfXAqUOflWqXEWur7fFGPTO_bmxBj4R4M-RN14MISOCOgNvmqA-t80"
    password = testingUsers[userName]
    parameter = {"client_id": "UEjRDlMUtQ4GLe5wiKgTRfALDsk35Gee",
                 "client_secret": client_secret,
                 "audience": 'casting',
                 "grant_type": "password",
                 "username": userName,
                 "password": password, "scope": "openid"}
    # do the equivalent of a CURL request from https://auth0.com/docs/
    # quickstart/
    # backend/python/02-using#obtaining-an-access-token-for-testing
    responseDICT = json.loads(requests.post(
        url, json=parameter, headers=headers).text)
    return responseDICT['access_token']


def getUserTokenHeaders(userName='testingUser2@funnymail.com'):
    return {'authorization': "Bearer " + getUserToken(userName)}


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
                          'gender': 'male',
                          }
        self.new_invalid_actor = {'name': 'Maximilian Messing',
                                  'age': 'twenty five',
                                  'gender': 'male',
                                  }
        self.new_movie = {'title': 'Terminator',
                          'release_date': '2002-12-04',
                          'actors': [1],
                          }
        self.new_invalid_movie = {'name': 'Terminator',
                                  'release_date': "hey there",
                                  'actors': [1],
                                  }
        self.auth_header_executive = AUTH_HEADER_EXECUTIVE
        self.auth_header_director = AUTH_HEADER_DIRECTOR
        self.auth_header_assistant = AUTH_HEADER_ASSISTANT

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

# All test use executive producer permission as he has all permission.
# Other RBAC Tests are at the end of the file.

    def test_0_get_empty_movie_404(self):
        res = self.client().get('movies', headers=self.auth_header_executive)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Resource was not found")

    def test_0_get_empty_actor_404(self):
        res = self.client().get('actors', headers=self.auth_header_executive)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Resource was not found")

    def test_1_post_actors(self):
        res = self.client().post('actors', json=self.new_actor,
                                 headers=self.auth_header_executive)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['actors']), 1)

    def test_post_invalid_actors_yield_422(self):
        res = self.client().post('actors', json=self.new_invalid_actor,
                                 headers=self.auth_header_executive)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unprocessable Entity")

    def test_1_post_movies(self):
        res = self.client().post('movies', json=self.new_movie,
                                 headers=self.auth_header_executive)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['movies']), 1)

    def test_post_invalid_movies_yield_422(self):
        res = self.client().post('movies', json=self.new_invalid_movie,
                                 headers=self.auth_header_executive)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unprocessable Entity")

    def test_2_get_actors(self):
        res = self.client().get('actors', headers=self.auth_header_executive)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['actors']), 1)

    def test_2_get_movies(self):
        res = self.client().get('movies', headers=self.auth_header_executive)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['movies']), 1)

    def test_patch_non_existing_actor_yield_404(self):
        res = self.client().patch('actors/5', json=self.new_actor,
                                  headers=self.auth_header_executive)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Resource was not found")

    def test_patch_non_existing_movie_yield_404(self):
        res = self.client().patch('movies/5', json=self.new_movie,
                                  headers=self.auth_header_executive)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Resource was not found")

    def test_2_patch_actors(self):
        res = self.client().patch('actors/1',
                                  json={'name': 'Maximilian Messing',
                                        'age': 25,
                                        'gender': 'male',
                                        }, headers=self.auth_header_executive)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['actors']), 1)

    def test_2_patch_movies(self):
        res = self.client().patch('movies/1',
                                  json={'title': 'Terminator',
                                        'release_date': '2012-12-04',
                                        'actors': [1],
                                        },
                                  headers=self.auth_header_executive)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['movies']), 1)

    def test_3_delete_movie(self):
        res = self.client().delete('movies/1',
                                   headers=self.auth_header_executive)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['movies']), 0)

    def test_3_delete_actor(self):
        res = self.client().delete('actors/1',
                                   headers=self.auth_header_executive)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['actors']), 0)

    def test_delete_non_existing_actor_yield_404(self):
        res = self.client().delete('actors/5',
                                   headers=self.auth_header_executive)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Resource was not found")

    def test_delete_non_existing_movie_yield_404(self):
        res = self.client().delete('movies/5',
                                   headers=self.auth_header_executive)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Resource was not found")

    # RBAC TESTS
    # A casting assistant should view actors but not create new movies

    def test_2_get_actors_assistant(self):
        res = self.client().get('actors',
                                headers=self.auth_header_assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['actors']), 1)

    def test_post_actors_not_allowed_assistant(self):
        res = self.client().post('actors', json=self.new_invalid_actor,
                                 headers=self.auth_header_assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['description'], "Permission not found.")
        self.assertEqual(data['code'], "unauthorized")

    # A casting director can add and delete actor but not delete or add movies

    def test_4_post_actors_director(self):
        res = self.client().post('actors', json=self.new_actor,
                                 headers=self.auth_header_director)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['actors']), 1)

    def test_5_delete_actor_director(self):
        res = self.client().delete('actors/2',
                                   headers=self.auth_header_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['actors']), 0)

    def test_5_post_movies_director_yield_403(self):
        res = self.client().post('movies', json=self.new_movie,
                                 headers=self.auth_header_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['description'], "Permission not found.")
        self.assertEqual(data['code'], "unauthorized")


# Make the tests conveniently executable
if __name__ == "__main__":
    AUTH_HEADER_EXECUTIVE = getUserTokenHeaders(
        'messing.maximilian+executive@gmail.com')
    AUTH_HEADER_DIRECTOR = getUserTokenHeaders(
        'messing.maximilian+director@gmail.com')
    AUTH_HEADER_ASSISTANT = getUserTokenHeaders(
        'messing.maximilian+assistant@gmail.com')
    # You can use the print method to print the token for Testing
    # print(AUTH_HEADER_EXECUTIVE)
    unittest.main()
