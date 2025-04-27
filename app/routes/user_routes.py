from flask import Blueprint
from app.controllers.user_controller import UserController


user_bp = Blueprint('user', __name__, url_prefix='api/user')


@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return UserController.get_user(user_id)

@user_bp.route('/', methods=['POST'])
def create_user():
    return UserController.create_user()