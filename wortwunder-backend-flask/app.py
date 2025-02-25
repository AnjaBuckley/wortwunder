from flask import Flask, jsonify, request, session
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from lib.db import (
    initialize_database, get_vocabulary, get_favorites, add_to_favorites,
    remove_from_favorites, create_study_session, get_study_sessions_count,
    create_user, get_user_by_username, verify_password, add_vocabulary
)
import logging
import os

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key')  # Change in production
CORS(app, supports_credentials=True)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, user_data):
        self.id = user_data['id']
        self.username = user_data['username']
        self.email = user_data['email']


@login_manager.user_loader
def load_user(user_id):
    user_data = get_user_by_username(user_id)
    if user_data:
        return User(user_data)
    return None


@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not all([username, email, password]):
        return jsonify({'error': 'Missing required fields'}), 400

    user_id = create_user(username, email, password)
    if user_id:
        user_data = get_user_by_username(username)
        user = User(user_data)
        login_user(user)
        return jsonify({'message': 'User registered successfully', 'user_id': user_id}), 201
    else:
        return jsonify({'error': 'Username or email already exists'}), 409


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not all([username, password]):
        return jsonify({'error': 'Missing credentials'}), 400

    user_data = get_user_by_username(username)
    if user_data and verify_password(user_data['password_hash'], password):
        user = User(user_data)
        login_user(user)
        return jsonify({'message': 'Login successful', 'user_id': user_data['id']}), 200
    return jsonify({'error': 'Invalid credentials'}), 401


@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200


@app.route('/api/user', methods=['GET'])
@login_required
def get_current_user():
    return jsonify({
        'id': current_user.id,
        'username': current_user.username,
        'email': current_user.email
    })


@app.route('/api/vocabulary', methods=['GET'])
def get_vocabulary_list():
    level = request.args.get('level')
    word_group_id = request.args.get('word_group_id')
    if word_group_id:
        word_group_id = int(word_group_id)
    vocabulary = get_vocabulary(level, word_group_id)
    return jsonify(vocabulary)


@app.route('/api/vocabulary/import', methods=['POST'])
@login_required
def import_vocabulary():
    try:
        data = request.get_json()
        if not isinstance(data, list):
            return jsonify({'error': 'Expected a list of vocabulary items'}), 400

        imported_count = 0
        failed_items = []

        for item in data:
            try:
                # Validate required fields
                required_fields = ['german_word', 'english_translation', 'theme', 'cefr_level']
                if not all(field in item for field in required_fields):
                    failed_items.append({
                        'item': item,
                        'error': 'Missing required fields'
                    })
                    continue

                # Add the vocabulary item
                add_vocabulary(
                    german_word=item['german_word'],
                    english_translation=item['english_translation'],
                    theme=item['theme'],
                    cefr_level=item['cefr_level'],
                    word_group_id=item.get('word_group_id'),
                    example_sentence=item.get('example_sentence'),
                    example_sentence_translation=item.get('example_sentence_translation')
                )
                imported_count += 1

            except Exception as e:
                failed_items.append({
                    'item': item,
                    'error': str(e)
                })

        response = {
            'message': f'Successfully imported {imported_count} vocabulary items',
            'imported_count': imported_count,
        }
        
        if failed_items:
            response['failed_items'] = failed_items
            if imported_count == 0:
                return jsonify(response), 400
            
        return jsonify(response), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/favorites', methods=['GET'])
@login_required
def get_user_favorites():
    favorites = get_favorites(current_user.id)
    return jsonify(favorites)


@app.route('/api/favorites/<int:vocabulary_id>', methods=['POST'])
@login_required
def add_favorite(vocabulary_id):
    success = add_to_favorites(current_user.id, vocabulary_id)
    if success:
        return jsonify({'message': 'Added to favorites'}), 201
    return jsonify({'error': 'Failed to add to favorites'}), 400


@app.route('/api/favorites/<int:vocabulary_id>', methods=['DELETE'])
@login_required
def remove_favorite(vocabulary_id):
    success = remove_from_favorites(current_user.id, vocabulary_id)
    if success:
        return jsonify({'message': 'Removed from favorites'}), 200
    return jsonify({'error': 'Failed to remove from favorites'}), 400


@app.route('/api/study-sessions', methods=['POST'])
@login_required
def add_study_session():
    data = request.get_json()
    logger.info(f"Received study session data: {data}")
    
    activity_type = data.get('activity_type')
    if not activity_type:
        return jsonify({'error': 'activity_type is required'}), 400

    success = create_study_session(current_user.id, activity_type)
    if success:
        return jsonify({'message': 'Study session created successfully'}), 201
    return jsonify({'error': 'Failed to create study session'}), 500


@app.route('/api/study-sessions/count', methods=['GET'])
@login_required
def get_sessions_count():
    count = get_study_sessions_count(current_user.id)
    return jsonify({'count': count})


if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)
