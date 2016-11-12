import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True)
    name = Column(String(50), unique = False)
    password = Column(String(50), unique = False, nullable = False)
    email = Column(String(120), nullable = False)
    image = Column(String(200), unique = True)

    posts = relationship('Post', backref = 'user', lazy = 'dynamic')

    def __init__(self, name = None, email = None, password = None, image = None):
        self.name = name
        self.password = password
        self.email = email
        self.image = image
        
class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key = True)
    contents = Column(Text, unique = False)
    userid = Column(Integer, nullable = False)
    writer = Column(Integer, ForeignKey('users.id'), nullable = False)
    date = Column(DateTime, default = datetime.datetime.utcnow, unique = False)

    users = relationship('User', backref = 'post', lazy = 'joined')

    def __init__(self, contents = None, userid = None, writer = None):
        self.contents = contents
        self.userid = userid
        self.writer = writer