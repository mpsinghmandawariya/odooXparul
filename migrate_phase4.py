"""
Phase 4 & 5 Migration Script
Adds AI, Weather, Achievements tables and prepares for production
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'traveloop.db')

def migrate_phase4():
    print("Starting Phase 4 & 5 database migration...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # AI Recommendations
    try:
        cursor.execute("""
            CREATE TABLE ai_recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                recommendation_type VARCHAR(50) NOT NULL,
                recommendation_data TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        print("  + Created ai_recommendations table")
    except sqlite3.OperationalError:
        print("  - ai_recommendations table already exists")
    
    # Weather Cache
    try:
        cursor.execute("""
            CREATE TABLE weather_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city_name VARCHAR(100) NOT NULL,
                temperature FLOAT,
                weather_condition VARCHAR(50),
                forecast_data TEXT,
                cached_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("  + Created weather_cache table")
    except sqlite3.OperationalError:
        print("  - weather_cache table already exists")
    
    # Achievements
    try:
        cursor.execute("""
            CREATE TABLE achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                badge_name VARCHAR(100) NOT NULL,
                badge_description VARCHAR(256),
                unlocked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        print("  + Created achievements table")
    except sqlite3.OperationalError:
        print("  - achievements table already exists")
    
    conn.commit()
    conn.close()
    
    print("\nPhase 4 & 5 migration completed!")
    print("Run: python app.py")

if __name__ == '__main__':
    if not os.path.exists(DB_PATH):
        print("Database not found. Run the app first.")
    else:
        migrate_phase4()
