import connexion
from sqlalchemy.schema import CreateSchema
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import os
import shutil

DB_PORT = os.environ['DB_PORT']
DB_TYPE = os.environ['DB_TYPE']
DB_USER = os.environ['DB_USER']
DB_HOST = os.environ['DB_HOST']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_NAME = os.environ['DB_NAME']

# DB_PORT = 5432
# DB_TYPE = "postgresql"
# DB_USER = "postgres"
# DB_HOST = "10.0.2.2"
# # DB_HOST = "localhost"
# DB_PASSWORD = "nopassword"
# DB_NAME = "fileservice_db"

BASE_DIR = os.getcwd()
UPLOAD_DIR = "fileupload"




DB_URI = f"{DB_TYPE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

DB_SCHEMAS = ["filemetadata"]

def create_app():
    """
    A function that returns the Flask app instance and check for the database existence
    """
    connex = connexion.App(__name__, specification_dir="./")
    connex.app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI

    @connex.route("/")
    def index():
        return "<h4>File Upload service by Reagan Balongcas, GRID Trainee</h4>"
    return connex

def create_db():

    dir_path = os.path.join(BASE_DIR, UPLOAD_DIR, "files")
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        shutil.rmtree(dir_path)
        os.mkdir(dir_path)
    else:
        os.mkdir(dir_path)

    if database_exists(DB_URI):
        engine = create_engine(DB_URI)
        conn = engine.connect()
        for schema in DB_SCHEMAS:
            if not conn.dialect.has_schema(conn, schema=schema):
                engine.execute(CreateSchema(schema))
        conn.close()
    else:
        create_database(DB_URI)
        engine = create_engine(DB_URI)
        conn = engine.connect()
        for schema in DB_SCHEMAS:
            if not conn.dialect.has_schema(conn, schema=schema):
                engine.execute(CreateSchema(schema))
        conn.close()

