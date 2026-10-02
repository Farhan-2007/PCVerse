from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS

login_manager = LoginManager()

db = SQLAlchemy()

def create_app(config_object='config.Config'):
    app = Flask(__name__)
    CORS(
    app,
    origins=["http://localhost:5173"],
    supports_credentials=True)
    app.config.from_object(config_object)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    db.init_app(app)

    from app import models
    
    from app.routes import main
    from app.auth import auth
    from app.api import api

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(api)

    return app