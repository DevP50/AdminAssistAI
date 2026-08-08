from flask import Flask
from config import BaseConfig
from app.extensions import db
from app.routes.students import students_bp,app_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(BaseConfig)
    app.register_blueprint(students_bp , url_prefix='/students')
    app.register_blueprint(app_bp , url_prefix='/')
    db.init_app(app)
    from app.models.model import Student, Payment
    return app

