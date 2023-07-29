from flask_wtf import FlaskForm
from wtforms.fields import StringField , EmailField , PasswordField , BooleanField
from wtforms.validators import DataRequired , Email , EqualTo , ValidationError

from mod_blog.models import User

class LoginForm(FlaskForm):
    email = EmailField('Email' ,validators=[DataRequired() ])
    password = PasswordField('Password' , validators=[DataRequired()])
    remember = BooleanField('Remember Me' ,validators=[])
    
    def validate_email(self , email):
        e = User.query.filter(User.email.ilike(f'{email.data}')).first()
        if e == None :
            raise ValidationError('There is no email entered')

class RegisterForm(FlaskForm):
    fullname = StringField('Full Name' , validators=[DataRequired()])
    email = StringField('Email' , validators=[DataRequired() ])
    password = StringField('Password' , validators=[DataRequired()])
    confirm_password = StringField('Confirm Password' , validators=[DataRequired() , EqualTo(password , message='Password Must Match')])

    def validate_email(self , email):
        e = User.query.filter(User.email.ilike(f'{email}')).first()
        if e != None :
            raise ValidationError('This Email Already Exists')
