from flask_wtf import FlaskForm
from wtforms import StringField , TextAreaField
from wtforms.validators import DataRequired , ValidationError
from utils.forms import MultipleCheckboxField

from mod_blog.models import Post
from mod_user.froms import _get_fields

class PostForm(FlaskForm):
    title = StringField( label='Title' , validators=[DataRequired()])
    content = TextAreaField(label='Content' , validators=[DataRequired()])
    summary = StringField(label='Summary' , validators=[])
    slug = StringField('Slug' , validators=[DataRequired()])
    # categories = MultipleCheckboxField(label='Categories' , coerce=int)

    def validate_title(self , title):
        post = Post.query.filter(Post.title.ilike(f'{title}')).first()
        if post :
            raise ValidationError('This title already exists')
    
    def validate_content(self , content):
        content = Post.query.filter(Post.content.ilike(f'{content}')).first()
        if content :
            raise ValidationError('This content already exists')
        
    def validate_summary(self , summary):
        summary = Post.query.filter(Post.summary.ilike(f'{summary}')).first()
        if summary :
            raise ValidationError('This summary already exists')

    def validate_slug(self , slug):
        slug = Post.query.filter(Post.slug.ilike(f'{slug}')).first()
        if slug :
            raise ValidationError('This slug already exists')
    
    def get_fields(self):
        return _get_fields(self)