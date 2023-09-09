<<<<<<< HEAD
from flask import render_template
from mod_blog.models import SITE

def custom_render_template(*args , **kwargs):
    site = SITE.query.get(0)
    return render_template(*args , **kwargs , site=site)
=======
from flask import render_template as _render_template
from app import site
def custom_render_template(*args , **kwrags):
    return _render_template(*args , **kwrags , site=site)
>>>>>>> 4a7c4fef053b657b246d6f989e6d93e2e515bca3
