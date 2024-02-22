from flask import render_template ,  redirect ,  request , flash , url_for
from flask_login import login_user , logout_user , login_required , current_user
from sqlalchemy.exc import IntegrityError
from mod_admin import admin
from mod_admin.froms import SiteSettingsForm , IndexPageSettingsForm , FooterContentSettingsForm
from mod_blog.models import Post , Category , User , Madie , SITE , INDEXPAGE, Admin
from mod_blog.forms import PostForm , CategoryForm
from mod_user.froms import UserRoleForm
from utils.calculation import readin_time
from utils.forms import formats
from utils.flask import custom_render_template
from utils.CreateCalendar import CreateCalendar
from app import db 
from utils.flask import custom_render_template 
import uuid
import datetime
import calendar
import os
import pickle
@admin.route('/')
def index():
    _time_now = datetime.datetime.now()
    
    total_posts = Post.query.count()
    total_m_posts = Post.query.filter(Post.time >= _time_now.replace(month=_time_now.month-1)).count()
    
    total_users = User.query.count()
    total_m_users = User.query.filter(User.time >= _time_now.replace(month=_time_now.month-1)).count()
    
    total_likes = db.session.query(Post.total_liks).filter(Post.total_liks >= 1 ).all()
    total_likes = sum([int(n[0]) for n in total_likes])
    
    total_views = db.session.query(Post.views).filter(Post.views >= 1 ).all()
    total_views = sum([int(n[0]) for n in total_views])

    top_posts = Post.query.order_by(Post.views.desc()).limit(5).all()

    admin = Admin.query.filter(Admin.email==current_user.email).first()
    if not admin.to_do: # If it is None, it will be filled with an empty list (to avoid errors)
        admin.to_do = pickle.dumps(list())
        db.session.commit()
    to_do_list = pickle.loads(admin.to_do)

    calendar_dict = CreateCalendar()
    days = list()
    for week in range(7, (43+7), 7):
        days.append((day for day in calendar_dict['days'][week - 7 : week]))
    calendar_dict['days'] = days

    return custom_render_template('admin/index.html', title='Dashboard',
                                  total_posts=total_posts, total_m_posts=total_m_posts,
                                  total_users=total_users, total_m_users=total_m_users,
                                  total_likes=total_likes, total_m_likes='null',
                                  total_views=total_views, total_m_views='null',
                                  top_posts=top_posts, to_do_list=to_do_list,
                                  calendar=calendar_dict)

# Manage to-do lists 
# Add-Done-Remove
@admin.route('to-do/<string:action>', methods=['GET'])
def to_do(action):
    ## Get the task list and convert it into a Python list
    admin:Admin = Admin.query.filter(Admin.email==current_user.email).first()
    to_do:bytes = admin.to_do
    if not to_do: # If it is None, it will be filled with an empty list (to avoid errors)
        to_do:bytes = pickle.dumps(list())
    to_do:list= pickle.loads(to_do)
    
    #  To add item
    if action == 'add':
        name = request.args.get('name', default=None, type=str)
        if (not name) :
            flash('The value entered is invalid')
            return redirect(url_for('admin.index'))
        
        if (not len(name) >= 1) :
            return redirect(url_for('admin.index'))
        
        if (not len(name) < 64):
            flash('The length is more than 64 characters')
            return redirect(url_for('admin.index'))
        
        to_do.append({
            'name':name,
            'date':datetime.datetime.now(),
            'is_done':False
        })
    # Change the status of the task
    elif action == 'done':
        name = request.args.get('name', default=None, type=str)
        if not name :
            return redirect(url_for('admin.index'))
        for task in to_do:
            if name == task.get('name'):
                task['is_done'] = (not task['is_done'])
    
    # Remove the task
    elif action == 'delete':
        name = request.args.get('name', default=None, type=str)
        if not name :
            return redirect(url_for('admin.index'))
        for task in to_do:
            if name == task.get('name'):
                to_do.remove(task)

    # 
    else :
        return redirect(url_for('admin.index'))
    
    # Convert to string to store edits in the database 
    admin.to_do = pickle.dumps(to_do)
    
    try :
        db.session.commit()
    except IntegrityError :
        db.session.rollback()
        flash('The operation was not performed, please try again')
    return redirect(url_for('admin.index'))

#### Post ####

