from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextField
from wtforms.validators import InputRequired, Optional, Email



class AddUserForm(FlaskForm):
    """Form to sign up for account."""

    email = StringField('Email', render_kw={"placeholder": "Email"}, validators=[InputRequired(), Email(message="Please enter a valid email address.")])
    password = PasswordField('Password', render_kw={"placeholder": "Password"},  validators=[InputRequired(message="Please enter a password.")])
    username = StringField('Username', render_kw={"placeholder": "Username"}, validators=[InputRequired(message="Please enter a username.")])
    
class LoginForm(FlaskForm):
    """Form to login to account."""

    email = StringField('Email', render_kw={"placeholder": "Email"}, validators=[InputRequired(), Email(message="Please enter a valid email address.")])
    password = PasswordField('Password', render_kw={"placeholder": "Password"},  validators=[InputRequired(message="Please enter a password.")])


# first_name = StringField('First Name', render_kw={"placeholder": "First Name (Optional)"}, validators=[Optional()])
# last_name = StringField('Last Name', render_kw={"placeholder": "Last Name (Optional)"}, validators=[Optional()])
# bio = TextField('Bio', render_kw={"placeholder": "Bio (Optional)"}, validators=[Optional()])