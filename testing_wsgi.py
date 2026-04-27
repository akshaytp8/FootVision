"""
testing_wsgi.py
---------------
PythonAnywhere WSGI configuration file.

SETUP STEPS ON PYTHONANYWHERE:
  1. Sign up at pythonanywhere.com (free account)

  2. Go to "Files" tab
     → Upload your entire project folder
     → Your path will be: /home/YOUR_USERNAME/final_project/

  3. Go to "Bash Console" tab → run:
     cd final_project
     pip install -r requirements.txt --user

  4. Go to "Web" tab
     → Click "Add a new web app"
     → Choose "Manual configuration"
     → Choose Python 3.10

  5. Still in "Web" tab, scroll to "WSGI configuration file"
     → Click the link to open it
     → DELETE everything in that file
     → PASTE the code below into it (update YOUR_USERNAME)
     → Save

  6. Click the big green "Reload" button
     → Your site is live at YOUR_USERNAME.pythonanywhere.com

---
PASTE THIS INTO THE PYTHONANYWHERE WSGI FILE:
(Replace YOUR_USERNAME with your actual PythonAnywhere username)
"""

# ================================================================
# PASTE FROM HERE ↓
# ================================================================

import sys
import os

# Add your project folder to Python path
# CHANGE "YOUR_USERNAME" to your PythonAnywhere username
project_path = "/home/YOUR_USERNAME/final_project"
if project_path not in sys.path:
    sys.path.insert(0, project_path)

# Set working directory so SQLite database is found correctly
os.chdir(project_path)

# Import and create the Flask app
from app import create_app
application = create_app()

# ================================================================
# PASTE UNTIL HERE ↑
# ================================================================
