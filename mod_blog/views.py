from flask import render_template ,  redirect ,  request
from mod_blog import blog
from mod_blog.models import Post

@blog.route('/')
def index():
    return render_template('blog/index.html')


@blog.route('author/')
def author():
    return render_template('blog/author.html')


@blog.route('post/<string:slug>')
def post(slug):
    post = Post.query.filter(Post.slug == slug).first()
    return render_template('blog/post.html' , post=post , title=post.title)