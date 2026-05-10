"""
Database Migration Script - Phase 2 to Phase 3
Adds Phase 3 tables for packing, community, notes, notifications, invoices, collaboration
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'traveloop.db')

def migrate_phase3():
    print("Starting Phase 3 database migration...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Packing Items
    try:
        cursor.execute("""
            CREATE TABLE packing_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trip_id INTEGER NOT NULL,
                category VARCHAR(50) NOT NULL,
                item_name VARCHAR(100) NOT NULL,
                is_packed BOOLEAN DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (trip_id) REFERENCES trips(id)
            )
        """)
        print("  + Created packing_items table")
    except sqlite3.OperationalError:
        print("  - packing_items table already exists")
    
    # Community Posts
    try:
        cursor.execute("""
            CREATE TABLE community_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title VARCHAR(200) NOT NULL,
                post_content TEXT NOT NULL,
                image_path VARCHAR(256),
                trip_id INTEGER,
                likes_count INTEGER DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (trip_id) REFERENCES trips(id)
            )
        """)
        print("  + Created community_posts table")
    except sqlite3.OperationalError:
        print("  - community_posts table already exists")
    
    # Comments
    try:
        cursor.execute("""
            CREATE TABLE comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                comment_text TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (post_id) REFERENCES community_posts(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        print("  + Created comments table")
    except sqlite3.OperationalError:
        print("  - comments table already exists")
    
    # Post Likes
    try:
        cursor.execute("""
            CREATE TABLE post_likes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (post_id) REFERENCES community_posts(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        print("  + Created post_likes table")
    except sqlite3.OperationalError:
        print("  - post_likes table already exists")
    
    # Trip Notes
    try:
        cursor.execute("""
            CREATE TABLE trip_notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trip_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                note_title VARCHAR(200),
                note_content TEXT NOT NULL,
                note_date VARCHAR(20),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (trip_id) REFERENCES trips(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        print("  + Created trip_notes table")
    except sqlite3.OperationalError:
        print("  - trip_notes table already exists")
    
    # Notifications
    try:
        cursor.execute("""
            CREATE TABLE notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                notification_text VARCHAR(256) NOT NULL,
                notification_type VARCHAR(50),
                is_read BOOLEAN DEFAULT 0,
                link VARCHAR(256),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        print("  + Created notifications table")
    except sqlite3.OperationalError:
        print("  - notifications table already exists")
    
    # Invoices
    try:
        cursor.execute("""
            CREATE TABLE invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trip_id INTEGER NOT NULL,
                invoice_number VARCHAR(50) UNIQUE,
                total_amount FLOAT NOT NULL,
                payment_status VARCHAR(20) DEFAULT 'unpaid',
                generated_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (trip_id) REFERENCES trips(id)
            )
        """)
        print("  + Created invoices table")
    except sqlite3.OperationalError:
        print("  - invoices table already exists")
    
    # Collaborations
    try:
        cursor.execute("""
            CREATE TABLE collaborations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trip_id INTEGER NOT NULL,
                collaborator_id INTEGER NOT NULL,
                role VARCHAR(20) DEFAULT 'viewer',
                invited_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (trip_id) REFERENCES trips(id),
                FOREIGN KEY (collaborator_id) REFERENCES users(id)
            )
        """)
        print("  + Created collaborations table")
    except sqlite3.OperationalError:
        print("  - collaborations table already exists")
    
    conn.commit()
    conn.close()
    
    print("\nPhase 3 migration completed successfully!")
    print("Run the app: python app.py")

if __name__ == '__main__':
    if not os.path.exists(DB_PATH):
        print("Database not found. Run the app first to create it.")
    else:
        migrate_phase3()
