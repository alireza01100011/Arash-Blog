from sqlalchemy import Column , Integer , String , Text , Table , ForeignKey , DateTime
from app import db 

from datetime import datetime 

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
    views = Column(Integer , nullable=False , unique=False)
    author_id = Column(Integer , ForeignKey('users.id') , nullable=True)
    categories = db.relationship('Category' , secondary=posts_categories , back_populates='posts')
    users_liks = db.relationship('User' , secondary=liks , back_populates='posts_liked')
    users_disliks = db.relationship('User' , secondary=disliks , back_populates='posts_disliked')


    def __repr__(self):
        return f'Post < {self.id} - {self.title[:24]} - {self.slug}> '
    
    def __init__(self , title : str , content : str , summary : str , slug : str , image : int ):
        self.title = title
        self.content = content
        self.summary = summary
        self.slug = slug
        self.image = image


class Category(db.Model):
    __tablename__ = 'categories'
    id = Column(Integer() , primary_key=True , unique=True , nullable=False)
    name = Column(String(128) , nullable=False , unique=True)
    description = Column(String(256) , nullable=True , unique=True)
    slug = Column(String(128) , nullable=False , unique=True)
    posts = db.relationship('Post' , secondary=posts_categories , back_populates='categories')

    def __repr__(self):
        return f'Category <{self.id} - {self.name} - {self.slug}>'
    
    def __init__(self , name : str , description : str , slug : str ):
        self.name = name 
        self.description = description
        self.slug = slug

class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer , primary_key=True)
    full_name = Column(String(128) , nullable=False , unique=False)
    email = Column(Integer , nullable=False , unique=True)
    password = Column(String(128) , nullable=False , unique=False)
    role = Column(Integer , nullable=False , unique=False)
    posts = db.relationship('Post' , backref='author')
    posts_liked = db.relationship('Post' , secondary=liks , back_populates='users_liks')
    posts_disliked = db.relationship('Post' , secondary=liks , back_populates='users_disliks')

    def __repr__(self):
        return f'User < {self.id} - {self.email}> '
    
    def __init__(self , full_name : str , email : str , password : str , role : int):
        self.full_name = full_name
        self.email = email 
        self.password = password
        self.role = role
        