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

    # Add some new sample words if we didn't have existing ones
    sample_data = [
        # Basic Words (A1)
        ("und", "and", "General", "A1"),
        ("sein", "to be", "General", "A1"),
        ("ich", "I", "General", "A1"),
        ("du", "you", "General", "A1"),
        ("er", "he", "General", "A1"),
        ("sie", "she/they", "General", "A1"),
        ("es", "it", "General", "A1"),
        ("wir", "we", "General", "A1"),
        ("ihr", "you (plural)", "General", "A2"),
        ("haben", "to have", "General", "A2"),
        # Food and Drink (A1-B1)
        ("Essen", "food", "Food", "A1"),
        ("Trinken", "drink", "Food", "A1"),
        ("Brot", "bread", "Food", "A1"),
        ("Wasser", "water", "Food", "A1"),
        ("Kaffee", "coffee", "Food", "A1"),
        ("Tee", "tea", "Food", "A1"),
        ("Milch", "milk", "Food", "A1"),
        ("Apfel", "apple", "Food", "A1"),
        ("Banane", "banana", "Food", "A1"),
        ("Orange", "orange", "Food", "A1"),
        ("Kartoffel", "potato", "Food", "A1"),
        ("Suppe", "soup", "Food", "A1"),
        ("Salat", "salad", "Food", "A1"),
        ("Fleisch", "meat", "Food", "A2"),
        ("Gemüse", "vegetables", "Food", "A2"),
        ("Obst", "fruit", "Food", "A2"),
        ("Frühstück", "breakfast", "Food", "A2"),
        ("Mittagessen", "lunch", "Food", "A2"),
        ("Abendessen", "dinner", "Food", "A2"),
        ("Restaurant", "restaurant", "Food", "A2"),
        ("Speisekarte", "menu", "Food", "B1"),
        ("Vorspeise", "appetizer", "Food", "B1"),
        ("Hauptgericht", "main course", "Food", "B1"),
        ("Nachspeise", "dessert", "Food", "B1"),
        ("Rechnung", "bill", "Food", "B1"),
        # Travel (A1-C1)
        ("Reise", "journey/trip", "Travel", "A2"),
        ("Zug", "train", "Travel", "A1"),
        ("Bus", "bus", "Travel", "A1"),
        ("Auto", "car", "Travel", "A1"),
        ("Flugzeug", "airplane", "Travel", "A1"),
        ("Bahnhof", "train station", "Travel", "A1"),
        ("Flughafen", "airport", "Travel", "A1"),
        ("Hotel", "hotel", "Travel", "A1"),
        ("Ticket", "ticket", "Travel", "A1"),
        ("Pass", "passport", "Travel", "A1"),
        ("Koffer", "suitcase", "Travel", "A2"),
        ("Rucksack", "backpack", "Travel", "A2"),
        ("Reservierung", "reservation", "Travel", "A2"),
        ("Ausflug", "excursion", "Travel", "B1"),
        ("Sehenswürdigkeit", "sight/attraction", "Travel", "B1"),
        ("Reiseführer", "travel guide", "Travel", "B1"),
        ("Unterkunft", "accommodation", "Travel", "B1"),
        ("Reisebüro", "travel agency", "Travel", "B1"),
        ("Ausland", "foreign country", "Travel", "B1"),
        ("Rundreise", "round trip", "Travel", "B2"),
        # Numbers and Math (A1-B1)
        ("Zahl", "number", "Numbers", "A1"),
        ("eins", "one", "Numbers", "A1"),
        ("zwei", "two", "Numbers", "A1"),
        ("drei", "three", "Numbers", "A1"),
        ("vier", "four", "Numbers", "A1"),
        ("fünf", "five", "Numbers", "A1"),
        ("sechs", "six", "Numbers", "A1"),
        ("sieben", "seven", "Numbers", "A1"),
        ("acht", "eight", "Numbers", "A1"),
        ("neun", "nine", "Numbers", "A1"),
        ("zehn", "ten", "Numbers", "A1"),
        ("hundert", "hundred", "Numbers", "A1"),
        ("tausend", "thousand", "Numbers", "A2"),
        ("Million", "million", "Numbers", "A2"),
        ("plus", "plus", "Numbers", "A1"),
        ("minus", "minus", "Numbers", "A1"),
        ("mal", "times", "Numbers", "A1"),
        ("geteilt", "divided", "Numbers", "A2"),
        ("Prozent", "percent", "Numbers", "A2"),
        ("Summe", "sum", "Numbers", "B1"),
        # General Verbs (A1-B2)
        ("gehen", "to go", "General", "A1"),
        ("kommen", "to come", "General", "A1"),
        ("machen", "to make/do", "General", "A1"),
        ("sagen", "to say", "General", "A1"),
        ("sprechen", "to speak", "General", "A1"),
        ("hören", "to hear", "General", "A1"),
        ("sehen", "to see", "General", "A1"),
        ("wissen", "to know", "General", "A1"),
        ("denken", "to think", "General", "A1"),
        ("glauben", "to believe", "General", "A2"),
        ("verstehen", "to understand", "General", "A2"),
        ("lernen", "to learn", "General", "A2"),
        ("arbeiten", "to work", "General", "A2"),
        ("spielen", "to play", "General", "A2"),
        ("lesen", "to read", "General", "A2"),
        ("schreiben", "to write", "General", "A2"),
        ("kaufen", "to buy", "General", "A2"),
        ("verkaufen", "to sell", "General", "B1"),
        ("beginnen", "to begin", "General", "B1"),
        ("enden", "to end", "General", "B1"),
        # General Nouns (A1-B2)
        ("Zeit", "time", "General", "A1"),
        ("Tag", "day", "General", "A1"),
        ("Woche", "week", "General", "A1"),
        ("Monat", "month", "General", "A1"),
        ("Jahr", "year", "General", "A1"),
        ("Name", "name", "General", "A1"),
        ("Familie", "family", "General", "A1"),
        ("Freund", "friend", "General", "A1"),
        ("Haus", "house", "General", "A1"),
        ("Schule", "school", "General", "A1"),
        ("Arbeit", "work", "General", "A1"),
        ("Stadt", "city", "General", "A1"),
        ("Land", "country", "General", "A1"),
        ("Welt", "world", "General", "A2"),
        ("Leben", "life", "General", "A2"),
        ("Problem", "problem", "General", "A2"),
        ("Lösung", "solution", "General", "B1"),
        ("Meinung", "opinion", "General", "B1"),
        ("Idee", "idea", "General", "B1"),
        ("Beispiel", "example", "General", "B1"),
        # General Adjectives (A1-B2)
        ("gut", "good", "General", "A1"),
        ("schlecht", "bad", "General", "A1"),
        ("groß", "big", "General", "A1"),
        ("klein", "small", "General", "A1"),
        ("neu", "new", "General", "A1"),
        ("alt", "old", "General", "A1"),
        ("schön", "beautiful", "General", "A1"),
        ("hässlich", "ugly", "General", "A2"),
        ("schnell", "fast", "General", "A1"),
        ("langsam", "slow", "General", "A1"),
        ("heiß", "hot", "General", "A1"),
        ("kalt", "cold", "General", "A1"),
        ("leicht", "easy/light", "General", "A2"),
        ("schwer", "difficult/heavy", "General", "A2"),
        ("interessant", "interesting", "General", "A2"),
        ("langweilig", "boring", "General", "A2"),
        ("wichtig", "important", "General", "A2"),
        ("möglich", "possible", "General", "B1"),
        ("unmöglich", "impossible", "General", "B1"),
        ("wahrscheinlich", "probable", "General", "B1"),
        # Food Adjectives (A2-B2)
        ("süß", "sweet", "Food", "A2"),
        ("sauer", "sour", "Food", "A2"),
        ("salzig", "salty", "Food", "A2"),
        ("bitter", "bitter", "Food", "A2"),
        ("scharf", "spicy", "Food", "A2"),
        ("frisch", "fresh", "Food", "A2"),
        ("gekocht", "cooked", "Food", "A2"),
        ("gebraten", "fried", "Food", "B1"),
        ("gedämpft", "steamed", "Food", "B1"),
        ("gegrillt", "grilled", "Food", "B1"),
        # Travel Verbs (A2-B2)
        ("buchen", "to book", "Travel", "A2"),
        ("reservieren", "to reserve", "Travel", "A2"),
        ("packen", "to pack", "Travel", "A2"),
        ("ankommen", "to arrive", "Travel", "A2"),
        ("abfahren", "to depart", "Travel", "A2"),
        ("übernachten", "to stay overnight", "Travel", "B1"),
        ("besichtigen", "to visit/view", "Travel", "B1"),
        ("wandern", "to hike", "Travel", "B1"),
        ("campen", "to camp", "Travel", "B1"),
        ("fotografieren", "to photograph", "Travel", "B1"),
        # Additional General Words (B1-C1)
        ("Entwicklung", "development", "General", "B1"),
        ("Erfahrung", "experience", "General", "B1"),
        ("Verantwortung", "responsibility", "General", "B2"),
        ("Möglichkeit", "possibility", "General", "B2"),
        ("Voraussetzung", "requirement", "General", "B2"),
        ("Zusammenhang", "connection", "General", "B2"),
        ("Wahrnehmung", "perception", "General", "C1"),
        ("Auswirkung", "impact", "General", "C1"),
        ("Nachhaltigkeit", "sustainability", "General", "C1"),
        ("Herausforderung", "challenge", "General", "C1"),
        # Advanced Academic and Professional (C2)
        ("Paradigmenwechsel", "paradigm shift", "General", "C2"),
        ("Erkenntnistheorie", "epistemology", "General", "C2"),
        ("Weltanschauung", "worldview/philosophy of life", "General", "C2"),
        ("Querdenker", "lateral thinker/maverick", "General", "C2"),
        ("Zeitgeist", "spirit of the age", "General", "C2"),
        ("Fingerspitzengefühl", "intuitive flair/sensitivity", "General", "C2"),
        ("Wesenszug", "characteristic trait", "General", "C2"),
        ("Gedankengut", "body of thought/ideology", "General", "C2"),
        ("Sachverhalt", "state of affairs/facts", "General", "C2"),
        ("Zusammenhang", "correlation/context", "General", "C2"),
        # Scientific and Technical (C2)
        ("Quantenmechanik", "quantum mechanics", "General", "C2"),
        ("Relativitätstheorie", "theory of relativity", "General", "C2"),
        ("Nanotechnologie", "nanotechnology", "General", "C2"),
        ("Biotechnologie", "biotechnology", "General", "C2"),
        ("Künstliche Intelligenz", "artificial intelligence", "General", "C2"),
        ("Neuroplastizität", "neuroplasticity", "General", "C2"),
        ("Gentechnik", "genetic engineering", "General", "C2"),
        ("Quantencomputer", "quantum computer", "General", "C2"),
        ("Algorithmus", "algorithm", "General", "C2"),
        ("Datenverarbeitung", "data processing", "General", "C2"),
        # Business and Economics (C2)
        ("Wirtschaftsprüfung", "financial auditing", "General", "C2"),
        ("Unternehmensführung", "corporate management", "General", "C2"),
        ("Marktforschung", "market research", "General", "C2"),
        ("Börsenaufsicht", "stock exchange supervision", "General", "C2"),
        ("Gewinnmaximierung", "profit maximization", "General", "C2"),
        ("Vermögensverwaltung", "asset management", "General", "C2"),
        ("Risikostreuung", "risk diversification", "General", "C2"),
        ("Handelsabkommen", "trade agreement", "General", "C2"),
        ("Wettbewerbsvorteil", "competitive advantage", "General", "C2"),
        ("Geschäftsmodell", "business model", "General", "C2"),
        # Legal and Political (C2)
        ("Rechtsstaatlichkeit", "rule of law", "General", "C2"),
        ("Verfassungsrecht", "constitutional law", "General", "C2"),
        ("Gesetzgebung", "legislation", "General", "C2"),
        ("Völkerrecht", "international law", "General", "C2"),
        ("Menschenrechte", "human rights", "General", "C2"),
        ("Staatsangehörigkeit", "citizenship", "General", "C2"),
        ("Rechtsprechung", "jurisdiction", "General", "C2"),
        ("Gewaltenteilung", "separation of powers", "General", "C2"),
        ("Diplomatie", "diplomacy", "General", "C2"),
        ("Souveränität", "sovereignty", "General", "C2"),
        # Philosophy and Arts (C2)
        ("Existenzialismus", "existentialism", "General", "C2"),
        ("Metaphysik", "metaphysics", "General", "C2"),
        ("Ästhetik", "aesthetics", "General", "C2"),
        ("Impressionismus", "impressionism", "General", "C2"),
        ("Expressionismus", "expressionism", "General", "C2"),
        ("Symbolismus", "symbolism", "General", "C2"),
        ("Abstraktion", "abstraction", "General", "C2"),
        ("Interpretation", "interpretation", "General", "C2"),
        ("Komposition", "composition", "General", "C2"),
        ("Perspektive", "perspective", "General", "C2"),
        # Environmental and Sustainability (C2)
        ("Klimawandel", "climate change", "General", "C2"),
        ("Umweltschutz", "environmental protection", "General", "C2"),
        ("Ressourcenknappheit", "resource scarcity", "General", "C2"),
        ("Energiewende", "energy transition", "General", "C2"),
        ("Kreislaufwirtschaft", "circular economy", "General", "C2"),
        ("Biodiversität", "biodiversity", "General", "C2"),
        ("Nachhaltigkeit", "sustainability", "General", "C2"),
        ("Ökosystem", "ecosystem", "General", "C2"),
        ("Klimaneutralität", "climate neutrality", "General", "C2"),
        ("Umweltbewusstsein", "environmental awareness", "General", "C2"),
    ]

    cursor.executemany(
        """
        INSERT OR IGNORE INTO vocabulary 
        (german_word, english_translation, theme, cefr_level)
        VALUES (?, ?, ?, ?)
        """,
        sample_data,
    )
    print(f"Inserted {len(sample_data)} vocabulary items")

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
            'word_group_id': row['word_group_id']
        })
    
    print(f"Retrieved {len(vocabulary)} vocabulary items")
    return vocabulary

# Remove automatic initialization - it will be called from wsgi.py
