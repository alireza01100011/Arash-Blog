from flask import render_template ,  redirect , url_for

from mod_blog.models import User , ImageProfile , SITE , INDEXPAGE
from app import app , db , becrypt
import os



@app.route('/setup' , methods=['GET' , 'POST'])
def setupsite():
    models = [ImageProfile() , SITE() , INDEXPAGE()]
    models[0].filename = "default-profile.svg"
    for _ in models:
        db.session.add(_)
        db.session.commit()

    NewUser = User(
        full_name= "Admin" ,
        email="admin@admin.com" ,
        password= becrypt.generate_password_hash('admin') ,
        role= 1
    )
    NewUser.image = ImageProfile.query.get(1)

    db.session.add(NewUser)
    db.session.commit()

    # Comment line 42 in the app file
    with open('app.py' , 'r+') as re :
        lines = re.readlines()

        lines[41] = f"# {lines[41]}"
        lines.insert(43 , f'# ^ The above line is automatically commented (By SETUP.PY)\n\n')

        text = "".join(lines)
        
        with open('app.py' , 'w') as wr :  wr.write(text)
    
    return f"The site is ready, please login... <br> Email : admin@admin.com <br><br> Paassword : admin <br> <a href='{ url_for('user.login') }'> Login Page <a>"
