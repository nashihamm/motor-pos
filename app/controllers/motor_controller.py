# app/controllers/motor_controller.py
from app.models.motor import Motor
from app import db
from flask import abort

def get_all_motors(tenant_id):
    motors = Motor.query.filter_by(tenant_id=tenant_id).all()
    return [motor.serialize() for motor in motors]

def create_motor(data, tenant_id):
    motor = Motor(**data, tenant_id=tenant_id)
    db.session.add(motor)
    db.session.commit()
    return motor.serialize()

def get_motor_by_id(motor_id, tenant_id):
    motor = Motor.query.filter_by(id=motor_id, tenant_id=tenant_id).first()
    if not motor:
        abort(404, description="Motor not found")
    return motor.serialize()

def update_motor(motor_id, data, tenant_id):
    motor = Motor.query.filter_by(id=motor_id, tenant_id=tenant_id).first()
    if not motor:
        abort(404, description="Motor not found")

    for key, value in data.items():
        setattr(motor, key, value)

    db.session.commit()
    return motor.serialize()

def delete_motor(motor_id, tenant_id):
    motor = Motor.query.filter_by(id=motor_id, tenant_id=tenant_id).first()
    if not motor:
        abort(404, description="Motor not found")

    db.session.delete(motor)
    db.session.commit()
    return {'message': 'Motor deleted'}
