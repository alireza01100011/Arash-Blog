from flask_wtf import FlaskForm
from wtforms.fields import StringField , EmailField , PasswordField , BooleanField
from wtforms.validators import DataRequired , Email , EqualTo , ValidationError
from app import becrypt
from mod_blog.models import User

import re
def _get_fields(obj):
    fields = [_ for _ in obj._fields]
    return [getattr(obj , _ ) for _ in fields]

class LoginForm(FlaskForm):
    email = EmailField('Email' ,validators=[DataRequired() ])
    password = PasswordField('Password' , validators=[DataRequired()])
    remember = BooleanField('Remember Me' ,validators=[])
    
    def validate_email(self , email):
        user = User.query.filter(User.email.ilike(f'{email.data}')).first()
        if not user or not becrypt.check_password_hash(user.password , self.password.data) :
            raise ValidationError('The email or password is incorrect')
            


    def get_fields(self):
        return _get_fields(self)

class RegisterForm(FlaskForm):
    fullname = StringField('Full Name' , validators=[DataRequired()])
    email = StringField('Email' , validators=[DataRequired() ])
    password = StringField('Password' , validators=[DataRequired()])
    confirm_password = StringField('Confirm Password' , validators=[DataRequired() , EqualTo('password' , message='Password Must Match')])

    def validate_email(self , email):
        _ = User.query.filter(User.email.ilike(f'{email.data}')).first()
        if _ :
            raise ValidationError('This Email Already Exists')
    
    def validate_password(self , password):        
        if not len(password.data) >= 8 :
            raise ValidationError('The password is shorter than 8 characters')
             
        if not re.search("[a-z]", password.data) or not re.search("[A-Z]", password.data) or not re.search("[0-9]", password.data):
            raise ValidationError('The password is simple, please use a combination of uppercase and lowercase letters and numbers')
    
    def get_fields(self):
        return _get_fields(self)
