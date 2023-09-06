from flask import render_template as _render_template
from app import site
def custom_render_template(*args , **kwrags):
    return _render_template(*args , **kwrags , site=site)