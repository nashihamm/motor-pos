
# app/controllers/user_controller.py
from app.models.user import User
from app import db
from flask import jsonify, request
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity

class UserController:
    @staticmethod
    @jwt_required()
    def get_user(user_id):
        # Get current user's identity
        current_user = get_jwt_identity()
        
        # Check permissions (only admin or same user can view details)
        if current_user['role'] != 'admin' and current_user['user_id'] != user_id:
            return jsonify({'msg': 'Unauthorized access'}), 403
            
        user = User.query.get(user_id)
        if user:
            return jsonify(user.serialize()), 200
        return jsonify({'msg': 'User not found'}), 404

    @staticmethod
    @jwt_required()
    def create_user():
        # Check if user has admin permissions
        current_user = get_jwt_identity()
        if current_user['role'] not in ['admin', 'Owner']:
            return jsonify({'msg': 'Unauthorized access'}), 403
            
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'password', 'tenant_id']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'msg': f'Missing required field: {field}'}), 400

        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        tenant_id = data.get('tenant_id')
        role = data.get('role', 'employee')

        # Validate email format
        import re
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return jsonify({'msg': 'Invalid email format'}), 400

        # Check if user already exists
        if User.query.filter_by(email=email).first():
            return jsonify({'msg': 'Email already registered'}), 400

        # Check if user belongs to the same tenant as the creator
        if current_user['role'] != 'admin' and current_user['tenant_id'] != tenant_id:
            return jsonify({'msg': 'Cannot create user for different tenant'}), 403

        try:
            user = User(
                name=name,
                email=email,
                tenant_id=tenant_id,
                role=role
            )
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            return jsonify({'msg': 'User created successfully', 'user': user.serialize()}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'msg': f'Error creating user: {str(e)}'}), 500

    @staticmethod
    @jwt_required()
    def update_user(user_id):
        # Check permissions
        current_user = get_jwt_identity()
        if current_user['role'] not in ['admin', 'Owner'] and current_user['user_id'] != user_id:
            return jsonify({'msg': 'Unauthorized access'}), 403
            
        user = User.query.get(user_id)
        if not user:
            return jsonify({'msg': 'User not found'}), 404
            
        data = request.get_json()
        
        # Update user fields
        if data.get('name'):
            user.name = data.get('name')
            
        if data.get('email'):
            # Validate email format
            import re
            if not re.match(r"[^@]+@[^@]+\.[^@]+", data.get('email')):
                return jsonify({'msg': 'Invalid email format'}), 400
                
            # Check if email is already taken
            existing_user = User.query.filter_by(email=data.get('email')).first()
            if existing_user and existing_user.id != user_id:
                return jsonify({'msg': 'Email already registered'}), 400
                
            user.email = data.get('email')
            
        # Only admin or Owner can change roles
        if data.get('role') and current_user['role'] in ['admin', 'Owner']:
            user.role = data.get('role')
            
        if data.get('password'):
            user.set_password(data.get('password'))
            
        try:
            db.session.commit()
            return jsonify({'msg': 'User updated successfully', 'user': user.serialize()}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'msg': f'Error updating user: {str(e)}'}), 500

    @staticmethod
    @jwt_required()
    def delete_user(user_id):
        # Only admin or Owner can delete users
        current_user = get_jwt_identity()
        if current_user['role'] not in ['admin', 'Owner']:
            return jsonify({'msg': 'Unauthorized access'}), 403
            
        user = User.query.get(user_id)
        if not user:
            return jsonify({'msg': 'User not found'}), 404
            
        try:
            db.session.delete(user)
            db.session.commit()
            return jsonify({'msg': 'User deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'msg': f'Error deleting user: {str(e)}'}), 500