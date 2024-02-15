import os
import json

class config():
    SECRET_KEY = os.urandom(64)
    SECRET_KEY = 'asdfasdfasdfadfS'
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    REDIS_SERVER_URL = os.getenv('REDIS_SERVER_URL')

    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')

    SERVER_NAME_MAIL = os.getenv('SERVER_NAME_MAIL') 


class DictToClass():
    def __init__(self, _dict:dict):
        for key, value in _dict.items():
            setattr(self, key, value)
