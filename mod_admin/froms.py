from flask_wtf import FlaskForm
from wtforms import StringField 
from wtforms.validators import DataRequired , Length
from flask_ckeditor import CKEditorField
from utils.forms import _get_fields

class SiteSettingsForm(FlaskForm):
    name_site = StringField(label="Site Name" , validators=[DataRequired() , Length(1 , 128)]) 
    title_home = StringField(label="Home Title (Home Page Title)" , validators=[DataRequired() , Length(1 , 128)]) 
    h1_home = StringField(label="Home Title (Home Page Title {H1})" , validators=[DataRequired() , Length(1 , 128)]) 
    description = StringField(label="Home Description" , validators=[DataRequired() , Length(1 , 128)]) 
    footer = CKEditorField(label='Footer Content' , validators=[DataRequired()])

    def get_fields(self):
        return _get_fields(self)