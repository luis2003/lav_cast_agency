import unittest
import json
import os
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie
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
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each endpoint for successful operation and for expected errors.
    """

    def test_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['movies'])
        self.assertTrue(len(data['movies']))

    def test_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['actors'])
        self.assertTrue(len(data['actors']))


if __name__ == "__main__":
    unittest.main()