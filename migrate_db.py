"""
Database Migration Script - Phase 1 to Phase 2
Adds new columns to existing tables without losing data
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'traveloop.db')

def migrate():
    print("Starting Phase 2 database migration...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Add new columns to users table
        print("Migrating users table...")
        cursor.execute("ALTER TABLE users ADD COLUMN profile_picture VARCHAR(256)")
        print("  + Added profile_picture")
    except sqlite3.OperationalError:
        print("  - profile_picture already exists")
    
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN language VARCHAR(10) DEFAULT 'en'")
        print("  + Added language")
    except sqlite3.OperationalError:
        print("  - language already exists")
    
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN dark_mode BOOLEAN DEFAULT 1")
        print("  + Added dark_mode")
    except sqlite3.OperationalError:
        print("  - dark_mode already exists")
    
    # Add new columns to trips table
    print("\nMigrating trips table...")
    try:
        cursor.execute("ALTER TABLE trips ADD COLUMN destination_country VARCHAR(100)")
        print("  + Added destination_country")
    except sqlite3.OperationalError:
        print("  - destination_country already exists")
    
    try:
        cursor.execute("ALTER TABLE trips ADD COLUMN status VARCHAR(20) DEFAULT 'upcoming'")
        print("  + Added status")
    except sqlite3.OperationalError:
        print("  - status already exists")
    
    try:
        cursor.execute("ALTER TABLE trips ADD COLUMN is_archived BOOLEAN DEFAULT 0")
        print("  + Added is_archived")
    except sqlite3.OperationalError:
        print("  - is_archived already exists")
    
    # Add new columns to activities table
    print("\nMigrating activities table...")
    try:
        cursor.execute("ALTER TABLE activities ADD COLUMN category VARCHAR(50)")
        print("  + Added category")
    except sqlite3.OperationalError:
        print("  - category already exists")
    
    try:
        cursor.execute("ALTER TABLE activities ADD COLUMN duration VARCHAR(50)")
        print("  + Added duration")
    except sqlite3.OperationalError:
        print("  - duration already exists")
    
    # Create new tables
    print("\nCreating new tables...")
    
    # Expenses table
    try:
        cursor.execute("""
            CREATE TABLE expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trip_id INTEGER NOT NULL,
                category VARCHAR(50) NOT NULL,
                amount FLOAT NOT NULL,
                description TEXT,
                expense_date VARCHAR(20),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (trip_id) REFERENCES trips(id)
            )
        """)
        print("  + Created expenses table")
    except sqlite3.OperationalError:
        print("  - expenses table already exists")
    
    # Saved Destinations table
    try:
        cursor.execute("""
            CREATE TABLE saved_destinations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                city_name VARCHAR(100) NOT NULL,
                country VARCHAR(100),
                cost_index FLOAT,
                popularity INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        print("  + Created saved_destinations table")
    except sqlite3.OperationalError:
        print("  - saved_destinations table already exists")
    
    conn.commit()
    conn.close()
    
    print("\nMigration completed successfully!")
    print("You can now run the app: python app.py")

if __name__ == '__main__':
    if not os.path.exists(DB_PATH):
        print("Database not found. Run the app first to create it.")
    else:
        migrate()
