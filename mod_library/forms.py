from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed , FileRequired
from wtforms import StringField , FileField
from wtforms.validators import DataRequired , ValidationError

from mod_blog.forms  import _get_fields

from mod_blog.models import File
from mod_blog.models import Madie

class FileForm(FlaskForm):
    name = StringField('Name File' , validators=[DataRequired()])
    discription = StringField('Discription File' , validators=[])
    alt = StringField('Alt File' , validators=[])

    _file = None

    file = FileField('File' , 
                        validators =[
                            FileRequired(),
                            FileAllowed(['zip' , 'rar' , 'jpg' , 'jpeg' , 'png' , 'webp' , 'mp3' , 'mp4', 'exe' , 'apk' , 'txt'] , message='This file extension is not supported')
                            ])
    
    def validate_name(self , name):
        if self._file and self._file.name == name.data :
            return
        _ = File.query.filter(File.name.ilike(f'{name.data}')).first()
        if _ :
            raise ValidationError('This Name Is Already Used')
    
    def get_fields(self):
        return _get_fields(self)

    

class MadieForm(FlaskForm):
    name = StringField('Name' , validators=[DataRequired()])
    alt = StringField('Alt')
    title = StringField('Title')
    
    madie = FileField('Madie',
                      validators=[
                          FileRequired(),
                          FileAllowed(['jpg' , 'jpeg' , 'png' , 'webp' ,'gif'])
                      ]
    )
    _madie = None

    def validate_name(self , name):
        if self._madie and self._madie.name == name.data :
            return
        _ = Madie.query.filter(File.name.ilike(f'{name.data}')).first()
        if _ :
            raise ValidationError('This Name Is Already Used')
    
    def get_fields(self):
        return _get_fields(self)