from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed , FileRequired
from wtforms import StringField , FileField
from wtforms.validators import DataRequired , ValidationError

from utils.forms  import _get_fields , formats

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
                            FileAllowed(
                                formats['image'] + formats['audio'] + formats['video'] + formats['exe'] + formats['compressed'] + formats['document'],
                                message='This file extension is not supported'
                                )
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
                          FileAllowed(
                              formats['audio'] + formats['image'] + formats['video'] ,
                              message='This file extension is not supported'
                          )
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