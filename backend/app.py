from flask import Flask, request, jsonify, render_template_string
import uuid

app = Flask(__name__)

@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # In real logic you'd validate the file here
        upload_id = str(uuid.uuid4())
        print(f"✅ Accepted mock upload, ID: {upload_id}")
        return jsonify({"status": "accepted", "upload_id": upload_id})

    # Basic HTML form for manual testing in browser
    return render_template_string("""
    <h1>Upload a JSON file</h1>
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="file" accept=".json"/>
        <button type="submit">Upload</button>
    </form>
    """)
