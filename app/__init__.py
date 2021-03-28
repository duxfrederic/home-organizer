from __future__ import absolute_import
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mobility import Mobility
from flask_bootstrap import Bootstrap

from flask_nav import Nav
from flask_nav.elements import Navbar, View

from dominate.tags import img



##################### navbar
topbar = Navbar(
                View('Home', 'index'),
                View('login', 'login'),
                View('Recherche', 'search'),
                View('Ajout Objet', 'add_object'),
                View('Ajout Rangement', 'add_location'),
                View('Liste des rangements', 'list_locations')
                )

# registers the "top" menubar
nav = Nav()
nav.register_element('top', topbar)
####################################


app = Flask(__name__)
Mobility(app)
Bootstrap(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models

nav.init_app(app)
