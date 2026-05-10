"""
Activate Premium UI for Traveloop
This script switches the application to use the new premium design
"""
import os
import shutil
import sys

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def activate_premium_ui():
    print("="*60)
    print("  ACTIVATING TRAVELOOP PREMIUM UI")
    print("="*60)
    print()
    
    # Step 1: Backup old app.py
    if os.path.exists('app.py'):
        print("[OK] Backing up old app.py to app_old_backup.py...")
        shutil.copy('app.py', 'app_old_backup.py')
    
    # Step 2: Use app_new.py as main app
    if os.path.exists('app_new.py'):
        print("[OK] Activating app_new.py (with blueprints and premium features)...")
        if os.path.exists('app.py'):
            os.remove('app.py')
        shutil.copy('app_new.py', 'app.py')
    
    # Step 3: Verify premium CSS exists
    if os.path.exists('static/css/premium.css'):
        print("[OK] Premium CSS found")
    else:
        print("[WARNING] premium.css not found in static/css/")
    
    # Step 4: Verify premium templates exist
    premium_templates = [
        'templates/base_premium.html',
        'templates/dashboard.html',
        'templates/login_premium.html'
    ]
    
    for template in premium_templates:
        if os.path.exists(template):
            print(f"[OK] {template} found")
        else:
            print(f"[WARNING] {template} not found")
    
    print()
    print("="*60)
    print("  PREMIUM UI ACTIVATED!")
    print("="*60)
    print()
    print("Next steps:")
    print("1. Run: python app.py")
    print("2. Open: http://127.0.0.1:5000")
    print("3. Login and enjoy the new premium UI!")
    print()
    print("Note: The dashboard now uses the premium design.")
    print("      Other pages will gradually be updated.")
    print()

if __name__ == '__main__':
    try:
        activate_premium_ui()
    except Exception as e:
        print(f"\n[ERROR] {e}")
        print("\nPlease run this script from the traveloop directory.")
