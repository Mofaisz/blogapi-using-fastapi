from sqlalchemy import Column, Integer, String, ForeignKey
from .database import Base  # Import the Base class
from sqlalchemy.orm import relationship


class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    description = Column(String)

    user_id = Column(Integer,ForeignKey("users_detail.id"))
    owner = relationship("User" , back_populates = "blogs" )
    like = relationship("Like",back_populates="blog", cascade="all, delete")
    

class User(Base):
    __tablename__="users_detail"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    blogs = relationship("Blog" , back_populates = "owner")
    like = relationship("Like",back_populates="user", cascade="all, delete")


# why we are using Base here 
#Base tells sqlalchemy this class is orm model
class Like(Base):
    __tablename__="like"
    id = Column(Integer,primary_key=True,index=True)
    blog_id = Column(Integer, ForeignKey("blogs.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users_detail.id", ondelete="CASCADE"))

    blog = relationship("Blog",back_populates="like")
    user = relationship("User",back_populates="like")
