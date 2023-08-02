from flask_wtf import FlaskForm
from wtforms import StringField , TextAreaField
from wtforms.validators import DataRequired ,Length , ValidationError
from utils.forms import MultipleCheckboxField

from mod_blog.models import Post , Category
from mod_user.froms import _get_fields

class PostForm(FlaskForm):
    title = StringField( label='Title' , validators=[DataRequired()])
    content = TextAreaField(label='Content' , validators=[DataRequired()])
    summary = StringField(label='Summary' , validators=[])
    slug = StringField('Slug' , validators=[DataRequired()])
    # categories = MultipleCheckboxField(label='Categories' , coerce=int)

    def validate_title(self , title):
        _ = Post.query.filter(Post.title.ilike(f'{title.data}')).first()
        if _ :
            raise ValidationError('This title already exists')
    
    def validate_content(self , content):
        _ = Post.query.filter(Post.content.ilike(f'{content.data}')).first()
        if _ :
            raise ValidationError('This content already exists')
        
    def validate_summary(self , summary):
        _ = Post.query.filter(Post.summary.ilike(f'{summary.data}')).first()
        if _ :
            raise ValidationError('This summary already exists')

    def validate_slug(self , slug):
        _ = Post.query.filter(Post.slug.ilike(f'{slug.data}')).first()
        if _ :
            raise ValidationError('This slug already exists')
    
    def get_fields(self):
        return _get_fields(self)


class CategoryForm(FlaskForm):
    name = StringField('Name' , validators=[DataRequired() , Length(1 , 128)])
    description = TextAreaField('Description' , validators=[DataRequired() , Length(1 , 256)])
    slug = StringField('Slug' , validators=[DataRequired() , Length(1 , 128)])

    def validate_name(self , name):
        _ = Category.query.filter(Category.name.ilike(f'{name.data}')).first()
        if _ :
            raise ValidationError('This Name Alredy Exists')
    
    def validate_description(self , description):
        _ = Category.query.filter(Category.description.ilike(f'{description.data}')).first()
        if _ :
            raise ValidationError('This Description Alredy Exists')
    
    def validate_slug(self , slug):
        _ = Category.query.filter(Category.slug.like(f'{slug.data}')).first()
        if _ :
            raise ValidationError("This Slug Alredy Exists")
        
    def get_fields(self):
        return _get_fields(self)