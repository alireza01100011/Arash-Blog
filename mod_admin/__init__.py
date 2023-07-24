from flask import Blueprint

admin = Blueprint('admin' , __name__ ,url_prefix='admin/')

from mod_admin import models
from mod_admin import views