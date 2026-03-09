"""
Passenger WSGI entry point for Plesk deployment
"""
import sys
import os
from a2wsgi import ASGIMiddleware

backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

os.chdir(backend_dir)

from main import app

application = ASGIMiddleware(app)
