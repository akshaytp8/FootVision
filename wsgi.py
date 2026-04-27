"""
wsgi.py
-------
Entry point for production server (gunicorn).

Run with:  gunicorn wsgi:app
"""

from app import create_app

app = create_app()
