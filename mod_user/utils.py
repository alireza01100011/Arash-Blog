from flask import redirect , url_for
from flask_login import current_user
from functools import wraps

def refute_only_view(func):
    @wraps(func)
    def decrtory(*args , **kwargs):
        if current_user.is_authenticated :
            return redirect(url_for('user.index'))
        
        return func(*args , **kwargs)
    
    return decrtory

def refute_only_view_except_admin(func):
    @wraps(func)
    def decrtory(*args , **kwargs):
        if current_user.is_authenticated :
            if current_user.role == 1 : 
                return func(*args , **kwargs)
            
            return redirect(url_for('user.index'))
        
        return func(*args , **kwargs)
    
    return decrtory
