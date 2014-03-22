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

@app.route("/book/search", methods=["GET", "POST"])
def amazon_search():
	form = AmazonSearch()
	if form.validate_on_submit():
		flash ("Information supplied is complete.")
		books = get_book_by_title_author(form.title.data, form.author.data)
		#get_book_by_title_author is defined in search_amazon
		return render_template("amazon_results.html", amazon_res=books)
	
	return render_template("amazon_search.html", form=form)

@app.route("/book/add", methods=["GET"])
def add_book():
	asin = request.args.get("asin")
	title = request.args.get("title")
	author = request.args.get("author")
	image_url, description, genre = get_book_info(asin)
	print asin, title, author, image_url, description, genre
	# genre = get_book_info(book_genre.Items.Item.BrowseNodes.BrowseNode.Name)
	# description = get_book_info(editorial_review.Items.Item.EditorialReviews.EditorialReview.Content)
	# image_url = get_book_info(image_url.Items.Item.ImageSets.ImageSet.LargeImage.URL)
	#amazon_url = request.args.get("DetailPageURL")
	return render_template("view_added_book.html")

