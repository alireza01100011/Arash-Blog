from flask import render_template
from mod_blog.models import SITE

def custom_render_template(*args , **kwargs):
    site = SITE.query.get(0)
    return render_template(*args , **kwargs , site=site)