from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from wtforms import Form, BooleanField, StringField, validators

engine = create_engine("sqlite:///books.db", echo=False)
session = scoped_session(sessionmaker(bind=ENGINE,
                                      autocommit = False,
                                      autoflush = False))
Base = declarative_base()
Base.query = session.query_property()


class Book(Base):
	__tablename__= "books"
	id = Column(Integer, primary_key = True)
	title = Column(String(256), nullable = False)
	author = Column(String(128), nullable = False)
	genre = Column(String(64), nullable = True)
	description = Column(String(2000), nullable = True)
	image_url = Column(String(500), nullable= True)
	amazon_url = Column(String(500), nullable = True)
	asin = Column(String(25), nullable = False)


class User(Base):
	__tablename__= "users"
	id = Column(Integer, query_property = True)
	user_name = Column(String(128), nullable = False)
	email = Column(String(64), nullable = False)
	password = Column(String(64), nullable = False)


