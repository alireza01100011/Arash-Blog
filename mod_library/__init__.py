from flask import Blueprint

library_admin = Blueprint('library_admin',__name__,url_prefix='/library/' , template_folder='Themes')

library_views = Blueprint('library_views',__name__,url_prefix='/library/' , template_folder='Themes')

from mod_library import views