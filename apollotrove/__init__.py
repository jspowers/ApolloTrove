import logging, os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy 
from dotenv import load_dotenv
load_dotenv()
from apollotrove.extensions import apollo_db


def create_apollo_trove(): 
    apollo_trove = Flask(__name__)

    apollo_trove.config['SECRET_KEY'] = os.getenv('apollo_flask_secret', 'ERROR: No Flask Secret Found')
    apollo_trove.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///apollo_db.sqlite'

    apollo_db.init_app(apollo_trove)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.auth_login'
    login_manager.login_message = "Please login to see this content."
    login_manager.init_app(apollo_trove)

    from apollotrove.models.user import User
    @login_manager.user_loader
    def load_user(id):
        return apollo_db.session.execute(
            apollo_db.select(User).filter_by(id=id)
            ).scalar_one_or_none()


    # --------------------- #
    # Blueprints Imports
    from apollotrove.blueprints.home.home import home_bp
    from apollotrove.blueprints.auth.auth import auth_bp
    from apollotrove.blueprints.spotify_api.spotify_api import spotify_api_bp
    
    # --------------------- #
    # Blueprint Manager
    apollo_trove.register_blueprint(blueprint=home_bp)
    apollo_trove.register_blueprint(blueprint=auth_bp, url_prefix='/auth')
    apollo_trove.register_blueprint(blueprint=spotify_api_bp, url_prefix='/spotify_api')


    return apollo_trove

