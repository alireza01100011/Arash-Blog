from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed , FileRequired
from wtforms import StringField , FileField
from wtforms.validators import DataRequired

class FileForm(FlaskForm):
    name = StringField('Name File' , validators=[DataRequired()])
    title = StringField('Title File' , validators=[])
    alt = StringField('Alt File' , validators=[])
    file = FileField('File' , 
                     validators=[
                         DataRequired() , 
                         FileAllowed(['jpeg' , 'jpg' , 'png'])
                         
                         ])