from flask import Flask, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_ckeditor import CKEditor
from flask_mail import Mail

from redis import Redis

from config import config

app = Flask(__name__ , template_folder='Themes')
app.config.from_object(config)
db = SQLAlchemy()
db.init_app(app=app)

migrate = Migrate(app , db)

login_manager = LoginManager(app)
login_manager.login_view = 'user.login'
login_manager.login_message = 'first Login'
login_manager.login_message_category = 'info'

becrypt = Bcrypt(app)

ckeditor = CKEditor(app)
redis = Redis.from_url(config.REDIS_SERVER_URL)

mail = Mail()
mail.init_app(app)
mail.server = config.MAIL_SERVER
mail.password = config.MAIL_PASSWORD
mail.port = config.MAIL_PORT
mail.username = config.MAIL_USERNAME

from views import *

from mod_admin import admin
from mod_blog import blog
from mod_user import user
from mod_library import library_views

app.register_blueprint(admin)
app.register_blueprint(library_views)
app.register_blueprint(blog)
app.register_blueprint(user)

# Error Handler
from utils.flask import custom_render_template
def _http_error_handler(error):
    return make_response(
        custom_render_template('error.html', error=error, title=error.code),
        error.code)

from werkzeug.exceptions import default_exceptions
for code in default_exceptions:
    app.errorhandler(code)(_http_error_handler)
# -------


# Delete this line and file (SETUP.PY) after launching the site
# This line is commented by default after launching the website
# # # # # # # # # # #
# from SETUP import *
# # # # # # # # # # #
# ^ The above line is automatically commented (By SETUP.PY)

#
#
# The blueprint of the library is registered in __init__.py Blueprint Admin because it is accessible only to the admin
#
#