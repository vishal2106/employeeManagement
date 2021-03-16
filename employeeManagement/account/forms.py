from flask_wtf import FlaskForm
from wtforms.fields import StringField, IntegerField, DateField, PasswordField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, DataRequired, Length, ValidationError, Email
from employeeManagement.models import User
from employeeManagement.auth.routes import current_user


class UpdateAccountForm(FlaskForm):
    username = StringField("Username *", validators=[
        InputRequired("Input is required!"),
        DataRequired("Data is required!"),
        Length(min=5, max=20, message="Username must be between 5 and 20 characters long")
    ])
    first_name = StringField("First Name*", validators=[
        InputRequired("Input is required!"),
        DataRequired("Data is required!"),
        Length(min=3, max=20, message="First name must be between 3 and 20 characters long")
    ])
    last_name = StringField("Last Name")
    phone = IntegerField("Phone *", validators=[
        InputRequired("Input is required!"),
        DataRequired("Data is required!")
    ])
    dob = DateField("Date of birth*", validators=[
        InputRequired("Input is required!"),
        DataRequired("Data is required!")
    ])
    email = EmailField("Email *", validators=[
        InputRequired("Input is required!"),
        DataRequired("Data is required!"),
        Length(min=5, max=30, message="Email must be between 5 and 30 characters long"),
        Email("You did not enter a valid email!")
    ])
    password = PasswordField("Password *", validators=[
        InputRequired("Input is required!"),
        DataRequired("Data is required!"),
        Length(min=10, max=40, message="Password must be between 10 and 40 characters long")
    ])
    location = StringField("Your location (e.g. city, country)", validators=[
        InputRequired("Input is required!"),
        DataRequired("Data is required!"),
        Length(min=3, max=40, message="Location must be between 3 and 40 characters long")
    ])
    submit = SubmitField("Update")

    def validate_username(form, field):
        user = User.query.filter_by(username=field.data).first()

        if current_user.is_admin():
            return
        if user != current_user:
            raise ValidationError("Username already exists.")

    def validate_email(form, field):
        user = User.query.filter_by(email=field.data).first()
        if current_user.is_admin():
            return
        if user != current_user:
            raise ValidationError("Email already exists.")

    def validate_phone(form, field):
        if len(str(field.data)) != 10:
            raise ValidationError("Phone number should be 10 digits long")
        user = User.query.filter_by(phone=field.data).first()
        if current_user.is_admin():
            return
        if user != current_user:
            raise ValidationError("Phone number already exists.")
