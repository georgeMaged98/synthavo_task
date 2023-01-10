import unittest
import json
from datetime import datetime
import time

DATABASE_URI = "postgresql://georgemaged@localhost:5432/ep_database_test"
from app import app
from helpers.db_helper import DBHelper
        
class GetEPSuccess(unittest.TestCase):

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
            from helpers.entities import User
            new_user = User(name='name 1', date= datetime.now())
            db.session.add(new_user)
            db.session.commit()
            print(new_user)
            print('Added User 1 to database')

    def test_successful_getEP(self):
        time.sleep(15)
        # When
        response = self.app.get('/getEP?userID=1')
        # Then
        # print(str(response.json))
        self.assertEqual(response.json['user']['name'], 'name 1')
        self.assertEqual(200, response.status_code)

    def tearDown(self):
        # Delete Database collections after the test is complete
        with app.app_context():
            self.db.drop_all()
