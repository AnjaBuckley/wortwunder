from flask import Flask, request, jsonify
from flask_cors import CORS
from lib.db import get_vocabulary, init_db, add_to_favorites, remove_from_favorites, get_favorites

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

@app.route('/api/favorites', methods=['GET'])
def get_favorite_words():
    try:
        favorites = get_favorites()
        return jsonify(favorites)
    except Exception as e:
        print(f"Error getting favorites: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/favorites/<int:vocabulary_id>', methods=['POST'])
def add_favorite(vocabulary_id):
    try:
        success = add_to_favorites(vocabulary_id)
        if success:
            return jsonify({"message": "Added to favorites"})
        return jsonify({"error": "Failed to add to favorites"}), 400
    except Exception as e:
        print(f"Error adding favorite: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/favorites/<int:vocabulary_id>', methods=['DELETE'])
def remove_favorite(vocabulary_id):
    try:
        success = remove_from_favorites(vocabulary_id)
        if success:
            return jsonify({"message": "Removed from favorites"})
        return jsonify({"error": "Failed to remove from favorites"}), 400
    except Exception as e:
        print(f"Error removing favorite: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Initialize database on startup when run directly
    with app.app_context():
        init_db()
        vocab = get_vocabulary()
        print(f"Database initialized with {len(vocab)} vocabulary items")
    app.run(port=5006)
