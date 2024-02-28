import base64

from flask import render_template
from mod_blog.models import SITE

def custom_render_template(*args , **kwargs):
    site = SITE.query.get(1)
    return render_template(*args , **kwargs , site=site)

bytes_to_base64 = lambda obj: str(base64.b64encode(obj), 'ascii')
base64_to_bytes = lambda byt: base64.b64decode(byt)