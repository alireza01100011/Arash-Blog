from flask import render_template ,  redirect ,  request ,flash , url_for
from flask_login import current_user
from mod_library import library
from mod_library.forms import FileForm

from mod_blog.models import File 
from app import db 
import uuid
### File ###

# Show  File
@library.route('files/')
def file_show():
    file_type = request.args.get('type' , default='all' , type=str)
    page = request.args.get('p' , default=1 , type=int)
    per_page = request.args.get('n' , default=30 , type=int)

    files = File.query.paginate(page=page , per_page=per_page , error_out=False)

    return render_template('admin/library/files/file.html' , title='Show Files' , files=files)


# Upload File
@library.route('files/upload/' , methods=['GET' , 'POST'])
def file_upload():
    form = FileForm()
    
    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('admin/library/file-library.html' , title='Upload New File' , form=form )

        _totla_test = 0
        while True :
            _totla_test += 1
            filename = f'{uuid.uuid1()}_{form.file.data.filename}'
            _ = File.query.filter(File.filename.ilike(f'{filename}')).first()
            if not _ : break
            if _totla_test == 100 : 
                flash('Error, please try again')
                return render_template('admin/library/files/file-form.html' , title='Upload New File' , form=form )        
        
        NewFile = File(
            filename=filename,
            name=form.name.data,
            alt=form.alt.data,
            discription=form.discription.data
        )
        try :
            db.session.add(NewFile)
            db.session.commit()
            file = request.files['file']
            file.save(f'static/library/files/{filename}')
            flash('File uploaded successfully')
            return redirect(url_for('admin.library.file_show'))
        except :
            db.session.rollback()
            flash("Error, please try again")
    return render_template('admin/library/files/file-form.html' , title='Upload New File' , form=form )