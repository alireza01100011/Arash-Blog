from flask import Blueprint

library = Blueprint('library',__name__,url_prefix='/library/' , template_folder='Themes')

from mod_library import views