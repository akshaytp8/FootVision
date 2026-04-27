"""
extensions.py
-------------
Flask extensions are created here once and shared across all files.
This avoids circular import errors.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db     = SQLAlchemy()
bcrypt = Bcrypt()
