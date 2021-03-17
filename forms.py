from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextField, FileField, RadioField
from wtforms.validators import InputRequired, Optional, Email, DataRequired



class AddUserForm(FlaskForm):
    """Form to sign up for account."""

    email = StringField('Email', render_kw={"placeholder": "Email"}, validators=[InputRequired(), Email(message="Please enter a valid email address.")])
    password = PasswordField('Password', render_kw={"placeholder": "Password"},  validators=[InputRequired(message="Please enter a password.")])
    username = StringField('Username', render_kw={"placeholder": "Username"}, validators=[InputRequired(message="Please enter a username.")])
    first_name = StringField('First Name', render_kw={"placeholder": "First Name"}, validators=[InputRequired(message="Please enter a first name.")])
    last_name = StringField('Last Name', render_kw={"placeholder": "Last Name"}, validators=[InputRequired(message="Please enter a last name.")])
    bio = TextField('Bio', render_kw={"placeholder": "Bio"}, validators=[InputRequired(message="Please enter a bio.")])
    
class LoginForm(FlaskForm):
    """Form to login to account."""

    email = StringField('Email', render_kw={"placeholder": "Email"}, validators=[InputRequired(), Email(message="Please enter a valid email address.")])
    password = PasswordField('Password', render_kw={"placeholder": "Password"},  validators=[InputRequired(message="Please enter a password.")])


class EditUserForm(FlaskForm):
    """Form to edit user profile."""

    email = StringField('Email', render_kw={"placeholder": "Email"}, validators=[DataRequired(), Email()])
    password = PasswordField('Password', render_kw={"placeholder": "Enter your password to confirm."}, validators=[DataRequired()])
    username = StringField('Username', render_kw={"placeholder": "Username"}, validators=[DataRequired()])
    first_name = StringField('First Name', render_kw={"placeholder": "First Name"}, validators=[DataRequired()])
    last_name = StringField('Last Name', render_kw={"placeholder": "Last Name"}, validators=[DataRequired()])
    bio = StringField('Bio', render_kw={"placeholder": "Bio"}, validators=[DataRequired()])
    image_url = StringField('Image URL', render_kw={"placeholder": "Image URL"}, validators=[DataRequired()])
    


class RatingForm(FlaskForm):
    """Form for rating lyrics."""

    RATING_CHOICES = [
        (1, '<i class="fas fa-star"></i>'),
        (2, '<i class="fas fa-star"></i><i class="fas fa-star"></i>'),
        (3, '<i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i>'),
        (4, '<i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i>'),
        (5, '<i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i>'),
    ] 

    rating = RadioField("Rating", choices=RATING_CHOICES, coerce=int)


class UpdateRatingForm(FlaskForm):
    """Form for updating rating."""

    RATING_CHOICES = [
        (1, '<i class="fas fa-star"></i>'),
        (2, '<i class="fas fa-star"></i><i class="fas fa-star"></i>'),
        (3, '<i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i>'),
        (4, '<i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i>'),
        (5, '<i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i>'),
    ]
    
    rating = RadioField("Rating", choices=RATING_CHOICES, coerce=int)