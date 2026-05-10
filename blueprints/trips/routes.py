from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db, Trip, Stop, Activity, Expense, SavedDestination, PackingItem, TripNote, Invoice, Collaboration, Notification
from datetime import date
import secrets

trips_bp = Blueprint('trips', __name__)

@trips_bp.route('/dashboard')
@login_required
def dashboard():
    trips = Trip.query.filter_by(user_id=current_user.id).order_by(Trip.created_at.desc()).limit(6).all()
    return render_template('dashboard.html', trips=trips)

@trips_bp.route('/create-trip', methods=['GET', 'POST'])
@login_required
def create_trip():
    if request.method == 'POST':
        trip_name = request.form.get('trip_name', '').strip()
        if not trip_name:
            flash('Trip name is required.', 'error')
            return render_template('create_trip.html')
        
        try:
            trip = Trip(
                user_id=current_user.id,
                trip_name=trip_name,
                start_date=request.form.get('start_date', ''),
                end_date=request.form.get('end_date', ''),
                description=request.form.get('description', '').strip()
            )
            db.session.add(trip)
            db.session.commit()
            flash('Trip created successfully!', 'success')
            return redirect(url_for('trips.build_itinerary', trip_id=trip.id))
        except Exception as e:
            db.session.rollback()
            flash('Error creating trip. Please try again.', 'error')
            return render_template('create_trip.html')
    return render_template('create_trip.html')

@trips_bp.route('/build-itinerary/<int:trip_id>', methods=['GET', 'POST'])
@login_required
def build_itinerary(trip_id):
    trip = Trip.query.filter_by(id=trip_id, user_id=current_user.id).first_or_404()
    if request.method == 'POST':
        try:
            Stop.query.filter_by(trip_id=trip_id).delete()
            db.session.commit()
            
            sections = request.form.getlist('section_title[]')
            cities = request.form.getlist('city_name[]')
            start_dates = request.form.getlist('start_date[]')
            end_dates = request.form.getlist('end_date[]')
            budgets = request.form.getlist('budget[]')
            act_names = request.form.getlist('activity_name[]')
            act_descs = request.form.getlist('activity_description[]')
            act_costs = request.form.getlist('activity_cost[]')
            act_stops = request.form.getlist('activity_stop[]')

            stops = []
            for i, title in enumerate(sections):
                try:
                    budget_val = float(budgets[i]) if i < len(budgets) and budgets[i] else 0
                except (ValueError, IndexError):
                    budget_val = 0
                    
                stop = Stop(
                    trip_id=trip_id,
                    section_title=title,
                    city_name=cities[i] if i < len(cities) else '',
                    start_date=start_dates[i] if i < len(start_dates) else '',
                    end_date=end_dates[i] if i < len(end_dates) else '',
                    budget=budget_val
                )
                db.session.add(stop)
                stops.append(stop)
            db.session.flush()

            for j, name in enumerate(act_names):
                try:
                    stop_idx = int(act_stops[j]) if j < len(act_stops) else 0
                except (ValueError, IndexError):
                    stop_idx = 0
                    
                if stop_idx < len(stops):
                    try:
                        cost_val = float(act_costs[j]) if j < len(act_costs) and act_costs[j] else 0
                    except (ValueError, IndexError):
                        cost_val = 0
                        
                    act = Activity(
                        stop_id=stops[stop_idx].id,
                        activity_name=name,
                        activity_description=act_descs[j] if j < len(act_descs) else '',
                        activity_cost=cost_val
                    )
                    db.session.add(act)
            db.session.commit()
            flash('Itinerary saved!', 'success')
            return redirect(url_for('trips.itinerary_view', trip_id=trip_id))
        except Exception as e:
            db.session.rollback()
            flash('Error saving itinerary. Please try again.', 'error')
            return render_template('itinerary_builder.html', trip=trip)
    return render_template('itinerary_builder.html', trip=trip)

@trips_bp.route('/itinerary/<int:trip_id>')
@login_required
def itinerary_view(trip_id):
    trip = Trip.query.filter_by(id=trip_id, user_id=current_user.id).first_or_404()
    return render_template('itinerary_view.html', trip=trip)

@trips_bp.route('/my-trips')
@login_required
def my_trips():
    search = request.args.get('search', '').strip()
    query = Trip.query.filter_by(user_id=current_user.id, is_archived=False)
    
    if search:
        query = query.filter(Trip.trip_name.ilike(f'%{search}%'))
    
    trips = query.order_by(Trip.created_at.desc()).all()
    
    today = date.today().isoformat()
    ongoing = [t for t in trips if t.start_date and t.end_date and t.start_date <= today <= t.end_date]
    upcoming = [t for t in trips if t.start_date and t.start_date > today]
    completed = [t for t in trips if t.end_date and t.end_date < today]
    
    return render_template('trip_listing.html', ongoing=ongoing, upcoming=upcoming, completed=completed)

