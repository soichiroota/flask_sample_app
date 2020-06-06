from flask import flash, Blueprint, jsonify
from flask_login import current_user

from project.server.models import Micropost
from project.server import db


micropost_blueprint = Blueprint(
    "micropost",
    __name__
)


@micropost_blueprint.route(
    '/micropost/<int:micropost_id>/delete/', methods=['DELETE']
)
def delete(micropost_id):
    micropost = Micropost.query.filter_by(id=micropost_id).first()
    if current_user.id != micropost.user.id:
        response = jsonify({'status': 'Not Found'})
        response.status_code = 404
        return response
    db.session.delete(micropost)
    db.session.commit()
    flash("Micropost deleted", "success")
    return jsonify({'status': 'OK'})
