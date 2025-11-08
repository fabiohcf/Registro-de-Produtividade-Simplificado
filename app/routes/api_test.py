# app/routes/api_test.py
from flask import Blueprint, jsonify

api_test_bp = Blueprint("api_test_bp", __name__, url_prefix="/api/test")

@api_test_bp.route("/", methods=["GET"])
def test_connection():
    return jsonify({"message": "Flask API is connected!"})
