from app import db
import uuid

class Tenant(db.Model):
    __tablename__ = 'tenants'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    logo = db.Column(db.String(200))

    users = db.relationship('User', back_populates='tenant', lazy='dynamic')
    motors = db.relationship('Motor', back_populates='tenant', lazy='dynamic')
