from flask import render_template ,  redirect ,  request , abort ,url_for , flash
from flask_login import login_required , current_user
from mod_blog import blog
from mod_blog.models import Post , Madie , User

from app import db

@blog.route('/')
def index():
    special_posts = Post.query.filter(Post.special.like(1)).order_by(Post.time.desc()).limit(4).all()
    posts = Post.query.filter(Post.special.like(0)).order_by(Post.time.desc()).limit(6).all()
    return render_template('blog/index.html' , title='Blog' , s_post = special_posts , posts=posts)

@blog.route('authors/')
def author_archive():
    return f'Archive of authors'


@blog.route('authors/<int:user_id>')
def author(user_id):
    author = User.query.get_or_404(int(user_id))
    if author.role == 0 :
        return abort(404)
    return render_template('blog/author.html' , title= author.full_name , author = author)

@blog.route('posts/')
def post_archive():
    page = request.args.get('page' , default=1 , type=int)
    posts = Post.query.order_by(Post.time.desc()).paginate(page=page , per_page=18 , error_out=False)
    return render_template('blog/archive.html' , title='Posts' , posts=posts , page=page)

@blog.route('p/<int:post_id>')
def post_short_link(post_id):
    post = Post.query.get_or_404(int(post_id))
    return redirect(url_for('blog.post' , slug=post.slug))



@blog.route('posts/<string:slug>')
def post(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()

    return render_template('blog/post.html' , post=post , title=post.title )


# Like

@blog.route('posts/like/<int:post_id>' , methods=['GET' , 'POST'])
@login_required
def like(post_id):
    failed = 0
    post = Post.query.get(int(post_id))
    user = current_user
    user.posts_liked.append(post)
    try :
        db.session.commit()
    except :
        failed = 1

    if request.method == 'GET':
        if failed :
            flash("This post was not liked successfully" , 'danger')
        return redirect(url_for('blog.post' , slug=post.slug))
    if request.method == 'POST':
        return f'{failed}'


@blog.route('posts/like/test')
def likes():
    return render_template('blog/test-pys.html')