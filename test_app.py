import unittest
import json
import os
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, db_drop_and_create_all, create_test_data, Movie
from dotenv import load_dotenv

load_dotenv()

user_name = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')


class AgencyTestCase(unittest.TestCase):
    """This class represents the Casting Agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "lav_cast_agency_TEST"
        # better: pass the db password as a secret/environment variable
        self.database_path = "postgresql://" + user_name + ":" + password + "@{}/{}".format('localhost:5432',
                                                                                            self.database_name)

        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

        # drop and create all tables for TEST db
        db_drop_and_create_all()
        create_test_data()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each endpoint for successful operation and for expected errors.
    """

    def test_SUCCESS_GET_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['movies'])
        self.assertTrue(len(data['movies']))

    def test_ERROR_GET_movies_empty_db(self):
        db_drop_and_create_all()
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_SUCCESS_GET_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['actors'])
        self.assertTrue(len(data['actors']))

    def test_ERROR_GET_actors_empty_db(self):
        db_drop_and_create_all()
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_SUCCESS_POST_movie(self):
        res = self.client().post('/movies', json={'title': 'TestDune',
                                                  'release_date': '1984-1-1'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_ERROR_POST_movie_wo_title(self):
        res = self.client().post('/movies', json={'release_date': '1984-1-1'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_SUCCESS_POST_actor(self):
        res = self.client().post('/actors', json={'name': 'TestActor',
                                                  'age': 20,
                                                  'gender': 'Male'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_ERROR_POST_actor_wo_name(self):
        res = self.client().post('/actors', json={'age': 20,
                                                  'gender': 'Male'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_SUCCESS_PATCH_movie(self):
        res = self.client().patch('/movies/1', json={'title': 'TestPatchDune',
                                                     'release_date': '2021-10-1'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_ERROR_PATCH_movie(self):
        # deleting nonexistent movie
        res = self.client().patch('/movies/-33', json={'title': 'TestPatchDune',
                                                     'release_date': '2021-10-1'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_SUCCESS_PATCH_actor(self):
        res = self.client().patch('/actors/1', json={'name': 'NewName',
                                                     'age': '25',
                                                     'gender': 'NewGender'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_ERROR_PATCH_actor(self):
        res = self.client().patch('/actors/-33', json={'name': 'NewName',
                                                     'age': '25',
                                                     'gender': 'NewGender'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_SUCCESS_DELETE_movie(self):
        res = self.client().delete('/movies/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_ERROR_DELETE_movie_wrong_id(self):
        res = self.client().delete('/movies/-33')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_SUCCESS_DELETE_actor(self):
        res = self.client().delete('/actors/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_ERROR_DELETE_actor_wrong_id(self):
        res = self.client().delete('/actors/-33')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


if __name__ == "__main__":
    unittest.main()