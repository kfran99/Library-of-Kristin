import os
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

engine = create_engine(os.environ.get("DATABASE_URL","postgres://localhost/libraryofkristin"), echo=True)
session = scoped_session(sessionmaker(bind=engine,
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
	description = Column(String(5000), nullable = True)
	image_url = Column(String(500), nullable= True)
	amazon_url = Column(String(500), nullable = True)
	asin = Column(String(25), nullable = False)


class User(Base):
	__tablename__= "users"
	id = Column(Integer, primary_key = True)
	given_name = Column(String(30), nullable = False)
	surname = Column(String(30), nullable = False)
	email = Column(String(64), nullable = False)
	password = Column(String(64), nullable = False)
	admin = Column(Integer, nullable=False, default=0)

class BookStatus(Base):
	__tablename__= "status"
	id = Column(Integer, primary_key = True)
	book_id = Column(Integer, ForeignKey("books.id"), nullable = False)
	requester_id = Column(Integer, ForeignKey("users.id"), nullable = False)
	status = Column(String(64), nullable = False)
	requested = Column(DateTime, nullable = False, default=datetime.now)
	checked_out = Column(DateTime, nullable = True) 
	checked_in = Column(DateTime, nullable = True)


def main():
	Base.metadata.create_all(engine)

if __name__ == "__main__":
	main()	





