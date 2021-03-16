from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api
from flask_jwt_extended import jwt_required, create_access_token
from employeeManagement.models import User

api_bp = Blueprint("api", __name__)
api_v1 = Api(api_bp)


class Search(Resource):
    @jwt_required()
    def get(self):
        keyword = request.args.get('keyword', None)
        username = User.query.filter_by(username=keyword).all()
        email = User.query.filter_by(email=keyword).all()
        first_name = User.query.filter_by(first_name=keyword).all()
        last_name = User.query.filter_by(last_name=keyword).all()
        location = User.query.filter_by(location=keyword).all()
        result = username + email + first_name + last_name + location
        return jsonify(result)


class SearchAdmin(Resource):
    def get(self):
        keyword = request.args.get('keyword', None)
        username = User.query.filter_by(username=keyword).all()
        email = User.query.filter_by(email=keyword).all()
        first_name = User.query.filter_by(first_name=keyword).all()
        last_name = User.query.filter_by(last_name=keyword).all()
        location = User.query.filter_by(location=keyword).all()
        result = username + email + first_name + last_name + location
        return jsonify(result)


class Login(Resource):
    def post(self):
        email = request.headers.get("email")
        password = request.headers.get("password")
        user = User.query.filter_by(email=email).first()
        if user and user.is_admin():
            if user.check_password(password):
                access_token = create_access_token(identity=email)
                return jsonify(message="Login Succeeded", access_token=access_token)
        else:
            return jsonify(message="Bad Email or Password")


api_v1.add_resource(Search, '/search')
api_v1.add_resource(SearchAdmin, '/search_admin')
api_v1.add_resource(Login, '/login')
