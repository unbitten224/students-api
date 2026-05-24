from flask import Blueprint, jsonify, request
from . import store

students_bp = Blueprint("students", __name__)


@students_bp.route("/students", methods=["POST"])
def create_student():
    data = request.get_json()
    for field in ("nombre", "apellido", "correo"):
        if not data or not data.get(field):
            return jsonify({"error": f"Missing field: {field}"}), 400
    if store.email_exists(data["correo"]):
        return jsonify({"error": "Email already exists"}), 409
    student = store.create(data["nombre"], data["apellido"], data["correo"])
    return jsonify(student), 201


@students_bp.route("/students", methods=["GET"])
def list_students():
    return jsonify(store.get_all()), 200


@students_bp.route("/students/<student_id>", methods=["GET"])
def get_student(student_id):
    student = store.get_by_id(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(student), 200


@students_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "version": "1.0.0"}), 200
