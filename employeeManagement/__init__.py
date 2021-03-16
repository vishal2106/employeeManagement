import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()

basedir = os.path.abspath(os.path.dirname(__file__))


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("FLASK_SECRET_KEY") or 'prc9FWjeLYh_KsPGm0vJcg',
        JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY") or 'WhyEncryptIT@0',
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'employee.sqlite'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        DEBUG=True
    )

    db.init_app(app)
    jwt.init_app(app)
    with app.app_context():
        db.create_all()

    from employeeManagement.auth.routes import auth
    from employeeManagement.main.routes import main
    from employeeManagement.account.routes import account
    from employeeManagement.admin.routes import admin
    from employeeManagement.api.routes import api_bp

    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(account, url_prefix="/user")
    app.register_blueprint(admin, url_prefix="/admin")
    app.register_blueprint(api_bp, url_prefix="/api")

    from employeeManagement.main.errors import page_not_found, not_allowed
    app.register_error_handler(403, not_allowed)
    app.register_error_handler(404, page_not_found)

    return app
