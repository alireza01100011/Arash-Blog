from flask_wtf import FlaskForm
from wtforms import StringField , FileField , IntegerField
from wtforms.validators import DataRequired , Length
from flask_wtf.file import FileAllowed 
from flask_ckeditor import CKEditorField
from utils.forms import _get_fields , formats

class SiteSettingsForm(FlaskForm):
    name_site = StringField(label="Site Name" , validators=[DataRequired() , Length(1 , 128)]) 
    logo_site = FileField('Logo Site',
                      validators=[
                          
                          FileAllowed(
                              formats['image'] ,
                              message='This file extension is not supported'
                          )
                      ]
            )
    search_placeholder = StringField(label="Search Placeholder" , validators=[DataRequired() , Length(1 , 16)]) 


    def get_fields(self):
        return _get_fields(self)
    
class IndexPageSettingsForm(FlaskForm):
    title_home = StringField(label="Home Description" , validators=[DataRequired() , Length(1 , 128)])
    site_title = CKEditorField(label='Site Title' , validators=[DataRequired()])
    description = CKEditorField(label="Home Description" , validators=[DataRequired() , Length(1 , 128)])
    total_posts = IntegerField(label="How many posts are displayed on the home page" , validators=[DataRequired()]) 
    total_special_posts = IntegerField(label="How many special posts are displayed on the home page" , validators=[DataRequired()]) 

    def get_fields(self):
        return _get_fields(self)
    
class FooterContentSettingsForm(FlaskForm):

    footer = CKEditorField(label='Footer Content' , validators=[DataRequired()])

    def get_fields(self):
        return _get_fields(self)