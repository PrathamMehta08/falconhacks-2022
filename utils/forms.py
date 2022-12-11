from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, IntegerField, RadioField, SelectField
from wtforms.validators import DataRequired, Length, Regexp

class LoginForm(FlaskForm):
    username  = StringField("Username / Email:", validators=[DataRequired(), Length(min=3, max=128)])
    password = PasswordField("Password:", validators=[DataRequired(), Length(min=3, max=32)])
    submit = SubmitField("Log In")

class SignupForm(FlaskForm):
    username  = StringField("Username:", validators=[DataRequired(), Length(min=3, max=32), Regexp(r"\w|\d|_+", message="Username can only contain letters, numbers and underscores.")])
    email = EmailField("Email:", validators = [DataRequired(), Length(min=3, max=128)])
    password = PasswordField("Password:", validators=[DataRequired(), Length(min=3, max=32)])
    submit = SubmitField("Sign Up")

class ListingForm(FlaskForm):
    address = StringField("Address:", validators=[DataRequired()])
    price = IntegerField("Price per Month:", validators=[DataRequired()])
    bedrooms = IntegerField("Bedrooms:", validators=[DataRequired()])
    bathrooms = IntegerField("Bathrooms:", validators=[DataRequired()])
    square_ft = IntegerField("Square Feet:", validators=[DataRequired()])
    lot_size = IntegerField("Lot Size:", validators=[DataRequired()])
    type_of_house = SelectField(label='Property Type', choices=[("House", "House"), ("Townhouse", "Townhouse"), ("Condo", "Condo")])
    pets = RadioField("Pets:", choices = [("Yes", "Yes"), ("No", "No")], default="No")
    submit = SubmitField("List")
