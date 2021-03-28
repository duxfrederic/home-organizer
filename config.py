import os
basedir = os.path.abspath(os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv(os.path.join(basedir, '.flaskenv'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess-3jfrjljfajqeorynv'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ITEMS_PICTURES = 'app/static/items_pictures/'
    LOCATIONS_PICTURES = 'app/static/locations_pictures'