# Show List Post
@admin.route('posts/')
def post_show():
    page = request.args.get('p' , default=1 , type=int)
    per_page = request.args.get('n' , default=10 , type=int)
    posts = Post.query.paginate(page=page , per_page=per_page , error_out=False)
    return custom_render_template('admin/posts/post.html' , title='Show Posts' , posts=posts , page=page , per_page=per_page)

# Create Post
@admin.route('posts/create/' , methods=['GET' , 'POST'])
def post_create():
    form = PostForm()
    page =  request.args.get('page-image' , default=1 , type=int)
    _imag_madie = Madie.query.order_by(Madie.id.desc()).paginate(page=page , per_page = 30 , error_out = False )
    imag_madie = [ img for img in _imag_madie.items if img.filename.split('.')[-1] in (formats['image']) ]
    categories = Category.query.order_by(Category.id.asc()).all()
    form.categories.choices = [(cat.id , cat.name) for cat in categories] 
    form.image.choices = [(img.id , img ) for img in imag_madie]
    
    if request.method == 'GET':
        form.read_time.data = 0
        form.special.data = 1
        
    
    if request.method == 'POST':
        if not form.validate_on_submit():
            return custom_render_template('admin/posts/post-form.html' , title=f'Create New Post' , form=form)
        
        NewPost = Post(
            title=form.title.data,
            content=form.content.data,
            summary=form.summary.data,
            slug=form.slug.data,
            image= int(form.image.data),
            special = int(form.special.data) - 1
        )

        if form.read_time.data == 0 :
            NewPost.read_time = readin_time(str(form.content.data))
        else :
            NewPost.read_time = int(form.read_time.data)
        
        NewPost.author = current_user
        NewPost.categories = [Category.query.get(_) for _ in form.categories.data]

        try :
            db.session.add(NewPost)
            db.session.commit()
            flash('Post successfully created')
            return redirect(url_for('admin.post_show'))
        except IntegrityError :
            db.session.rollback()
            flash('Post could not be created successfully')

    return custom_render_template('admin/posts/post-form.html' , title=f'Create New Post' , form=form)


# Edite Post
@admin.route('posts/edit/<int:post_id>' , methods=['GET' , 'POST'])
def post_edit(post_id):
    form = PostForm()
    
    post = Post.query.get_or_404(int(post_id))
    page =  request.args.get('page-image' , default=1 , type=int)
    _imag_madie = Madie.query.order_by(Madie.id.desc()).paginate(page=page , per_page = 30 , error_out = False )
    imag_madie = [ img for img in _imag_madie.items if img.filename.split('.')[-1] in (formats['image']) ]

    form._post = post
    categories = Category.query.order_by(Category.id.asc()).all()
    form.categories.choices = [(cat.id , cat.name) for cat in categories] 
    form.image.choices = [(img.id , img ) for img in imag_madie]

    if request.method == 'GET' :
        form.title.data = post.title
        form.content.data = post.content
        form.slug.data = post.slug
        form.summary.data = post.summary
        form.read_time.data = post.read_time
        form.categories.data = [category.id for category in post.categories]
        form.image.data = [post.image]
        form.special.data = post.special + 1

    if request.method == 'POST':
        if not form.validate_on_submit():
            return custom_render_template('admin/posts/post-form.html' , title=f'Edite {post.title}' , form=form , post=post )
        
        post.title = form.title.data
        post.content = form.content.data
        post.slug = form.slug.data
        post.summary = form.summary.data
        post.image = int(form.image.data)
        post.special = int(form.special.data) - 1
        post.time = datetime.datetime.now()
        if form.read_time.data == 0 and form.read_time.data == 0.0 :
            post.read_time = readin_time(str(form.content.data))
        else :
            post.read_time = int(form.read_time.data)
        post.categories = [Category.query.get(_) for _ in form.categories.data]

        try :
            db.session.commit()
            flash('Post successfully edit')
            return redirect(url_for('admin.post_show'))
        except IntegrityError :
            db.session.rollback()
            flash('Post could not be edit successfully')

    return custom_render_template('admin/posts/post-form.html' , title=f'Edite {post.title}' , form=form , post = post )



# Delete Post
@admin.route('posts/delete/<int:post_id>')
def post_delete(post_id):
    post = Post.query.get_or_404(int(post_id))
    db.session.delete(post)
    db.session.commit()
    flash('The Post Has Been Successfully Deleted')
    return redirect(url_for('admin.post_show'))



