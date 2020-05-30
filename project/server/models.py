# project/server/models.py


import datetime

from flask import current_app
from sqlalchemy.orm import synonym

from project.server import db, bcrypt
from project.server.helpers.user_helper import gravatar_url_for


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    _email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    updated_on = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now
    )
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, name, email, password, admin=False):
        self.name = name
        self._set_email(email)
        self.password = bcrypt.generate_password_hash(
            password, current_app.config.get("BCRYPT_LOG_ROUNDS")
        ).decode("utf-8")
        self.registered_on = datetime.datetime.now()
        self.admin = admin

    def _get_email(self):
        return self._email

    def _set_email(self, email):
        self._email = email.lower()

    email_descriptor = property(_get_email, _set_email)
    email = synonym('_email', descriptor=email_descriptor)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def gravatar_url(self, size=80):
        return gravatar_url_for(self, size=size)

    def __repr__(self):
        return "<User {0}>".format(self.email)
