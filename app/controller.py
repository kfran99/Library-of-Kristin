from app import app
from flask import render_template, redirect, request, flash, session, url_for, escape
import model
from forms import RegistrationForm, AmazonSearch, LoginForm, BookSearch, UpdateUser
from wtforms import Form, BooleanField, StringField, validators
from search_amazon import get_book_by_title_author, get_book_info
import config 
from config import *
import hashlib
from sqlalchemy import distinct
from datetime import datetime
from twilio.rest import TwilioRestClient


client = TwilioRestClient(config.account_sid, config.auth_token)
my_phone = config.my_phone
twilio_phone = config.twilio_phone

@app.route("/")
@app.route("/index")
def index():
	if "email" in session:
		user = model.session.query(model.User).filter_by(email=session["email"]).one()
	else:
		user = None
	return render_template("index.html", title="Home", user=user)

@app.route("/user/new", methods=["GET"])
def new_user_form():
	"""Display HTML form to create a new user"""
	form = RegistrationForm()
	return render_template("new_user_form.html", form=form)

@app.route("/user/new", methods=["POST"])
def add_new_user():
	salt = PASSWORD_SALT
	"""Get data from Registration Form"""
	form = RegistrationForm(request.form)
	if not form.validate():
		flash("All fields are required.")
		return render_template("new_user_form.html", form=form)
	given_name = form.given_name.data
	surname = form.surname.data
	email = form.email.data
	password = hashlib.sha1(form.password.data+salt).hexdigest()
	user_exist = model.session.query(model.User).filter_by(email=email).all()
	"""check to see if user exists"""
	if user_exist:
		flash("User account has already been created with this email.")
		return render_template("login_user.html", form=form)
	"""create user object"""
	user = model.User(given_name=given_name, surname=surname, email=email, password=password, admin=0)
	model.session.add(user)
	model.session.commit()
	session["email"] = email
	if form.validate_on_submit():
		flash ("Your account has been created, " + form.given_name.data + ".")		
		return redirect("/index")
	return redirect("/user/new")

@app.route("/user/login", methods=["GET"])
def user_login_form():
	form = LoginForm()
	return render_template("login_user.html", form=form)

@app.route("/user/login", methods=["POST"])
def user_login():	
	salt = PASSWORD_SALT
	form = LoginForm(request.form)
	email = form.email.data
	password = hashlib.sha1(form.password.data+salt).hexdigest()
	user_list = model.session.query(model.User).filter_by(email=email, password=password).all()
	if user_list:	
		session["email"] = email
		if user_list[0].admin == 1:
			session["admin"] = True
		else:
			session["admin"] = False
		given_name = user_list[0].given_name
		flash("You are authenticated, " + given_name + ".")
		return redirect("/index")
	else:
		flash("User not authenticated.")
		return render_template("login_user.html", form=form)

@app.route("/user/logout")
def logout():
	session.clear()
	flash("You are now logged out.")
	return redirect("/index")

@app.route("/user/<id>/edit")
def edit_user(id):
	current_user = model.session.query(model.User).get(id)
	if not current_user:	
		flash ("You are not logged in.")
	form = UpdateUser()
	return render_template("update_user.html", user=current_user, form=form)

@app.route("/user/<id>/update",methods=["POST"])
def update_user(id):
	salt = PASSWORD_SALT
	form = UpdateUser(request.form)
	current_user = model.session.query(model.User).get(id)
	if not current_user:
		flash ("You are not logged in.")

	user_save = False	

	form = UpdateUser(request.form)
	if form.given_name and form.given_name.data != '':
		current_user.given_name = form.given_name.data
		user_save = True
	if form.surname and form.surname.data != '':
		current_user.surname = form.surname.data
		user_save = True
	if form.email and form.email.data != '':
		current_user.email = form.email.data
		session["email"] = current_user.email
		user_save = True
	if form.password and form.password.data != '':	
		current_user.password = hashlib.sha1(form.password.data+salt).hexdigest() 
		user_save = True
	if user_save:
		model.session.add(current_user)
		model.session.commit()
    
	flash("You have successfully updated your account, " + current_user.given_name + ".")
	return redirect("/index")
		
