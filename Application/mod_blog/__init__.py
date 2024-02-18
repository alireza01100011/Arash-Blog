from flask import Blueprint

blog = Blueprint('blog' , __name__ , url_prefix='/')

from mod_blog import models
from mod_blog import views