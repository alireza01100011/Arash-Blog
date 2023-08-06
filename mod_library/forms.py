from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed , FileRequired
from wtforms import StringField , FileField
from wtforms.validators import DataRequired , ValidationError

from mod_blog.forms  import _get_fields

from mod_blog.models import File
class FileForm(FlaskForm):
    name = StringField('Name File' , validators=[DataRequired()])
    discription = StringField('Discription File' , validators=[])
    alt = StringField('Alt File' , validators=[])
    file = FileField('File' , 
                     validators=[
                         FileRequired() , 
                         FileAllowed(['zip' , 'rar' , 'jpg' , 'jpeg' , 'png' , 'mp3' , 'mp4', 'exe' , 'apk' , 'txt'] , message='Filee')
                         ])
    
    def validate_name(self , name):
        _ = File.query.filter(File.name.ilike(f'{name.data}')).first()
        if _ :
            raise ValidationError('This Name Is Already Used')
    
    def get_fields(self):
        return _get_fields(self)

    

