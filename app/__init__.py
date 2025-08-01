from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)  # Allow frontend connections
    
    # Register blueprints (routes)
    from .routes import bp
    app.register_blueprint(bp)
    
    return app