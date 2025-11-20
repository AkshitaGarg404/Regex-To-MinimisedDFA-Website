from flask import Flask, request, jsonify, render_template
from uuid import uuid4
import os
from convert import process_regex

# Use the project root (one folder up) as the templates folder so
# render_template("index.html") will find index.html located at the repo root.
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
app = Flask(__name__, template_folder=BASE_DIR)


# Simple CORS support so the frontend (served by Vite) can call this API in
# development without installing extra packages. If you prefer, install
# flask-cors and use CORS(app) instead.
@app.after_request
def add_cors_headers(response):
    response.headers.setdefault('Access-Control-Allow-Origin', '*')
    response.headers.setdefault('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.setdefault('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response

@app.post('/convert')
def convert_endpoint():
    data = request.get_json(silent=True) or {}
    regex = data.get('regex', '').strip()
    if not regex:
        return jsonify({"error": "Missing 'regex' in request body"}), 400

    uid = str(uuid4())
    try:
        result = process_regex(regex, uid)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


@app.route('/convert', methods=['OPTIONS'])
def convert_options():
    # Reply to preflight CORS requests
    return ('', 204)
    


if __name__ == '__main__':
    # Run: python main.py
    app.run(host='0.0.0.0', port=8000, debug=True)
