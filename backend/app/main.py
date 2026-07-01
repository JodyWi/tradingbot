from flask import Flask
from flask_cors import CORS

from backend.app.api import app_bp, luno_bp, audi_bot_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(app_bp)
app.register_blueprint(luno_bp)
app.register_blueprint(audi_bot_bp)
