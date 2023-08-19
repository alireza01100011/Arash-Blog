from flask_wtf import FlaskForm
from wtforms import StringField , TextAreaField , IntegerField
from wtforms.validators import DataRequired ,Length , ValidationError
from utils.forms import MultipleCheckboxField , _get_fields

from mod_blog.models import Post , Category

class PostForm(FlaskForm):
    title = StringField( label='Title' , validators=[DataRequired()])
    content = TextAreaField(label='Content' , validators=[DataRequired()])
    summary = StringField(label='Summary' , validators=[])
    slug = StringField('Slug' , validators=[DataRequired()])
    read_time = IntegerField('Read Time /M ( If the value is 0, it is calculated automatically )')
    categories = MultipleCheckboxField(label='Categories' , coerce=int)
    
    _post = None 
    
    def validate_title(self , title):
        # To avoid "This title already exists" error during update
        if self._post and self._post.title == title.data : return

        _ = Post.query.filter(Post.title.ilike(f'{title.data}')).first()
        if _ :
            raise ValidationError('This title already exists')
    
    def validate_content(self , content):
        # To avoid "This content already exists" error during update
        if self._post and self._post.content == content.data : return

        _ = Post.query.filter(Post.content.ilike(f'{content.data}')).first()
        if _ :
            raise ValidationError('This content already exists')
        
    def validate_summary(self , summary):
        # To avoid "This summary already exists" error during update
        if self._post and self._post.summary == summary.data : return

        _ = Post.query.filter(Post.summary.ilike(f'{summary.data}')).first()
        if _ :
            raise ValidationError('This summary already exists')

    def validate_slug(self , slug):
        # To avoid "This slug already exists" error during update
        if self._post and self._post.slug == slug.data : return

        _ = Post.query.filter(Post.slug.ilike(f'{slug.data}')).first()
        if _ :
            raise ValidationError('This slug already exists')
    
    def get_fields(self):
        return _get_fields(self)


class CategoryForm(FlaskForm):
    name = StringField('Name' , validators=[DataRequired() , Length(1 , 128)])
    description = TextAreaField('Description' , validators=[DataRequired() , Length(1 , 256)])
    slug = StringField('Slug' , validators=[DataRequired() , Length(1 , 128)])

    _category = None
    def validate_name(self , name):
        # To avoid "This name already exists" error during update
        if self._category and self._category.name == name.data : return

        _ = Category.query.filter(Category.name.ilike(f'{name.data}')).first()
        if _ :
            raise ValidationError('This Name Alredy Exists')
    
    def validate_description(self , description):
        # To avoid "This description already exists" error during update
        if self._category and self._category.description == description.data : return

        _ = Category.query.filter(Category.description.ilike(f'{description.data}')).first()
        if _ :
            raise ValidationError('This Description Alredy Exists')
    
    def validate_slug(self , slug):
        # To avoid "This slug already exists" error during update
        if self._category and self._category.slug == slug.data : return
        
        _ = Category.query.filter(Category.slug.like(f'{slug.data}')).first()
        if _ :
            raise ValidationError("This Slug Alredy Exists")
        
    def get_fields(self):
        return _get_fields(self)