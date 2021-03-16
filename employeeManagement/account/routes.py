from flask import Blueprint, render_template, flash, url_for, redirect, abort
from employeeManagement.auth.routes import current_user, login_required, logout_user
from employeeManagement.models import User
from employeeManagement import db
from werkzeug.utils import escape, unescape
from employeeManagement.account.forms import UpdateAccountForm

account = Blueprint("account", __name__, template_folder="templates")


@account.route("/profile/<username>")
@login_required
def show(username):
    user = User.query.filter_by(username=username).first()
    if user == current_user or current_user.is_admin():
        return render_template("show_account.html", user=user)
    return abort(403)


@account.route("/edit/<username>", methods=["GET", "POST"])
@login_required
def edit(username):
    form = UpdateAccountForm()
    user = User.query.filter_by(username=username).first()
    if user == current_user or current_user.is_admin():
        if form.validate_on_submit():
            user.location = escape(form.location.data)
            user.username = form.username.data
            user.first_name = escape(form.first_name.data)
            user.last_name = escape(form.last_name.data)
            user.email = form.email.data
            user.phone = form.phone.data
            user.dob = form.dob.data
            user.password = form.password.data
            db.session.add(user)
            db.session.commit()
            flash("Account has been updated.", "success")
            return redirect(url_for("account.show", username=user.username))

        form.location.data = unescape(user.location)
        form.username.data = user.username
        form.first_name.data = unescape(user.first_name)
        form.last_name.data = unescape(user.last_name)
        form.email.data = user.email
        form.phone.data = user.phone
        form.dob.data = user.dob
        return render_template("edit_account.html", form=form, user=user)
    return abort(403)


@account.route("/delete", methods=["POST"])
@login_required
def delete():
    db.session.delete(current_user)
    db.session.commit()
    logout_user()
    flash("Your account has been deleted.", "success")
    return redirect(url_for("main.home"))

