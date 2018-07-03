from app import create_app
from flask_cors import CORS
import psycopg2

app = create_app("development")
CORS(app)

if __name__ == "__main__":
    app.run()