from flask import Flask, request, jsonify
from flask_cors import CORS
from backend.services.submission_repository import SubmissionRepository
from backend.services.upload_service import process_uploaded_json
from backend.services.leaderboard_service import compute_leaderboard
from backend.services.leaderboard_read_db import LeaderboardReadDB
import uuid

app = Flask(__name__)
CORS(app)  # ← Enables CORS for all routes

repository = SubmissionRepository()
leaderboard_read_db = LeaderboardReadDB()

@app.route("/upload", methods=["POST"])
def upload_file():
    upload_id = str(uuid.uuid4())
    print(f"[POST /upload] new upload request {upload_id} started")
    raw_data = request.files["file"].read().decode("utf-8")
    print(f"[POST /upload {upload_id}] raw data recieved")
    
    added = process_uploaded_json(raw_data, repository)
    print(f"[POST /upload {upload_id}] processing complete and total processed is {len(added)}")

    new_lb = compute_leaderboard(repository)
    leaderboard_read_db.set(new_lb)

    return jsonify({"status": "accepted", "upload_id": upload_id, "stored": len(added)})


@app.route("/leaderboard", methods=["GET"])
def get_leaderboard():
    print("[GET /leaderboard] returning leaderboard", flush=True)
    # top = compute_leaderboard(repository)
    return jsonify([entry.__dict__ for entry in leaderboard_read_db.get()])   


@app.route("/submissions/<username>", methods=["GET"])
def get_user_submissions(username):
    submissions = repository.get_user_submissions(username)
    submissions_sorted = sorted(submissions, key=lambda s: s.date, reverse=True)

    return jsonify([
        {
            "title": s.title,
            "score": s.score,
            "date": s.date.strftime("%d/%m/%Y")
        }
        for s in submissions_sorted
    ])


@app.route("/submissions", methods=["DELETE"])
def clear_submissions():
    repository.clear()
    leaderboard_read_db.clear()
    return jsonify({"status": "cleared"})