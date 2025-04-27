from functools import wraps
from flask import request, jsonify

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Contoh logika validasi token
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        # Logika verifikasi token...
        return f(*args, **kwargs)
    return decorated

def tenant_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Contoh logika validasi tenant
        return f(*args, **kwargs)
    return decorated
