from flask import abort
from flask_login import current_user 
from functools import wraps

def admin_only_view(func):
    wraps(func)
    def decrtory(*args , **kwargs):
        if not  current_user.is_authenticated :
            abort(401)
        if current_user.role == 0 :
            abort(403)
        
        return func(*args , **kwargs)

    return decrtory
