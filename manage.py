# manage.py

import datetime
import unittest

import coverage

from flask.cli import FlaskGroup
from faker import Faker

from project.server import create_app, db
from project.server.models import User
import subprocess
import sys

app = create_app()
cli = FlaskGroup(create_app=create_app)

# code coverage
COV = coverage.coverage(
    branch=True,
    include="project/*",
    omit=[
        "project/tests/*",
        "project/server/config.py",
        "project/server/*/__init__.py",
    ],
)
COV.start()


@cli.command()
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def drop_db():
    """Drops the db tables."""
    db.drop_all()


@cli.command()
def create_admin():
    """Creates the admin user."""
    db.session.add(User(
        name="admin",
        email="ad@min.com",
        password="admin",
        admin=True,
        activated=True,
        activated_on=datetime.datetime.now()
    ))
    db.session.commit()


@cli.command()
def create_data():
    """Creates sample data."""
    db.session.add(User(
        name="Example User",
        email="example@railstutorial.org",
        password="foobar",
        admin=False,
        activated=True,
        activated_on=datetime.datetime.now()
    ))
    db.session.commit()

    users = []
    names = []
    for n in range(99):
        fake = Faker()
        while fake.name() in names:
            fake = Faker()
        name = fake.name()
        email = f"example-{n+1}@railstutorial.org"
        password = "password"
        user = User(
            name=name,
            email=email,
            password=password,
            admin=False,
            activated=True,
            activated_on=datetime.datetime.now()
        )
        users.append(user)
    db.session.bulk_save_objects(users)


@cli.command()
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover("project/tests", pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        sys.exit(0)
    else:
        sys.exit(1)


@cli.command()
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover("project/tests")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print("Coverage Summary:")
        COV.report()
        COV.html_report()
        COV.erase()
        sys.exit(0)
    else:
        sys.exit(1)


@cli.command()
def flake():
    """Runs flake8 on the project."""
    subprocess.run(["flake8", "project"])


if __name__ == "__main__":
    cli()
