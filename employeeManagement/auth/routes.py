from flask import Blueprint, session, g, has_request_context, request, current_app, make_response, \
    render_template, flash, redirect, url_for
from employeeManagement.auth.forms import RegistrationForm, LoginForm, UpdatePasswordForm, PasswordResetForm
from employeeManagement import db
from employeeManagement.models import User, Role
from employeeManagement.auth.utils import send_reset_email
from werkzeug.local import LocalProxy
from itsdangerous.url_safe import URLSafeSerializer
from functools import wraps

auth = Blueprint("auth", __name__, template_folder="templates")

current_user = LocalProxy(lambda: get_current_user())


def login_required(f):
    @wraps(f)
    def _login_required(*args, **kwargs):
        if current_user.is_anonymous():
            flash("You need to be logged in to access this page", "danger")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return _login_required


def role_required(role):
    def _role_required(f):
        @wraps(f)
        def __role_required(*args, **kwargs):
            if not current_user.is_role(role):
                flash("You are not authorized to access this page", "danger")
                return redirect(url_for("main.home"))
            return f(*args, **kwargs)
        return __role_required
    return _role_required


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_anonymous():
        form = LoginForm()

        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data

            user = User.query.filter_by(email=email).first()

            if user.check_password(password):
                flash("You are successfully logged in.", "success")
                login_user(user)
                if form.remember_me.data:
                    resp = make_response(redirect(url_for("main.home")))
                    remember_token = user.get_remember_token()
                    db.session.commit()
                    resp.set_cookie('remember_token', encrypt_cookie(remember_token), max_age=60*60*24*30)
                    resp.set_cookie('user_id', encrypt_cookie(user.id), max_age=60*60*24*30)
                    return resp
                return redirect(url_for("main.home"))
            else:
                form.password.errors.append("The password is not correct.")

        return render_template("login.html", form=form)
    flash("You are already logged in.", "danger")
    return redirect(url_for('main.home'))


@auth.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_anonymous() or current_user.is_admin():
        form = RegistrationForm()

        if form.validate_on_submit():
            username = form.username.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            phone = form.phone.data
            dob = form.dob.data
            email = form.email.data
            password = form.password.data
            location = form.location.data
            if username == 'admin':
                role = 1
            else:
                role = 2

            user = User(username, first_name, last_name, phone, dob, email, password, location, role)
            db.session.add(user)
            db.session.commit()
            if current_user.is_admin():
                flash("User is registered", "success")
            else:
                flash("You are registered", "success")
            return redirect(url_for("main.home"))

        return render_template("register.html", form=form)
    flash("You are already registered", "danger")
    return redirect(url_for('main.home'))


@auth.route("/logout")
@login_required
def logout():
    current_user.forget()
    db.session.commit()
    resp = make_response(redirect(url_for("main.home")))
    resp.set_cookie("remember_token", "", max_age=0)
    resp.set_cookie("user_id", "", max_age=0)
    logout_user()
    flash("You are logged out", "success")
    return resp


@auth.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_anonymous():
        form = PasswordResetForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                send_reset_email(user)
                flash('An email has been sent with instructions to reset your password.', 'info')
                return redirect(url_for('auth.login'))
            else:
                flash("Account doesn't exist", 'danger')
                return redirect(url_for('auth.login'))
        return render_template('password_reset.html', form=form)
    else:
        return redirect(url_for('main.home'))


@auth.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_anonymous():
        user = User.verify_reset_token(token)
        if user is None:
            flash('That is an invalid or expired token', 'warning')
            return redirect(url_for('auth.reset_request'))
        form = UpdatePasswordForm()
        if form.validate_on_submit():
            user.password = form.password.data
            db.session.commit()
            flash('Your password has been updated! You are now able to log in', 'success')
            return redirect(url_for('auth.login'))
        return render_template('update_password.html', title='Reset Password', form=form)
    else:
        return redirect(url_for('main.home'))


def login_user(user):
    session["user_id"] = user.id


def logout_user():
    session.pop("user_id")


@auth.app_context_processor
def inject_current_user():
    if has_request_context():
        return dict(current_user=get_current_user())
    return dict(current_user="")


@auth.app_context_processor
def inject_roles():
    return dict(Role=Role)


def get_current_user():
    _current_user = getattr(g, "_current_user", None)
    if _current_user is None:
        if session.get("user_id"):
            user = User.query.get(session.get("user_id"))
            if user:
                _current_user = g._current_user = user
        elif request.cookies.get("user_id"):
            user = User.query.get(int(decrypt_cookie(request.cookies.get("user_id"))))
            if user and user.check_remember_token(decrypt_cookie(request.cookies.get("remember_token"))):
                login_user(user)
                _current_user = g._current_user = user

    if _current_user is None:
        _current_user = User()
    return _current_user


def encrypt_cookie(content):
    s = URLSafeSerializer(current_app.config["SECRET_KEY"], salt="cookie")
    encrypted_content = s.dumps(content)
    return encrypted_content


def decrypt_cookie(encrypted_content):
    s = URLSafeSerializer(current_app.config["SECRET_KEY"], salt="cookie")
    try:
        content = s.loads(encrypted_content)
    except():
        content = "-1"
    return content
