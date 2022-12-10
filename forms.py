from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email, Regexp

class LoginForm(FlaskForm):
    username  = StringField("Username:", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign Up")
    
class SignupForm(FlaskForm):
    username  = StringField("Username:", validators=[DataRequired()])
    email = EmailField("Email", validators = [DataRequired(), Regexp(
                r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', message=("Invalid Email")
            ),])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign In")