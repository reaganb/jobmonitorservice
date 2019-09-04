from app import create_app
from flask_migrate import Migrate, upgrade, Manager
from config import db, connex_app


Migrate = Migrate(connex_app.app, db)
db.init_app(connex_app.app)
db.create_all(app=connex_app.app)
db_uri = "postgresql://postgres:nopassword@localhost:5432/scraper_db"

connex_app.add_api("swagger.yml")

if __name__ == "__main__":

    connex_app.run(debug=True)