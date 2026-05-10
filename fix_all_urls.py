"""
Script to replace all url_for() calls with direct URLs in templates
"""
import os
import re

# Mapping of url_for endpoints to direct URLs
URL_MAPPING = {
    "url_for('dashboard')": '"/dashboard"',
    "url_for('my_trips')": '"/my-trips"',
    "url_for('create_trip')": '"/create-trip"',
    "url_for('search_city')": '"/search-city"',
    "url_for('search_activity')": '"/search-activity"',
    "url_for('community')": '"/community"',
    "url_for('analytics')": '"/analytics"',
    "url_for('profile')": '"/profile"',
    "url_for('logout')": '"/logout"',
    "url_for('login')": '"/login"',
    "url_for('register')": '"/register"',
    "url_for('forgot_password')": '"/forgot-password"',
    "url_for('notifications')": '"/notifications"',
    "url_for('change_password')": '"/change-password"',
    "url_for('save_destination')": '"/save-destination"',
    "url_for('create_post')": '"/create-post"',
    "url_for('public_itinerary', trip_id=trip.id)": '"/public-itinerary/" + str(trip.id)',
    "url_for('itinerary_view', trip_id=trip.id)": '"/itinerary/" + str(trip.id)',
    "url_for('edit_trip', trip_id=trip.id)": '"/edit-trip/" + str(trip.id)',
    "url_for('delete_trip', trip_id=trip.id)": '"/delete-trip/" + str(trip.id)',
    "url_for('budget', trip_id=trip.id)": '"/budget/" + str(trip.id)',
    "url_for('add_expense', trip_id=trip.id)": '"/add-expense/" + str(trip.id)',
    "url_for('packing_checklist', trip_id=trip.id)": '"/packing-checklist/" + str(trip.id)',
    "url_for('trip_notes', trip_id=trip.id)": '"/notes/" + str(trip.id)',
    "url_for('collaboration', trip_id=trip.id)": '"/collaboration/" + str(trip.id)',
    "url_for('invoice', trip_id=trip.id)": '"/invoice/" + str(trip.id)',
    "url_for('export_trip', trip_id=trip.id)": '"/export/" + str(trip.id)',
    "url_for('build_itinerary', trip_id=trip.id)": '"/build-itinerary/" + str(trip.id)',
}

templates_dir = "templates"
fixed_count = 0
files_fixed = []

for filename in os.listdir(templates_dir):
    if filename.endswith('.html'):
        filepath = os.path.join(templates_dir, filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Replace all url_for patterns
        for old_pattern, new_url in URL_MAPPING.items():
            # Handle both {{ url_for(...) }} and "{{ url_for(...) }}"
            pattern1 = '{{ ' + old_pattern + ' }}'
            pattern2 = '"{{ ' + old_pattern + ' }}"'
            
            if pattern1 in content:
                content = content.replace(pattern1, new_url)
                fixed_count += 1
            if pattern2 in content:
                content = content.replace(pattern2, new_url)
                fixed_count += 1
        
        # Save if changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            files_fixed.append(filename)
            print(f"Fixed: {filename}")

print(f"\nTotal replacements: {fixed_count}")
print(f"Files modified: {len(files_fixed)}")
print("\nDone!")
