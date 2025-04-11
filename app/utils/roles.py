from functools import wraps
from flask import abort
from flask_login import current_user

def role_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated or current_user.user_role != role:
                abort(403)  # Forbidden page
            return func(*args, **kwargs)
        return wrapper
    return decorator
