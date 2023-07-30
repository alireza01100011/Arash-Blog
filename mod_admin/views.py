from flask import render_template ,  redirect ,  request
from flask_login import login_user , logout_user , login_required , current_user

from mod_admin import admin
from mod_blog.models import Post
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
@admin.route('posts/create' , methods=['GET' , 'POST'])
def post_create():
    pass # Todo : Create Post


# Edite Post
@admin.route('posts/edite/<int:post_id>' , methods=['GET' , 'POST'])
def post_edite(post_id):
    pass # Todo : Edite Post


# Delete Post
@admin.route('posts/delete/<int:post_id>')
def post_delete(post_id):
    pass # Todo : Delete Post
