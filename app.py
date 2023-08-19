from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_ckeditor import CKEditor
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

from views import *

from mod_admin import admin
from mod_blog import blog
from mod_user import user
from mod_library import library_views

app.register_blueprint(admin)
app.register_blueprint(library_views)
app.register_blueprint(blog)
app.register_blueprint(user)

#
#
# The blueprint of the library is registered in __init__.py Blueprint Admin because it is accessible only to the admin
#
#