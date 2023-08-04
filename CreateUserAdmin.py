from mod_blog.models import User
from app import db , becrypt

# Creating the first admin user to start
def CreateUserAdmin():
    NewUser = User(
            'admin' , 'admin@admin.com' ,
            becrypt.generate_password_hash('root') ,
            1)
    db.session.add(NewUser)
    db.session.commit()