from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.validators import InputRequired, DataRequired


class SearchForm(FlaskForm):
    search = StringField("Search (Username, First Name, Last Name, Email, Location)...", validators=[
                                    InputRequired("Input is required!"),
                                    DataRequired("Data is required!")
                                ])
    submit = SubmitField("Search")
