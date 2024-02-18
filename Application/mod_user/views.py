import os
import uuid

from flask import render_template,  redirect,  request, url_for, flash,abort
from flask_login import login_user, current_user, logout_user, login_required

from sqlalchemy.exc import IntegrityError

from utils.flask import custom_render_template

from mod_user import user
from mod_user.utils import (
    refute_only_view, delete_from_redis,
    refute_only_view_except_admin,
    add_to_redis, get_from_redis,
    send_registration_message)

from mod_user.froms import RegisterForm, LoginForm, EditProfileForm
from mod_blog.models import User, ImageProfile, UnverifiedUser

from app import db, becrypt, config

def CreateFileName(filename):
    _totla_test= 0
    while True :
        _totla_test += 1
        filename= f'{uuid.uuid1()}_{filename}'
        _= ImageProfile.query.filter(ImageProfile.filename.ilike(f'{filename}')).first()
        if not _ : return filename
        if _totla_test== 256 : return False
# End Function

@user.route('/')
def index():
    return redirect(url_for('user.profile'))
# End Route

@user.route('profile/')
@login_required
def profile():
    form= EditProfileForm()
    tab= request.args.get('tab', default='like', type=str)
    user= User.query.get(current_user.id)

    return custom_render_template('user/profile.html', 
        title='User', user=user, form=form, tab=tab)
# End Route

