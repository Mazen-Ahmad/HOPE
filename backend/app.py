from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import traceback

from finance_router import route_query

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

@app.route('/api/finance/route-query', methods=['POST'])
def finance_route_query():
    try:
        data = request.get_json()
        raw_query = data.get('query', '')
        if not raw_query:
            return jsonify({'error': 'query is required'}), 400
        return jsonify(route_query(raw_query))
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "API is running"})

@app.route('/')
def home():
    return jsonify({
        "message": "Finance Query Router API",
        "endpoints": {
            "/api/finance/route-query": "POST - Route finance query",
            "/api/health": "GET - Health check"
        }
    })

if __name__ == '__main__':
    print("Starting Finance Query Router API...")
    print("Frontend should connect to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)