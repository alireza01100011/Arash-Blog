from flask import render_template ,  redirect ,  request
from mod_blog import blog

@blog.route('/')
def index():
    return render_template('blog/index.html')


@blog.route('author/')
def author():
    return render_template('blog/author.html')

@blog.route('post/')
def post():
    return render_template('blog/post.html')