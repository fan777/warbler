"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from sqlalchemy.exc import IntegrityError

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test model for Users."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()
        
        u1 = User.signup('test1', 'test1@test.com', 'password', None)
        u2 = User.signup('test2', 'test2@test.com', 'password', None)
        db.session.commit()

        self.u1 = u1
        self.u2 = u2

        self.client = app.test_client()
    
    def tearDown(self):
        db.session.rollback()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)
    
    def test_is_following(self):
        self.u1.following.append(self.u2)
        db.session.commit()
        self.assertTrue(self.u1.is_following(self.u2))
        self.assertFalse(self.u2.is_following(self.u1))

    def test_is_followed_by(self):
        self.u1.following.append(self.u2)
        db.session.commit()
        self.assertTrue(self.u2.is_followed_by(self.u1))
        self.assertFalse(self.u1.is_followed_by(self.u2))

    def test_signup(self):
        self.assertEqual(self.u1.username, 'test1')
        self.assertEqual(self.u1.email, 'test1@test.com')

    def test_unique_username(self):
        u_duplicate = User.signup('test1', 'test1@test.com', 'password', None)
        self.assertRaises(IntegrityError, db.session.commit)
    
    def test_missing_username(self):
        u_missing_username = User.signup(None, 'test@test.com', 'password', None)
        self.assertRaises(IntegrityError, db.session.commit)
    
    def test_missing_email(self):
        u_missing_email = User.signup('test3', None, 'password', None)
        self.assertRaises(IntegrityError, db.session.commit)
    
    def test_authentication(self):
        u = User.authenticate(self.u1.username, 'password')
        self.assertTrue(u)
        self.assertEqual(u.id, self.u1.id)
    
    def test_nonexistent_user(self):
        u = User.authenticate('abc', 'password')
        self.assertFalse(u)

    def test_bad_password(self):
        u = User.authenticate(self.u1.username, 'asdfasdf')
        self.assertFalse(u)