@user.route('profile/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form= EditProfileForm()
    user:User= User.query.get(current_user.id)
    form._user= user
    
    if request.method== 'GET':
        form.fullname.data= user.full_name
        form.email.data= user.email
        form.old_password.data= '*' * 8
        form.password.data= '*' * 8
        form.confirm_password.data= '*' * 8
        form.bio.data= user.bio or ''
    # ---
    if request.method== 'POST':
        if not form.validate_on_submit() :
            flash('Validation failed', 'danger')    
            custom_render_template('user/_edit-profile.html', form=form)
        # ---    

        if user.email != form.email.data:
            link_ = f'<a href="{url_for("user.confirm_registration")}">Email Confirm</a>'
            
            db.session.add(UnverifiedUser(user.id))
            flash(f'Please confirm your email ! ({link_})')
            
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                flash(f'Unsuccessful. Please confirm your email! Then try again...({link_})')
                
                return redirect(url_for('user.edit_profile'))

        user.full_name= form.fullname.data
        user.email= form.email.data
        user.bio= form.bio.data

        _condition_ = all(map(
                lambda _ : _ .data!= '*'*8 ,
                (
                form.password,
                form.old_password,
                form.confirm_password
                )))
                
        if _condition_:
            if not becrypt.check_password_hash(user.password, form.old_password.data):
                flash('The password is not valid', 'danger')
                custom_render_template('user/_edit-profile.html', form=form)
            # ---
            
            user.password= becrypt.\
                generate_password_hash(form.password.data)

        del _condition_
        # ---


        request_image_profile= request.files['profile_image']
        
        if request_image_profile :
            filename= CreateFileName(form.profile_image.data.filename)

            if not user.image.id== 1 :
                image_profile= ImageProfile.query.get(int(user.image.id))
                try : 
                    os.remove(os.path.\
                        join('static/img_profile',image_profile.filename))
            
                except FileNotFoundError :
                    pass
                image_profile.filename = filename
            # ---

            if user.image.id== 1 :
                image_profile= ImageProfile()
                image_profile.filename= filename
                db.session.add(image_profile)
            # ---

            user.image= image_profile
            request_image_profile.save(os.\
                path.join('static/img_profile', filename))
    
        try :
            db.session.commit()
            flash('Your profile information has been successfully edited', 
                'success')
        except :
            db.session.rollback()
            flash('The operation failed. Please try again later', 
                'danger')
    # ---
    return custom_render_template('user/_edit-profile.html', 
        form=form)
# End Route

@user.route('login/', methods=['GET', 'POST'])
@refute_only_view
def login():
    form= LoginForm()

    if request.method== 'POST':
        if not form.validate_on_submit():
            return custom_render_template('user/login.html', 
                title='Login', form=form)
        # ---
        user = User.query.\
            filter(User.email.ilike(f'{form.email.data}')).first()
        login_user(user, remember=form.remember.data)

        # Has the user confirmed her email?
        user_not_auth = UnverifiedUser.\
            query.filter(UnverifiedUser.user_id.ilike(user.id)).first()
        if user_not_auth:
            return redirect(url_for('user.confirm_registration'))
        # ---
        
        
        flash('You have successfully logged in', 'info')
        return redirect(url_for('user.profile', tab='edit-profile'))
    # ---
    return custom_render_template('user/login.html',
        title='Login', form=form)
# End Route

@user.route('register/', methods=['GET', 'POST'])
@refute_only_view_except_admin
def register():
    form= RegisterForm()

    if request.method== 'POST':
        if not form.validate_on_submit():
            return custom_render_template('user/register.html',
                title='Register', form=form)
        # ---

        NewUser= User(
            full_name=form.fullname.data, 
            email=form.email.data, role= 0,
            password=becrypt.\
                generate_password_hash(form.password.data)
            )

        NewUser.image= ImageProfile.query.get(1)

        try :
            db.session.add(NewUser)
            db.session.commit()
            
            db.session.add(UnverifiedUser(NewUser.id))
            db.session.commit()

            flash('Your account has been created successfully')
            # To create a new user by admin
            try :
                if current_user.role== 1 : 
                    return redirect(url_for('admin.user_edit', 
                        user_id= NewUser.id))
                # ---
            except AttributeError : pass
            
            return redirect(url_for('user.confirm_registration'))
        
        except IntegrityError:
            db.session.rollback()
            flash('Error, try again')
            return custom_render_template('user/register.html',
                title='Register', form=form)
    # ---
    return custom_render_template('user/register.html',
        title='Register', form=form)
# End Route

@user.route('logout/')
@login_required
def logout():
    logout_user()
    flash('You have successfully logged out')
    return redirect(url_for('user.index'))
# End Route

@user.route('confirm/')
@login_required
def confirm_registration():

    # Get Datas
    email = current_user.email
    resend = request.args.get(key='resend')
    token = request.args.get(key='token', type=str)


    user_auth = UnverifiedUser.query.filter(
        UnverifiedUser.user_id.ilike(current_user.id)).first()

    # If the user is active
    if not user_auth:
        return custom_render_template(
            'user/email-confirmation-required.html',
            msg=f"This user is already activated.",
            url_href=url_for('user.profile'),
            url_text='Profile')
    # ---


    # To resend the email
    if resend :

        flash('The authentication email has been re-send to your email address')
        return redirect(url_for('user.confirm_registration'))
        
    # ---

    # Request without arguments
    if (not token):
        """
        If you send a request to this room without a token argument
        (an authentication token will be created and sent)
        """
        token = add_to_redis(current_user, 'register')
        send_registration_message(current_user, token)
    
        message = f"""Account activation link sent to your email address:
                {config.MAIL_USERNAME}
                Please follow the link inside to continue."""
    
        return custom_render_template(
            'user/email-confirmation-required.html', msg=message,
            url_href=url_for('user.confirm_registration', resend=True),
            url_text='Re-Send'
        )
    # ---

    # Checking the validity of the token
    token_from_redis = get_from_redis(current_user, 'register')

    if (not token_from_redis) or \
        (str(token) != token_from_redis.decode('UTF-8')):
        return custom_render_template(
            'user/email-confirmation-required.html',
            msg=f"The token has expired!",
            
            url_href=url_for(
                'user.confirm_registration', resend=True),
            url_text='Re-Send'
        )
    # ---

    # Activate the user
    delete_from_redis(current_user, 'register')

    UnverifiedUser.query.\
        filter(UnverifiedUser.user_id == current_user.id).\
            delete(synchronize_session='evaluate')
    db.session.commit()
    # ---

    flash('Your email has been successfully verified! welcome')
    return redirect(url_for('user.profile'))
# End Route

@user.route('profile/iframe/posts/<string:q>')
@login_required
def _show_posts(q):
    if q== 'like': posts= current_user.posts_liked
    elif q== 'dislike' : posts= current_user.posts_disliked
    elif q== 'saved' : posts= current_user.posts_saved
    else : abort(403)
    return custom_render_template('user/_posts.html', posts= posts)
# End Route