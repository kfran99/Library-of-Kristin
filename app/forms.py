from flask.ext.wtf import Form
from wtforms import BooleanField, StringField, PasswordField, validators, SelectField
from wtforms.validators import Required, Length, EqualTo

class RegistrationForm(Form):
	given_name = StringField("First Name", [Length(min=1, max=30), Required()])
	surname = StringField("Last Name", [Length(min=1, max=30), Required()])
	email = StringField("Email Address", [Length(min=6, max=64), Required()])
	password = PasswordField("Password", [Required(), EqualTo("confirm", message="Passwords must match.")])
	confirm = PasswordField("Repeat Password")

class LoginForm(Form):
	email = StringField("Email Address", [Length(min=6, max=64), Required()])
	password = PasswordField("Password", [Required()])

class AmazonSearch(Form):
	title = StringField("Title", [Required()])
	author = StringField("Author", [Required()])

class BookSearch(Form):
	title = StringField("Title")
	author = StringField("Author")
	
class UpdateUser(Form):
	given_name = StringField("First Name", [Length(min=1, max=30), Required()])
	surname = StringField("Last Name", [Length(min=1, max=30), Required()])
	email = StringField("Email Address", [Length(min=6, max=64), Required()])
	password = PasswordField("Password", [Required(), EqualTo("confirm", message="Passwords must match.")])
	confirm = PasswordField("Repeat Password")


