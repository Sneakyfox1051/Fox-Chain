"""
WSGI entry point for production deployment
This file is used by production WSGI servers like Gunicorn
"""
from app import app

if __name__ == "__main__":
    app.run()

