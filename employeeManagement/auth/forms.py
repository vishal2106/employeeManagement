from flask_wtf import FlaskForm
from wtforms.fields import StringField, IntegerField, DateField, PasswordField, SubmitField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, DataRequired, EqualTo, Length, ValidationError, Email
from employeeManagement.models import User


def user_exists_with_email(form, field):
    user = User.query.filter_by(email=field.data).first()
    if not user:
        raise ValidationError("There is no registered account with that email.")


class RegistrationForm(FlaskForm):
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
    dob = DateField("Date of birth*", format="%Y-%m-%d", validators=[
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
                                    Length(min=10, max=40, message="Password must be between 10 and 40 characters long"),
                                    EqualTo("password_confirm", message="Passwords must match")
                                ])
    password_confirm = PasswordField("Confirm Password *", validators=[
                                    InputRequired("Input is required!"),
                                    DataRequired("Data is required!")
                                ])
    location = StringField("Location (e.g. city, country)", validators=[
                                    InputRequired("Input is required!"),
                                    DataRequired("Data is required!"),
                                    Length(min=3, max=40, message="Location must be between 3 and 40 characters long")
                                ])
    submit = SubmitField("Register")

    def validate_username(form, field):
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError("Username already exists.")

    def validate_email(form, field):
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError("Email already exists.")

    def validate_phone(form, field):
        if len(str(field.data)) != 10:
            raise ValidationError("Phone number should be 10 digits long")
        user = User.query.filter_by(phone=field.data).first()
        if user:
            raise ValidationError("Phone number already exists.")


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[
                                    InputRequired("Input is required!"),
                                    DataRequired("Data is required!"),
                                    Length(min=5, max=30, message="Email must be between 5 and 30 characters long"),
                                    user_exists_with_email
                                ])
    password = PasswordField("Password", validators=[
                                    InputRequired("Input is required!"),
                                    DataRequired("Data is required!"),
                                    Length(min=10, max=40, message="Password must be between 10 and 40 characters long")
                                ])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Login")


class PasswordResetForm(FlaskForm):
    email = EmailField("Your email", validators=[
                                    InputRequired("Input is required!"),
                                    DataRequired("Data is required!"),
                                    user_exists_with_email
                                ])
    submit = SubmitField("Submit")


class UpdatePasswordForm(FlaskForm):
    password = PasswordField("New password", validators=[
                                    InputRequired("Input is required!"),
                                    DataRequired("Data is required!"),
                                    Length(min=10, max=40, message="Password must be between 10 and 40 characters long"),
                                    EqualTo("password_confirm", message="Passwords must match")
                                ])
    password_confirm = PasswordField("Confirm new password", validators=[
                                    InputRequired("Input is required!"),
                                    DataRequired("Data is required!")
                                ])
    submit = SubmitField("Update password")
