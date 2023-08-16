from flask import render_template ,  redirect ,  request , url_for , flash
from sqlalchemy.exc import IntegrityError
from flask_login import login_user , current_user , logout_user , login_required
from mod_user import user
from mod_user.utils import refute_only_view , refute_only_view_except_admin
from mod_user.froms import RegisterForm , LoginForm , EditProfileForm
from mod_blog.models import User , ImageProfile
from app import db , becrypt 

import os
import uuid

def CreateFileName(filename):
    _totla_test = 0
    while True :
        _totla_test += 1
        filename = f'{uuid.uuid1()}_{filename}'
        _ = ImageProfile.query.filter(ImageProfile.filename.ilike(f'{filename}')).first()
        if not _ : return filename
        if _totla_test == 256 : return False

@user.route('/')
def index():
    return redirect(url_for('user.profile'))

@user.route('profile/' )
@login_required
def profile():
    form = EditProfileForm()
    tab = request.args.get('tab' , default='like' , type=str)
    user =  User.query.get(current_user.id)

    return render_template('user/profile.html' , title='User' , user=user , form=form , tab=tab)

@user.route('profile/edit-profile' , methods=['GET' , 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    user = User.query.get(current_user.id)
    form._user = user
    if request.method == 'GET':
        form.fullname.data = user.full_name
        form.email.data = user.email
        form.old_password.data = '*' * 8
        form.password.data = '*' * 8
        form.confirm_password.data = '*' * 8
        form.bio.data = user.bio or ''
    if request.method == 'POST':
        if not form.validate_on_submit() :
            flash('Validation failed' , 'danger')    
            render_template('user/_edit-profile.html' , form=form)
        
        user.full_name = form.fullname.data
        user.email = form.email.data
        user.bio = form.bio.data
        
        if form.old_password.data != '*' * 8 and form.password.data != '*' * 8 and  form.confirm_password.data != '*' * 8:
            if not becrypt.check_password_hash(user.password , form.old_password.data):
                flash('The password is not valid' , 'danger')
                render_template('user/_edit-profile.html' , form=form)
            
        user.password = becrypt.generate_password_hash(form.password.data)
        
        image_profile = request.files['profile_image']
        if image_profile :
            filename = CreateFileName(form.profile_image.data.filename)

            if not user.image == 0 :
                image_profile = ImageProfile.query.get(int(user.image.id))
                os.remove(os.path.join('static/img_profile' , image_profile.filename ))
                image_profile.filename  = filename

            if user.image == 0 :
                image_profile = ImageProfile()
                image_profile.filename = filename
                db.session.add(image_profile)

            user.image = image_profile
            
            
            image_profile.save(os.path.join('static/img_profile' , filename))
            flash('File uploaded successfully')
        

        try :
            db.session.commit()
            flash('Your profile information has been successfully edited' , 'success')
        except :
            db.session.rollback()
            flash('The operation failed. Please try again later' , 'danger')
    
    return render_template('user/_edit-profile.html' , form=form)


@user.route('login/' , methods=['GET' , 'POST'])
@refute_only_view
def login():
    form = LoginForm()

    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('user/login.html' , title='Login' , form=form)
        
        user = User.query.filter(User.email.ilike(f'{form.email.data}')).first()
        login_user(user , remember=form.remember.data)
        flash('You have successfully logged in' , 'info')
        return redirect(url_for('user.index'))

    return render_template('user/login.html' , title='Login' , form=form)


@user.route('register/' , methods=['GET' , 'POST'])
@refute_only_view_except_admin
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('user/register.html' , title='Register' , form=form)
        
        NewUser = User(
            form.fullname.data , form.email.data ,
            becrypt.generate_password_hash(form.password.data) ,
            0

            )
        NewUser.image = ImageProfile.query.get(1)

        try :
            db.session.add(NewUser)
            db.session.commit()
            flash('Your account has been created successfully')
            # To create a new user by admin
            try :
                if current_user.role == 1 : 
                    return redirect(url_for('admin.user_edit' , user_id = NewUser.id ))
            except AttributeError :
                pass
            return redirect(url_for('user.login'))
        except IntegrityError:
            db.session.rollback()
            flash('Error, try again')
            return render_template('user/register.html' , title='Register' , form=form)
    
    return render_template('user/register.html' , title='Register' , form=form)

@user.route('logout/')
@login_required
def logout():
    logout_user()
    flash('You have successfully logged out')
    return redirect(url_for('user.index'))