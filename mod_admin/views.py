from flask import render_template ,  redirect ,  request , flash
from flask_login import login_user , logout_user , login_required , current_user
from sqlalchemy.exc import IntegrityError
from mod_admin import admin
from mod_blog.models import Post
from mod_blog.forms import PostForm
from app import db 

@admin.route('/')
def index():
    return render_template('admin/index.html' , title='Dashboard')


#### Post ####

# Show List Post
@admin.route('posts/')
def post_show():
    page = request.args.get('p' , default=1 , type=int)
    per_page = request.args.get('n' , default=10 , type=int)
    posts = Post.query.paginate(page=page , per_page=per_page , error_out=False)
    return f'{posts.items}'
    # return render_template('admin/posts/post.html' , title='Show Posts' , posts=posts)

# Create Post
@admin.route('posts/create/' , methods=['GET' , 'POST'])
def post_create():
    form = PostForm()

    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('admin/posts/post-form.html' , title=f'Create New Post' , form=form)
        
        NewPost = Post(
            title=form.title.data,
            content=form.content.data,
            summary=form.summary.data,
            slug=form.slug.data,
            image=1 # -> temporarily until the completion of the blueprint (media)
        )
        
        NewPost.author = current_user

        try :
            db.session.add(NewPost)
            db.session.commit()
            flash('Post successfully created')
        except IntegrityError :
            db.session.rollback()
            flash('Post could not be created successfully')

    return render_template('admin/posts/post-form.html' , title=f'Create New Post' , form=form)


# Edite Post
@admin.route('posts/edite/<int:post_id>' , methods=['GET' , 'POST'])
def post_edite(post_id):
    pass # Todo : Edite Post


# Delete Post
@admin.route('posts/delete/<int:post_id>')
def post_delete(post_id):
    pass # Todo : Delete Post
