from app import app
from flask import render_template, redirect, request, flash, session, url_for, escape
import model
from forms import RegistrationForm, AmazonSearch, LoginForm, BookSearch
from wtforms import Form, BooleanField, StringField, validators
from search_amazon import get_book_by_title_author, get_book_info
import config 
from config import *
import hashlib
from sqlalchemy import distinct

@app.route("/index")
def index():
	user = model.session.query(model.User).filter_by(email=session["email"]).one()
	
	return render_template("index.html", title="Home", user=user)

@app.route("/user/new", methods=["GET"])
def new_user_form():
	#Display HTML from to create a new user
	form = RegistrationForm()
	return render_template("new_user_form.html", form=form)

@app.route("/user/new", methods=["POST"])
def add_new_user():
	salt = PASSWORD_SALT
	#Get data from Registration Form
	form = RegistrationForm(request.form)
	if not form.validate():
		flash("All fields are required.")
		return render_template("new_user_form.html", form=form)
	given_name = form.given_name.data
	surname = form.surname.data
	email = form.email.data
	password = hashlib.sha1(form.password.data+salt).hexdigest()
	print password
	print email
	user_exist = model.session.query(model.User).filter_by(email=email).all()
	#check to see if user exists
	if user_exist:
		flash("User account has already been created with this email.")
		return render_template("login_user.html", form=form)
	#create user object
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
		given_name = user_list[0].given_name
		flash("You are authenticated, " + given_name + ".")
		return redirect("/index")
	else:
		flash("User not authenticated.")
		return render_template("login_user.html", form=form)

@app.route("/user/logout")
def logout():
	# user = model.session.query(model.User).filter_by(email=session["email"].one()
	session.pop(session["email"], None)
	flash("You are now logged out.")
	return redirect("/index")


# @app.route("/user/<id>", methods=["POST"])
# def update_user(id):
# 	current_user = User.Query.get(id)
# 	if not current_user:	
# 		flash ("You are not logged in.")
# 	return render_template("update_user.html", current_user=current_user)
		

		


@app.route("/amazon/search", methods=["GET", "POST"])
def amazon_search():
	form = AmazonSearch()
	if form.validate_on_submit():
		books = get_book_by_title_author(form.title.data, form.author.data)
		#get_book_by_title_author is defined in search_amazon
		return render_template("amazon_results.html", amazon_res=books)
	
	return render_template("amazon_search.html", form=form)

@app.route("/amazon/add_book", methods=["GET"])
def add_book():
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
	#if book is already in the database, return to amazon_search
	if book_exist:	
	 	flash("Book is already in the database.")
	 	return render_template("amazon_search.html", form=form)
	model.session.add(book)
	model.session.commit()
	return render_template("view_added_book.html", book=book)

@app.route("/book/search", methods=["GET", "POST"])
def book_search_form():
	form = BookSearch()
	title = request.form.get("title")
	author = request.form.get("author")
	# genre = request.form.get("genre")
	
	# genres = model.session.query(distinct(model.Book.genre)).all()
	  	

	if form.validate_on_submit():
		books_title = model.session.query(model.Book).filter(model.Book.title.ilike("%"+title+"%")).all()
		books_author = model.session.query(model.Book).filter(model.Book.author.ilike("%"+author+"%")).all()
		# books_genre = model.session.query(model.Book.genre).distinct()
		books_query = model.session.query(model.Book)
		
		if books_title:
			books_query = books_query.filter(model.Book.title.ilike("%"+title+"%"))

		if books_author:
			books_query = books_query.filter(model.Book.author.ilike("%"+author+"%"))
		
		# if books_genre:
		# 	books_query =model.session.query(distinct(model.Book.genre)).all()	
		
		books = books_query.all()

		if not books:
			flash("No books were found matching your search terms.")
			return render_template("book_search.html", form=form)
				# genres=genres)		
		return render_template("book_results.html", book_results=books)

	return render_template("book_search.html", form=form)
	# , genres=genres)	

