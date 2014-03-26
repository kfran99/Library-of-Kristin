from app import app
from flask import render_template, redirect, request, flash, session, url_for
import model
from forms import RegistrationForm, AmazonSearch
from wtforms import Form, BooleanField, StringField, validators
from search_amazon import get_book_by_title_author, get_book_info

@app.route("/")
@app.route("/index")
def index():
	#placeholder for now
	user = {"given_name": "Kristin"}
	return render_template("index.html", title="Home", user=user)


@app.route("/user/new", methods=["GET", "POST"])
def new_user_form():
	#Display HTML from to create a new user
	form = RegistrationForm()
	if form.validate_on_submit():
		flash ("Your account has been created, " + form.given_name.data)		
		return redirect("/index")
	return render_template("new_user_form.html", form=form)

@app.route("/book/search", methods=["GET", "POST"])
def amazon_search():
	form = AmazonSearch()
	if form.validate_on_submit():
		books = get_book_by_title_author(form.title.data, form.author.data)
		#get_book_by_title_author is defined in search_amazon
		return render_template("amazon_results.html", amazon_res=books)
	
	return render_template("amazon_search.html", form=form)

@app.route("/book/add", methods=["GET"])
def add_book():
	asin = request.args.get("asin")
	title = request.args.get("title")
	author = request.args.get("author")
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




	