@trips_bp.route('/edit-trip/<int:trip_id>', methods=['GET', 'POST'])
@login_required
def edit_trip(trip_id):
    trip = Trip.query.filter_by(id=trip_id, user_id=current_user.id).first_or_404()
    if request.method == 'POST':
        try:
            trip.trip_name = request.form.get('trip_name', '').strip()
            trip.start_date = request.form.get('start_date', '')
            trip.end_date = request.form.get('end_date', '')
            trip.description = request.form.get('description', '').strip()
            trip.destination_country = request.form.get('destination_country', '').strip()
            db.session.commit()
            flash('Trip updated successfully!', 'success')
            return redirect(url_for('trips.my_trips'))
        except Exception as e:
            db.session.rollback()
            flash('Error updating trip. Please try again.', 'error')
    return render_template('edit_trip.html', trip=trip)

@trips_bp.route('/delete-trip/<int:trip_id>', methods=['POST'])
@login_required
def delete_trip(trip_id):
    trip = Trip.query.filter_by(id=trip_id, user_id=current_user.id).first_or_404()
    try:
        db.session.delete(trip)
        db.session.commit()
        flash('Trip deleted.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting trip. Please try again.', 'error')
    return redirect(url_for('trips.my_trips'))

@trips_bp.route('/budget/<int:trip_id>')
@login_required
def budget(trip_id):
    trip = Trip.query.filter_by(id=trip_id, user_id=current_user.id).first_or_404()
    
    stop_budget = sum(s.budget for s in trip.stops)
    activity_cost = sum(a.activity_cost for a in Activity.query.join(Stop).filter(Stop.trip_id == trip_id).all())
    expense_total = sum(e.amount for e in trip.expenses)
    
    total_budget = stop_budget + activity_cost
    total_spent = expense_total
    remaining = total_budget - total_spent
    
    categories = {}
    for exp in trip.expenses:
        categories[exp.category] = categories.get(exp.category, 0) + exp.amount
    
    return render_template('budget.html', trip=trip, total_budget=total_budget, 
                         total_spent=total_spent, remaining=remaining, categories=categories)

@trips_bp.route('/add-expense/<int:trip_id>', methods=['POST'])
@login_required
def add_expense(trip_id):
    trip = Trip.query.filter_by(id=trip_id, user_id=current_user.id).first_or_404()
    
    amount = request.form.get('amount', 0)
    try:
        amount = float(amount)
    except ValueError:
        flash('Invalid amount.', 'error')
        return redirect(url_for('trips.budget', trip_id=trip_id))
    
    expense = Expense(
        trip_id=trip_id,
        category=request.form.get('category', '').strip(),
        amount=amount,
        description=request.form.get('description', '').strip(),
        expense_date=request.form.get('expense_date', '')
    )
    db.session.add(expense)
    db.session.commit()
    flash('Expense added!', 'success')
    return redirect(url_for('trips.budget', trip_id=trip_id))

@trips_bp.route('/packing-checklist/<int:trip_id>', methods=['GET', 'POST'])
@login_required
def packing_checklist(trip_id):
    trip = Trip.query.filter_by(id=trip_id, user_id=current_user.id).first_or_404()
    if request.method == 'POST':
        try:
            item = PackingItem(
                trip_id=trip_id,
                category=request.form.get('category', '').strip(),
                item_name=request.form.get('item_name', '').strip()
            )
            db.session.add(item)
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': 'Failed to add item'}), 500
    
    items = PackingItem.query.filter_by(trip_id=trip_id).all()
    categories = {}
    for item in items:
        if item.category not in categories:
            categories[item.category] = []
        categories[item.category].append(item)
    
    total = len(items)
    packed = sum(1 for i in items if i.is_packed)
    progress = int((packed / total * 100)) if total > 0 else 0
    
    return render_template('packing_checklist.html', trip=trip, categories=categories, 
                         progress=progress, total=total, packed=packed)

@trips_bp.route('/toggle-packing/<int:item_id>', methods=['POST'])
@login_required
def toggle_packing(item_id):
    try:
        item = PackingItem.query.get_or_404(item_id)
        item.is_packed = not item.is_packed
        db.session.commit()
        return jsonify({'success': True, 'is_packed': item.is_packed})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Failed to toggle item'}), 500

@trips_bp.route('/delete-packing-item/<int:item_id>', methods=['POST'])
@login_required
def delete_packing_item(item_id):
    try:
        item = PackingItem.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Failed to delete item'}), 500

