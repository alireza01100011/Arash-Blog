import os
import json

class config():
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')


class site():
    with open(os.path.join('' , 'site.json') , 'r') as file:
        JSON_DATA = json.load(file)