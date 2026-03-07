"""
Passenger WSGI entry point for Plesk deployment
This file is used by Plesk to run the FastAPI application
"""
import sys
import os

# Add the backend directory to Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

# Change to backend directory
os.chdir(backend_dir)

# Import the FastAPI app
from main import app

# Passenger expects 'application' variable
application = app
