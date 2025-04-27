from flask import Blueprint, request, jsonify
from app.utils.decorators import token_required, tenant_required
from app.controllers import motor_controller
from app.utils.validators import validate_motor_data

motor_bp = Blueprint('motor', __name__, url_prefix='/api/motor')

@motor_bp.route('/', methods=['GET'])
@token_required
@tenant_required
def get_motor(current_user):
    motors = motor_controller.get_all_motors(current_user.tenant_id)
    return jsonify(motors), 200

@motor_bp.route('/', methods=['POST'])
@token_required
@tenant_required
def create_motor(current_user):
    data = request.get_json()
    validate_motor_data(data)
    motor = motor_controller.create_motor(data, current_user.tenant_id)
    return jsonify(motor), 201


@motor_bp.route('/<motor_id>', methods=['GET'])
@token_required
@tenant_required
def get_motor_by_id(current_user, motor_id):
    motor = motor_controller.get_motor_by_id(motor_id, current_user.tenant_id)
    return jsonify(motor), 200

@motor_bp.route('/<motor_id>', methods=['PATCH'])
@token_required
@tenant_required
def update_motor(current_user, motor_id):
    data = request.get_json()
    validate_motor_data(data)
    motor = motor_controller.update_motor(motor_id, data, current_user.tenant_id)
    return jsonify(motor), 200

@motor_bp.route('/<motor_id>', methods=['DELETE'])
def delete_motor(current_user, motor_id):
    motor_controller.delete_motor(motor_id, current_user.tenant_id)
    return jsonify({'message': 'Motor deleted'}), 200

