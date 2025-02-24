import sqlite3
import os
from typing import List, Dict, Optional

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


def init_db():
    print(f"Initializing database at {DB_PATH}")
    conn = get_db_connection()
    cursor = conn.cursor()

    # Drop existing tables to ensure clean slate
    cursor.execute("DROP TABLE IF EXISTS vocabulary")
    cursor.execute("DROP TABLE IF EXISTS word_groups")
    print("Dropped existing tables")

    # Create word_groups table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS word_groups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        description TEXT
    )
    """)

    # Create vocabulary table with word_group reference and explicit CEFR level
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vocabulary (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        german_word TEXT NOT NULL UNIQUE,
        english_translation TEXT NOT NULL,
        theme TEXT NOT NULL,
        cefr_level TEXT NOT NULL,
        word_group_id INTEGER,
        example_sentence TEXT,
        example_sentence_translation TEXT,
        FOREIGN KEY (word_group_id) REFERENCES word_groups (id)
    )
    """)
    print("Created database tables")

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
        ("schlafen", "to sleep", "Activities", "A1", None, "Ich schlafe acht Stunden.", "I sleep for eight hours.")
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
) -> bool:
    """Add a new vocabulary item"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO vocabulary 
            (german_word, english_translation, theme, cefr_level, word_group_id)
            VALUES (?, ?, ?, ?, ?)
            """,
            (german_word, english_translation, theme, cefr_level, word_group_id),
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding vocabulary: {e}")
        return False


def get_vocabulary(level=None, word_group_id=None):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    if level and level != "All Levels":
        cursor.execute(
            "SELECT * FROM vocabulary WHERE cefr_level = ? ORDER BY german_word",
            (level,)
        )
    else:
        cursor.execute("SELECT * FROM vocabulary ORDER BY german_word")
    
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
            'example_sentence_translation': row['example_sentence_translation']
        })
    
    print(f"Retrieved {len(vocabulary)} vocabulary items")
    return vocabulary

# Remove automatic initialization - it will be called from wsgi.py
