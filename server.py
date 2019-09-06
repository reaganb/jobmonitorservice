from flask_migrate import Migrate
from config import db, connex_app

migrate = Migrate(connex_app.app, db)
connex_app.add_api("swagger.yml")


@connex_app.route("/")
def index():
    return "<h4>Job Monitoring by Reagan Balongcas, GRID Trainee</h4>"

if __name__ == "__main__":
    connex_app.run()