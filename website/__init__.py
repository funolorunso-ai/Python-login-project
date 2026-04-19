import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()


def create_app():
    import os
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'bigtokz-secret-key')
    
    print("Vercel env keys:", sorted([k for k in os.environ.keys() if not k.startswith('_')]))
    
    postgres_url = os.environ.get('POSTGRES_URL')
    print("POSTGRES_URL value:", postgres_url)
    
    if not postgres_url:
        raise ValueError("POSTGRES_URL is None. Go to Vercel , settings, environment variables, add POSTGRES_URL for Production, Redeploy")
    
    if postgres_url.startswith("postgres://"):
        postgres_url = postgres_url.replace("postgres://", "postgresql://", 1)
        
    app.config['SQLALCHEMY_DATABASE-URI'] = postgres_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    from .models import User, Note
    
    with app.app_context():
        db.create_all()
    

    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app
