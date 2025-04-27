from app import db
import uuid

class Motor(db.Model):
    __tablename__ = 'motors'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = db.Column(db.String(36), db.ForeignKey('tenants.id'), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(50))
    plate_number = db.Column(db.String(50))
    km = db.Column(db.Integer)
    buy_price = db.Column(db.Integer)
    sell_price = db.Column(db.Integer)
    status = db.Column(db.String(20), default='available')  # available, sold

    tenant = db.relationship('Tenant', back_populates='motors')
