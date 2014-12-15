import os

WTF_CSRF_ENABLED = True
SECRET_KEY = os.environ.get('CSRF_SECRET')