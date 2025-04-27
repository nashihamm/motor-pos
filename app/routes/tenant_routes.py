from flask import Blueprint, jsonify

tenant_bp = Blueprint('tenant', __name__, url_prefix='/api/tenant')

@tenant_bp.route('/', methods=['GET'])
def get_tenants():
    # Contoh respon, ganti dengan implementasi sesungguhnya
    return jsonify({'message': 'Tenant route works!'})