#### Category ####

# Show List Category
@admin.route('categories/')
def category_show():
    page = request.args.get('p' , default=1 , type=int)
    per_page = request.args.get('n' , default=10 , type=int)
    categories = Category.query.paginate(page=page , per_page=per_page , error_out=False)
    return custom_render_template('admin/categories/category.html' ,
                                  categories=categories , title='Show Categories',
                                  per_page=per_page , page=page
                                    )

# Create Category
@admin.route('categories/create' , methods=['GET' , 'POST'])
def category_create():
    form = CategoryForm()
    
    page =  request.args.get('page-image' , default=1 , type=int)
    _imag_madie = Madie.query.order_by(Madie.id.desc()).paginate(page=page , per_page = 30 , error_out = False )
    imag_madie = [ img for img in _imag_madie.items if img.filename.split('.')[-1] in (formats['image']) ]
    form.image.choices = [(img.id , img ) for img in imag_madie]
    if request.method == 'POST':
        if not form.validate_on_submit():
            return custom_render_template('admin/categories/category_form.html' , form=form , title='Create Category')
        
        NewCategory = Category(
            name = form.name.data ,
            description = form.description.data ,
            slug = form.slug.data,
            image= int(form.image.data)
        )

        try :
            db.session.add(NewCategory)
            db.session.commit()
            flash('Category created successfully')
            return redirect(url_for('admin.category_show'))
        except IntegrityError :
            db.session.rollback()
            flash('There was a problem creating a new category, please try again!')

    return custom_render_template('admin/categories/category-form.html' , form=form , title='Create Category')

# Edit Category
@admin.route('categories/edit/<int:category_id>' , methods=['GET' , 'POST'])
def category_edit(category_id):
    form = CategoryForm()
    category = Category.query.get_or_404(category_id)
    form._category = category

    page =  request.args.get('page-image' , default=1 , type=int)
    _imag_madie = Madie.query.order_by(Madie.id.desc()).paginate(page=page , per_page = 30 , error_out = False )
    imag_madie = [ img for img in _imag_madie.items if img.filename.split('.')[-1] in (formats['image']) ]
    form.image.choices = [(img.id , img ) for img in imag_madie]

    if request.method == 'GET':
        form.name.data = category.name
        form.description.data = category.description
        form.slug.data = category.slug
        form.image.data = [category.image]

    if request.method == 'POST':
        if not form.validate_on_submit():
            return custom_render_template('admin/categories/category-form.html' , title=f'Edite Categoty {category.name}' , form=form , category=category)

        category.name = form.name.data
        category.description = form.description.data
        category.slug = form.slug.data
        category.image = form.image.data

        try :
            db.session.commit()
            flash('category successfully edit')
            return redirect(url_for('admin.category_show'))
        except IntegrityError :
            db.session.rollback()
            flash('There was a problem edit category , please try again!')

    return custom_render_template('admin/categories/category-form.html' , title=f'Edite Categoty {category.name}' , form=form , category=category)
        
# Delete Category
@admin.route('categories/delete/<int:category_id>')
def category_delete(category_id):
    category = Category.query.get_or_404(int(category_id))
    try:
        db.session.delete(category)
        db.session.commit()
        flash('Category removed successfully')
    except :
        flash('There was a problem deleting the category')

    return redirect(url_for('admin.category_show'))




#### User ###

# Show User (index)
@admin.route('users/')
def user_show():
    page = request.args.get('p' , default=1 , type=int)
    per_page = request.args.get('n' , default=10 , type=int)
    users = User.query.paginate(page=page , per_page=per_page , error_out=False)
    return custom_render_template('admin/users/user.html' ,
                                  title='Show User' , users=users ,
                                  per_page = per_page , page = page
                                  )

# Create User 
@admin.route('users/create')
def user_create():
    return redirect(url_for('user.register'))

