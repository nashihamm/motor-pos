from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User
from app.models.tenant import Tenant
from app.models.motor import Motor

from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    tenant_name = data.get('tenant_name')


    # create new tenant
    tenant = Tenant(name=tenant_name)
    db.session.add(tenant)
    db.session.flush()

    # create new user
    user = User(
        name=name,
        email=email,
        tenant_id=tenant.id,
        role='Owner'
    )

    user.set_password(password)

    db.session.add(user)
    db.session.commit()
    return jsonify({'msg': 'User registered successfully'}), 201
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity={
            'user_id' : user.id,
            'tenant_id': user.tenant_id,
            'role': user.role
        })

        return jsonify({
            'access_token': access_token,
            'user_id': user.id,
            'tenant_id': user.tenant_id,
            'role': user.role
        }), 200
    return jsonify({'msg': 'Invalid email or password'}), 401
@auth_bp.route('/logout', methods=['POST'])
def logout():
    return jsonify({'msg': 'Logout successful'}), 200
@auth_bp.route('/user', methods=['GET'])
def get_user():
    user_id = request.args.get('user_id')
    user = User.query.get(user_id)
    if user:
        return jsonify({
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role
        }), 200
    return jsonify({'msg': 'User not found'}), 404
@auth_bp.route('/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = User.query.get(user_id)
    if user:
        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        user.role = data.get('role', user.role)
        db.session.commit()
        return jsonify({'msg': 'User updated successfully'}), 200
    return jsonify({'msg': 'User not found'}), 404
@auth_bp.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'msg': 'User deleted successfully'}), 200
    return jsonify({'msg': 'User not found'}), 404
