import logging
from flask import Blueprint, render_template
auth_bp = Blueprint('auth', __name__, template_folder='templates')

from . import auth_routes
from apollotrove.extensions import apollo_db
from apollotrove.models import *

