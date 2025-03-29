# WortWunder - German Language Learning Platform

WortWunder is an interactive German language learning platform featuring multiple engaging games to help students practice vocabulary, spelling, and comprehension.

<img width="1500" alt="Screenshot 2025-03-29 at 16 23 25" src="https://github.com/user-attachments/assets/8b695dff-e595-4d5d-b83a-5f1caa7c4b24" />



<img width="1496" alt="Screenshot 2025-03-29 at 16 23 35" src="https://github.com/user-attachments/assets/85493756-e644-4a35-a62b-7ec913343aa8" />



<img width="1500" alt="Screenshot 2025-03-29 at 16 23 43" src="https://github.com/user-attachments/assets/99ea0414-3db1-4779-9727-93f53a4ba8c7" />




<img width="1508" alt="Screenshot 2025-03-29 at 16 23 53" src="https://github.com/user-attachments/assets/9a0f86de-52d0-4dbb-9f3d-2edf0e1aeefb" />




<img width="1501" alt="Screenshot 2025-03-29 at 16 24 01" src="https://github.com/user-attachments/assets/f4953994-6db7-4e20-8f17-a1be13f12158" />




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

# Initialize and start the Flask server
PORT=5006 python app.py  # This will create the database and start the server on port 5006
```

The backend will:
1. Create and initialize the database with vocabulary data
2. Start the Flask server on port 5006 (you can change this by setting the PORT environment variable)

### Step 3: Frontend Setup
```bash
# Open a new terminal and navigate to frontend directory
cd wortwunder-launchpad

# Install dependencies (Note: You may see some npm warnings, these are normal)
npm install

# Create .env file with the backend URL (use the same port as in Step 2)
echo "VITE_API_URL=http://localhost:5006" > .env

# Start the development server
npm run dev
```

The application should now be running at:
- Frontend: http://localhost:5173 (or another port if 5173 is in use)
- Backend: http://localhost:5006 (or your custom port)

You can access the application by opening the frontend URL in your browser. The backend API will be automatically used by the frontend.

Note: If you see npm warnings during installation, these are normal and won't affect the application's functionality.

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

## Production Environment

### Deployment URLs
- Frontend: https://lucent-griffin-a98935.netlify.app
- Backend API: https://mimivader.pythonanywhere.com

### Deployment Setup

#### Frontend (Netlify)
The frontend is deployed on Netlify with the following configuration in `netlify.toml`:
```toml
[build]
  command = "npm install && npm run build"
  publish = "dist"

[build.environment]
  NODE_VERSION = "18"
  # API URL is configured in Netlify environment settings

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

#### Backend (PythonAnywhere)
The backend is hosted on PythonAnywhere. Key configuration points:
1. Python version: 3.8
2. WSGI configuration file: `wsgi.py`
3. Required files: `app.py`, `requirements.txt`

To update the backend:
1. Log in to PythonAnywhere dashboard
2. Pull the latest changes from GitHub
3. Reload the web app

### Environment Variables
- Development: Create a `.env` file in the frontend directory with your local API URL
- Production: Configure the API URL in your Netlify environment settings

### Security Notes
- Environment variables and sensitive paths are configured directly in the hosting platforms
- Database credentials and paths should never be committed to the repository
- Use environment-specific configuration for database paths and credentials

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
