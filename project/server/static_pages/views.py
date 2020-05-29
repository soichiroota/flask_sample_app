# project/server/static_pages/views.py


from flask import render_template, Blueprint


static_pages_blueprint = Blueprint("static_pages", __name__)


@static_pages_blueprint.route("/static_pages/home/")
def home():
    return render_template("static_pages/home.html")


@static_pages_blueprint.route("/static_pages/help/")
def help():
    return render_template("static_pages/help.html")


@static_pages_blueprint.route("/static_pages/about/")
def about():
    return render_template("static_pages/about.html")


@static_pages_blueprint.route("/static_pages/contact/")
def contact():
    return render_template("static_pages/contact.html")
