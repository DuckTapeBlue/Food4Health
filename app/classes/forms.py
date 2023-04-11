# This file is where data entry forms are created. Forms are placed on templates 
# and users fill them out.  Each form is an instance of a class. Forms are managed by the 
# Flask-WTForms library.

from flask_wtf import FlaskForm
import mongoengine.errors
from wtforms.validators import URL, Email, DataRequired
from wtforms.fields.html5 import URLField
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, SelectField, FileField, BooleanField

class ProfileForm(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()]) 
    image = FileField("Image") 
    role = SelectField('Role',choices=[("Teacher","Teacher"),("Student","Student")])
    submit = SubmitField('Post')
   

class BlogForm(FlaskForm):
    subject = StringField('Topic', validators=[DataRequired()])
    content = TextAreaField('Question', validators=[DataRequired()])
    submit = SubmitField('Blog')

class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Comment')

class RecipeForm(FlaskForm):
    name = StringField('Recipe Name', validators=[DataRequired()])
    genre = SelectField('Recipe Genre',choices=[("Breakfast","Breakfast"),("Brunch","Brunch"),("Lunch","Lunch"),("Dinner","Dinner"),("Dessert","Dessert")])
    recauthor = StringField('Author', validators=[DataRequired()])
    recimage = FileField('Image', validators=[DataRequired()])
    summary = StringField('Recipe summary', validators=[DataRequired()])
    ingredients = StringField('Ingredients', validators=[DataRequired()])
    time = StringField('Time (hrs)', validators=[DataRequired()])
    recrecipe = StringField('Recipe', validators=[DataRequired()])
    tags = StringField('Tags', validators=[DataRequired()])
    submit = SubmitField('Post')
   