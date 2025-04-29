# app/routes/auth_routes.py
from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User
from app.models.tenant import Tenant
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import datetime

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['name', 'email', 'password', 'tenant_name']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'msg': f'Missing required field: {field}'}), 400
    
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    tenant_name = data.get('tenant_name')

    # Validate email format
    import re
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({'msg': 'Invalid email format'}), 400

    # Check if user already exists
    if User.query.filter_by(email=email).first():
        return jsonify({'msg': 'Email already registered'}), 400
        
    # Check if tenant name already exists
    if Tenant.query.filter_by(name=tenant_name).first():
        return jsonify({'msg': 'Tenant name already exists'}), 400

    try:
        # Create new tenant
        tenant = Tenant(name=tenant_name)
        db.session.add(tenant)
        db.session.flush()  # Get tenant ID before commit

        # Create new user
        user = User(
            name=name,
            email=email,
            tenant_id=tenant.id,
            role='Owner'  # First user is always the Owner
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()
        
        return jsonify({'msg': 'Registration successful', 'user_id': user.id, 'tenant_id': tenant.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': f'Registration failed: {str(e)}'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Validate required fields
    if not data.get('email') or not data.get('password'):
        return jsonify({'msg': 'Email and password are required'}), 400
        
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        # Create token with expiration time
        expires = datetime.timedelta(days=1)
        access_token = create_access_token(
            identity={
                'user_id': user.id,
                'tenant_id': user.tenant_id,
                'role': user.role,
                'email': user.email
            },
            expires_delta=expires
        )

        return jsonify({
            'access_token': access_token,
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'tenant_id': user.tenant_id,
                'role': user.role
            }
        }), 200
    return jsonify({'msg': 'Invalid email or password'}), 401

@auth_bp.route('/user', methods=['GET'])
@jwt_required()
def get_current_user():
    current_user = get_jwt_identity()
    user_id = current_user['user_id']
    
    user = User.query.get(user_id)
    if user:
        return jsonify({
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'tenant_id': user.tenant_id,
            'role': user.role
        }), 200
    return jsonify({'msg': 'User not found'}), 404

@auth_bp.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    return user_controller.get_user(user_id)

@auth_bp.route('/user', methods=['POST'])
@jwt_required()
def create_user():
    return user_controller.create_user()

@auth_bp.route('/user/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    return user_controller.update_user(user_id)

@auth_bp.route('/user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    return user_controller.delete_user(user_id)