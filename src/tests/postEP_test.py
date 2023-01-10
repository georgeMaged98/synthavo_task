import unittest
import json
from datetime import datetime


DATABASE_URI = "postgresql://georgemaged@localhost:5432/ep_database_test"
from app import app
from helpers.db_helper import DBHelper
        
class PostEPTest(unittest.TestCase):
  
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        db = DBHelper()

        db.init_app(app)
        with app.app_context():
        # Run this file directly to create the database tables.
            print("Creating database tables...")
            db.create_all()
            print("Done!")
            self.app = app.test_client()
            self.db = db

    def test_successful_postEP(self):
        # Given
        payload = json.dumps({
            "name": "test name"
        })

        # When
        response = self.app.post('/postEP', headers={"Content-Type": "application/json"}, data=payload)
        # Then
        self.assertEqual(response.json['id'], 1)
        self.assertEqual(200, response.status_code)

    def tearDown(self):
        # Delete Database collections after the test is complete
        with app.app_context():
            self.db.drop_all()
