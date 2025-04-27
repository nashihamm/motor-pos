# app/utils/decorators.py
from flask import abort

def tenant_required(f):
    """
    Decorator to ensure that the current user has valid tenant information.
    
    Args:
        f (function): The function to decorate.
    
    Returns:
        function: The wrapped function with tenant validation.
    
    Functionality:
        - Checks if the current user has a valid tenant ID.
        - Raises a 403 error if the tenant ID is invalid.
    """
    def wrapper(*args, **kwargs):
        current_user = kwargs.get('current_user')
        if not current_user or not current_user.tenant_id:
            abort(403, "Tenant access required")
        return f(*args, **kwargs)
    return wrapper
