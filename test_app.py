"""
Quick test to verify Flask app configuration
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import app
    
    print("[OK] Flask app imported successfully")
    print(f"[OK] Secret key configured: {bool(app.config.get('SECRET_KEY'))}")
    print(f"[OK] Database URI: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
    
    # List all routes
    print("\n[ROUTES] Registered Routes:")
    routes = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            routes.append(f"  {rule.rule} -> {rule.endpoint}")
    
    for route in sorted(routes):
        print(route)
    
    print(f"\n[OK] Total routes: {len(routes)}")
    print("\n[READY] App is ready to run!")
    print("\nTo start the server, run:")
    print("  python app.py")
    print("\nThen open: http://127.0.0.1:5000")
    
except Exception as e:
    print(f"[ERROR] Error: {e}")
    import traceback
    traceback.print_exc()
