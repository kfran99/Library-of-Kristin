from app import app
from flask import render_template, redirect, request, flash, session, url_for
import model
from forms import RegistrationForm

@app.route("/")
def index():
	return "hello"
	#return render_template("")


@app.route("/user/new", methods=["GET", "POST"])
def new_user_form():
	form = RegistrationForm()
	if form.validate_on_submit():
		flash ("Your account has been created='" + form.first_name.data + "', remember_me=" + str(form.remember_me.data))		
		return redirect("/index")
	return render_template("new_user_form.html", form=form)


#@app.route("/user/new", methods=["POST"])
#def new_user():
#	form = RegistrationForm
#	if form.validate_on_submit():
#		flash("Your account has been created" + form.first_name.data)


#	return "hello"






