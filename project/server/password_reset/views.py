from flask import (
    redirect, url_for, flash, Blueprint,
    render_template, current_app
)
from flask_login import current_user

from project.server.models import User
from project.server import db
from project.server.password_reset.forms import (
    RequestResetForm, ResetPasswordForm
)


password_reset_blueprint = Blueprint(
    "password_reset",
    __name__
)


@password_reset_blueprint.route(
    '/password_reset/new/', methods=['GET', 'POST']
)
def new():
    if current_user.is_authenticated:
        return redirect(url_for('static_pages.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if current_app.config.get('MAIL_USERNAME'):
            user.send_password_reset_email()
            flash(
                'An email has been sent with instructions ' +
                'to reset your password',
                'info'
            )
            return redirect(url_for('user.login'))
        else:
            return redirect(url_for(
                'password_reset.edit',
                token=user.get_token()
            ))
    return render_template(
        'password_reset/new.html',
        title='Reset Password',
        form=form
    )


@password_reset_blueprint.route(
    '/password_reset/<token>/edit/', methods=['GET', 'POST']
)
def edit(token):
    if current_user.is_authenticated:
        return redirect(url_for('static_pages.home'))
    user = User.verify_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('password_reset.new'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        flash(
            'Your password has been updated! You are now able to log in',
            'success'
        )
        return redirect(url_for('user.login'))
    return render_template(
        'password_reset/edit.html',
        title='Reset Password',
        form=form
    )
