from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Trip, Stop, Activity, Expense, SavedDestination
from datetime import datetime, date
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'traveloop-secret-key-2024'
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_DIR = os.path.join(BASE_DIR, 'database')
os.makedirs(DB_DIR, exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(DB_DIR, "traveloop.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

# ── Auth Routes ──────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return redirect(url_for('dashboard') if current_user.is_authenticated else url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid email or password.', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')
        if password != confirm:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
            return render_template('register.html')
        user = User(
            first_name=request.form.get('first_name', '').strip(),
            last_name=request.form.get('last_name', '').strip(),
            email=email,
            phone=request.form.get('phone', '').strip(),
            city=request.form.get('city', '').strip(),
            country=request.form.get('country', '').strip(),
            password=generate_password_hash(password),
            additional_info=request.form.get('additional_info', '').strip()
        )
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    step = session.get('reset_step', 1)
    if request.method == 'POST':
        if step == 1:
            email = request.form.get('email', '').strip()
            user = User.query.filter_by(email=email).first()
            if user:
                session['reset_email'] = email
                session['reset_step'] = 2
                flash('Email verified. Set your new password.', 'success')
            else:
                flash('No account found with that email.', 'error')
            return redirect(url_for('forgot_password'))
        elif step == 2:
            email = session.get('reset_email')
            password = request.form.get('password', '')
            confirm = request.form.get('confirm_password', '')
            if password != confirm:
                flash('Passwords do not match.', 'error')
                return redirect(url_for('forgot_password'))
            user = User.query.filter_by(email=email).first()
            if user:
                user.password = generate_password_hash(password)
                db.session.commit()
                session.pop('reset_email', None)
                session.pop('reset_step', None)
                flash('Password reset successful! Please log in.', 'success')
                return redirect(url_for('login'))
    return render_template('forgot_password.html', step=step)

@app.route('/google-login', methods=['POST'])
def google_login():
    data = request.json
    email = data.get('email', '').strip()
    name = data.get('name', 'Google User')
    uid = data.get('uid', '')
    
    if not email:
        return jsonify({'error': 'Email required'}), 400
    
    name_parts = name.split(' ', 1)
    first_name = name_parts[0]
    last_name = name_parts[1] if len(name_parts) > 1 else ''
    
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=generate_password_hash(os.urandom(24).hex()),
            additional_info=f'Google UID: {uid}'
        )
        db.session.add(user)
        db.session.commit()
    
    login_user(user)
    return jsonify({'success': True, 'redirect': url_for('dashboard')})

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# ── App Routes ───────────────────────────────────────────────────────────────

@app.route('/dashboard')
@login_required
def dashboard():
    trips = Trip.query.filter_by(user_id=current_user.id).order_by(Trip.created_at.desc()).all()
    return render_template('dashboard.html', trips=trips)

@app.route('/create-trip', methods=['GET', 'POST'])
@login_required
def create_trip():
    if request.method == 'POST':
        trip = Trip(
            user_id=current_user.id,
            trip_name=request.form.get('trip_name', '').strip(),
            start_date=request.form.get('start_date', ''),
            end_date=request.form.get('end_date', ''),
            description=request.form.get('description', '').strip()
        )
        db.session.add(trip)
        db.session.commit()
        flash('Trip created successfully!', 'success')
        return redirect(url_for('build_itinerary', trip_id=trip.id))
    return render_template('create_trip.html')

@app.route('/build-itinerary/<int:trip_id>', methods=['GET', 'POST'])
@login_required
def build_itinerary(trip_id):
    trip = Trip.query.filter_by(id=trip_id, user_id=current_user.id).first_or_404()
    if request.method == 'POST':
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
            stop = Stop(
                trip_id=trip_id,
                section_title=title,
                city_name=cities[i] if i < len(cities) else '',
                start_date=start_dates[i] if i < len(start_dates) else '',
                end_date=end_dates[i] if i < len(end_dates) else '',
                budget=float(budgets[i]) if i < len(budgets) and budgets[i] else 0
            )
            db.session.add(stop)
            stops.append(stop)
        db.session.flush()

        for j, name in enumerate(act_names):
            stop_idx = int(act_stops[j]) if j < len(act_stops) else 0
            if stop_idx < len(stops):
                act = Activity(
                    stop_id=stops[stop_idx].id,
                    activity_name=name,
                    activity_description=act_descs[j] if j < len(act_descs) else '',
                    activity_cost=float(act_costs[j]) if j < len(act_costs) and act_costs[j] else 0
                )
                db.session.add(act)
        db.session.commit()
        flash('Itinerary saved!', 'success')
        return redirect(url_for('itinerary_view', trip_id=trip_id))
    return render_template('itinerary_builder.html', trip=trip)

@app.route('/itinerary/<int:trip_id>')
@login_required
def itinerary_view(trip_id):
    trip = Trip.query.filter_by(id=trip_id, user_id=current_user.id).first_or_404()
    return render_template('itinerary_view.html', trip=trip)

@app.route('/delete-trip/<int:trip_id>', methods=['POST'])
@login_required
def delete_trip(trip_id):
    trip = Trip.query.filter_by(id=trip_id, user_id=current_user.id).first_or_404()
    db.session.delete(trip)
    db.session.commit()
    flash('Trip deleted.', 'success')
    return redirect(url_for('dashboard'))

# ── Phase 2 Routes ───────────────────────────────────────────────────────────

@app.route('/my-trips')
@login_required
def my_trips():
    status_filter = request.args.get('status', 'all')
    search = request.args.get('search', '').strip()
    
    query = Trip.query.filter_by(user_id=current_user.id, is_archived=False)
    
    if search:
        query = query.filter(Trip.trip_name.ilike(f'%{search}%'))
    
    trips = query.order_by(Trip.created_at.desc()).all()
    
    # Categorize trips
    today = date.today().isoformat()
    ongoing = [t for t in trips if t.start_date and t.end_date and t.start_date <= today <= t.end_date]
    upcoming = [t for t in trips if t.start_date and t.start_date > today]
    completed = [t for t in trips if t.end_date and t.end_date < today]
    
    return render_template('trip_listing.html', ongoing=ongoing, upcoming=upcoming, completed=completed)

@app.route('/edit-trip/<int:trip_id>', methods=['GET', 'POST'])
@login_required
def edit_trip(trip_id):
    trip = Trip.query.filter_by(id=trip_id, user_id=current_user.id).first_or_404()
    if request.method == 'POST':
        trip.trip_name = request.form.get('trip_name', '').strip()
        trip.start_date = request.form.get('start_date', '')
        trip.end_date = request.form.get('end_date', '')
        trip.description = request.form.get('description', '').strip()
        trip.destination_country = request.form.get('destination_country', '').strip()
        db.session.commit()
        flash('Trip updated successfully!', 'success')
        return redirect(url_for('my_trips'))
    return render_template('edit_trip.html', trip=trip)

@app.route('/budget/<int:trip_id>')
@login_required
def budget(trip_id):
    trip = Trip.query.filter_by(id=trip_id, user_id=current_user.id).first_or_404()
    
    # Calculate totals
    stop_budget = sum(s.budget for s in trip.stops)
    activity_cost = sum(a.activity_cost for a in Activity.query.join(Stop).filter(Stop.trip_id == trip_id).all())
    expense_total = sum(e.amount for e in trip.expenses)
    
    total_budget = stop_budget + activity_cost
    total_spent = expense_total
    remaining = total_budget - total_spent
    
    # Expense breakdown by category
    categories = {}
    for exp in trip.expenses:
        categories[exp.category] = categories.get(exp.category, 0) + exp.amount
    
    return render_template('budget.html', trip=trip, total_budget=total_budget, 
                         total_spent=total_spent, remaining=remaining, categories=categories)

@app.route('/add-expense/<int:trip_id>', methods=['POST'])
@login_required
def add_expense(trip_id):
    trip = Trip.query.filter_by(id=trip_id, user_id=current_user.id).first_or_404()
    expense = Expense(
        trip_id=trip_id,
        category=request.form.get('category', '').strip(),
        amount=float(request.form.get('amount', 0)),
        description=request.form.get('description', '').strip(),
        expense_date=request.form.get('expense_date', '')
    )
    db.session.add(expense)
    db.session.commit()
    flash('Expense added!', 'success')
    return redirect(url_for('budget', trip_id=trip_id))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.first_name = request.form.get('first_name', '').strip()
        current_user.last_name = request.form.get('last_name', '').strip()
        current_user.phone = request.form.get('phone', '').strip()
        current_user.city = request.form.get('city', '').strip()
        current_user.country = request.form.get('country', '').strip()
        current_user.language = request.form.get('language', 'en')
        db.session.commit()
        flash('Profile updated!', 'success')
        return redirect(url_for('profile'))
    return render_template('profile.html')

@app.route('/change-password', methods=['POST'])
@login_required
def change_password():
    current_pw = request.form.get('current_password', '')
    new_pw = request.form.get('new_password', '')
    confirm_pw = request.form.get('confirm_password', '')
    
    if not check_password_hash(current_user.password, current_pw):
        flash('Current password is incorrect.', 'error')
        return redirect(url_for('profile'))
    
    if new_pw != confirm_pw:
        flash('New passwords do not match.', 'error')
        return redirect(url_for('profile'))
    
    current_user.password = generate_password_hash(new_pw)
    db.session.commit()
    flash('Password changed successfully!', 'success')
    return redirect(url_for('profile'))

@app.route('/search-city')
@login_required
def search_city():
    query = request.args.get('q', '').strip()
    
    # Static city data for demo
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

@app.route('/save-destination', methods=['POST'])
@login_required
def save_destination():
    dest = SavedDestination(
        user_id=current_user.id,
        city_name=request.form.get('city_name', '').strip(),
        country=request.form.get('country', '').strip(),
        cost_index=float(request.form.get('cost_index', 0)),
        popularity=int(request.form.get('popularity', 0))
    )
    db.session.add(dest)
    db.session.commit()
    flash('Destination saved!', 'success')
    return redirect(url_for('search_city'))

@app.route('/search-activity')
@login_required
def search_activity():
    category = request.args.get('category', 'all')
    
    # Static activity data
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

@app.route('/analytics')
@login_required
def analytics():
    trips = Trip.query.filter_by(user_id=current_user.id).all()
    
    total_trips = len(trips)
    total_budget = sum(s.budget for t in trips for s in t.stops)
    
    # Most visited city
    cities = {}
    for t in trips:
        for s in t.stops:
            if s.city_name:
                cities[s.city_name] = cities.get(s.city_name, 0) + 1
    
    most_visited = max(cities.items(), key=lambda x: x[1])[0] if cities else 'N/A'
    
    # Activity categories
    categories = {}
    for t in trips:
        for s in t.stops:
            for a in s.activities:
                cat = a.category or 'Other'
                categories[cat] = categories.get(cat, 0) + 1
    
    return render_template('analytics.html', total_trips=total_trips, total_budget=total_budget,
                         most_visited=most_visited, categories=categories)

if __name__ == '__main__':
    app.run(debug=True)
