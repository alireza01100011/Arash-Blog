from flask import render_template ,  redirect ,  request , abort ,url_for , flash
from flask_login import login_required , current_user
from mod_blog import blog
from mod_blog.models import Post , Madie , User , Category

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
    suggestion = []
    
    if len(post.categories) >= 4 :
        for cat in post.categories:
            if len(suggestion) == 4 : break
            _post = Post.query.order_by(Post.time.desc()).filter(Post.categories.any(name=cat.name)).first()
            suggestion.append(_post)
    else :
        _posts = Post.query.order_by(Post.time.desc()).filter(Post.author.has(id=post.author.id)).limit(4).all()
        for _post in _posts :
            suggestion.append(_post)
    
    if len(suggestion) < 4 :
        _limit = 4 - len(suggestion)
        _posts = Post.query.order_by(Post.time.desc()).limit(_limit).all()
        for _post in _posts :
            suggestion.append(_post)

    
    # try :
    #     suggestion = Post.query.order_by(Post.time.desc()).filter(Post.categories.any(name=post.categories[0].name)).limit(4).all()
    # except IndexError :
    #     pass
    return f'{suggestion}'
    return render_template('blog/post.html' , post=post , title=post.title )


# Like

@blog.route('posts/like/<int:post_id>' , methods=['GET' , 'POST'])
@login_required
def like(post_id):
    failed = 0
    result = 0
    post = Post.query.get(int(post_id))
    user = current_user
    if post in user.posts_disliked:
        post.total_disliks -= 1
        user.posts_disliked.remove(post)
    
    if not post in user.posts_liked :
        post.total_liks += 1
        user.posts_liked.append(post)
    else :
        result = 1
        post.total_liks -= 1
        user.posts_liked.remove(post)
    
    try :
        db.session.commit()
    except :
        failed = 1

    if request.method == 'GET':
        if failed :
            flash("This post was not liked successfully" , 'danger')
        return redirect(url_for('blog.post' , slug=post.slug))
    if request.method == 'POST':
        return f'{result}'

@blog.route('posts/dislike/<int:post_id>' , methods=['GET' , 'POST'])
@login_required
def dislike(post_id):
    failed = 0
    result = 0
    post = Post.query.get(int(post_id))
    user = current_user
    if post in user.posts_liked :
        post.total_liks -= 1
        user.posts_liked.remove(post)
    
    if not post in user.posts_disliked :
        post.total_disliks += 1
        user.posts_disliked.append(post)
    else : 
        result = 1
        post.total_disliks -= 1
        user.posts_disliked.remove(post)
    
    try :
        db.session.commit()
    except :
        failed = 1

    if request.method == 'GET':
        if failed :
            flash("This post was not disliked successfully" , 'danger')
        return redirect(url_for('blog.post' , slug=post.slug))
    if request.method == 'POST':
        return f'{result}'
    


# save Post

@blog.route('posts/save/<int:post_id>' , methods=['GET' , 'POST'])
@login_required
def save(post_id):
    data = 0
    failed = 0
    post = Post.query.get_or_404(int(post_id))
    user = current_user
    

    if post in user.posts_saved:
        user.posts_saved.remove(post)
        data = 1
    else :
        user.posts_saved.append(post)

    if not failed :
        try :
            db.session.commit()
        except :
            failed = 1

    if request.method == 'GET':
        if failed :
            flash("This post was not saved successfully" , 'danger')
        
        try :
            data = request.args.get('data').split(',') or None
            if data[0] == 'profile' :
                return redirect(data[1])
            elif data :
                return redirect(data[0])
        except AttributeError :
            pass
    
        return redirect(url_for('blog.post' , slug=post.slug))
    if request.method == 'POST':
        return f'{data}'