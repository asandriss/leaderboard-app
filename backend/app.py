from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app)  # ← Enables CORS for all routes

@app.route("/upload", methods=["POST"])
def upload_file():
    upload_id = str(uuid.uuid4())
    print(f"Accepted mock upload with ID: {upload_id}")
    return jsonify({"status": "accepted", "upload_id": upload_id})
