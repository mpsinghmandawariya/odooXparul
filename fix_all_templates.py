#!/usr/bin/env python3
"""
Comprehensive Template Fixer
Fixes all known issues in Traveloop templates
"""

import os
import re

TEMPLATES_DIR = 'templates'

# URL mappings for blueprint routes
URL_FIXES = {
    # Auth routes
    'href=""/dashboard""': 'href="{{ url_for(\'trips.dashboard\') }}"',
    'href=""/login""': 'href="{{ url_for(\'auth.login\') }}"',
    'href=""/register""': 'href="{{ url_for(\'auth.register\') }}"',
    'href=""/logout""': 'href="{{ url_for(\'auth.logout\') }}"',
    'href=""/profile""': 'href="{{ url_for(\'auth.profile\') }}"',
    'action=""/login""': 'action="{{ url_for(\'auth.login\') }}"',
    'action=""/register""': 'action="{{ url_for(\'auth.register\') }}"',
    
    # Trips routes
    'href=""/my-trips""': 'href="{{ url_for(\'trips.my_trips\') }}"',
    'href=""/create-trip""': 'href="{{ url_for(\'trips.create_trip\') }}"',
    'href=""/community""': 'href="{{ url_for(\'community.community\') }}"',
    'href=""/notifications""': 'href="{{ url_for(\'community.notifications\') }}"',
    'href=""/search-city""': 'href="{{ url_for(\'trips.search_city\') }}"',
    'href=""/search-activity""': 'href="{{ url_for(\'trips.search_activity\') }}"',
    'href=""/analytics""': 'href="{{ url_for(\'trips.analytics\') }}"',
    'action=""/create-post""': 'action="{{ url_for(\'community.create_post\') }}"',
    
    # Fix url_for without blueprint prefix
    'url_for("packing_checklist"': 'url_for("trips.packing_checklist"',
    "url_for('packing_checklist'": "url_for('trips.packing_checklist'",
    'url_for("add_comment"': 'url_for("community.add_comment"',
    "url_for('add_comment'": "url_for('community.add_comment'",
    'url_for("remove_collaborator"': 'url_for("trips.remove_collaborator"',
    "url_for('remove_collaborator'": "url_for('trips.remove_collaborator'",
    'url_for("delete_note"': 'url_for("trips.delete_note"',
    "url_for('delete_note'": "url_for('trips.delete_note'",
    'url_for("admin_dashboard"': 'url_for("admin.admin_dashboard"',
    "url_for('admin_dashboard'": "url_for('admin.admin_dashboard'",
}

def fix_template(filepath):
    """Fix a single template file"""
    print(f"\nProcessing: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"  Error reading file: {e}")
        return False
    
    original_content = content
    changes = []
    
    # Fix 1: Change base.html to base_premium.html
    if '{% extends "base.html" %}' in content:
        content = content.replace('{% extends "base.html" %}', '{% extends "base_premium.html" %}')
        changes.append("Changed base template")
    
    # Fix 2: Apply all URL fixes
    for old, new in URL_FIXES.items():
        if old in content:
            content = content.replace(old, new)
            changes.append(f"Fixed URL: {old[:30]}...")
    
    # Fix 3: Fix Python string concatenation in href
    pattern = r'href="(/[^"]+/)" \+ str\(([^)]+)\)'
    matches = re.findall(pattern, content)
    for match in matches:
        old_pattern = f'href="{match[0]}" + str({match[1]})'
        route_map = {
            '/build-itinerary/': 'trips.build_itinerary',
            '/itinerary/': 'trips.itinerary_view',
            '/edit-trip/': 'trips.edit_trip',
            '/delete-trip/': 'trips.delete_trip',
            '/budget/': 'trips.budget',
            '/add-expense/': 'trips.add_expense',
            '/packing-checklist/': 'trips.packing_checklist',
            '/notes/': 'trips.trip_notes',
            '/collaboration/': 'trips.collaboration',
        }
        route_name = route_map.get(match[0], 'unknown')
        if route_name != 'unknown':
            new_pattern = f'href="{{{{ url_for(\'{route_name}\', trip_id={match[1]}) }}}}"'
            content = content.replace(old_pattern, new_pattern)
            changes.append(f"Fixed href concatenation: {match[0]}")
    
    # Fix 4: Fix action concatenation
    pattern = r'action="(/[^"]+/)" \+ str\(([^)]+)\)'
    matches = re.findall(pattern, content)
    for match in matches:
        old_pattern = f'action="{match[0]}" + str({match[1]})'
        route_map = {
            '/add-expense/': 'trips.add_expense',
            '/build-itinerary/': 'trips.build_itinerary',
        }
        route_name = route_map.get(match[0], 'unknown')
        if route_name != 'unknown':
            new_pattern = f'action="{{{{ url_for(\'{route_name}\', trip_id={match[1]}) }}}}"'
            content = content.replace(old_pattern, new_pattern)
            changes.append(f"Fixed action concatenation: {match[0]}")
    
    # Only write if changes were made
    if content != original_content:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  Fixed! Changes:")
            for change in changes:
                print(f"     - {change}")
            return True
        except Exception as e:
            print(f"  Error writing file: {e}")
            return False
    else:
        print(f"  No changes needed")
        return False

def main():
    """Main function"""
    if not os.path.exists(TEMPLATES_DIR):
        print(f"Error: {TEMPLATES_DIR} directory not found!")
        print(f"Current directory: {os.getcwd()}")
        return
    
    print("="*60)
    print("COMPREHENSIVE TEMPLATE FIXER")
    print("="*60)
    
    fixed_count = 0
    total_count = 0
    errors = []
    
    for filename in sorted(os.listdir(TEMPLATES_DIR)):
        if filename.endswith('.html'):
            filepath = os.path.join(TEMPLATES_DIR, filename)
            total_count += 1
            try:
                if fix_template(filepath):
                    fixed_count += 1
            except Exception as e:
                errors.append(f"{filename}: {str(e)}")
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Total templates: {total_count}")
    print(f"Fixed: {fixed_count}")
    print(f"Unchanged: {total_count - fixed_count}")
    
    if errors:
        print(f"\nErrors encountered: {len(errors)}")
        for error in errors:
            print(f"   - {error}")
    else:
        print("\nNo errors!")
    
    print("="*60)

if __name__ == '__main__':
    main()
