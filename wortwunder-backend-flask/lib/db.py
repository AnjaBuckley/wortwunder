import sqlite3
import os
from typing import List, Dict, Optional
from werkzeug.security import generate_password_hash, check_password_hash

# Check if we're on PythonAnywhere
ON_PYTHONANYWHERE = 'PYTHONANYWHERE_DOMAIN' in os.environ

if ON_PYTHONANYWHERE:
    # Use PythonAnywhere's project directory with correct case
    BASE_DIR = '/home/AnjaBuckley/wortwunder/wortwunder-backend-flask'
    DB_PATH = os.path.join(BASE_DIR, "german_vocab.db")
else:
    # Local development path
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DB_PATH = os.path.join(BASE_DIR, "german_vocab.db")

print(f"Database will be created at: {DB_PATH}")


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_db_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = dict_factory
        print(f"Successfully connected to database at {DB_PATH}")
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise


def initialize_database():
    create_tables()
    if is_database_empty():
        insert_initial_data()


def create_tables():
    conn = get_db_connection()
    c = conn.cursor()

    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create word_groups table
    c.execute('''
        CREATE TABLE IF NOT EXISTS word_groups (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT
        )
    ''')

    # Create vocabulary table
    c.execute('''
        CREATE TABLE IF NOT EXISTS vocabulary (
            id INTEGER PRIMARY KEY,
            german_word TEXT NOT NULL,
            english_translation TEXT NOT NULL,
            theme TEXT,
            cefr_level TEXT,
            word_group_id INTEGER,
            example_sentence TEXT,
            example_sentence_translation TEXT,
            FOREIGN KEY (word_group_id) REFERENCES word_groups (id)
        )
    ''')

    # Create favorites table with user_id
    c.execute('''
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            vocabulary_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (vocabulary_id) REFERENCES vocabulary (id),
            FOREIGN KEY (user_id) REFERENCES users (id),
            UNIQUE(user_id, vocabulary_id)
        )
    ''')

    # Create study_sessions table with user_id
    c.execute('''
        CREATE TABLE IF NOT EXISTS study_sessions (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            activity_type TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # Create study_session_vocabulary table
    c.execute('''
        CREATE TABLE IF NOT EXISTS study_session_vocabulary (
            id INTEGER PRIMARY KEY,
            study_session_id INTEGER,
            vocabulary_id INTEGER,
            FOREIGN KEY (study_session_id) REFERENCES study_sessions (id),
            FOREIGN KEY (vocabulary_id) REFERENCES vocabulary (id)
        )
    ''')

    conn.commit()
    conn.close()


def create_user(username: str, email: str, password: str) -> Optional[int]:
    """Create a new user and return their ID."""
    conn = get_db_connection()
    c = conn.cursor()
    try:
        password_hash = generate_password_hash(password)
        c.execute(
            'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
            (username, email, password_hash)
        )
        conn.commit()
        return c.lastrowid
    except sqlite3.IntegrityError as e:
        print(f"Error creating user: {e}")
        return None
    finally:
        conn.close()


def get_user_by_username(username: str) -> Optional[Dict]:
    """Get user by username."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    return user


def verify_password(stored_password_hash: str, password: str) -> bool:
    """Verify a password against its hash."""
    return check_password_hash(stored_password_hash, password)


def add_to_favorites(user_id: int, vocabulary_id: int) -> bool:
    """Add a vocabulary item to user's favorites."""
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute(
            'INSERT INTO favorites (user_id, vocabulary_id) VALUES (?, ?)',
            (user_id, vocabulary_id)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def remove_from_favorites(user_id: int, vocabulary_id: int) -> bool:
    """Remove a vocabulary item from user's favorites."""
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute(
            'DELETE FROM favorites WHERE user_id = ? AND vocabulary_id = ?',
            (user_id, vocabulary_id)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error removing from favorites: {e}")
        return False
    finally:
        conn.close()


def get_favorites(user_id: int) -> List[Dict]:
    """Get all favorite vocabulary items for a user."""
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute('''
        SELECT v.* FROM vocabulary v
        JOIN favorites f ON v.id = f.vocabulary_id
        WHERE f.user_id = ?
        ORDER BY f.created_at DESC
    ''', (user_id,))
    
    favorites = c.fetchall()
    conn.close()
    return favorites


def get_study_sessions_count(user_id: int) -> int:
    """Get count of study sessions for a user."""
    conn = get_db_connection()
    c = conn.cursor()

    c.execute('SELECT COUNT(*) as count FROM study_sessions WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    count = result['count'] if result else 0

    conn.close()
    return count


def create_study_session(user_id: int, activity_type: str) -> bool:
    """Add a new study session for a user."""
    conn = None
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute(
            'INSERT INTO study_sessions (user_id, activity_type) VALUES (?, ?)',
            (user_id, activity_type)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error in create_study_session: {e}")
        return False
    finally:
        if conn:
            conn.close()


def add_vocabulary_to_study_session(study_session_id: int, vocabulary_id: int) -> bool:
    """Add a vocabulary item to a study session."""
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute(
            'INSERT INTO study_session_vocabulary (study_session_id, vocabulary_id) VALUES (?, ?)',
            (study_session_id, vocabulary_id)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding vocabulary to study session: {e}")
        return False
    finally:
        conn.close()


def get_study_session_vocabulary(study_session_id: int) -> List[Dict]:
    """Get all vocabulary items for a study session."""
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute('''
        SELECT v.* FROM vocabulary v
        JOIN study_session_vocabulary ssv ON v.id = ssv.vocabulary_id
        WHERE ssv.study_session_id = ?
    ''', (study_session_id,))
    
    vocabulary = c.fetchall()
    conn.close()
    return vocabulary


def is_database_empty():
    conn = get_db_connection()
    c = conn.cursor()
    
    try:
        c.execute('SELECT COUNT(*) FROM vocabulary')
        result = c.fetchone()
        return result[0] == 0 if result else True
    except:
        # If table doesn't exist, consider database empty
        return True
    finally:
        conn.close()


def insert_initial_data():
    print(f"Initializing database at {DB_PATH}")
    conn = get_db_connection()
    cursor = conn.cursor()

    # Drop existing tables to ensure clean slate
    cursor.execute("DROP TABLE IF EXISTS vocabulary")
    cursor.execute("DROP TABLE IF EXISTS word_groups")
    cursor.execute("DROP TABLE IF EXISTS favorites")
    cursor.execute("DROP TABLE IF EXISTS study_sessions")
    cursor.execute("DROP TABLE IF EXISTS study_session_vocabulary")
    print("Dropped existing tables")

    # Create word_groups table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS word_groups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        description TEXT
    )
    """)

    # Create vocabulary table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vocabulary (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        german_word TEXT NOT NULL,
        english_translation TEXT NOT NULL,
        theme TEXT NOT NULL,
        cefr_level TEXT NOT NULL,
        word_group_id INTEGER,
        example_sentence TEXT,
        example_sentence_translation TEXT,
        FOREIGN KEY (word_group_id) REFERENCES word_groups (id)
    )
    """)

    # Create favorites table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS favorites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        vocabulary_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (vocabulary_id) REFERENCES vocabulary (id),
        FOREIGN KEY (user_id) REFERENCES users (id),
        UNIQUE(user_id, vocabulary_id)
    )
    """)

    # Create study_sessions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS study_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        activity_type TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

    # Create study_session_vocabulary table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS study_session_vocabulary (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        study_session_id INTEGER,
        vocabulary_id INTEGER,
        FOREIGN KEY (study_session_id) REFERENCES study_sessions (id),
        FOREIGN KEY (vocabulary_id) REFERENCES vocabulary (id)
    )
    """)

    # Insert default word groups
    default_groups = [
        ("A1", "Beginner - Basic everyday expressions and phrases"),
        ("A2", "Elementary - Frequently used expressions and simple communication"),
        ("B1", "Intermediate - Clear language on familiar matters"),
        ("B2", "Upper Intermediate - Complex texts and abstract topics"),
        ("C1", "Advanced - Fluent expression for social and professional purposes"),
        ("C2", "Mastery - Understanding and expressing with precision"),
    ]

    cursor.executemany(
        "INSERT OR IGNORE INTO word_groups (name, description) VALUES (?, ?)",
        default_groups,
    )
    print(f"Inserted {len(default_groups)} word groups")

    # Insert initial vocabulary
    vocabulary_data = [
        # A1 Level - Basic Words with Example Sentences
        ("Hallo", "hello", "Greetings", "A1", None, "Hallo, wie geht es dir?", "Hello, how are you?"),
        ("Danke", "thank you", "Greetings", "A1", None, "Danke für deine Hilfe!", "Thank you for your help!"),
        ("Bitte", "please/you're welcome", "Greetings", "A1", None, "Bitte schön!", "You're welcome!"),
        ("Apfel", "apple", "Food", "A1", None, "Ich esse einen Apfel.", "I am eating an apple."),
        ("Brot", "bread", "Food", "A1", None, "Das Brot ist frisch.", "The bread is fresh."),
        ("Wasser", "water", "Food", "A1", None, "Ich trinke Wasser.", "I drink water."),
        ("Haus", "house", "Home", "A1", None, "Das Haus ist groß.", "The house is big."),
        ("Tisch", "table", "Home", "A1", None, "Der Tisch ist aus Holz.", "The table is made of wood."),
        ("Stuhl", "chair", "Home", "A1", None, "Der Stuhl ist bequem.", "The chair is comfortable."),
        ("Buch", "book", "Education", "A1", None, "Das Buch ist interessant.", "The book is interesting."),
        ("Schule", "school", "Education", "A1", None, "Die Schule beginnt um acht Uhr.", "School starts at eight o'clock."),
        ("lernen", "to learn", "Education", "A1", None, "Ich lerne Deutsch.", "I am learning German."),
        ("spielen", "to play", "Activities", "A1", None, "Die Kinder spielen im Park.", "The children are playing in the park."),
        ("laufen", "to run/walk", "Activities", "A1", None, "Ich laufe jeden Morgen.", "I run every morning."),
        ("schlafen", "to sleep", "Activities", "A1", None, "Ich schlafe acht Stunden.", "I sleep for eight hours."),

        # A2 Level - With Example Sentences
        ("Reise", "journey/trip", "Travel", "A2", None, "Die Reise nach Berlin war schön.", "The trip to Berlin was nice."),
        ("buchen", "to book", "Travel", "A2", None, "Ich buche ein Hotelzimmer.", "I am booking a hotel room."),
        ("Koffer", "suitcase", "Travel", "A2", None, "Mein Koffer ist schwer.", "My suitcase is heavy."),
        ("Rucksack", "backpack", "Travel", "A2", None, "Der Rucksack ist praktisch.", "The backpack is practical."),
        ("kaufen", "to buy", "General", "A2", None, "Ich kaufe neue Schuhe.", "I am buying new shoes."),

        # B1 Level - With Example Sentences
        ("Ausflug", "excursion", "Travel", "B1", None, "Wir machen einen Ausflug in die Berge.", "We are taking an excursion to the mountains."),
        ("Sehenswürdigkeit", "sight/attraction", "Travel", "B1", None, "Die Sehenswürdigkeit ist sehr bekannt.", "The attraction is very well-known."),
        ("Reiseführer", "travel guide", "Travel", "B1", None, "Der Reiseführer zeigt uns die Stadt.", "The tour guide shows us the city."),
        ("verstehen", "to understand", "General", "B1", None, "Ich verstehe die Grammatik gut.", "I understand the grammar well."),
        ("verkaufen", "to sell", "General", "B1", None, "Sie verkauft ihre alten Bücher.", "She is selling her old books."),

        # B2 Level - With Example Sentences
        ("Verantwortung", "responsibility", "General", "B2", None, "Sie übernimmt viel Verantwortung.", "She takes on a lot of responsibility."),
        ("Möglichkeit", "possibility", "General", "B2", None, "Es gibt viele Möglichkeiten.", "There are many possibilities."),
        ("Voraussetzung", "requirement", "General", "B2", None, "Das ist eine wichtige Voraussetzung.", "That is an important requirement."),
        ("Zusammenhang", "connection", "General", "B2", None, "Der Zusammenhang ist klar.", "The connection is clear."),
        ("wahrscheinlich", "probable", "General", "B2", None, "Das ist sehr wahrscheinlich.", "That is very probable."),

        # C1 Level - With Example Sentences
        ("Wahrnehmung", "perception", "General", "C1", None, "Die Wahrnehmung ist subjektiv.", "Perception is subjective."),
        ("Auswirkung", "impact", "General", "C1", None, "Die Auswirkung ist bedeutend.", "The impact is significant."),
        ("Nachhaltigkeit", "sustainability", "General", "C1", None, "Nachhaltigkeit ist wichtig für die Zukunft.", "Sustainability is important for the future."),
        ("Herausforderung", "challenge", "General", "C1", None, "Das ist eine große Herausforderung.", "That is a big challenge."),
        ("Entwicklung", "development", "General", "C1", None, "Die Entwicklung ist positiv.", "The development is positive."),

        # C2 Level - With Example Sentences
        ("Paradigmenwechsel", "paradigm shift", "General", "C2", None, "Ein Paradigmenwechsel ist notwendig.", "A paradigm shift is necessary."),
        ("Weltanschauung", "worldview", "General", "C2", None, "Seine Weltanschauung ist interessant.", "His worldview is interesting."),
        ("Fingerspitzengefühl", "intuitive flair", "General", "C2", None, "Sie hat viel Fingerspitzengefühl.", "She has a lot of intuitive flair."),
        ("Querdenker", "lateral thinker", "General", "C2", None, "Er ist ein echter Querdenker.", "He is a true lateral thinker."),
        ("Zeitgeist", "spirit of the age", "General", "C2", None, "Das entspricht dem Zeitgeist.", "That corresponds to the spirit of the age.")
    ]

    cursor.executemany(
        """INSERT OR IGNORE INTO vocabulary 
           (german_word, english_translation, theme, cefr_level, word_group_id, example_sentence, example_sentence_translation) 
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        vocabulary_data
    )
    print(f"Inserted {len(vocabulary_data)} vocabulary items")

    conn.commit()
    conn.close()
    print("Database initialization complete")


def get_word_groups() -> List[Dict]:
    """Get all word groups"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM word_groups ORDER BY name")
    groups = cursor.fetchall()
    conn.close()
    return groups


def add_vocabulary(
    german_word: str,
    english_translation: str,
    theme: str,
    cefr_level: str,
    word_group_id: Optional[int] = None,
    example_sentence: Optional[str] = None,
    example_sentence_translation: Optional[str] = None
) -> int:
    """
    Add a new vocabulary item to the database.
    
    Args:
        german_word: The German word
        english_translation: English translation
        theme: Theme or category of the word
        cefr_level: CEFR level (A1, A2, B1, B2, C1, C2)
        word_group_id: Optional ID of the word group
        example_sentence: Optional example sentence in German
        example_sentence_translation: Optional English translation of the example sentence
    
    Returns:
        The ID of the newly created vocabulary item
    
    Raises:
        sqlite3.Error: If there's a database error
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO vocabulary (
                german_word,
                english_translation,
                theme,
                cefr_level,
                word_group_id,
                example_sentence,
                example_sentence_translation
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            german_word,
            english_translation,
            theme,
            cefr_level,
            word_group_id,
            example_sentence,
            example_sentence_translation
        ))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError as e:
        conn.rollback()
        raise Exception(f"Failed to add vocabulary: {str(e)}")
    finally:
        conn.close()


def get_vocabulary(level=None, word_group_id=None):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if level and level != "All Levels":
        cursor.execute("""
            SELECT v.*, CASE WHEN f.id IS NOT NULL THEN 1 ELSE 0 END as is_favorite 
            FROM vocabulary v 
            LEFT JOIN favorites f ON v.id = f.vocabulary_id 
            WHERE v.cefr_level = ? 
            ORDER BY v.german_word
        """, (level,))
    else:
        cursor.execute("""
            SELECT v.*, CASE WHEN f.id IS NOT NULL THEN 1 ELSE 0 END as is_favorite 
            FROM vocabulary v 
            LEFT JOIN favorites f ON v.id = f.vocabulary_id 
            ORDER BY v.german_word
        """)

    result = cursor.fetchall()
    conn.close()

    vocabulary = []
    for row in result:
        vocabulary.append({
            'id': row['id'],
            'german_word': row['german_word'],
            'english_translation': row['english_translation'],
            'theme': row['theme'],
            'cefr_level': row['cefr_level'],
            'word_group_id': row['word_group_id'],
            'example_sentence': row['example_sentence'],
            'example_sentence_translation': row['example_sentence_translation'],
            'is_favorite': row['is_favorite']
        })

    print(f"Retrieved {len(vocabulary)} vocabulary items")
    return vocabulary
