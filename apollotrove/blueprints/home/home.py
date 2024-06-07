from flask import Blueprint, render_template, redirect, url_for

home_bp = Blueprint('home', __name__, template_folder='templates')
from .routes import (home_routes)