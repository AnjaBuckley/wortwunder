import sys
import os

# Get absolute path to the project directory
project_home = os.path.dirname(os.path.abspath(__file__))
print(f"Project home directory: {project_home}")

# Add project directory to Python path if not already there
if project_home not in sys.path:
    sys.path = [project_home] + sys.path
    print(f"Added {project_home} to Python path")

# Import your app
from app import app as application
print("Successfully imported Flask application")

# Initialize the database
from lib.db import init_db, get_vocabulary
print("Successfully imported database modules")

# Initialize and verify database
with application.app_context():
    print("Starting database initialization...")
    init_db()
    print("Database initialization completed, verifying data...")
    vocab = get_vocabulary()
    print(f"Database initialized with {len(vocab)} vocabulary items")
    if len(vocab) == 0:
        print("WARNING: No vocabulary items found in database!")
    else:
        print(f"First few vocabulary items: {vocab[:3]}")
