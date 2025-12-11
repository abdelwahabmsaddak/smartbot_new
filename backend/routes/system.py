from flask import Blueprint, jsonify

system_bp = Blueprint("system_bp", __name__)

@system_bp.route("/status")
def status():
    return jsonify({"status": "OK", "service": "SmartBot Backend"})
