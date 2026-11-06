import hmac
import secrets

from flask import Flask, abort, jsonify, redirect, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS

login_manager = LoginManager()

db = SQLAlchemy()

def create_app(config_object='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_object)
    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": app.config["CORS_ORIGINS"]
            }
        },
        supports_credentials=True
    )
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.unauthorized_handler
    def handle_unauthorized():
        if request.path.startswith("/api/"):
            return jsonify({
                "success": False,
                "message": "Authentication is required."
            }), 401
        return redirect(url_for(login_manager.login_view or "auth.login"))

    def csrf_token():
        token = session.get("_csrf_token")
        if token is None:
            token = secrets.token_urlsafe(32)
            session["_csrf_token"] = token
        return token

    @app.context_processor
    def inject_csrf_token():
        return {"csrf_token": csrf_token}

    @app.before_request
    def protect_state_changes():
        if request.method not in {"POST", "PUT", "PATCH", "DELETE"}:
            return None

        supplied = (
            request.headers.get("X-CSRF-Token")
            or request.form.get("csrf_token")
        )
        expected = session.get("_csrf_token")

        if not expected or not supplied or not hmac.compare_digest(
            expected,
            supplied
        ):
            if request.path.startswith("/api/"):
                return jsonify({
                    "success": False,
                    "message": "The request security token is missing or invalid."
                }), 400
            abort(400)

        return None

    @app.get("/api/csrf-token")
    def get_csrf_token():
        return jsonify({"csrf_token": csrf_token()})

    db.init_app(app)

    from app import models
    
    from app.routes import main
    from app.auth import auth
    from app.api import api

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(api)

    return app