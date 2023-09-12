from flask import render_template ,  redirect ,  request , abort ,url_for , flash
from flask_login import login_required , current_user
from mod_blog import blog
from mod_blog.models import Post , Madie , User , Category , SITE , INDEXPAGE
from sqlalchemy import or_
from utils.flask import custom_render_template
from app import db

@blog.route('/')
def index():
    special_posts = Post.query.filter(Post.special.like(1)).order_by(Post.time.desc()).limit(4).all()
    posts = Post.query.filter(Post.special.like(0)).order_by(Post.time.desc()).limit(6).all()

    home_page = INDEXPAGE.query.get(0)
    return custom_render_template('blog/index.html' , title=home_page.title_home , s_post = special_posts , posts=posts , home_page=home_page )

@blog.route('authors/')
def author_archive():
    # It will be added in the next update
    # This section requires the implementation of several types of access levels
    return f'<h2 style="text-align: center;">Archive of authors <br> It will be added in the next update <br> </h2>'


@blog.route('authors/<int:user_id>')
def author(user_id):
    author = User.query.get_or_404(int(user_id))
    if author.role == 0 :
        return abort(404)
    return custom_render_template('blog/author.html' , title= author.full_name , author = author)

@blog.route('posts/')
def post_archive():
    page = request.args.get('page' , default=1 , type=int)
    posts = Post.query.order_by(Post.time.desc()).paginate(page=page , per_page=18 , error_out=False)
    return custom_render_template('blog/archive.html' , title='Posts' , posts=posts , page=page , type='archive')

@blog.route('p/<int:post_id>')
def post_short_link(post_id):
    post = Post.query.get_or_404(int(post_id))
    return redirect(url_for('blog.post' , slug=post.slug))



@blog.route('posts/<string:slug>')
def post(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()
    
    # Total views
    post.views = Post.views + 1
    db.session.commit()

    suggestion = set() # -> Max Len == 6
    # Add posts with related categories
    if len(post.categories) >= 1 :
        for cat in post.categories:
            if len(suggestion) == 3 : break
            _post = Post.query.order_by(Post.time.desc()).filter(Post.categories.any(name=cat.name)).first()
            suggestion.add(_post)
    
    # Add co-authored posts
    _posts = Post.query.order_by(Post.time.desc()).filter(Post.author.has(id=post.author.id)).limit(4).all()
    for _post in _posts :
        if len(suggestion) == 4 : break
        suggestion.add(_post)

    # Add the latest posts 
    _posts = Post.query.order_by(Post.time.desc()).limit(12).all()
    for _post in _posts :
        if len(suggestion) == 6 : break
        suggestion.add(_post)

    return custom_render_template('blog/post.html' , post=post , suggestion_posts = suggestion, title=post.title , description=post.summary)


# Category
@blog.route('categories/<string:slug>/')
def category(slug):
    cate = Category.query.filter(Category.slug == slug).first()
    return custom_render_template('blog/archive.html' , posts=cate.posts , title = f'Category - {cate.name}')


# Show Categories
@blog.route('categories/')
def categories():
    page = request.args.get('page' , default=1 , type=int)
    categories = Category.query.order_by(Category.time.desc()).paginate(page=page , per_page=18 , error_out=False)
    return custom_render_template('blog/archive-categories.html' ,
                                  title='Categories' , categories=categories , page=page
                                  )

# Search

@blog.route('posts/search/')
def search():
    query = request.args.get(key='q' , default=' ' , type=str)
    page = request.args.get(key='page' , default=1 , type=int)
    title_cont = Post.title.ilike(f'%{query}%')
    content_cont = Post.content.ilike(f'%{query}%')
    summary_cont = Post.summary.ilike(f'%{query}%')

    posts = Post.query.filter(or_(
        title_cont , 
        content_cont ,
        summary_cont
    )).paginate(page=page , per_page=2 , error_out=False)

    return custom_render_template('blog/archive.html' , title=f'Search For {query}' , posts=posts , page=page , q=query , type='search')

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