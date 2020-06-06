# project/server/user/views.py


from flask import (
    render_template, Blueprint, url_for, redirect,
    flash, request, abort, jsonify
)
from flask_login import (
    login_user, logout_user, login_required, current_user
)
from flask_paginate import Pagination, get_page_args

from project.server import bcrypt, db
from project.server.models import User
from project.server.user.forms import LoginForm, RegisterForm
from project.server.helpers.user_helper import gravatar_url_for


user_blueprint = Blueprint("user", __name__)


@user_blueprint.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()

        login_user(user)

        flash("Thank you for registering.", "success")
        return redirect(url_for("user.show", user_id=user.id))

    return render_template("user/register.html", form=form)


@user_blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(
            email=form.email.data.lower()
        ).first()
        if user and bcrypt.check_password_hash(
            user.password, request.form["password"]
        ):
            login_user(user, remember=form.remember_me.data)
            flash("You are logged in. Welcome!", "success")
            return redirect(url_for("user.show", user_id=user.id))
        else:
            flash("Invalid email and/or password.", "danger")
            return render_template("user/login.html", form=form)
    return render_template("user/login.html", title="Please Login", form=form)


@user_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You were logged out. Bye!", "success")
    return redirect(url_for("main.home"))


@user_blueprint.route("/members")
@login_required
def members():
    page, per_page, offset = get_page_args(
        page_parameter='page',
        per_page_parameter='per_page'
    )

    users = User.query.all()
    pagination = Pagination(
        page=page,
        per_page=per_page,
        total=len(users),
        search=False,
        record_name='users',
        css_framework='bootstrap4'
    )
    return render_template(
        "user/members.html",
        users=users[offset: offset + per_page],
        pagination=pagination
    )


@user_blueprint.route('/users/<int:user_id>/')
@login_required
def show(user_id):
    user = User.query.get(user_id)
    gravatar_url = gravatar_url_for(user)
    return render_template(
        'user/show.html',
        user=user,
        gravatar_url=gravatar_url
    )


@user_blueprint.route('/users/<int:user_id>/edit/', methods=['GET', 'POST'])
@login_required
def edit(user_id):
    user = User.query.get(user_id)
    if user is None:
        abort(404)
    if user_id != current_user.id:
        return redirect(url_for('static_pages.home'))
    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']
        user.password = request.form['password']
        db.session.add(user)
        db.session.commit()
        flash("Profile updated", "success")
        return redirect(url_for(
            'user.show',
            user_id=user_id,
            gravatar_url=gravatar_url_for(user)
        ))
    form = RegisterForm(request.form)
    form.name.data = user.name
    form.email.data = user.email
    return render_template(
        'user/edit.html',
        user=user,
        form=form,
        gravatar_url=gravatar_url_for(user)
    )


@user_blueprint.route('/users/<int:user_id>/delete/', methods=['DELETE'])
@login_required
def delete(user_id):
    if not current_user.admin:
        return redirect(url_for('static_pages.home'))
    user = User.query.get(user_id)
    if user is None:
        response = jsonify({'status': 'Not Found'})
        response.status_code = 404
        return response
    db.session.delete(user)
    db.session.commit()
    flash("User deleted")
    return jsonify({'status': 'OK'})
