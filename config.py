from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from datetime import datetime

connex_app = create_app()
db = SQLAlchemy(connex_app.app)
ma = Marshmallow(connex_app.app)

def get_timestamp():
    """
    Returns the current time in
    """
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))