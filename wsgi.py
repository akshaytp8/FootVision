"""PythonAnywhere WSGI entry point.

In the PythonAnywhere Web tab, set the WSGI file to this file.
Do not run Gunicorn for a normal PythonAnywhere WSGI deployment.
"""

from app import create_app

app = create_app()
