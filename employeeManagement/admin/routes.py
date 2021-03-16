from flask import Blueprint, redirect, url_for, flash
from employeeManagement.auth.routes import role_required
from employeeManagement.models import Role, User
from employeeManagement import db

admin = Blueprint('admin', __name__, template_folder='templates')


@admin.route("/delete-user/<int:user_id>", methods=["POST"])
@role_required(Role.ADMIN)
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        flash("The account \"" + user.username + "\" is deleted.", "success")
        db.session.delete(user)
        db.session.commit()

        return redirect(url_for('main.home'))


@admin.route("/add-user", methods=["GET", "POST"])
@role_required(Role.ADMIN)
def add_user():
    return redirect(url_for('auth.register'))
