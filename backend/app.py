"""Flask app factory. Serves the artifact contract; trains nothing."""
from flask import Flask, jsonify
from .config import ENV, artifact_root

def create_app():
    app = Flask(__name__)

    @app.get("/api/health")
    def health():
        return jsonify(env=ENV, artifact_root=artifact_root(), ok=True)

    # TODO: register blueprints from backend/api/ (runs, compute, genealogy, eda, scorecard)
    return app

if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5000, debug=True)
