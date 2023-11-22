from flask import Blueprint

# Create a Blueprint for the tracking views
tracking_bp = Blueprint('tracking', __name__)
#register_bp = Blueprint('register', __name__)

# Import all the views
from . import tracking
#from . import register