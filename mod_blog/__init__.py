from flask import Blueprint

blog = Blueprint('blog' , __name__ , url_prefix='/blog/')

from mod_blog import models
from mod_blog import views