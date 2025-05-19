from flask import Blueprint, jsonify

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route("/test", methods=["GET"])
def test_route():
    return jsonify({"message": "Flask API is working!"}), 200
