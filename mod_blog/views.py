from flask import render_template ,  redirect ,  request
from mod_blog import blog

@blog.route('/')
def index():
    return render_template('blog/index.html')