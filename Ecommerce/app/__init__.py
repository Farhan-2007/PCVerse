from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.auth import auth

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    from app import models
    
    from app.routes import main
    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app