from flask import redirect, url_for, flash, Blueprint
from flask_login import current_user, login_user

from project.server.models import User
from project.server import db


account_activation_blueprint = Blueprint(
    "account_activation",
    __name__
)


@account_activation_blueprint.route(
    '/account_activation/<token>/edit/', methods=['GET', 'POST']
)
def edit(token):
    if current_user.is_authenticated:
        return redirect(url_for('user.show', user_id=current_user.id))
    user = User.verify_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('static_pages.home'))
    else:
        user.activate()
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("Thank you for registering.", "success")
        return redirect(url_for('user.show', user_id=user.id))
