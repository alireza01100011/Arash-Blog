from flask import render_template ,  redirect ,  request , url_for , flash
from sqlalchemy.exc import IntegrityError
from flask_login import login_user , current_user , logout_user , login_required
from mod_user import user
from mod_user.utils import refute_only_view
from mod_user.froms import RegisterForm , LoginForm
from mod_blog.models import User
from app import db , becrypt 

@user.route('/')
@user.route('profile/')
def index():
    return render_template('user/index.html' , title='User')



@user.route('login/' , methods=['GET' , 'POST'])

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
@refute_only_view
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
        
        try :
            db.session.add(NewUser)
            db.session.commit()
            return redirect(url_for('user.login'))
        except IntegrityError:
            db.session.rollback()
            return 'Error'
    
    return render_template('user/register.html' , title='Register' , form=form)

@user.route('logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user.index'))