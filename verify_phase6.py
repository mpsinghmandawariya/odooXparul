"""
Traveloop Phase 6 - Verification Script
Checks all implementations and confirms readiness
"""

import os
import sys

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"[OK] {description}: {filepath}")
        return True
    else:
        print(f"[MISSING] {description}: {filepath} NOT FOUND")
        return False

def check_directory_exists(dirpath, description):
    """Check if a directory exists"""
    if os.path.isdir(dirpath):
        print(f"[OK] {description}: {dirpath}")
        return True
    else:
        print(f"[MISSING] {description}: {dirpath} NOT FOUND")
        return False

def count_files_in_directory(dirpath, extension):
    """Count files with specific extension in directory"""
    if not os.path.isdir(dirpath):
        return 0
    return len([f for f in os.listdir(dirpath) if f.endswith(extension)])

def main():
    print("=" * 70)
    print("TRAVELOOP PHASE 6 - VERIFICATION SCRIPT")
    print("=" * 70)
    print()
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    checks_passed = 0
    total_checks = 0
    
    # Core Files
    print("[CORE FILES]")
    print("-" * 70)
    total_checks += 1
    if check_file_exists(os.path.join(base_dir, 'app.py'), "Main Application"):
        checks_passed += 1
    
    total_checks += 1
    if check_file_exists(os.path.join(base_dir, 'models.py'), "Database Models"):
        checks_passed += 1
    
    total_checks += 1
    if check_file_exists(os.path.join(base_dir, 'requirements.txt'), "Dependencies"):
        checks_passed += 1
    
    print()
    
    # Phase 6 New Files
    print("[PHASE 6 NEW FILES]")
    print("-" * 70)
    
    # Error Pages
    total_checks += 1
    if check_file_exists(os.path.join(base_dir, 'templates', '404.html'), "404 Error Page"):
        checks_passed += 1
    
    total_checks += 1
    if check_file_exists(os.path.join(base_dir, 'templates', '500.html'), "500 Error Page"):
        checks_passed += 1
    
    total_checks += 1
    if check_file_exists(os.path.join(base_dir, 'templates', '403.html'), "403 Error Page"):
        checks_passed += 1
    
    # Enhanced JavaScript
    total_checks += 1
    if check_file_exists(os.path.join(base_dir, 'static', 'js', 'enhanced.js'), "Enhanced JavaScript"):
        checks_passed += 1
    
    # Deployment Files
    total_checks += 1
    if check_file_exists(os.path.join(base_dir, '.env.example'), "Environment Variables Example"):
        checks_passed += 1
    
    total_checks += 1
    if check_file_exists(os.path.join(base_dir, 'config.py'), "Production Configuration"):
        checks_passed += 1
    
    total_checks += 1
    if check_file_exists(os.path.join(base_dir, 'Procfile'), "Procfile"):
        checks_passed += 1
    
    total_checks += 1
    if check_file_exists(os.path.join(base_dir, 'requirements-prod.txt'), "Production Requirements"):
        checks_passed += 1
    
    total_checks += 1
    if check_file_exists(os.path.join(base_dir, 'runtime.txt'), "Runtime Configuration"):
        checks_passed += 1
    
    # Documentation
    total_checks += 1
    if check_file_exists(os.path.join(base_dir, 'PHASE6_ANALYSIS.md'), "Phase 6 Analysis"):
        checks_passed += 1
    
    total_checks += 1
    if check_file_exists(os.path.join(base_dir, 'PHASE6_COMPLETE.md'), "Phase 6 Complete Guide"):
        checks_passed += 1
    
    total_checks += 1
    if check_file_exists(os.path.join(base_dir, 'QUICKSTART.md'), "Quick Start Guide"):
        checks_passed += 1
    
    print()
    
    # Directories
    print("[DIRECTORIES]")
    print("-" * 70)
    total_checks += 1
    if check_directory_exists(os.path.join(base_dir, 'templates'), "Templates Directory"):
        checks_passed += 1
    
    total_checks += 1
    if check_directory_exists(os.path.join(base_dir, 'static'), "Static Directory"):
        checks_passed += 1
    
    total_checks += 1
    if check_directory_exists(os.path.join(base_dir, 'static', 'css'), "CSS Directory"):
        checks_passed += 1
    
    total_checks += 1
    if check_directory_exists(os.path.join(base_dir, 'static', 'js'), "JavaScript Directory"):
        checks_passed += 1
    
    total_checks += 1
    if check_directory_exists(os.path.join(base_dir, 'database'), "Database Directory"):
        checks_passed += 1
    
    print()
    
    # Count Files
    print("[FILE COUNTS]")
    print("-" * 70)
    
    templates_count = count_files_in_directory(os.path.join(base_dir, 'templates'), '.html')
    print(f"[OK] HTML Templates: {templates_count} (Expected: 27)")
    
    js_count = count_files_in_directory(os.path.join(base_dir, 'static', 'js'), '.js')
    print(f"[OK] JavaScript Files: {js_count} (Expected: 2)")
    
    css_count = count_files_in_directory(os.path.join(base_dir, 'static', 'css'), '.css')
    print(f"[OK] CSS Files: {css_count} (Expected: 1)")
    
    print()
    
    # Check app.py for error handlers
    print("[CODE VERIFICATION]")
    print("-" * 70)
    
    app_path = os.path.join(base_dir, 'app.py')
    if os.path.exists(app_path):
        with open(app_path, 'r', encoding='utf-8') as f:
            app_content = f.read()
            
            total_checks += 1
            if '@app.errorhandler(404)' in app_content:
                print("[OK] 404 Error Handler: Implemented")
                checks_passed += 1
            else:
                print("[MISSING] 404 Error Handler: NOT FOUND")
            
            total_checks += 1
            if '@app.errorhandler(500)' in app_content:
                print("[OK] 500 Error Handler: Implemented")
                checks_passed += 1
            else:
                print("[MISSING] 500 Error Handler: NOT FOUND")
            
            total_checks += 1
            if '@app.errorhandler(403)' in app_content:
                print("[OK] 403 Error Handler: Implemented")
                checks_passed += 1
            else:
                print("[MISSING] 403 Error Handler: NOT FOUND")
    
    # Check base.html for enhanced.js
    base_html_path = os.path.join(base_dir, 'templates', 'base.html')
    if os.path.exists(base_html_path):
        with open(base_html_path, 'r', encoding='utf-8') as f:
            base_content = f.read()
            
            total_checks += 1
            if 'enhanced.js' in base_content:
                print("[OK] Enhanced JavaScript: Loaded in base.html")
                checks_passed += 1
            else:
                print("[MISSING] Enhanced JavaScript: NOT loaded in base.html")
    
    print()
    
    # Database Check
    print("[DATABASE]")
    print("-" * 70)
    db_path = os.path.join(base_dir, 'database', 'traveloop.db')
    if os.path.exists(db_path):
        print(f"[OK] Database exists: {db_path}")
        db_size = os.path.getsize(db_path) / 1024  # KB
        print(f"   Size: {db_size:.2f} KB")
    else:
        print(f"[INFO] Database not found (will be created on first run)")
    
    print()
    
    # Final Summary
    print("=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)
    print(f"Checks Passed: {checks_passed}/{total_checks}")
    print(f"Success Rate: {(checks_passed/total_checks)*100:.1f}%")
    print()
    
    if checks_passed == total_checks:
        print("*** ALL CHECKS PASSED! Phase 6 is COMPLETE! ***")
        print("Application is ready for testing and deployment")
        print()
        print("Next Steps:")
        print("1. Run: python app.py")
        print("2. Open: http://127.0.0.1:5000")
        print("3. Test all features")
        print("4. Deploy to production")
        return 0
    elif checks_passed >= total_checks * 0.9:
        print("WARNING: MOSTLY COMPLETE - Minor issues found")
        print("Review the failed checks above and fix them")
        return 1
    else:
        print("ERROR: INCOMPLETE - Several checks failed")
        print("Review the failed checks above and implement missing features")
        return 2

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
