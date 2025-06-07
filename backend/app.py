import logging
import os
import uuid

from flask import Flask, jsonify, request
from flask_cors import CORS

from backend.services.leaderboard_read_db import LeaderboardReadDB
from backend.services.leaderboard_service import compute_leaderboard
from backend.services.submission_repository import SubmissionRepository
from backend.services.upload_service import process_uploaded_json

app = Flask(__name__)
CORS(app)  # Enables CORS for all routes

# Logging setup
LOG_DIR = "backend"
LOG_PATH = os.path.join(LOG_DIR, "server.log")
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.FileHandler(LOG_PATH), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)

# In-memory services (can be replaced with production alternatives)
repository = SubmissionRepository()
leaderboard_read_db = LeaderboardReadDB()


@app.route("/upload", methods=["POST"])
def upload_file():
    """
    Accepts a JSON file upload, processes submissions,
    updates the leaderboard and stores the result in the read DB.
    """
    upload_id = str(uuid.uuid4())
    logger.info("[POST /upload] New upload request %s started", upload_id)

    raw_data = request.files["file"].read().decode("utf-8")
    logger.info("[POST /upload %s] Raw data received", upload_id)

    added = process_uploaded_json(raw_data, repository)
    logger.info("[POST /upload %s] Processed %d submissions", upload_id, len(added))

    leaderboard = compute_leaderboard(repository)
    leaderboard_read_db.set(leaderboard)
    logger.info("[POST /upload %s] Leaderboard updated", upload_id)

    return jsonify({"status": "accepted", "upload_id": upload_id, "stored": len(added)})


@app.route("/leaderboard", methods=["GET"])
def get_leaderboard():
    """
    Returns the current cached leaderboard.
    """
    leaderboard = leaderboard_read_db.get()
    logger.info("[GET /leaderboard] Returned %d entries", len(leaderboard))
    return jsonify([entry.__dict__ for entry in leaderboard])


@app.route("/submissions/<username>", methods=["GET"])
def get_user_submissions(username):
    """
    Returns all submissions for a given user, sorted by date (newest first).
    """
    submissions = repository.get_user_submissions(username)
    sorted_subs = sorted(submissions, key=lambda s: s.date, reverse=True)
    logger.info(
        "[GET /submissions/%s] Returned %d submissions", username, len(sorted_subs)
    )

    return jsonify(
        [
            {
                "title": s.title,
                "score": s.score,
                "date": s.date.strftime("%d/%m/%Y"),
            }
            for s in sorted_subs
        ]
    )


@app.route("/submissions", methods=["DELETE"])
def clear_submissions():
    """
    Clears all stored submissions and leaderboard data.
    Useful during development and testing.
    """
    repository.clear()
    leaderboard_read_db.clear()
    logger.info("[DELETE /submissions] Cleared all submissions and leaderboard")
    return jsonify({"status": "cleared"})
