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
    price = IntegerField("Price per Month (in USD):", validators=[DataRequired()])
    bedrooms = IntegerField("Bedrooms:", validators=[DataRequired()])
    bathrooms = IntegerField("Bathrooms:", validators=[DataRequired()])
    square_ft = IntegerField("Square Feet:", validators=[DataRequired()])
    lot_size = IntegerField("Lot Size:", validators=[DataRequired()])
    property_type = SelectField(label='Property Type', choices=[("House", "House"), ("Townhouse", "Townhouse"), ("Condo", "Condo")])
    pets = RadioField("Pets:", choices = [("Yes", "Yes"), ("No", "No")], default="No")
    submit = SubmitField("List")

class RoommatePreferences(FlaskForm):
    #generated with a helper script
    relationship = RadioField("What kind of relationship are you looking for in a roommate?", choices = [("To do everything together", "To do everything together"), ("To be friends", "To be friends"), ("To be respectful and peacefully coexist", "To be respectful and peacefully coexist")])
    time = RadioField("Which statement best describes you?", choices = [("I am a morning person and prefer to live with a morning person", "I am a morning person and prefer to live with a morning person"), ("I am a morning person and can live with a night person", "I am a morning person and can live with a night person"), ("I am a night person and prefer to live with a night person", "I am a night person and prefer to live with a night person"), ("I am a night person and can live with a morning person", "I am a night person and can live with a morning person")])
    space = RadioField("I use my personal space for...", choices = [("Studying", "Studying"), ("Relaxing", "Relaxing"), ("Hanging out with friends", "Hanging out with friends"), ("Quiet comtemplation", "Quiet comtemplation"), ("I plan on rarely using my space", "I plan on rarely using my space")])
    conflicts = RadioField("When dealing with conflicts...", choices = [("I am able to clearly express my feelings and concerns", "I am able to clearly express my feelings and concerns"), ("I will generally express my concerns in a joking fashion so that the other person gets the hint", "I will generally express my concerns in a joking fashion so that the other person gets the hint"), ("I usually wait until I am really annoyed or angry", "I usually wait until I am really annoyed or angry"), ("I am not comfortable asserting myself in conflict", "I am not comfortable asserting myself in conflict")])
    studying = RadioField("Which statement best describes your preferred studying environment in your room?", choices = [("I prefer a study environment that is very quiet", "I prefer a study environment that is very quiet"), ("I prefer a study environment with some noise", "I prefer a study environment with some noise"), ("I am able to study regardless of noise level", "I am able to study regardless of noise level"), ("I must have some level of noise in order to study", "I must have some level of noise in order to study")])
    shy = RadioField("I consider myself...", choices = [("Shy", "Shy"), ("Fairly Shy", "Fairly Shy"), ("Neutral", "Neutral"), ("Fairly Outgoing", "Fairly Outgoing"), ("Outgoing", "Outgoing")])
    home = RadioField("I plan on going home...", choices = [("Every weekend", "Every weekend"), ("Every other weekend", "Every other weekend"), ("Once a month", "Once a month"), ("Rarely or only during academic breaks", "Rarely or only during academic breaks"), ("Never", "Never")])
    music = RadioField("I like to have music or the TV on in my room...", choices = [("All the time", "All the time"), ("Most of the time", "Most of the time"), ("Sometimes", "Sometimes"), ("Rarely", "Rarely"), ("Never", "Never")])
    clean = RadioField("I like living in a...", choices = [("Very clean space", "Very clean space"), ("Clean space", "Clean space"), ("Messy space", "Messy space"), ("Indifferent", "Indifferent")])
    temp = RadioField("I prefer a room that is...", choices = [("Cold", "Cold"), ("Fairly cold", "Fairly cold"), ("Fairly warm", "Fairly warm"), ("Warm", "Warm")])
    submit = SubmitField("Update Preferences")
