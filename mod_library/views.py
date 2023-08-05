from flask import render_template ,  redirect ,  request
from mod_library import library

@library.route('/')
def index():
    return 'library'