import connexion
from sqlalchemy.schema import CreateSchema
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import os
#
# DB_PORT = os.environ['DB_PORT']
# DB_TYPE = os.environ['DB_TYPE']
# DB_USER = os.environ['DB_USER']
# DB_HOST = os.environ['DB_HOST']
# DB_PASSWORD = os.environ['DB_PASSWORD']
# DB_NAME = os.environ['DB_NAME']
# DB_SCHEMA = os.environ['DB_SCHEMA']

DB_PORT = 5432
DB_TYPE = "postgresql"
DB_USER = "postgres"
DB_HOST = "localhost"
DB_PASSWORD = "nopassword"
DB_NAME = "modulelog"
DB_SCHEMA = "modulelog"


def create_app():
    """
    A function that returns the Flask app instance and check for the database existence
    """
    connex = connexion.App(__name__, specification_dir="./")
    db_uri = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    connex.app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    if not database_exists(db_uri):
        create_database(db_uri)
        engine = create_engine(db_uri)
        conn = engine.connect()
        if not conn.dialect.has_schema(conn, schema='modulelog'):
            engine.execute(CreateSchema('modulelog'))
        conn.close()

    return connex
