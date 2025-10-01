from app import app  # your app.py defines: app = Flask(__name__)

@app.get("/health")
def health():
    return "ok", 200