"""
Database Migration Script for Traveloop
Initializes Flask-Migrate and creates initial migration
"""
from app_new import create_app
from models import db
from flask_migrate import Migrate, init, migrate, upgrade
import os

def initialize_migrations():
    """Initialize Flask-Migrate for the application"""
    app = create_app()
    
    with app.app_context():
        # Check if migrations folder exists
        if not os.path.exists('migrations'):
            print("Initializing migrations...")
            os.system('flask db init')
            print("✓ Migrations initialized")
        
        # Create initial migration
        print("\nCreating migration...")
        os.system('flask db migrate -m "Add indexes and optimize database"')
        print("✓ Migration created")
        
        # Apply migration
        print("\nApplying migration...")
        os.system('flask db upgrade')
        print("✓ Migration applied")
        
        print("\n✓ Database migration completed successfully!")

if __name__ == '__main__':
    initialize_migrations()
