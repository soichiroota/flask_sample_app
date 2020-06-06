from flask import redirect, url_for, Blueprint, jsonify
from flask_login import login_required, current_user

from project.server.models import User


relationship_blueprint = Blueprint(
    "relationship",
    __name__
)


@relationship_blueprint.route(
    '/relationships/<int:user_id>/create/',
    methods=['POST']
)
@login_required
def create(user_id):
    if not current_user.is_authenticated:
        return redirect(url_for('static_pages.home'))
    user = User.query.get(user_id)
    if user is None:
        response = jsonify({'status': 'Not Found'})
        response.status_code = 404
        return response
    current_user.follow(user)
    return jsonify({'status': 'OK'})


@relationship_blueprint.route(
    '/relationships/<int:user_id>/delete/',
    methods=['DELETE']
)
@login_required
def delete(user_id):
    if not current_user.is_authenticated:
        return redirect(url_for('static_pages.home'))
    user = User.query.get(user_id)
    if user and current_user.is_following(user):
        current_user.unfollow(user)
        return jsonify({'status': 'OK'})
    response = jsonify({'status': 'Not Found'})
    response.status_code = 404
    return response
