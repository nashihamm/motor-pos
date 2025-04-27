from app import db
import uuid
from datetime import date

class Motor(db.Model):
    __tablename__ = 'motors'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = db.Column(db.String(36), db.ForeignKey('tenants.id'), nullable=False)

    # Basic motor info
    brand = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(50))
    plate_number = db.Column(db.String(50))
    km = db.Column(db.Integer)
    condition = db.Column(db.String(20), default='baru')  # 'baru' atau 'seken'

    # Additional motor specs
    engine_capacity = db.Column(db.Integer)  # cc
    transmission = db.Column(db.String(20))  # manual, matic, semi-auto
    fuel_type = db.Column(db.String(20))     # bensin, listrik
    frame_number = db.Column(db.String(50))
    engine_number = db.Column(db.String(50))

    # Legal documents
    stnk_expiry_date = db.Column(db.Date)
    bpkb_status = db.Column(db.String(50))   # ada, tidak ada, ditahan

    # Pricing
    buy_price = db.Column(db.Integer)
    sell_price = db.Column(db.Integer)
    discount_price = db.Column(db.Integer)  # opsional

    # Sales
    status = db.Column(db.String(20), default='masih ada')  # masih ada, terjual
    sold_date = db.Column(db.Date)
    sold_to = db.Column(db.String(100))  # opsional

    # Operational
    acquisition_source = db.Column(db.String(50))  # beli, tukar tambah, konsinyasi
    description = db.Column(db.Text)

    # Media
    main_photo_url = db.Column(db.String(255))

    # Quality control
    inspection_passed = db.Column(db.Boolean, default=False)
    warranty = db.Column(db.String(100))  # contoh: "1 bulan mesin", "3 bulan mesin"

    tenant = db.relationship('Tenant', back_populates='motors')

def serialize(self):
    return {
        'id': self.id,
        'brand': self.brand,
        'type': self.type,
        'year': self.year,
        'color': self.color,
        'plate_number': self.plate_number,
        'km': self.km,
        'condition': self.condition,
        'engine_capacity': self.engine_capacity,
        'transmission': self.transmission,
        'fuel_type': self.fuel_type,
        'frame_number': self.frame_number,
        'engine_number': self.engine_number,
        'stnk_expiry_date': self.stnk_expiry_date.isoformat() if self.stnk_expiry_date else None,
        'bpkb_status': self.bpkb_status,
        'buy_price': self.buy_price,
        'sell_price': self.sell_price,
        'discount_price': self.discount_price,
        'status': self.status,
        'sold_date': self.sold_date.isoformat() if self.sold_date else None,
        'sold_to': self.sold_to,
        'acquisition_source': self.acquisition_source,
        'description': self.description,
        'main_photo_url': self.main_photo_url,
        'inspection_passed': self.inspection_passed,
        'warranty': self.warranty
    }