@trips_bp.route('/notes/<int:trip_id>', methods=['GET', 'POST'])
@login_required
def trip_notes(trip_id):
    trip = Trip.query.filter_by(id=trip_id, user_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        try:
            note = TripNote(
                trip_id=trip_id,
                user_id=current_user.id,
                note_title=request.form.get('title', '').strip(),
                note_content=request.form.get('content', '').strip(),
                note_date=request.form.get('date', '')
            )
            db.session.add(note)
            db.session.commit()
            flash('Note added!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error adding note. Please try again.', 'error')
        return redirect(url_for('trips.trip_notes', trip_id=trip_id))
    
    notes = TripNote.query.filter_by(trip_id=trip_id).order_by(TripNote.created_at.desc()).all()
    return render_template('notes_journal.html', trip=trip, notes=notes)

@trips_bp.route('/delete-note/<int:note_id>', methods=['POST'])
@login_required
def delete_note(note_id):
    note = TripNote.query.filter_by(id=note_id, user_id=current_user.id).first_or_404()
    trip_id = note.trip_id
    try:
        db.session.delete(note)
        db.session.commit()
        flash('Note deleted!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting note. Please try again.', 'error')
    return redirect(url_for('trips.trip_notes', trip_id=trip_id))

@trips_bp.route('/invoice/<int:trip_id>')
@login_required
def invoice(trip_id):
    trip = Trip.query.filter_by(id=trip_id, user_id=current_user.id).first_or_404()
    existing_invoice = Invoice.query.filter_by(trip_id=trip_id).first()
    
    if not existing_invoice:
        try:
            invoice_num = f"INV-{trip_id}-{secrets.token_hex(4).upper()}"
            total = sum(e.amount for e in trip.expenses)
            
            new_invoice = Invoice(
                trip_id=trip_id,
                invoice_number=invoice_num,
                total_amount=total,
                payment_status='unpaid'
            )
            db.session.add(new_invoice)
            db.session.commit()
            existing_invoice = new_invoice
        except Exception as e:
            db.session.rollback()
            flash('Error generating invoice.', 'error')
    
    return render_template('invoice.html', trip=trip, invoice=existing_invoice)

@trips_bp.route('/toggle-payment/<int:invoice_id>', methods=['POST'])
@login_required
def toggle_payment(invoice_id):
    try:
        invoice = Invoice.query.get_or_404(invoice_id)
        invoice.payment_status = 'paid' if invoice.payment_status == 'unpaid' else 'unpaid'
        db.session.commit()
        return jsonify({'success': True, 'status': invoice.payment_status})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Failed to update payment status'}), 500

@trips_bp.route('/collaboration/<int:trip_id>', methods=['GET', 'POST'])
@login_required
def collaboration(trip_id):
    trip = Trip.query.filter_by(id=trip_id, user_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        role = request.form.get('role', 'viewer')
        
        from models import User
        collaborator = User.query.filter_by(email=email).first()
        if collaborator:
            existing = Collaboration.query.filter_by(trip_id=trip_id, collaborator_id=collaborator.id).first()
            if not existing:
                try:
                    collab = Collaboration(
                        trip_id=trip_id,
                        collaborator_id=collaborator.id,
                        role=role
                    )
                    db.session.add(collab)
                    
                    notif = Notification(
                        user_id=collaborator.id,
                        notification_text=f"{current_user.first_name} invited you to collaborate on {trip.trip_name}",
                        notification_type='collaboration',
                        link=f'/itinerary/{trip_id}'
                    )
                    db.session.add(notif)
                    db.session.commit()
                    flash('Collaborator added!', 'success')
                except Exception as e:
                    db.session.rollback()
                    flash('Error adding collaborator. Please try again.', 'error')
            else:
                flash('User already collaborating on this trip.', 'info')
        else:
            flash('User not found.', 'error')
        
        return redirect(url_for('trips.collaboration', trip_id=trip_id))
    
    collaborators = Collaboration.query.filter_by(trip_id=trip_id).all()
    return render_template('collaboration.html', trip=trip, collaborators=collaborators)

@trips_bp.route('/remove-collaborator/<int:collab_id>', methods=['POST'])
@login_required
def remove_collaborator(collab_id):
    collab = Collaboration.query.get_or_404(collab_id)
    trip_id = collab.trip_id
    try:
        db.session.delete(collab)
        db.session.commit()
        flash('Collaborator removed!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error removing collaborator. Please try again.', 'error')
    return redirect(url_for('trips.collaboration', trip_id=trip_id))

@trips_bp.route('/public-itinerary/<int:trip_id>')
def public_itinerary(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    return render_template('public_itinerary.html', trip=trip)

@trips_bp.route('/export/<int:trip_id>')
@login_required
def export_trip(trip_id):
    trip = Trip.query.filter_by(id=trip_id, user_id=current_user.id).first_or_404()
    return render_template('export.html', trip=trip)

@trips_bp.route('/search-city')
@login_required
def search_city():
    query = request.args.get('q', '').strip()
    
    cities = [
        {'name': 'Paris', 'country': 'France', 'cost_index': 85, 'popularity': 95},
        {'name': 'Tokyo', 'country': 'Japan', 'cost_index': 90, 'popularity': 92},
        {'name': 'New York', 'country': 'USA', 'cost_index': 95, 'popularity': 90},
        {'name': 'Bali', 'country': 'Indonesia', 'cost_index': 45, 'popularity': 88},
        {'name': 'Dubai', 'country': 'UAE', 'cost_index': 80, 'popularity': 85},
        {'name': 'London', 'country': 'UK', 'cost_index': 92, 'popularity': 93},
        {'name': 'Barcelona', 'country': 'Spain', 'cost_index': 70, 'popularity': 87},
        {'name': 'Rome', 'country': 'Italy', 'cost_index': 75, 'popularity': 89},
        {'name': 'Bangkok', 'country': 'Thailand', 'cost_index': 40, 'popularity': 86},
        {'name': 'Sydney', 'country': 'Australia', 'cost_index': 88, 'popularity': 84},
    ]
    
    if query:
        cities = [c for c in cities if query.lower() in c['name'].lower() or query.lower() in c['country'].lower()]
    
    return render_template('city_search.html', cities=cities, query=query)

@trips_bp.route('/save-destination', methods=['POST'])
@login_required
def save_destination():
    try:
        cost_index = float(request.form.get('cost_index', 0))
        popularity = int(request.form.get('popularity', 0))
    except ValueError:
        flash('Invalid cost index or popularity value.', 'error')
        return redirect(url_for('trips.search_city'))
    
    try:
        dest = SavedDestination(
            user_id=current_user.id,
            city_name=request.form.get('city_name', '').strip(),
            country=request.form.get('country', '').strip(),
            cost_index=cost_index,
            popularity=popularity
        )
        db.session.add(dest)
        db.session.commit()
        flash('Destination saved!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error saving destination. Please try again.', 'error')
    
    return redirect(url_for('trips.search_city'))

@trips_bp.route('/search-activity')
@login_required
def search_activity():
    category = request.args.get('category', 'all')
    
    activities = [
        {'name': 'Eiffel Tower Visit', 'category': 'Historical', 'cost': 25, 'duration': '2-3 hours', 'rating': 4.8},
        {'name': 'Scuba Diving', 'category': 'Adventure', 'cost': 120, 'duration': '4-5 hours', 'rating': 4.9},
        {'name': 'Food Tour', 'category': 'Food', 'cost': 60, 'duration': '3-4 hours', 'rating': 4.7},
        {'name': 'Hiking Trail', 'category': 'Nature', 'cost': 0, 'duration': '5-6 hours', 'rating': 4.6},
        {'name': 'Museum Visit', 'category': 'Historical', 'cost': 15, 'duration': '2-3 hours', 'rating': 4.5},
        {'name': 'Beach Day', 'category': 'Relaxation', 'cost': 0, 'duration': 'Full day', 'rating': 4.8},
        {'name': 'Shopping District', 'category': 'Shopping', 'cost': 50, 'duration': '3-4 hours', 'rating': 4.3},
        {'name': 'Night Club', 'category': 'Nightlife', 'cost': 40, 'duration': '4-5 hours', 'rating': 4.4},
    ]
    
    if category != 'all':
        activities = [a for a in activities if a['category'].lower() == category.lower()]
    
    return render_template('activity_search.html', activities=activities, category=category)

@trips_bp.route('/analytics')
@login_required
def analytics():
    trips = Trip.query.filter_by(user_id=current_user.id).all()
    
    total_trips = len(trips)
    total_budget = sum(s.budget for t in trips for s in t.stops)
    
    cities = {}
    for t in trips:
        for s in t.stops:
            if s.city_name:
                cities[s.city_name] = cities.get(s.city_name, 0) + 1
    
    most_visited = max(cities.items(), key=lambda x: x[1])[0] if cities else 'N/A'
    
    categories = {}
    for t in trips:
        for s in t.stops:
            for a in s.activities:
                cat = a.category or 'Other'
                categories[cat] = categories.get(cat, 0) + 1
    
    return render_template('analytics.html', total_trips=total_trips, total_budget=total_budget,
                         most_visited=most_visited, categories=categories)
