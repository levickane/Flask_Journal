from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, DateField, IntegerField
from wtforms.validators import DataRequired

from models import Entry

class EntryForm(FlaskForm):
    title = StringField(
        "Title",
        validators = [DataRequired()
        ])
    timespent = IntegerField(
        "Time Spent (minutes)",
        validators = [DataRequired()
        ])
    stuff_learned = TextAreaField(
        "Stuff I Learned",
        validators = [DataRequired()
        ])
    resources_to_remember = TextAreaField("Resources To Remember")
