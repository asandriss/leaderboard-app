from flask import Flask, request, jsonify
from flask_cors import CORS
from backend.services.submission_repository import SubmissionRepository
from backend.services.upload_service import process_uploaded_json
import uuid

app = Flask(__name__)
CORS(app)  # ← Enables CORS for all routes

repository = SubmissionRepository()

@app.route("/upload", methods=["POST"])
def upload_file():
    upload_id = str(uuid.uuid4())
    print(f"[POST /upload] new upload request {upload_id} started")
    raw_data = request.files["file"].read().decode("utf-8")
    print(f"[POST /upload {upload_id}] raw data recieved")
    
    added = process_uploaded_json(raw_data, repository)
    # print(f"Accepted mock upload with ID: {upload_id}")
    print(f"[POST /upload {upload_id}] processing complete and total processed is {len(added)}")

    return jsonify({"status": "accepted", "upload_id": upload_id, "stored": len(added)})
