import os
import requests
import json
from flask import Blueprint, render_template
from employeeManagement.auth.routes import current_user, role_required
from employeeManagement.models import User, Role
from employeeManagement.main.forms import SearchForm


main = Blueprint('main', __name__, template_folder='templates')


@main.route('/')
def home():
    if current_user.is_admin():
        users = User.query.all()
        form = SearchForm()
    else:
        form = ""
        users = ""
    return render_template('home.html', form=form, users=users, search_flag=False)


@main.route('/search', methods=["GET", "POST"])
@role_required(Role.ADMIN)
def search():
    form = SearchForm()
    if form.validate_on_submit():
        keyword = form.search.data
        params = {'keyword': keyword}
        users = requests.get('http://'+os.getenv('HOST')+'/api/search_admin', params=params)
        form.search.data = ""
        users = json.loads(users.text)
        return render_template('home.html', form=form, users=users, search_flag=True
                               , keyword=keyword, count=len(users))

