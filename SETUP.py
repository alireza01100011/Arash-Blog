from flask import render_template ,  redirect , url_for

from mod_blog.models import User , ImageProfile , SITE , INDEXPAGE
from app import app , db , becrypt
import os



@app.route('/setup' , methods=['GET' , 'POST'])
def setupsite():
    site = SITE()
    indxpage = INDEXPAGE()
    imageprofile = ImageProfile()
    imageprofile.filename = "default-profile.svg"

    db.session.add(imageprofile)
    db.session.add(site)
    db.session.add(indxpage)
    
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
    return "Account created successfully"