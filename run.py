from app import create_app
from flask_cors import CORS
import os
import psycopg2
from create_tables import create_tables

app = create_app(os.getenv("production"))
CORS(app)

if __name__ == "__main__":
    app.run()
    create_tables()

