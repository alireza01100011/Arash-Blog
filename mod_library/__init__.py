from flask import Blueprint

library = Blueprint('library',__name__,url_prefix='/library/')

from mod_library import views