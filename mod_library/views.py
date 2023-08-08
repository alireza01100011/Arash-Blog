from flask import render_template ,  redirect ,  request ,flash , url_for
from flask_login import current_user
from mod_library import library
from mod_library.forms import FileForm

from mod_blog.models import File 
from app import db 
import uuid
import os
### File ###

def CreateFileName(filename):
    _totla_test = 0
    while True :
        _totla_test += 1
        filename = f'{uuid.uuid1()}_{filename}'
        _ = File.query.filter(File.filename.ilike(f'{filename}')).first()
        if not _ : return filename
        if _totla_test == 256 : return False

# Show  File
@library.route('files/')
def file_show():
    file_type = request.args.get('type' , default='all' , type=str)
    page = request.args.get('p' , default=1 , type=int)
    per_page = request.args.get('n' , default=30 , type=int)

    files = File.query.order_by(File.id.desc()).paginate(page=page , per_page=per_page , error_out=False)

    return render_template('admin/library/files/file.html' , title='Show Files' , files=files)


# Upload File
@library.route('files/upload/' , methods=['GET' , 'POST'])
def file_upload():
    form = FileForm()

    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('admin/library/files/file-form.html' , title='Upload New File' , form=form )
        
        filename = CreateFileName(form.file.data.filename)
        if not filename :
            flash('Error, please try again')
            return render_template('admin/library/files/file-form.html' , title='Upload New File' , form=form )        
        
        NewFile = File(
            filename=filename,
            name=form.name.data,
            alt=form.alt.data,
            discription=form.discription.data
        )
        NewFile.uploader = current_user
        
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

# File Edit
@library.route('files/edit/<int:file_id>' , methods=['GET' , 'POST'])
def file_edit(file_id):
    file = File.query.get_or_404(int(file_id))
    
    from flask_wtf.file import FileAllowed
    form = FileForm()
    form._file = file
    form.file.validators = ([FileAllowed(['zip' , 'rar' , 'jpg' , 'jpeg' , 'png' , 'webp' , 'mp3' , 'mp4', 'exe' , 'apk' , 'txt'] , message='This file extension is not supported')])
    
    if request.method == 'GET':
        form.name.data = file.name
        form.discription.data = file.discription
        form.alt.data = file.alt

    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('admin/library/files/file-form.html' , title=f'Update File {file.name}' , form=form , file=file)    

        file.name = form.name.data
        file.discription = form.discription.data
        file.alt = form.alt.data

        if request.files['file'] :
            os.remove(os.path.join('static/library/files' , file.filename))
            filename = CreateFileName(form.file.data.filename)
            
            if not filename :
                flash("Error, please try again (Error creating file name)")
                return render_template('admin/library/files/file-form.html' , title=f'Update File {file.name}' , form=form , file=file)

            file.filename = filename
            request.files['file'].save(os.path.join('static/library/files' , filename))

        try :
            db.session.commit()
            flash('File Update successfully')
            return redirect(url_for('admin.library.file_show'))
        except :
            db.session.rollback()
            flash("Error, please try again")

        
    return render_template('admin/library/files/file-form.html' , title=f'Update File {file.name}' , form=form , file=file)

# File Delete
@library.route('files/delete/<int:file_id>')
def file_delete(file_id):
    file = File.query.get_or_404(int(file_id))

    try :
        db.session.delete(file)
        db.session.commit()
        os.remove( os.path.join('static/library/files' , file.filename))
        flash('File deleted successfully')
    except :
        db.session.rollback()
        flash('File deletion was not successful')
    
    return redirect(url_for('admin.library.file_show'))