
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Simple in-memory storage
# Data resets when the container restarts.
notes = []


@app.route("/health")
def health():
    return jsonify(status="ok"), 200


@app.route("/notes", methods=["GET"])
def list_notes():
    return jsonify(notes)


@app.route("/notes", methods=["POST"])
def add_note():
    data = request.get_json(silent=True) or {}
    text = data.get("text")

    if not text or not text.strip():
        return jsonify(error="'text' is required"), 400

    note = {
        "id": len(notes) + 1,
        "text": text.strip()
    }

    notes.append(note)

    return jsonify(note), 201


@app.route("/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    for note in notes:
        if note["id"] == note_id:
            notes.remove(note)
            return jsonify(message="Note deleted"), 200

    return jsonify(error="Note not found"), 404


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

