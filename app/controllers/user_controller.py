# app/controllers/user_controller.py
from app.models.user import User
from app import db
from flask import jsonify, request

class UserController:
    @staticmethod
    def get_user(user_id):
        user = User.query.get(user_id)
        if user:
            return jsonify(user.serialize()), 200
        return jsonify({'msg': 'User not found'}), 404

    @staticmethod
    def create_user():
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        tenant_id = data.get('tenant_id')
        role = data.get('role', 'employee')

        if not all([name, email, password, tenant_id]):
            return jsonify({'msg': 'Missing required fields'}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({'msg': 'Email already registered'}), 400

        user = User(
            name=name,
            email=email,
            tenant_id=tenant_id,
            role=role
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return jsonify({'msg': 'User created', 'user': user.serialize()}), 201
