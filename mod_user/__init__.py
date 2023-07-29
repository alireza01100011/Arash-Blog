from flask import Blueprint

user = Blueprint('user' , __name__ , url_prefix='/user/')

from mod_user import views