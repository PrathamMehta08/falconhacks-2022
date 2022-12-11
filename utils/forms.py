from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, IntegerField, RadioField, SelectField
from wtforms.validators import DataRequired, Length, Regexp

questionnaire = {
    "What kind of relationship are you looking for in a roommate?": [
        "To do everything together",
        "To be friends",
        "To be respectful and peacefully coexist",
    ],
    "Which statement best describes you?": [
        "I am a morning person and prefer to live with a morning person",
        "I am a morning person and can live with a night person",
        "I am a night person and prefer to live with a night person",
        "I am a night person and can live with a morning person",
    ],
    "I use my personal space for...": [
        "Studying",
        "Relaxing",
        "Hanging out with friends",
        "Quiet comtemplation",
        "I plan on rarely using my space",
    ],
    "When dealing with conflicts...": [
        "I am able to clearly express my feelings and concerns",
        "I will generally express my concerns in a joking fashion so that the other person gets the hint",
        "I usually wait until I am really annoyed or angry",
        "I am not comfortable asserting myself in conflict",
    ],
    "Which statement best describes your preferred studying environment in your room?": [
        "I prefer a study environment that is very quiet",
        "I prefer a study environment with some noise",
        "I am able to study regardless of noise level",
        "I must have some level of noise in order to study",
    ],
    "I consider myself...": [
        "Shy",
        "Fairly Shy",
        "Neutral",
        "Fairly Outgoing",
        "Outgoing",
    ],
    "I plan on going home...": [
        "Every weekend",
        "Every other weekend",
        "Once a month",
        "Rarely or only during academic breaks",
        "Never",
    ],
    "I like to have music or the TV on in my room...": [
        "All the time",
        "Most of the time",
        "Sometimes",
        "Rarely",
        "Never",
    ],
    "I like living in a...": [
        "Very clean space",
        "Clean space",
        "Messy space",
        "Indifferent",
    ],
    "I prefer a room that is...": [
        "Cold",
        "Fairly cold",
        "Fairly warm",
        "Warm"
    ]
}

questionnaire_names = [
    "relationship",
    "time",
    "space",
    "conflicts",
    "studying",
    "shy",
    "home",
    "music",
    "clean",
    "temp",
]

state_names = [("AL","Alabama"),("AK","Alaska"),("AZ","Arizona"),("AR","Arkansas"),("CA", "California"),("CO", "Colorado"),
("CT","Connecticut"),("DC","Washington DC"),("DE","Delaware"),("FL","Florida"),("GA","Georgia"),
("HI","Hawaii"),("ID","Idaho"),("IL","Illinois"),("IN","Indiana"),("IA","Iowa"),("KS","Kansas"),("KY","Kentucky"),
("LA","Louisiana"),("ME","Maine"),("MD","Maryland"),("MA","Massachusetts"),("MI","Michigan"),("MN","Minnesota"),
("MS","Mississippi"),("MO","Missouri"),("MT","Montana"),("NE","Nebraska"),("NV","Nevada"),("NH","New Hampshire"),
("NJ","New Jersey"),("NM","New Mexico"),("NY","New York"),("NC","North Carolina"),("ND","North Dakota"),("OH","Ohio"),
("OK","Oklahoma"),("OR","Oregon"),("PA","Pennsylvania"),("RI","Rhode Island"),("SC","South Carolina"),("SD","South Dakota"),
("TN","Tennessee"),("TX","Texas"),("UT","Utah"),("VT","Vermont"),("VA","Virginia"),("WA","Washington"),("WV","West Virginia"),
("WI","Wisconsin"),("WY","Wyoming")]

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
    state_code = SelectField(label="State:", choices=state_names)
    city = StringField("City:", validators=[DataRequired()])
    postal = IntegerField("Postal Code:", validators=[DataRequired()])
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
    for i in range(0, len(questionnaire_names)):
        title = list(questionnaire.keys())[i]
        question = questionnaire[list(questionnaire.keys())[i]]
        name = questionnaire_names[i]

        choices = []
        for j in range(0, len(question)):
            choices.append((j, question[j]))

        vars()[name] = RadioField(title, choices=choices)
        i+=1

    submit = SubmitField("Submit")

class ProfileForm(FlaskForm):
    full_name = StringField("Full Name:", validators=[DataRequired(), Length(min=3)])
    age = IntegerField("Age:", validators = [DataRequired()])
    gender = RadioField("Gender:", choices = [(0, "Male"), (1, "Female"), (2, "Other")])
    submit = SubmitField("Update")
