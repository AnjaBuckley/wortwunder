from flask import Flask, request, jsonify
from flask_cors import CORS
import importlib
import lib.db
importlib.reload(lib.db)
from lib.db import (
    get_vocabulary, initialize_database, add_to_favorites, 
    remove_from_favorites, get_favorites, get_study_sessions_count, 
    create_study_session
)

app = Flask(__name__)
CORS(app)

@app.route('/api/vocabulary', methods=['GET'])
def get_vocabulary_list():
    level = request.args.get('level')
    return jsonify(get_vocabulary(level))

@app.route('/api/favorites', methods=['GET'])
def get_favorites_list():
    try:
        favorites = get_favorites()
        return jsonify(favorites)
    except Exception as e:
        print(f"Error getting favorites: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/favorites/<int:vocabulary_id>', methods=['POST'])
def add_favorite(vocabulary_id):
    try:
        add_to_favorites(vocabulary_id)
        return jsonify({"message": "Added to favorites"})
    except Exception as e:
        print(f"Error adding favorite: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/favorites/<int:vocabulary_id>', methods=['DELETE'])
def remove_favorite(vocabulary_id):
    try:
        remove_from_favorites(vocabulary_id)
        return jsonify({"message": "Removed from favorites"})
    except Exception as e:
        print(f"Error removing favorite: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/study-sessions/count', methods=['GET'])
def get_study_sessions():
    try:
        count = get_study_sessions_count()
        return jsonify({'count': count})
    except Exception as e:
        print(f"Error getting study sessions count: {str(e)}")
        return jsonify({'error': 'Failed to get study sessions count'}), 500

@app.route('/api/study-sessions', methods=['POST'])
def add_study_session():
    try:
        data = request.get_json()
        activity_type = data.get('activity_type')
        print(f"Received request to add study session with activity_type: {activity_type}")
        
        if not activity_type:
            return jsonify({'error': 'Activity type is required'}), 400
            
        success = create_study_session(activity_type)
        if not success:
            return jsonify({'error': 'Failed to add study session'}), 500
            
        count = get_study_sessions_count()
        return jsonify({'count': count})
    except Exception as e:
        print(f"Error adding study session: {str(e)}")
        return jsonify({'error': 'Failed to add study session'}), 500

if __name__ == '__main__':
    # Initialize database on startup when run directly
    with app.app_context():
        initialize_database()
    app.run(port=5006)
