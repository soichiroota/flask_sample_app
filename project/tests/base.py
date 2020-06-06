# project/server/tests/base.py
import datetime

from flask_testing import TestCase

from project.server import db, create_app
from project.server.models import User, Micropost

app = create_app()


class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object("project.server.config.TestingConfig")
        return app

    def setUp(self):
        self.base_title = "Flask Sample App"
        db.create_all()
        user1 = User(
            name="admin_user",
            email="ad@min.com",
            password="admin_user",
            admin=True,
            activated=True,
            activated_on=datetime.datetime.now()
        )
        user2 = User(
            name="admin_user2",
            email="ad2@min.com",
            password="admin_user2",
            activated=True,
            activated_on=datetime.datetime.now()
        )
        db.session.bulk_save_objects([user1, user2])
        user = User.query.first()
        micropost = Micropost(content="Lorem ipsum", user_id=user.id)
        db.session.add(micropost)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