# Edit Role User
@admin.route('users/edit-role/<int:user_id>' , methods=['POST' , 'GET'])
def user_edit(user_id):
    form = UserRoleForm()
    form.role.choices = [(0 , 'User') , (1 , 'Admin')]

    user = User.query.get_or_404(int(user_id))
    
    if request.method == 'GET':
        form.role.data = user.role
    
    if request.method == 'POST':
        if form.validate_on_submit():
            return custom_render_template('admin/users/user-edit.html' , title=f'Change Ueer Role {user.full_name}' , form=form , user=user)        
        
        if form.role.data == '1':
            AddAdmin = Admin()
            AddAdmin.email = user.email
            try :
                db.session.add(AddAdmin)
                db.session.commit()
            except :
                db.session.rollback()
                flash('Failed. Please try again')
        else :
            DelAdmin = Admin.query.filter(Admin.email==user.email).first()
            if DelAdmin:
                try :
                    db.session.delete(DelAdmin)
                    db.session.commit()
                except :
                    db.session.rollback()
                    flash('Failed. Please try again')
        user.role = form.role.data
        try :
            db.session.commit()
            flash('User role change was done successfully')
            return redirect(url_for('admin.user_show'))
        except :
            db.session.rollback()
            flash('Failed. Please try again')
    return custom_render_template('admin/users/user-edit.html' , title=f'Change Ueer Role {user.full_name}' , form=form , user=user)

# Delete User
@admin.route('users/delete/<int:user_id>')
def user_delete(user_id):
    user = User.query.get_or_404(int(user_id))

    if current_user == user : 
        flash("You cannot delete your account from this section. Please refer to your profile")
        return redirect(url_for('admin.user_show'))
    
    try :
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully')
    except :
        flash("Failed to delete user")
    
    return redirect(url_for('admin.user_show'))


# Site Setting 
@admin.route('setting/site/' , methods=['GET' , 'POST'])
def setting_site():
    form = SiteSettingsForm()
    settings = SITE.query.get(1)
    if request.method == 'GET':
        form.name_site.data = settings.name_site
        form.logo_site.data = settings.logo_site
        form.search_placeholder.data = settings.search_placeholder
    
    if request.method == 'POST':
        if not form.validate_on_submit() :
            return custom_render_template('admin/settings/site.html' , form=form , title='Site Settings')
        settings.name_site = form.name_site.data
        settings.search_placeholder = form.search_placeholder.data
        if form.logo_site.data.filename :
            filename = f'{uuid.uuid1()}_{form.logo_site.data.filename}'
            settings.logo_site = filename

            
        try :
            db.session.commit()
            if form.logo_site.data.filename :
                try : os.remove(f'static/images/{settings.logo_site}')
                except FileNotFoundError : 
                    flash('The previous logo was not found and we were not successful in deleting it' ,'danger')
                except PermissionError :
                    flash('We did not have access to delete the previous logo and we were not successful in deleting it' ,'danger')
                file = request.files['logo_site']
                file.save(f'static/images/{filename}')
            flash('Saving settings was successful')
        except :
            flash('Failed to save settings')
    return custom_render_template('admin/settings/site.html' , form=form , title='Site Settings')

@admin.route('setting/index-page/' , methods=['GET' , 'POST'])
def setting_index_page():
    form = IndexPageSettingsForm()
    settings = INDEXPAGE.query.get(1)
    
    if request.method == 'GET':
        form.title_home.data = settings.title_home
        form.site_title.data = settings.site_title
        form.description.data = settings.description
        form.total_posts.data = settings.total_posts
        form.total_special_posts.data = settings.total_special_posts

    if request.method == 'POST':
        if not form.validate_on_submit() :
            return custom_render_template('admin/settings/home-page.html' , form=form , title='Site Settings')

        settings.title_home = form.title_home.data
        settings.site_title = form.site_title.data
        settings.description = form.description.data
        settings.description = form.description.data
        settings.total_posts = form.total_posts.data
        settings.total_special_posts = form.total_special_posts.data

        try :
            db.session.commit()
            flash('Saving settings was successful')
        except :
            flash('Failed to save settings')
    return custom_render_template('admin/settings/home-page.html' , form=form , title='Site Settings')

@admin.route('setting/footer/' , methods=['GET' , 'POST'])
def setting_footer():
    form = FooterContentSettingsForm()
    settings = SITE.query.get(1)
    
    if request.method == 'GET':
        form.footer.data = settings.footer


    if request.method == 'POST':
        if not form.validate_on_submit() :
            return custom_render_template('admin/settings/footer.html' , form=form , title='Site Settings')

        settings.footer = form.footer.data

        try :
            db.session.commit()
            flash('Saving settings was successful')
        except :
            flash('Failed to save settings')
    return custom_render_template('admin/settings/footer.html' , form=form , title='Site Settings')

