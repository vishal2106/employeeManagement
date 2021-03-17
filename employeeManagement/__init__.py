import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail
import redis
from celery import Celery

db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()
celery = Celery()
r = redis.Redis(host='redis', port=6379, db=0)

basedir = os.path.abspath(os.path.dirname(__file__))


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("FLASK_SECRET_KEY") or 'prc9FWjeLYh_KsPGm0vJcg',
        JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY") or 'WhyEncryptIT@0',
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'employee.sqlite'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        MAIL_SERVER='smtp.googlemail.com',
        MAIL_PORT=587,
        MAIL_USE_TLS=True,
        MAIL_USERNAME=os.environ.get('EMAIL_USER'),
        MAIL_PASSWORD=os.environ.get('EMAIL_PASS'),
        SEND_MAILS_WITH_CELERY=True,
        CELERY_BROKER_URL='redis://redis:6379/0',
        CELERY_RESULT_BACKEND='redis://redis:6379/0'
    )

    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    init_celery(app)
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


def init_celery(app):
    celery.conf.broker_url = app.config["CELERY_BROKER_URL"]
    celery.conf.result_backend = app.config["CELERY_RESULT_BACKEND"]

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
