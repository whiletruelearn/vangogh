# manage.py

from flask_script import Manager
from api import api

manager = Manager(api)

if __name__ == "__main__":
	manager.run()