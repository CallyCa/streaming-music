from flask_jwt_extended import verify_jwt_in_request
from functools import wraps

def jwt_required_mutation(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        return func(*args, **kwargs)
    return wrapper
