from flask import jsonify

def error(message, status=400, details=None):
    payload = {"error": message}
    if details:
        payload["details"] = details
    return jsonify(payload), status

def required(data, fields):
    return [field for field in fields if data.get(field) is None or data.get(field) == ""]
