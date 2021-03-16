from flask import render_template
from employeeManagement.main.routes import main


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template("errors/404.html")


@main.app_errorhandler(403)
def not_allowed(e):
    return render_template("errors/403.html")
