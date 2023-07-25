from sqlalchemy import Column , Integer , String , Text , Table , ForeignKey 
from app import db 

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
    categories = db.relationship('Category' , secondary=posts_categories , back_populates='posts')
    
    def __repr__(self):
        return f'Post < {self.id} - {self.title[:24]} - {self.slug}> '
    
    def __init__(self , title : str , content : str , summary : str , slug : str , image : int , categories : list):
        self.title = title
        self.content = content
        self.summary = summary
        self.slug = slug
        self.image = image
        self.categories = categories


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