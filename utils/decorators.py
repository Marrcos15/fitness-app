from functools import wraps
from flask import abort
from flask_login import current_user
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)  # Forbidden
        return f(*args, **kwargs)
    return decorated_function

# Configuración del limitador de tasa
limiter = Limiter(
    key_func=get_remote_address, 
    default_limits=["200 per day", "50 per hour"]
)