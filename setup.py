"""
Automated Setup Script for Traveloop Enhanced
Handles installation, configuration, and initialization
"""
import os
import sys
import subprocess
import secrets

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def print_success(text):
    """Print success message"""
    print(f"✓ {text}")

def print_error(text):
    """Print error message"""
    print(f"✗ {text}")

def check_python_version():
    """Check if Python version is 3.10+"""
    print_header("Checking Python Version")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print_success(f"Python {version.major}.{version.minor}.{version.micro} detected")
        return True
    else:
        print_error(f"Python 3.10+ required, found {version.major}.{version.minor}")
        return False

def install_dependencies():
    """Install required packages"""
    print_header("Installing Dependencies")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print_success("All dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print_error("Failed to install dependencies")
        return False

def create_env_file():
    """Create .env file from template"""
    print_header("Setting Up Environment Variables")
    
    if os.path.exists('.env'):
        response = input(".env file already exists. Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Skipping .env creation")
            return True
    
    try:
        # Generate secure secret key
        secret_key = secrets.token_hex(32)
        
        # Read template
        with open('.env.example', 'r') as f:
            content = f.read()
        
        # Replace secret key
        content = content.replace('your-secret-key-here-change-in-production', secret_key)
        
        # Write .env file
        with open('.env', 'w') as f:
            f.write(content)
        
        print_success(".env file created with secure SECRET_KEY")
        return True
    except Exception as e:
        print_error(f"Failed to create .env file: {e}")
        return False

def create_directories():
    """Create required directories"""
    print_header("Creating Directories")
    
    directories = ['database', 'logs', 'static/uploads']
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print_success(f"Created {directory}/")
        except Exception as e:
            print_error(f"Failed to create {directory}/: {e}")
            return False
    
    return True

def initialize_database():
    """Initialize database"""
    print_header("Initializing Database")
    
    try:
        from app_new import create_app
        from models import db
        
        app = create_app()
        with app.app_context():
            db.create_all()
            print_success("Database tables created")
        
        return True
    except Exception as e:
        print_error(f"Failed to initialize database: {e}")
        return False

def run_tests():
    """Run test suite"""
    print_header("Running Tests")
    
    response = input("Run tests? (y/n): ")
    if response.lower() != 'y':
        print("Skipping tests")
        return True
    
    try:
        subprocess.check_call([sys.executable, "tests.py"])
        print_success("All tests passed")
        return True
    except subprocess.CalledProcessError:
        print_error("Some tests failed")
        return False

def print_summary():
    """Print setup summary"""
    print_header("Setup Complete!")
    
    print("✓ Dependencies installed")
    print("✓ Environment configured")
    print("✓ Directories created")
    print("✓ Database initialized")
    print("\n" + "="*60)
    print("\n🚀 To start the application, run:")
    print("\n   python app_new.py")
    print("\n📖 For more information, see:")
    print("   - QUICKSTART_NEW.md")
    print("   - IMPROVEMENTS.md")
    print("\n🌍 Access the app at: http://127.0.0.1:5000")
    print("\n" + "="*60 + "\n")

def main():
    """Main setup function"""
    print("\n" + "="*60)
    print("  Traveloop Enhanced - Automated Setup")
    print("="*60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n⚠ Setup incomplete. Please install dependencies manually.")
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        print("\n⚠ Setup incomplete. Please create .env file manually.")
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        print("\n⚠ Setup incomplete. Please create directories manually.")
        sys.exit(1)
    
    # Initialize database
    if not initialize_database():
        print("\n⚠ Setup incomplete. Please initialize database manually.")
        sys.exit(1)
    
    # Run tests (optional)
    run_tests()
    
    # Print summary
    print_summary()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ Setup failed: {e}")
        sys.exit(1)
