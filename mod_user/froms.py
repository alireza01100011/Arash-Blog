from flask_wtf import FlaskForm
from wtforms.fields import StringField , EmailField , PasswordField , BooleanField
from wtforms.validators import DataRequired , Email , EqualTo , ValidationError
from app import becrypt
from mod_blog.models import User


class LoginForm(FlaskForm):
    email = EmailField('Email' ,validators=[DataRequired() ])
    password = PasswordField('Password' , validators=[DataRequired()])
    remember = BooleanField('Remember Me' ,validators=[])
    
    def validate_email(self , email):
        user = User.query.filter(User.email.ilike(f'{email.data}')).first()
        if not user or not becrypt.check_password_hash(user.password , self.password.data) :
            raise ValidationError('The email or password is incorrect')
            


    def get_fields(self):
        fields = [_ for _ in self._fields]
        return [getattr(self , _ ) for _ in fields]

class RegisterForm(FlaskForm):
    fullname = StringField('Full Name' , validators=[DataRequired()])
    email = StringField('Email' , validators=[DataRequired() ])
    password = StringField('Password' , validators=[DataRequired()])
    confirm_password = StringField('Confirm Password' , validators=[DataRequired() , EqualTo('password' , message='Password Must Match')])

    def validate_email(self , email):
        e = User.query.filter(User.email.ilike(f'{email}')).first()
        if e != None :
            raise ValidationError('This Email Already Exists')
