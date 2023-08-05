from sqlalchemy import Column , Integer , String , Text , Table , ForeignKey , DateTime
from datetime import datetime
from flask_login import UserMixin
from app import db , login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


liks = Table('liks' , db.metadata ,
    Column('user_id' , Integer , ForeignKey('users.id' , ondelete='cascade')),
    Column('post_id' , Integer , ForeignKey('posts.id' , ondelete='cascade')),
    Column('time' , DateTime , default=datetime.now)
)

disliks = Table('disliks' , db.metadata ,
    Column('user_id' , Integer , ForeignKey('users.id' , ondelete='cascade')),
    Column('post_id' , Integer , ForeignKey('posts.id' , ondelete='cascade')),
    Column('time' , DateTime , default=datetime.now)

)
posts_categories = Table( 'posts_categories' , db.metadata ,
    Column('post_id' , Integer , ForeignKey('posts.id' , ondelete='cascade')),
    Column('categories_id' , Integer , ForeignKey('categories.id' , ondelete='cascade'))
)

class Post(db.Model):
    __tablename__ = 'posts'
    id = Column(Integer() , primary_key=True , unique=True , nullable=False)
    title = Column(String(256) , nullable=False , unique=True)
    content = Column(Text , nullable=False , unique=True)
    summary = Column(String(256) , nullable=True , unique=True)
    slug = Column(String(128) , nullable=False , unique=True)
    image = Column(Integer , nullable=True , unique=False)
    
    views = Column(Integer , nullable=False , unique=False , default=0)
    total_liks = Column(Integer , default=0 , unique=False , nullable=True)
    total_disliks = Column(Integer , default=0 , unique=False , nullable=True)
    time = Column(DateTime , default=datetime.now)

    author_id = Column(Integer , ForeignKey('users.id') , nullable=True)
    comments = db.relationship('Comment' , backref='post')
    categories = db.relationship('Category' , secondary=posts_categories , back_populates='posts')
    users_liks = db.relationship('User' ,viewonly=True,  secondary=liks , back_populates='posts_liked')
    users_disliks = db.relationship('User' , viewonly=True, secondary=disliks , back_populates='posts_disliked')


    def __repr__(self):
        return f'{self.__class__.__name__} < {self.id} - {self.title[:24]} - {self.slug}> '
    
    def __init__(self , title : str , content : str , summary : str , slug : str , image : int ):
        self.title = title
        self.content = content
        self.summary = summary
        self.slug = slug
        self.image = image



class Comment(db.Model):
    id = Column(Integer , primary_key=True)
    content = Column(String(1024) , nullable=False , unique=False)
    post_id = Column(Integer , ForeignKey('posts.id') , nullable=True)
    user_id = Column(Integer , ForeignKey('users.id') , nullable=True)
    time = Column(DateTime , default=datetime.now)

    def __repr__(self):
        return f'{self.__class__.__name__} <{self.id} , {self.post_id}> '


class Category(db.Model):
    __tablename__ = 'categories'
    id = Column(Integer() , primary_key=True , unique=True , nullable=False)
    name = Column(String(128) , nullable=False , unique=True)
    description = Column(String(256) , nullable=True , unique=True)
    slug = Column(String(128) , nullable=False , unique=True)
    time = Column(DateTime , default=datetime.now)
    posts = db.relationship('Post' , secondary=posts_categories , back_populates='categories')

    def __repr__(self):
        return f'{self.__class__.__name__} <{self.id} - {self.name} - {self.slug}>'
    
    def __init__(self , name : str , description : str , slug : str ):
        self.name = name 
        self.description = description
        self.slug = slug

class User(db.Model , UserMixin):
    __tablename__ = 'users'
    id = Column(Integer , primary_key=True)
    full_name = Column(String(128) , nullable=False , unique=False)
    email = Column(String(128) , nullable=False , unique=True)
    password = Column(String(128) , nullable=False , unique=False)
    role = Column(Integer , nullable=False , unique=False)
    image_id = Column(Integer , ForeignKey('imageprofile.id') , nullable=True)
    posts = db.relationship('Post' , backref='author')
    files = db.relationship('File' , backref='uploader')
    madies = db.relationship('Madie' , backref='uploader')
    comments = db.relationship('Comment' , backref='user')
    posts_liked = db.relationship('Post' , secondary=liks , back_populates='users_liks')
    posts_disliked = db.relationship('Post' , secondary=liks , back_populates='users_disliks')

    def __repr__(self):
        return f'{self.__class__.__name__} < {self.id} - {self.email}> '
    
    def __init__(self , full_name : str , email : str , password : str , role : int):
        self.full_name = full_name
        self.email = email 
        self.password = password
        self.role = role

class ImageProfile(db.Model):
    __tablename__ = "imageprofile"
    id = Column(Integer , primary_key=True)
    filename = Column(String(256) , nullable=False , unique=True)
    user = db.relationship('User' , backref='image')


class File(db.Model):
    __tablename__ = 'files'
    id = Column(Integer , primary_key=True)
    filename = Column(String(256) , nullable=False , unique=True)
    name = Column(String(256) , nullable=False , unique=True)
    alt = Column(String(256) , nullable=True , unique=False)
    discription = Column(String(256) , nullable=True , unique=False)
    time = Column(DateTime , default=datetime.now)
    uploader_id = Column(Integer , ForeignKey('users.id'))

    def __init__(self , filename : str , name : str , alt : str , discription : str):
        self.filename = filename
        self.name = name
        self.alt = alt
        self.discription = discription


class Madie(db.Model):
    __tablename__ = 'madies'
    id = Column(Integer , primary_key=True)
    filename = Column(String(256) , nullable=False , unique=True)
    name = Column(String(256) , nullable=False , unique=True)
    alt = Column(String(256) , nullable=True , unique=False)
    title = Column(String(256) , nullable=True , unique=False)
    time = Column(DateTime , default=datetime.now)
    uploader_id = Column(Integer , ForeignKey('users.id'))