from flask import render_template ,  redirect ,  request
from flask_login import login_user , logout_user , login_required , current_user

from mod_admin import admin
from mod_admin.utils import admin_only_view
from app import db 

@admin.route('/')

def index():
    return render_template('admin/index.html' , title='Dashboard')
