import os
import json

class config():
    SECRET_KEY = os.urandom(64)

    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    REDIS_SERVER_URL = os.getenv('REDIS_SERVER_URL')

    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')

    SERVER_NAME_MAIL = os.getenv('SERVER_NAME_MAIL') 

class site():
    with open(os.path.join('' , 'site.json') , 'r') as file:
        JSON_DATA = json.load(file)