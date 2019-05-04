import sys
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, nullable=False)
    picture = Column(String)


class BookCategory(Base):

    __tablename__ = 'book_category'

    id = Column(Integer, primary_key=True)
    name = Column(String(140), nullable=False)

    @property
    def serializable(self):
        return {
            'id': self.id,
            'Categoryname': self.name
        }


class Books(Base):

    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    description = Column(String)
    author = Column(String)
    price = Column(String)
    category_id = Column(Integer, ForeignKey("book_category.id"))
    book_category = relationship(BookCategory)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship(User)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow,
                        onupdate=datetime.datetime.utcnow)

    @property
    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'author': self.author,
            'price': self.price,
            'user': self.user_id,
            'category': self.book_category.serializable,
            'created_at': self.created_at,
            'updated_at': self.updated_at
            }


engine = create_engine('sqlite:///books.db')
Base.metadata.create_all(engine)

print "Database Created"
