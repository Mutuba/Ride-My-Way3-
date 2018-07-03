from app import create_app
from flask_cors import CORS
import psycopg2

app = create_app("development")
CORS(app)

if __name__ == "__main__":
    app.run()
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='127.0.0.1', port=port)