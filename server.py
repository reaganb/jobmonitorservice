# from flask_migrate import Migrate
# from config import db, connex_app
from config import connex_app


# Migrate = Migrate(connex_app.app, db)
connex_app.add_api("swagger.yml")

def run():
    connex_app.run(debug=True,port=5005)

if __name__ == "__main__":
    run()
