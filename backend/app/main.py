from flask import Flask
from flask_cors import CORS

# from backend.app.api import app_bp, audi_bot_bp
from backend.app.core.config import Settings
from backend.app.core.db import MongoPrimaryDatabase, PrimaryDatabase, configure_database


def create_app(settings: Settings | None = None, *, database: PrimaryDatabase | None = None) -> Flask:
    resolved = (settings or Settings.from_env()).validate()
    primary = database or MongoPrimaryDatabase(resolved)
    configure_database(primary)
    app = Flask(__name__)
    app.config["AUTOLUNO_SETTINGS"] = resolved
    app.config["PRIMARY_DATABASE"] = primary
    CORS(app)
    # app.register_blueprint(app_bp)
    # app.register_blueprint(luno_bp)
    # app.register_blueprint(audi_bot_bp)
    return app


app = create_app()
