import os

from unittest import TestCase

from app import app
from models import db, Follows, Likes, User, Message

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///warbler_test'))
app.config['SQLALCHEMY_ECHO'] = False
