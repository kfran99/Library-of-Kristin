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

	def get_status(self):
		checked_out_books = BookStatus.query.filter_by(book_id=self.id, checked_in=None).all()
		if len(checked_out_books) > 0:
			return "Checked Out"
		return "Available"

class User(Base):
	__tablename__= "users"
	id = Column(Integer, primary_key = True)
	given_name = Column(String(30), nullable = False)
	surname = Column(String(30), nullable = False)
	email = Column(String(64), nullable = False)
	password = Column(String(64), nullable = False)
	admin = Column(Integer, nullable = False, default = 0)

class BookStatus(Base):
	__tablename__= "status"
	id = Column(Integer, primary_key = True)
	book_id = Column(Integer, ForeignKey("books.id"), nullable = False)
	requester_id = Column(Integer, ForeignKey("users.id"), nullable = False)
	requested = Column(DateTime, nullable = False, default=datetime.now)
	checked_out = Column(DateTime, nullable = True) 
	checked_in = Column(DateTime, nullable = True)
	requester = relationship("User", backref = backref("history", order_by = checked_out))
	book = relationship("Book", backref = backref("history", order_by = checked_out))


#Later can add model to have users create a library of books to loan			


def main():
	Base.metadata.create_all(engine)

if __name__ == "__main__":
	main()	





