from flask_sqlalchemy import SQLAlchemy
import connexion
from sqlalchemy.schema import CreateSchema
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database


def create_app(config_name=None):
    connex = connexion.App(__name__, specification_dir="./")
    db_uri = "postgresql://postgres:nopassword@localhost:5432/scraper_db"
    connex.app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    if not database_exists(db_uri):
        create_database(db_uri)
        engine = create_engine(db_uri)
        conn = engine.connect()
        if not conn.dialect.has_schema(conn, schema='modulelog'):
            engine.execute(CreateSchema('modulelog'))
        conn.close()
    return connex
