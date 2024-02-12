# Standard libs
import smtplib
from random import randint
from email.message import EmailMessage
from functools import wraps

# Flask libs
from flask import url_for , redirect
from flask_login import current_user

# local vars
from app import redis, mail, config
from .models import User

def refute_only_view(func):
    @wraps(func)
    def decrtory(*args , **kwargs):
        if current_user.is_authenticated :
            return redirect(url_for('user.index'))
        
        return func(*args , **kwargs)
    
    return decrtory
# End Function

def refute_only_view_except_admin(func):
    @wraps(func)
    def decrtory(*args , **kwargs):
        if current_user.is_authenticated :
            if current_user.role == 1 : 
                return func(*args , **kwargs)
            
            return redirect(url_for('user.index'))
        
        return func(*args , **kwargs)
    
    return decrtory
# End Function


def add_to_redis(user:User, mode:str)-> int:
    """
    Adds a new record to Redis
    'For authentication'

    user -> User
    mode -> [register, reset_passw, ...]
    """
    token = randint(100_000, 999_999)
    redis.set(
        name=f'{user.id}_{mode.lower()}',
        value=token, ex=14400)

    return token
# End Function

def get_from_redis(user:User, mode:str)-> bytes:
    """
    Receive token from Redis
    'For authentication'

    user -> User
    mode -> [register, reset_passw, ...]
    """
    name = f'{user.id}_{mode.lower()}'
    return redis.get(name=name)
# End Function

def delete_from_redis(user:User, mode:str)->None:
    """
    delete record from Redis
    'For authentication'

    user -> User
    mode -> [register, reset_passw, ...]
    """
    name = f'{user.id}_{mode.lower()}'
    redis.delete(name)
# End Function

def send_registration_message(user:User, token:int)-> None:
    """
    Send email confirmation email
    'For authentication'

    user -> User
    toke -> int[123456]
    """
    url_email_confirm = f"http://{Configs.SERVER_NAME_MAIL}{url_for('user.confirm_registration', token=token)}"

    msg  = EmailMessage()
    msg['Subject'] = 'Welcoome - Your email verification code'
    msg['From'] = Configs.MAIL_USERNAME
    msg['To'] = user.email
    msg.set_content(
        f"""Open this link to verify your email : {url_email_confirm}""")

    with smtplib.SMTP_SSL(
        host=Configs.MAIL_SERVER, port=Configs.MAIL_PORT) as server:

        server.login(Configs.MAIL_USERNAME,
                            Configs.MAIL_PASSWORD)

        server.send_message(msg)
# End Function