@app.route("/amazon/search", methods=["GET", "POST"])
def amazon_search():
	if "email" in session:
		user = model.session.query(model.User).filter_by(email=session["email"]).one()
	if session['admin']:
		form = AmazonSearch()
		if form.validate_on_submit():
			books = get_book_by_title_author(form.title.data, form.author.data)
			#get_book_by_title_author is defined in search_amazon
			return render_template("amazon_results.html", amazon_res=books, user=user)
		else:
			return render_template("amazon_search.html", form=form, user=user)
	else:
		return "You are not authorized to do this."

@app.route("/amazon/add_book", methods=["GET"])
def add_book():
	if "email" in session:
		user = model.session.query(model.User).filter_by(email=session["email"]).one()
	asin = request.args.get("asin")
	title = unicode(request.args.get("title"))
	author = unicode(request.args.get("author"))
	amazon_url = request.args.get("amazon_url")
	genre, description, image = get_book_info(asin)
	book = model.Book(title=title,
	                  author=author,
	                  genre=genre,
	                  description=description,
	                  image_url=image,
	                  amazon_url=amazon_url,
	                  asin=asin)
	book_exist = model.session.query(model.Book).filter_by(title=title).all()
	form = AmazonSearch()
	"""if book is already in the database, return to amazon_search"""
	if book_exist:	
	 	flash("Book is already in the database.")
	 	return render_template("amazon_search.html", form=form, user=user)
	model.session.add(book)
	model.session.commit()
	return render_template("view_added_book.html", book=book, user=user)

@app.route("/book/search", methods=["GET", "POST"])
def book_search_form():
	if "email" in session:
		user = model.session.query(model.User).filter_by(email=session["email"]).one()
	form = BookSearch()
	title = request.form.get("title")
	author = request.form.get("author")
	
	if form.validate_on_submit():
		books_title = model.session.query(model.Book).filter(model.Book.title.ilike("%"+title+"%")).all()
		books_author = model.session.query(model.Book).filter(model.Book.author.ilike("%"+author+"%")).all()
		books_query = model.session.query(model.Book)
		
		if books_title:
			books_query = books_query.filter(model.Book.title.ilike("%"+title+"%"))

		if books_author:
			books_query = books_query.filter(model.Book.author.ilike("%"+author+"%"))
		books = books_query.all()

		if not books:
			flash("No books were found matching your search terms.")
			return render_template("book_search.html", form=form, user=user)
		return render_template("book_results.html", book_results=books, user=user)
	return render_template("book_search.html", form=form, user=user)

@app.route("/book/<id>", methods=["GET"])
def view_book(id):
	book = model.session.query(model.Book).get(id)
	user = model.session.query(model.User).filter_by(email=session["email"]).one()
	status = book.get_status()
	return render_template("view_book.html", book=book, status=status, user=user) 

@app.route("/book/<id>/request", methods=["GET"])
def book_request(id):	
	if session["email"]:
		book = model.session.query(model.Book).get(id)
		requester = model.session.query(model.User).filter_by(email=session["email"]).one()
		new_request = model.BookStatus(book_id=book.id, requester_id=requester.id)
		model.session.add(new_request)
		model.session.commit()
		flash ("You have requested to borrow this book.")
		"""Send Twilio message when someone requests to borrow a book"""
		message = client.messages.create(body="Kristin, " + requester.given_name + 
			                             " " + requester.surname + 
			                             " has requested to borrow the book: " 
			                             + book.title + ".",
			                             to=my_phone, 
			                             from_=twilio_phone)			
	return redirect(url_for("view_book", id=id)) 

@app.route("/book/<id>/update_status", methods=["GET"])
def book_update_status(id):	
	if session['admin']:
		book = model.session.query(model.Book).get(id)
		requester = model.session.query(model.User).filter_by(email=session["email"]).one()
		status = model.session.query(model.BookStatus).filter_by(book_id=book.id, checked_in=None).all()
		"""Checks in specific book if it shows as either requested or checked-out.""" 
		for s in status:
			if s.checked_in == None:
				s.checked_in = datetime.now()		
		model.session.commit()
	return redirect(url_for("view_book", id=id))





		


