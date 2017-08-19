# manage.py

from flask.script import Manager

from api import api

manager = Manager(api)

@manager.command
def migrate(action):
    from flask.ext.evolution import Evolution
    evolution = Evolution(api)
    evolution.manager(action)

if __name__ == "__main__":
    manager.run()
