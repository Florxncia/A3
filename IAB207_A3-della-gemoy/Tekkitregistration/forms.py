from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateField, IntegerField, SelectField, FileField
from wtforms.validators import InputRequired, Email, EqualTo, DataRequired

ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'}

class EventForm(FlaskForm):
    name = StringField('Event Name', validators=[InputRequired()])
    artist = StringField('Artist(s) Name', validators=[InputRequired()])
    startDateTime = DateField('Start Open Booking Time', validators=[InputRequired()], format='%Y-%m-%d')
    endDateTime = DateField('Close Open Booking Time', validators=[InputRequired()], format='%Y-%m-%d')
    genre_one = SelectField('Genre 1', coerce=str, option_widget=None, choices=[
        ('', '-'),
        ('Pop', 'Pop'),
        ('Rock', 'Rock'),
        ('Rap', 'Rap'),
        ('Hip-Hop', 'Hip-Hop'),
        ('R&B', 'R&B'),
        ('Reggae', 'Reggae'),
        ('Punk', 'Punk'),
        ('K-Pop', 'K-Pop'),
        ('Ballad', 'Ballad'),
        ('Dangdut', 'Dangdut'),
        ('Festivals', 'Festivals'),
        ('Classical', 'Classical'),
        ('Jazz', 'Jazz'),
        ('EDM', 'EDM'),
        ('Opera', 'Opera'),
        ('Traditional', 'Traditional'),
        ('Contemporary', 'Contemporary'),
        ('Concert', 'Concert'),
        ('Musical', 'Musical'),
        ('Recital', 'Recital'),
        ('Choir', 'Choir'),
        ('Live', 'Live')
        ], default='') 
    description = TextAreaField('Description', validators=[InputRequired()])
    image = FileField('Event Image', validators=[InputRequired()])
    numtickets = IntegerField('Available Amount of Tickets', validators=[InputRequired()])
    price = IntegerField('Ticket Price', validators=[InputRequired()])
    submit = SubmitField("Create")


class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired('Enter user name')])
    password = PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    password = PasswordField("Password", validators=[InputRequired(), EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    address = StringField("Address", validators=[InputRequired()])
    contact_number = StringField("Contact Number", validators=[InputRequired()])
    submit = SubmitField("Register")

class SearchForm(FlaskForm):
    genre = SelectField("Genre", choices=[
        ('', 'All'),
        ('Pop', 'Pop'),
        ('Rock', 'Rock'),
        ('Rap', 'Rap'),
        ('Hip-Hop', 'Hip-Hop'),
        ('R&B', 'R&B'),
        ('Reggae', 'Reggae'),
        ('Punk', 'Punk'),
        ('K-Pop', 'K-Pop'),
        ('Ballad', 'Ballad'),
        ('Dangdut', 'Dangdut'),
        ('Festivals', 'Festivals'),
        ('Classical', 'Classical'),
        ('Jazz', 'Jazz'),
        ('EDM', 'EDM'),
        ('Opera', 'Opera'),
        ('Traditional', 'Traditional'),
        ('Contemporary', 'Contemporary'),
        ('Concert', 'Concert'),
        ('Musical', 'Musical'),
        ('Recital', 'Recital'),
        ('Choir', 'Choir'),
        ('Live', 'Live')
    ], default='')
    submit = SubmitField("")
    searched = StringField("Searched", validators=[InputRequired()])

