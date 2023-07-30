from flask_wtf import FlaskForm
from wtforms import StringField , TextAreaField
from wtforms.validators import DataRequired
from utils.forms import ListWidget

class PostForm(FlaskForm):
    title = StringField( label='Title' , validators=[DataRequired()])
    content = TextAreaField(label='Content' , validators=[DataRequired()])
    summary = StringField(label='Summary' , validators=[])
    slug = StringField('Slug' , validators=[DataRequired()])
    categories = ListWidget(label='Categories' , coerce=int)