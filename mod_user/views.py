from flask import render_template ,  redirect ,  request , url_for
from flask_login import login_user , current_user , logout_user 
from mod_user import user
from mod_user.froms import RegisterForm , LoginForm
from mod_blog.models import User
from app import db , becrypt 

@user.route('/')
def index():
    return 'User'



@user.route('login/' , methods=['GET' , 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))
    form = LoginForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            return 'Error'
        
        email , password , remember = form.email.data , form.password.data , form.remember.data
        user = User.query.filter(User.email.ilike(f'{email}')).first()
        if becrypt.check_password_hash(user.password , password) and user != None :
            login_user(user , remember=remember)
            return 'Loggin'
        return 'True'
    return render_template('user/login.html' , title='Login' , form=form)


@user.route('register/' , methods=['GET' , 'POST'])
def register():
    pass
