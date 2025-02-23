CREATE TABLE IF NOT EXISTS vocabulary (
    id INTEGER PRIMARY KEY,
    german_word TEXT NOT NULL,
    english_translation TEXT NOT NULL,
    theme TEXT NOT NULL
);
