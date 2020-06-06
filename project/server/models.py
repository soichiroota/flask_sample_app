# project/server/models.py

import datetime
from urllib.parse import quote
from secrets import token_urlsafe

from flask import current_app
from sqlalchemy.orm import synonym
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from project.server import db, bcrypt
from project.server.helpers.user_helper import gravatar_url_for
from project.server.mailers.user_mailer import UserMailer


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    _email = db.Column(db.String(255), unique=True, nullable=False)
    _password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    updated_on = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now
    )
    admin = db.Column(db.Boolean, nullable=False, default=False)
    activated = db.Column(db.Boolean, nullable=False, default=False)
    activated_on = db.Column(db.DateTime, nullable=True)
    microposts = db.relationship(
        "Micropost",
        backref="user",
        order_by="desc(Micropost.created_on)"
    )

    def __init__(
        self,
        name,
        email,
        password,
        admin=False,
        activated=False,
        activated_on=None
    ):
        self.name = name
        self._set_email(email)
        self._set_password(password)
        self.registered_on = datetime.datetime.now()
        self.admin = admin
        self.activated = activated
        self.activated_on = activated_on
        self.activation_token = None
        self.activation_digest = None

    def _get_email(self):
        return self._email

    def _set_email(self, email):
        self._email = email.lower()

    email_descriptor = property(_get_email, _set_email)
    email = synonym('_email', descriptor=email_descriptor)

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = User.get_digest(password)

    password_descriptor = property(_get_password, _set_password)
    password = synonym('_password', descriptor=password_descriptor)

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.activated

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def gravatar_url(self, size=80):
        return gravatar_url_for(self, size=size)

    @classmethod
    def get_digest(cls, string):
        return bcrypt.generate_password_hash(
            string,
            current_app.config.get("BCRYPT_LOG_ROUNDS")
        ).decode("utf-8")

    def get_token(self, expires_sec=1800):
        serializer = Serializer(
            current_app.config['SECRET_KEY'],
            expires_sec
        )
        return serializer.dumps(
            {'user_id': self.id}
        ).decode('utf-8')

    # 有効化トークンとダイジェストを作成および代入する
    def _create_activation_digest(self):
        self.activation_token = self.get_token()
        self.activation_digest = User.get_digest(
            self.activation_token
        )

    @classmethod
    def verify_token(cls, token):
        serializer = Serializer(current_app.config['SECRET_KEY'])
        user_id = serializer.loads(token).get('user_id')
        if user_id:
            return User.query.get(user_id)
        else:
            return None

    def send_activation_email(self):
        UserMailer.account_activation(self)

    def send_password_reset_email(self):
        UserMailer.password_reset(self)

    # アカウントを有効にする
    def activate(self):
        self.activated = True
        self.activated_on = datetime.datetime.now()

    def micropost_count(self):
        return len(self.microposts)

    def feed(self):
        return Micropost.query.filter_by(user_id=self.id).all()

    def __repr__(self):
        return "<User {0}>".format(self.email)


class Micropost(db.Model):
    __tablename__ = 'microposts'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(140))
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )
    _picture_name = db.Column(db.String(1023), unique=True)
    # user = db.relationship(User, primaryjoin=user_id == User.id)
    created_on = db.Column(db.DateTime, nullable=False)
    updated_on = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now
    )

    def __init__(self, content, user_id, picture_name=None):
        self.content = content
        self.user_id = user_id
        self.created_on = datetime.datetime.now()
        self._set_picture_name(picture_name)

    def _get_picture_name(self):
        return self._picture_name

    def _set_picture_name(self, picture_name):
        if picture_name:
            self._picture_name = token_urlsafe(
                self.user_id
            ) + quote(picture_name)
        else:
            self._picture_name = None

    picture_name_descriptor = property(
        _get_picture_name,
        _set_picture_name
    )
    picture_name = synonym(
        '_picture_name',
        descriptor=picture_name_descriptor
    )

    def created_on_in_words(self):
        return self.created_on.strftime('%Y-%m-%d %H:%M:%S')

    def updated_on_in_words(self):
        return self.updated_on.strftime('%Y-%m-%d %H:%M:%S')

    def __repr__(self):
        return '<Entry id={id} content={content!r}>'.format(
                id=self.id, content=self.content)
