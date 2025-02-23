# WortWunder - German Language Learning Platform

WortWunder is an interactive German language learning platform featuring multiple engaging games to help students practice vocabulary, spelling, and comprehension.

## Features

- **Multiple Choice Quiz**: Test vocabulary knowledge with interactive multiple-choice questions
- **Spelling Bee**: Practice German word spelling with audio pronunciation support
- **Flashcards**: Review vocabulary with digital flashcards
- **CEFR Level Support**: Content filtered by CEFR language proficiency levels
- **Audio Support**: Text-to-speech for German word pronunciation

## Tech Stack

### Frontend (wortwunder-launchpad)
- React with TypeScript
- Vite
- Tailwind CSS
- Lucide Icons
- React Router
- TanStack Query

### Backend (wortwunder-backend-flask)
- Python
- Flask
- SQLite
- SQLAlchemy

## Local Development Setup

### Prerequisites
- Node.js (v18 or higher)
- Python (v3.8 or higher)
- pip (Python package manager)
- Git

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/wortwunder.git
cd wortwunder
```

### Step 2: Backend Setup
```bash
# Navigate to backend directory
cd wortwunder-backend-flask

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize the database
flask db upgrade
python init_db.py  # This will populate the database with initial vocabulary

# Start the Flask server
flask run --port 5006
```

### Step 3: Frontend Setup
```bash
# Open a new terminal and navigate to frontend directory
cd wortwunder-launchpad

# Install dependencies
npm install

# Create .env file
echo "VITE_API_URL=http://localhost:5006" > .env

# Start the development server
npm run dev
```

The application should now be running at:
- Frontend: http://localhost:5173
- Backend: http://localhost:5006

## Database Management

### Initial Setup
The `init_db.py` script creates and populates the SQLite database with:
- Vocabulary table with German-English word pairs
- CEFR levels for each word
- Example sentences

### Troubleshooting Database Issues
If you encounter database issues:

1. Stop both frontend and backend servers
2. Delete the existing database file:
   ```bash
   cd wortwunder-backend-flask
   rm instance/vocabulary.db
   ```
3. Recreate the database:
   ```bash
   flask db upgrade
   python init_db.py
   ```

### Backup and Restore
To backup your database:
```bash
cd wortwunder-backend-flask
sqlite3 instance/vocabulary.db ".backup 'backup.db'"
```

To restore from backup:
```bash
cd wortwunder-backend-flask
sqlite3 instance/vocabulary.db ".restore 'backup.db'"
```

## API Endpoints

### Vocabulary Endpoints
- `GET /api/vocabulary`: Get all vocabulary items
- `GET /api/vocabulary?level=A1`: Get vocabulary filtered by CEFR level
- `POST /api/vocabulary`: Add new vocabulary item
- `PUT /api/vocabulary/<id>`: Update vocabulary item
- `DELETE /api/vocabulary/<id>`: Delete vocabulary item

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
