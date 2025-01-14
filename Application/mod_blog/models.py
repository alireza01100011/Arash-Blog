from sqlalchemy import Column , Integer , String , Text , Table , ForeignKey , DateTime , Float, BINARY
from datetime import datetime
from flask_login import UserMixin
from app import db , login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


liks = Table('liks' , db.metadata ,
    Column('user_id' , Integer , ForeignKey('users.id' )),
    Column('post_id' , Integer , ForeignKey('posts.id' , ondelete='cascade')),
    Column('time' , DateTime , default=datetime.now)
)

disliks = Table('disliks' , db.metadata ,
    Column('user_id' , Integer , ForeignKey('users.id' , ondelete='cascade')),
    Column('post_id' , Integer , ForeignKey('posts.id' , ondelete='cascade')),
    Column('time' , DateTime , default=datetime.now)

)

posts_saves = Table('posts_saves' , db.metadata ,
                    Column('user_id' , Integer , ForeignKey('users.id' )) ,
                    Column('post_id' , Integer , ForeignKey('posts.id' , ondelete='cascade')),
                    Column('time' , DateTime , default=datetime.now)
                    )

posts_categories = Table( 'posts_categories' , db.metadata ,
    Column('post_id' , Integer , ForeignKey('posts.id' , ondelete='cascade')),
    Column('categories_id' , Integer , ForeignKey('categories.id' , ondelete='cascade'))
)



class SITE(db.Model):
    __tablename__ = '_site'
    id = Column(Integer , primary_key=True , default=0)
    
    # Site Settings
    name_site =  Column(String(128) , nullable=False , default='Blog with Flask')
    logo_site = Column(String(128) , nullable=False , default='logo.svg')
    default_description =  Column(String(256) , nullable=False , default='Default description for all pages - Blog with Flask')
    # Navbar 
    search_placeholder = Column(String(16) , default='Search')
    
    # Footer Content
    default_footer = """<h4>Flask Blog</h4><h4>Developer : <a href="https://github.com/alireza01100011/Blog-With-Falsk">GITHUB</a></h4>"""
    footer =  Column(Text , nullable=False , default=default_footer)


class INDEXPAGE(db.Model):
    __tablename__ = '_index_page'
    # Index Page Settings
    id = Column(Integer , primary_key=True , default=0)
    title_home =  Column(String(128) , nullable=False , default='Blog with Flask')
    site_title =  Column(Text() , nullable=False , default='Blog') 
    description =  Column(String(128) , nullable=False , default='A simple blog with Python')
    total_posts = Column(Integer , default=6)
    total_special_posts = Column(Integer , default=4)

class Post(db.Model):
    __tablename__ = 'posts'
    id = Column(Integer() , primary_key=True , unique=True , nullable=False)
    title = Column(String(256) , nullable=False , unique=True)
    content = Column(Text , nullable=False)
    summary = Column(String(256) , nullable=True , unique=True)
    slug = Column(String(128) , nullable=False , unique=True)
    image = Column(Integer , nullable=True , unique=False)
    read_time = Column(Float , nullable=True , unique=False)
    special = Column(Integer , default=0 , unique=False)
    views = Column(Integer , nullable=False , unique=False , default=0)
    total_liks = Column(Integer , default=0 , unique=False , nullable=True)
    total_disliks = Column(Integer , default=0 , unique=False , nullable=True)
    time = Column(DateTime , default=datetime.now)

    author_id = Column(Integer , ForeignKey('users.id') , nullable=True)
    comments = db.relationship('Comment' , backref='post')
    categories = db.relationship('Category' , secondary=posts_categories , back_populates='posts')
    users_liks = db.relationship('User' ,viewonly=True,  secondary=liks , back_populates='posts_liked')
    users_disliks = db.relationship('User' , viewonly=True, secondary=disliks , back_populates='posts_disliked')
    users_saves = db.relationship('User' , viewonly=True , secondary=posts_saves , back_populates='posts_saved')

    def __repr__(self):
        return f'{self.__class__.__name__} < {self.id} - {self.title[:24]} - {self.slug}> '
    
    def __init__(self , title : str , content : str , summary : str , slug : str , image : int , special : int ):
        self.title = title
        self.content = content
        self.summary = summary
        self.slug = slug
        self.image = image
        self.special = special



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
    image = Column(Integer , nullable=True , unique=False )
    description = Column(String(256) , nullable=True , unique=True)
    slug = Column(String(128) , nullable=False , unique=True)
    time = Column(DateTime , default=datetime.now)
    posts = db.relationship('Post' , secondary=posts_categories , back_populates='categories')

    def __repr__(self):
        return f'{self.__class__.__name__} <{self.id} - {self.name} - {self.slug}>'
    
    def __init__(self , name : str , description : str , slug : str , image : int ):
        self.name = name 
        self.description = description
        self.slug = slug
        self.image = image
        
class User(db.Model , UserMixin):
    __tablename__ = 'users'
    id = Column(Integer , primary_key=True)
    full_name = Column(String(128) , nullable=False , unique=False)
    email = Column(String(128) , nullable=False , unique=True)
    password = Column(String(128) , nullable=False , unique=False)
    bio = Column(String(256) , nullable=True , unique=False)
    role = Column(Integer , nullable=False , unique=False)
    image_id = Column(Integer , ForeignKey('imageprofile.id') , nullable=True)
    time = Column(DateTime, default=datetime.now)
    posts = db.relationship('Post' , backref='author')
    files = db.relationship('File' , backref='uploader')
    madies = db.relationship('Madie' , backref='uploader')
    comments = db.relationship('Comment' , backref='user')
    posts_liked = db.relationship('Post' , secondary=liks , back_populates='users_liks')
    posts_disliked = db.relationship('Post' , secondary=disliks , back_populates='users_disliks')
    posts_saved = db.relationship('Post' , secondary=posts_saves , back_populates='users_saves')
    def __repr__(self):
        return f'{self.__class__.__name__} < {self.id} - {self.email}> '
    
    def __init__(self , full_name : str , email : str , password : str , role : int):
        self.full_name = full_name
        self.email = email 
        self.password = password
        self.role = role
# ---

class UnverifiedUser(db.Model):
    __tablename__ = 'unverified_users'
    id = Column(Integer , primary_key=True)
    user_id = Column(Integer , nullable=False)

    def __repr__(self)-> str:
        return f'{self.__class__.__name__} < {self.id} - {self.user_id}>'
    
    def __init__(self, user_id:int)-> None:
        self.user_id = user_id
# ---


class Admin(db.Model):
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True)
    email = Column(String(128) , nullable=False , unique=True)
    to_do = Column(Text , nullable=True , unique=False)
    
    def __repr__(self):
        return f'{self.__class__.__name__} < {self.id} - {self.email}> '

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

    def __init__(self , filename : str , name : str , alt : str , title : str):
        self.filename = filename
        self.name = name 
        self.alt = alt
        self.title = title