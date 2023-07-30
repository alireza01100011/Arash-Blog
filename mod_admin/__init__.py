from flask import Blueprint
from mod_admin.utils import admin_only_view

admin = Blueprint('admin' , __name__ ,url_prefix='/admin/' )

@admin.before_request
@admin_only_view
def admin_only_view_before_request():
    pass

from mod_admin import models
from mod_admin import views