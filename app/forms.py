from flask.ext.wtf import Form
from wtforms import BooleanField, StringField, PasswordField, validators
from wtforms.validators import Required, Length, EqualTo

class RegistrationForm(Form):
	given_name = StringField("First Name", [Length(min=1, max=30), Required()])
	surname = StringField("Last Name", [Length(min=1, max=30), Required()])
	email = StringField("Email Address", [Length(min=6, max=64), Required()])
	password = PasswordField("Password", [Required(), EqualTo("confirm", message="Passwords must match.")])
	confirm = PasswordField("Repeat Password")


class AmazonSearch(Form):
	title = StringField("Title", [Required()])
	author = StringField("Author", [Required()])	


