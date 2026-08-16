import os
from flask import Flask, jsonify
from flask_cors import CORS
from app.database.connection import init_db
from app.api.events import events_bp
from app.api.students import students_bp
from app.api.replay import replay_bp
from app.api.audit import audit_bp
from app.api.dashboard import dashboard_bp
from app.api.exports import exports_bp

def create_app(db_path: str = None) -> Flask:
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})

    target_db = db_path or Config.DB_PATH
    app.config["DB_PATH"] = target_db

    # Initialize Database Schema
    init_db(target_db)

    # Health Check Endpoint
    @app.route("/health", methods=["GET"])
    def health_check():
        return jsonify({
            "status": "healthy",
            "system": "EngageResolve Engine",
            "version": "1.0.0"
        }), 200

    # Register API Blueprints
    app.register_blueprint(events_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(replay_bp)
    app.register_blueprint(audit_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(exports_bp)

    # Global Error Handlers
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"success": False, "error": {"code": "BAD_REQUEST", "message": str(e)}}), 400

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"success": False, "error": {"code": "NOT_FOUND", "message": "Resource not found"}}), 404

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"success": False, "error": {"code": "INTERNAL_ERROR", "message": "An internal server error occurred."}}), 500

    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
