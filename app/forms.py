# Add any form classes for Flask-WTF here
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired, Length

class MovieForm(FlaskForm):
    title = StringField('Movie Title', validators=[
        DataRequired(message='Please enter a movie title'),
        Length(min=1, max=100, message='Title must be between 1 and 100 characters')
    ])
    
    description = TextAreaField('Description', validators=[
        DataRequired(message='Please enter a movie description'),
        Length(min=10, max=500, message='Description must be between 10 and 500 characters')
    ])
    
    poster = FileField('Movie Poster', validators=[
        DataRequired(message='Please upload a movie poster'),
        FileAllowed(['jpg', 'jpeg', 'png'], message='Only JPG, JPEG, and PNG images are allowed')
    ])