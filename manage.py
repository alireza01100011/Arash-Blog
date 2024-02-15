import click
from flask.cli import FlaskGroup

from app import app, db , becrypt 
from mod_blog.models import User, ImageProfile, Admin, INDEXPAGE, SITE
cli = FlaskGroup(app)

@cli.command('create-db')
def create_db():
    from os import system
    for db_com in ('init', 'migrate', 'upgrade'):
        system(f'python -m flask db {db_com}')
    
    DefultImageProfile = ImageProfile()
    DefultImageProfile.filename = 'default-profile.svg'
    site = SITE()
    indexPage = INDEXPAGE()

    db.session.add_all((DefultImageProfile, site, indexPage))
    db.session.commit()



# Creating the first admin user to start
@cli.command('create-admin')
@click.argument('fullname')
@click.argument('email')
@click.argument('password')
def CreateUserAdmin(fullname, email, password):
    AdminUser = User(
            fullname, email,
            becrypt.generate_password_hash(password),1)
    AdminUser.image= ImageProfile.query.get(1)
    
    NewAdmin = Admin()
    NewAdmin.email = email

    db.session.add_all((AdminUser, NewAdmin))
    db.session.commit()

    print(f'Create Admin User : \n email {email},\n password : {password}')

if __name__ == '__main__':
    cli()
