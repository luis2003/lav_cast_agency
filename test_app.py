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
        self.casting_assistant = os.environ.get('ASSISTANT')
        self.casting_director = os.environ.get('DIRECTOR')
        self.executive_producer = os.environ.get('PRODUCER')
        self.new_actor = {'name': 'TestActor',
                          'age': 20,
                          'gender': 'Male'}
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

    def test_SUCCESS_ASSISTANT_GET_movies(self):
        res = self.client().get('/movies', headers={"Authorization": "Bearer {}".format(
                                    self.casting_assistant)
                                    })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['movies'])
        self.assertTrue(len(data['movies']))

    def test_ERROR_ASSISTANT_GET_movies_empty_db(self):
        db_drop_and_create_all()
        res = self.client().get('/movies', headers={"Authorization": "Bearer {}".format(
                                    self.casting_assistant)
                                    })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_SUCCESS_ASSISTANT_GET_actors(self):
        res = self.client().get('/actors', headers={"Authorization": "Bearer {}".format(
                                    self.casting_assistant)
                                    })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['actors'])
        self.assertTrue(len(data['actors']))

    def test_ERROR_ASSISTANT_GET_actors_empty_db(self):
        db_drop_and_create_all()
        res = self.client().get('/actors', headers={"Authorization": "Bearer {}".format(
                                    self.casting_assistant)
                                    })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_SUCCESS_PRODUCER_POST_movie(self):
        res = self.client().post('/movies', json={'title': 'TestDune',
                                                  'release_date': '1984-1-1'}, headers=
                                                 {"Authorization": "Bearer {}".format(
                                                    self.executive_producer)
                                                  })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_UNAUTH_ERROR_ASSISTANT_POST_movie(self):
        res = self.client().post('/movies', json={'title': 'TestDune',
                                                  'release_date': '1984-1-1'}, headers=
                                                 {"Authorization": "Bearer {}".format(
                                                    self.casting_assistant)
                                                  })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_ERROR_PRODUCER_POST_movie_wo_title(self):
        res = self.client().post('/movies', json={'release_date': '1984-1-1'}, headers=
                                                 {"Authorization": "Bearer {}".format(
                                                    self.executive_producer)
                                                  })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_SUCCESS_DIRECTOR_POST_actor(self):
        res = self.client().post('/actors', json=self.new_actor, headers=
                                                 {"Authorization": "Bearer {}".format(
                                                    self.casting_director)
                                                  })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_ERROR_DIRECTOR_POST_actor_wo_name(self):
        res = self.client().post('/actors', json={'age': 20,
                                                  'gender': 'Male'}, headers=
                                                 {"Authorization": "Bearer {}".format(
                                                    self.casting_director)
                                                  })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_SUCCESS_DIRECTOR_PATCH_movie(self):
        res = self.client().patch('/movies/1', json={'title': 'TestPatchDune',
                                                     'release_date': '2021-10-1'}, headers=
                                                 {"Authorization": "Bearer {}".format(
                                                    self.casting_director)
                                                  })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_ERROR_DIRECTOR_PATCH_movie(self):
        # deleting nonexistent movie
        res = self.client().patch('/movies/-33', json={'title': 'TestPatchDune',
                                                     'release_date': '2021-10-1'}, headers=
                                                 {"Authorization": "Bearer {}".format(
                                                    self.casting_director)
                                                  })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_SUCCESS_PRODUCER_PATCH_actor(self):
        res = self.client().patch('/actors/1', json={'name': 'NewName',
                                                     'age': '25',
                                                     'gender': 'NewGender'}, headers=
                                                 {"Authorization": "Bearer {}".format(
                                                    self.executive_producer)
                                                  })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_ERROR_DIRECTOR_PATCH_actor(self):
        res = self.client().patch('/actors/-33', json={'name': 'NewName',
                                                     'age': '25',
                                                     'gender': 'NewGender'}, headers=
                                                 {"Authorization": "Bearer {}".format(
                                                    self.casting_director)
                                                  })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_SUCCESS_PRODUCER_DELETE_movie(self):
        res = self.client().delete('/movies/1', headers=
                                                 {"Authorization": "Bearer {}".format(
                                                    self.executive_producer)
                                                  })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_UNAUTH_ERROR_DIRECTOR_DELETE_movie(self):
        res = self.client().delete('/movies/1', headers=
                                                 {"Authorization": "Bearer {}".format(
                                                    self.casting_director)
                                                  })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_ERROR_PRODUCER_DELETE_movie_wrong_id(self):
        res = self.client().delete('/movies/-33', headers=
                                                 {"Authorization": "Bearer {}".format(
                                                    self.executive_producer)
                                                  })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_SUCCESS_DIRECTOR_DELETE_actor(self):
        res = self.client().delete('/actors/1', headers=
                                                 {"Authorization": "Bearer {}".format(
                                                    self.casting_director)
                                                  })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_ERROR_DIRECTOR_DELETE_actor_wrong_id(self):
        res = self.client().delete('/actors/-33', headers=
                                                 {"Authorization": "Bearer {}".format(
                                                    self.casting_director)
                                                  })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_UNAUTH_ERROR_ASSISTANT_POST_actor(self):
        res = self.client().post('/actors',
                                 headers={"Authorization": "Bearer {}".format(
                                    self.casting_assistant)
                                    }, json=self.new_actor)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['message'], 'Permission not found')


if __name__ == "__main__":
    unittest.main()