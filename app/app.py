from flask import Flask, jsonify, request

app = Flask(__name__)

# Simple in-memory storage (resets when the container restarts)
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
    if not text:
        return jsonify(error="'text' is required"), 400
    note = {"id": len(notes) + 1, "text": text}
    notes.append(note)
    return jsonify(note), 201


@app.route("/")
def index():
    return jsonify(message="Hello from AWS ECS Fargate!")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
