from flask import render_template ,  redirect ,  request , abort
from mod_blog import blog
from mod_blog.models import Post , Madie , User

@blog.route('/')
def index():
    return render_template('blog/index.html')

@blog.route('authors/')
def author_archive():
    return f'Archive of authors'


@blog.route('authors/<int:user_id>')
def author(user_id):
    author = User.query.get_or_404(int(user_id))
    if author.role == 0 :
        return abort(404)
    return render_template('blog/author.html' , title= author.full_name , author = author)

@blog.route('posts')
def post_archive():
    return f'Archive of posts'


@blog.route('posts/<string:slug>')
def post(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()

    return render_template('blog/post.html' , post=post , title=post.title )