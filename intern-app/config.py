import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TESTING = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + _basedir + '/intern.db'
SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = True

THREADS_PER_PAGE = 8

CSRF_ENABLED = False
SESSION_COOKIE_HTTPONLY = False
SESSION_COOKIE_SECURE = False
