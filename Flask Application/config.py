# config.py

import os

# Secret Key for JWT
SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key_here')

# Database URI for PostgreSQL (update with your actual database details)
SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost:5432/flaskdb'
SQLALCHEMY_TRACK_MODIFICATIONS = False
