from app import app
from flask import render_template, redirect, request, flash, session, url_for
from model import *
from forms import RegistrationForm, AmazonSearch
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

	#return render_template("new_user_form.html")


# @app.route("/user/new", methods=["POST"])
# def new_user():
# 	form = RegistrationForm()
# 	if form.validate_on_submit():
# 		flash ("Your account has been created=" + form.given_name.data)		
# 		return redirect("/index")
# 	return render_template("new_user_form.html", form=form)

@app.route("/book/search", methods=["GET", "POST"])
def amazon_search():
	form = AmazonSearch()	
	if form.validate_on_submit():
		flash ("Information supplied is complete.")
		books = get_book_by_title_author(form.title.data, form.author.data)
		for book in books:
			title = book.ItemAttributes.Title
			author = book.ItemAttributes.Author
			link_to_amazon = book.DetailPageURL
			asin = book.ASIN
			#asin can be used as an ID
		#book = book.ItemAttributes.Title, book.ItemAttributes.Author, book.DetailPageURL, book.ASIN
			print unicode(title), unicode(author), unicode(link_to_amazon), unicode(asin)			
		return redirect("/index")
	return render_template("amazon_search.html", form=form)







