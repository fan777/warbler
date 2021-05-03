"""Message model tests."""

# run these tests like:
#
#    python -m unittest test_message_model.py


import os
from unittest import TestCase

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


class MessageModelTestCase(TestCase):
    """Test model for Messagse."""

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
    
    def test_message_model(self):
        """Does basic model work?"""

        m = Message(text="test@test.com", user_id=self.u1.id)

        db.session.add(m)
        db.session.commit()

        # User should have 1 messages
        self.assertEqual(len(self.u1.messages), 1)
    
    def test_message_likes(self):
        m1 = Message(text='abcdefg', user_id=self.u1.id)
        m2 = Message(text='hijklmn', user_id=self.u1.id)

        self.u1.likes.append(m2)
        db.session.commit()
        
        self.assertEqual(len(self.u1.likes), 1)
        self.assertTrue(m2 in self.u1.likes)
        self.assertFalse(m1 in self.u1.likes)