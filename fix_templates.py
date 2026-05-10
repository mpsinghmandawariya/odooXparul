#!/usr/bin/env python3
"""
Template Fixer Script
Automatically fixes common issues in Traveloop templates
"""

import os
import re

# Define URL mappings
URL_MAPPINGS = {
    '"/dashboard"': '"{{ url_for(\'trips.dashboard\') }}"',
    '"/my-trips"': '"{{ url_for(\'trips.my_trips\') }}"',
    '"/create-trip"': '"{{ url_for(\'trips.create_trip\') }}"',
    '"/search-city"': '"{{ url_for(\'trips.search_city\') }}"',
    '"/search-activity"': '"{{ url_for(\'trips.search_activity\') }}"',
    '"/analytics"': '"{{ url_for(\'trips.analytics\') }}"',
    '"/profile"': '"{{ url_for(\'auth.profile\') }}"',
    '"/logout"': '"{{ url_for(\'auth.logout\') }}"',
    '"/community"': '"{{ url_for(\'community.community\') }}"',
    '"/notifications"': '"{{ url_for(\'community.notifications\') }}"',
}

# Files that need base.html changed to base_premium.html
FILES_TO_UPDATE_BASE = [
    'itinerary_view.html',
    'budget.html',
    'itinerary_builder.html',
    'packing_checklist.html',
    'notes_journal.html',
    'collaboration.html',
    'invoice.html',
    'export.html',
    'city_search.html',
    'activity_search.html',
    'analytics.html',
    'community.html',
    'notifications.html',
    'profile.html',
]

def fix_template(filepath):
    """Fix a single template file"""
    print(f"Fixing {filepath}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Fix base template
    if 'base.html' in content:
        content = content.replace('{% extends "base.html" %}', '{% extends "base_premium.html" %}')
        print(f"  - Changed base template to base_premium.html")
    
    # Fix hardcoded URLs
    for old_url, new_url in URL_MAPPINGS.items():
        if old_url in content:
            content = content.replace(old_url, new_url)
            print(f"  - Fixed URL: {old_url}")
    
    # Fix Python string concatenation in href
    # Pattern: href="/something/" + str(variable)
    pattern = r'href="(/[^"]+/)" \+ str\(([^)]+)\)'
    matches = re.findall(pattern, content)
    for match in matches:
        old_pattern = f'href="{match[0]}" + str({match[1]})'
        # Determine the route name from the URL
        route_map = {
            '/build-itinerary/': 'trips.build_itinerary',
            '/itinerary/': 'trips.itinerary_view',
            '/edit-trip/': 'trips.edit_trip',
            '/delete-trip/': 'trips.delete_trip',
            '/budget/': 'trips.budget',
            '/add-expense/': 'trips.add_expense',
        }
        route_name = route_map.get(match[0], 'unknown')
        new_pattern = f'href="{{{{ url_for(\'{route_name}\', trip_id={match[1]}) }}}}"'
        content = content.replace(old_pattern, new_pattern)
        print(f"  - Fixed Python concatenation: {old_pattern}")
    
    # Fix action="/something/" + str(variable)
    pattern = r'action="(/[^"]+/)" \+ str\(([^)]+)\)'
    matches = re.findall(pattern, content)
    for match in matches:
        old_pattern = f'action="{match[0]}" + str({match[1]})'
        route_map = {
            '/add-expense/': 'trips.add_expense',
            '/build-itinerary/': 'trips.build_itinerary',
        }
        route_name = route_map.get(match[0], 'unknown')
        new_pattern = f'action="{{{{ url_for(\'{route_name}\', trip_id={match[1]}) }}}}"'
        content = content.replace(old_pattern, new_pattern)
        print(f"  - Fixed action concatenation: {old_pattern}")
    
    # Only write if changes were made
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ Fixed {filepath}")
        return True
    else:
        print(f"  ℹ️  No changes needed for {filepath}")
        return False

def main():
    """Main function"""
    templates_dir = 'templates'
    
    if not os.path.exists(templates_dir):
        print(f"Error: {templates_dir} directory not found!")
        return
    
    fixed_count = 0
    total_count = 0
    
    for filename in os.listdir(templates_dir):
        if filename.endswith('.html'):
            filepath = os.path.join(templates_dir, filename)
            total_count += 1
            if fix_template(filepath):
                fixed_count += 1
    
    print(f"\n{'='*50}")
    print(f"Summary: Fixed {fixed_count} out of {total_count} templates")
    print(f"{'='*50}")

if __name__ == '__main__':
    main()
