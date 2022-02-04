# General Package
import os, sys

from pymongo import settings
# Set the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# General Packages
from flask_script import Manager, Server
# User Pacakages
import settings
from application import create_app, create_db, config_app
from utilities.databaselayer import DatabaseLayer

# App
app = create_app()
# Database
settings.database = DatabaseLayer(create_db(app))
# Config App
config_app(app)
# Manager
manager = Manager(app)

# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = True,
    host = os.getenv('IP', '0.0.0.0'),
    port = int(os.getenv('PORT', 5000)))
)

if __name__ == "__main__":
    manager.run()
