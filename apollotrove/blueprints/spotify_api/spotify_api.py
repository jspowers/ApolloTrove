import logging
from flask import Blueprint

spotify_api_bp = Blueprint('spotify_api', __name__, template_folder='templates')
from .routes import spotify_api_auth_routes
from .routes import spotify_data_request_routes