from flask_migrate import MigrateCommand
from flask_script import Manager
from server import connex_app


app_db = connex_app.app

manager = Manager(app_db)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
