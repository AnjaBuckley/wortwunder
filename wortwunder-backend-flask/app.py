from flask import Flask, request, jsonify
from flask_cors import CORS
from lib.db import get_vocabulary, init_db

app = Flask(__name__)
CORS(app)

@app.route('/api/vocabulary')
def vocabulary():
    try:
        level = request.args.get('level', 'All Levels')
        print(f"Fetching vocabulary for level: {level}")
        words = get_vocabulary(level)
        print(f"Found {len(words)} words")
        return jsonify(words)
    except Exception as e:
        print(f"Error in vocabulary route: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Initialize database on startup when run directly
    with app.app_context():
        init_db()
        vocab = get_vocabulary()
        print(f"Database initialized with {len(vocab)} vocabulary items")
    app.run(port=5006)
