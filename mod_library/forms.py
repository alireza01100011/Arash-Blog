from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed , FileRequired
from wtforms import StringField , FileField
from wtforms.validators import DataRequired

class FileForm(FlaskForm):
    name = StringField('Name File' , validators=[DataRequired()])
    discription = StringField('Discription File' , validators=[])
    alt = StringField('Alt File' , validators=[])
    file = FileField('File' , 
                     validators=[
                         DataRequired() , 
                         FileAllowed(['zip' , 'rar' , 'jpg' , 'jpeg' , 'png' , 'mp3' , 'mp4', 'exe' , 'apk'] , 'Upload File')
                         ])

