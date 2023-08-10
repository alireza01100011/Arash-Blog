from flask import render_template ,  redirect ,  request ,flash , url_for , send_file
from flask_login import current_user
from flask_wtf.file import FileAllowed
from mod_library import library_admin , library_views
from mod_library.forms import FileForm , MadieForm , formats

from mod_blog.models import File , Madie
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
@library_admin.route('files/')
def file_show():
    file_type = request.args.get('type' , default='all' , type=str)
    page = request.args.get('p' , default=1 , type=int)
    per_page = request.args.get('n' , default=30 , type=int)

    files = File.query.order_by(File.id.desc()).paginate(page=page , per_page=per_page , error_out=False)

    return render_template('admin/library/files/file.html' , title='Show Files' , files=files)


# Upload File
@library_admin.route('files/upload/' , methods=['GET' , 'POST'])
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
@library_admin.route('files/edit/<int:file_id>' , methods=['GET' , 'POST'])
def file_edit(file_id):
    file = File.query.get_or_404(int(file_id))
    
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
@library_admin.route('files/delete/<int:file_id>')
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


# Madies

# Show Madie
@library_admin.route('madies/')
def madie_show():
    madie_type = request.args.get('type' , default='all' , type=str)
    per_page = request.args.get('n' , default=30 , type=int)
    page = request.args.get('p' , default=1 , type=int)

    madies = Madie.query.order_by(Madie.id.desc()).paginate(page=page , per_page=per_page , error_out=False)

    return render_template('admin/library/madies/madie.html' , title = 'Show Madies' , madies = madies)


# Upload Madie
@library_admin.route('madies/upload/' , methods=['GET' , 'POST'])
def madie_upload():
    form = MadieForm()
    
    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('admin/library/madies/madie-form.html' , title='Upload New Madie' , form=form)
        
        file = request.files['madie']
        filename = CreateFileName(form.madie.data.filename)
        
        if not filename :
            flash("Error, please try again (Error creating file name)")
            return render_template('admin/library/madies/madie-form.html' , title='Upload New Madie' , form=form)
        
        NewMadie = Madie(
            filename=filename , 
            name = form.name.data ,
            alt = form.alt.data ,
            title= form.title.data ,
        )

        try :
            db.session.add(NewMadie)
            db.session.commit()
            file.save(os.path.join('static/library/madies' , filename))
            flash('Media upload was successful')
            return redirect(url_for('admin.library.madie_show'))
        except :
            db.session.rollback()
            flash('Media upload failed' , 'danger')
    
    return render_template('admin/library/madies/madie-form.html' , title='Upload New Madie' , form=form)


# Madie Edit
@library_admin.route('madies/edit/<int:madie_id>' , methods=['GET' , 'POST'])
def madie_edit(madie_id):
    madie = Madie.query.get_or_404(int(madie_id))

    form = MadieForm()
    form._madie = madie
    form.madie.validators = (
        [
            FileAllowed(
                formats['audio'] + formats['image'] + formats['video'] , 
                message='This file extension is not supported' )
        ]
        )

    if request.method == 'GET':
        form.name.data = madie.name
        form.alt.data = madie.alt
        form.title.data = madie.title
    
    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('admin/library/madies/madie-form.html' , title=f'Edit {madie.name}' , form = form , madie=madie)
    
        madie.name = form.name.data
        madie.alt = form.alt.data
        madie.title = form.title.data
        
        file = request.files['madie']
        if file :
            filename = CreateFileName(file.filename)

            if not filename :
                flash("Error, please try again (Error creating file name)")
                return render_template('admin/library/madies/madie-form.html' , title=f'Edit {madie.name}' , form = form , madie=madie)
            
            try :
                os.remove(os.path.join('static/library/madies' , madie.filename))
            except FileNotFoundError :
                flash('The previous file was not found and we failed to delete it!' , 'warning')

            file.save(os.path.join('static/library/madies/' , filename))
            
            madie.filename = filename
        
        try :
            db.session.commit()
            flash('Madie Update successfully')
            return redirect(url_for('admin.library.madie_show'))
        except :
            db.session.rollback()
            flash("Error, please try again")
    return render_template('admin/library/madies/madie-form.html' , title=f'Edit {madie.name}' , form = form , madie=madie)

# Madie DeLete
@library_admin.route('madies/delete/<int:madie_id>')
def madie_delete(madie_id):
    madie = Madie.query.get_or_404(int(madie_id))
    try :
        db.session.delete(madie)
        db.session.commit()
        os.remove(os.path.join('static/library/madies' , madie.filename))
        flash('The media was successfully removed')
    except :
        db.session.rollback()
        flash('The media was not successfully deleted')
    
    return redirect(url_for('admin.library.madie_show'))