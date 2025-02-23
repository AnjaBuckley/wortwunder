from flask import Flask, request, jsonify
from flask_cors import CORS
from lib.db import get_vocabulary, init_db

app = Flask(__name__)
CORS(app)

@app.route('/api/vocabulary')
def vocabulary():
    level = request.args.get('level', 'All Levels')
    words = get_vocabulary(level)
    return jsonify(words)

if __name__ == '__main__':
    # Initialize database on startup
    init_db()
    app.run(port=5006)
