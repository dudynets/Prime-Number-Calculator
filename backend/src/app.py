from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .database import db
from .auth import auth_bp
from .tasks import tasks_bp
import os

def create_app():
    app = Flask(__name__)
    
    # Configure CORS
    CORS(app)
    
    # Configure app
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    
    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(tasks_bp, url_prefix='/api/tasks')
    
    @app.route('/api/health')
    def health_check():
        return {'status': 'healthy'}, 200
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run() 