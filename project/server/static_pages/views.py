# project/server/static_pages/views.py
import os

from flask import (
    render_template, Blueprint, request,
    flash, current_app
)
from flask_login import current_user
from flask_paginate import Pagination, get_page_parameter
from werkzeug.utils import secure_filename

from project.server.models import Micropost
from project.server.micropost.forms import CreateMicropostForm
from project.server import db


static_pages_blueprint = Blueprint("static_pages", __name__)


@static_pages_blueprint.route("/static_pages/home/", methods=['GET', 'POST'])
def home():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    form = CreateMicropostForm(request.form)

    if form.validate_on_submit():
        form_for_picture = CreateMicropostForm()
        if form_for_picture.picture.data:
            f = form_for_picture.picture.data
            filename = secure_filename(f.filename)
            micropost = Micropost(
                user_id=current_user.id,
                content=form.content.data,
                picture_name=filename
            )
            f.save(os.path.join(
                current_app.config['UPLOAD_FOLDER'],
                'images',
                micropost.picture_name
            ))
            db.session.add(micropost)
            db.session.commit()
            flash("Micropost created!", "success")

    micropost = Micropost(
        content='',
        user_id=current_user.id
    ) if current_user.is_authenticated else None
    feed_items = current_user.feed() if current_user.is_authenticated else []
    pagination = Pagination(
        page=page,
        total=len(feed_items),
        search=False,
        record_name='microposts'
    )
    return render_template(
        "static_pages/home.html",
        micropost=micropost,
        form=form,
        feed_items=feed_items,
        pagination=pagination
    )


@static_pages_blueprint.route("/static_pages/help/")
def help():
    return render_template("static_pages/help.html")


@static_pages_blueprint.route("/static_pages/about/")
def about():
    return render_template("static_pages/about.html")


@static_pages_blueprint.route("/static_pages/contact/")
def contact():
    return render_template("static_pages/contact.html")
