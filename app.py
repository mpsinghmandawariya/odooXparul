from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_file
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from models import db, User, Trip, Stop, Activity, Expense, SavedDestination, PackingItem, CommunityPost, Comment, PostLike, TripNote, Notification, Invoice, Collaboration
from datetime import datetime, date
import os, secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = 'traveloop-secret-key-2024'
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_DIR = os.path.join(BASE_DIR, 'database')
os.makedirs(DB_DIR, exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(DB_DIR, "traveloop.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

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


# ── Phase 3 Routes ───────────────────────────────────────────────────────────

# Packing Checklist
@app.route('/packing-checklist/<int:trip_id>', methods=['GET', 'POST'])
@login_required
def packing_checklist(trip_id):
    trip = Trip.query.filter_by(id=trip_id, user_id=current_user.id).first_or_404()
    if request.method == 'POST':
        item = PackingItem(
            trip_id=trip_id,
            category=request.form.get('category', '').strip(),
            item_name=request.form.get('item_name', '').strip()
        )
        db.session.add(item)
        db.session.commit()
        return jsonify({'success': True})
    
    items = PackingItem.query.filter_by(trip_id=trip_id).all()
    categories = {}
    for item in items:
        if item.category not in categories:
            categories[item.category] = []
        categories[item.category].append(item)
    
    total = len(items)
    packed = sum(1 for i in items if i.is_packed)
    progress = int((packed / total * 100)) if total > 0 else 0
    
    return render_template('packing_checklist.html', trip=trip, categories=categories, progress=progress, total=total, packed=packed)

@app.route('/toggle-packing/<int:item_id>', methods=['POST'])
@login_required
def toggle_packing(item_id):
    item = PackingItem.query.get_or_404(item_id)
    item.is_packed = not item.is_packed
    db.session.commit()
    return jsonify({'success': True, 'is_packed': item.is_packed})

@app.route('/delete-packing-item/<int:item_id>', methods=['POST'])
@login_required
def delete_packing_item(item_id):
    item = PackingItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'success': True})

# Community
@app.route('/community')
@login_required
def community():
    posts = CommunityPost.query.order_by(CommunityPost.created_at.desc()).all()
    return render_template('community.html', posts=posts)

@app.route('/create-post', methods=['POST'])
@login_required
def create_post():
    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()
    trip_id = request.form.get('trip_id')
    
    post = CommunityPost(
        user_id=current_user.id,
        title=title,
        post_content=content,
        trip_id=int(trip_id) if trip_id else None
    )
    
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename:
            filename = secure_filename(f"{secrets.token_hex(8)}_{file.filename}")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            post.image_path = filename
    
    db.session.add(post)
    db.session.commit()
    
    # Create notification for followers (placeholder)
    flash('Post created successfully!', 'success')
    return redirect(url_for('community'))

@app.route('/like-post/<int:post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    post = CommunityPost.query.get_or_404(post_id)
    existing = PostLike.query.filter_by(post_id=post_id, user_id=current_user.id).first()
    
    if existing:
        db.session.delete(existing)
        post.likes_count -= 1
        liked = False
    else:
        like = PostLike(post_id=post_id, user_id=current_user.id)
        db.session.add(like)
        post.likes_count += 1
        liked = True
        
        # Create notification
        if post.user_id != current_user.id:
            notif = Notification(
                user_id=post.user_id,
                notification_text=f"{current_user.first_name} liked your post",
                notification_type='like',
                link=f'/community'
            )
            db.session.add(notif)
    
    db.session.commit()
    return jsonify({'success': True, 'liked': liked, 'likes_count': post.likes_count})

@app.route('/add-comment/<int:post_id>', methods=['POST'])
@login_required
def add_comment(post_id):
    post = CommunityPost.query.get_or_404(post_id)
    comment_text = request.form.get('comment', '').strip()
    
    if comment_text:
        comment = Comment(
            post_id=post_id,
            user_id=current_user.id,
            comment_text=comment_text
        )
        db.session.add(comment)
        
        # Create notification
        if post.user_id != current_user.id:
            notif = Notification(
                user_id=post.user_id,
                notification_text=f"{current_user.first_name} commented on your post",
                notification_type='comment',
                link=f'/community'
            )
            db.session.add(notif)
        
        db.session.commit()
        flash('Comment added!', 'success')
    
    return redirect(url_for('community'))

# Trip Notes & Journal
@app.route('/notes/<int:trip_id>', methods=['GET', 'POST'])
@login_required
def trip_notes(trip_id):
    trip = Trip.query.filter_by(id=trip_id, user_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
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
        return redirect(url_for('trip_notes', trip_id=trip_id))
    
    notes = TripNote.query.filter_by(trip_id=trip_id).order_by(TripNote.created_at.desc()).all()
    return render_template('notes_journal.html', trip=trip, notes=notes)

@app.route('/delete-note/<int:note_id>', methods=['POST'])
@login_required
def delete_note(note_id):
    note = TripNote.query.filter_by(id=note_id, user_id=current_user.id).first_or_404()
    trip_id = note.trip_id
    db.session.delete(note)
    db.session.commit()
    flash('Note deleted!', 'success')
    return redirect(url_for('trip_notes', trip_id=trip_id))

# Public Itinerary
@app.route('/public-itinerary/<int:trip_id>')
def public_itinerary(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    return render_template('public_itinerary.html', trip=trip)

# Invoice
@app.route('/invoice/<int:trip_id>')
@login_required
def invoice(trip_id):
    trip = Trip.query.filter_by(id=trip_id, user_id=current_user.id).first_or_404()
    
    # Check if invoice exists
    existing_invoice = Invoice.query.filter_by(trip_id=trip_id).first()
    
    if not existing_invoice:
        # Generate invoice
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
    
    return render_template('invoice.html', trip=trip, invoice=existing_invoice)

@app.route('/toggle-payment/<int:invoice_id>', methods=['POST'])
@login_required
def toggle_payment(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    invoice.payment_status = 'paid' if invoice.payment_status == 'unpaid' else 'unpaid'
    db.session.commit()
    return jsonify({'success': True, 'status': invoice.payment_status})

# Notifications
@app.route('/notifications')
@login_required
def notifications():
    notifs = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).all()
    return render_template('notifications.html', notifications=notifs)

@app.route('/mark-notification-read/<int:notif_id>', methods=['POST'])
@login_required
def mark_notification_read(notif_id):
    notif = Notification.query.filter_by(id=notif_id, user_id=current_user.id).first_or_404()
    notif.is_read = True
    db.session.commit()
    return jsonify({'success': True})

@app.route('/delete-notification/<int:notif_id>', methods=['POST'])
@login_required
def delete_notification(notif_id):
    notif = Notification.query.filter_by(id=notif_id, user_id=current_user.id).first_or_404()
    db.session.delete(notif)
    db.session.commit()
    return jsonify({'success': True})

# Collaboration
@app.route('/collaboration/<int:trip_id>', methods=['GET', 'POST'])
@login_required
def collaboration(trip_id):
    trip = Trip.query.filter_by(id=trip_id, user_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        role = request.form.get('role', 'viewer')
        
        collaborator = User.query.filter_by(email=email).first()
        if collaborator:
            existing = Collaboration.query.filter_by(trip_id=trip_id, collaborator_id=collaborator.id).first()
            if not existing:
                collab = Collaboration(
                    trip_id=trip_id,
                    collaborator_id=collaborator.id,
                    role=role
                )
                db.session.add(collab)
                
                # Create notification
                notif = Notification(
                    user_id=collaborator.id,
                    notification_text=f"{current_user.first_name} invited you to collaborate on {trip.trip_name}",
                    notification_type='collaboration',
                    link=f'/itinerary/{trip_id}'
                )
                db.session.add(notif)
                db.session.commit()
                flash('Collaborator added!', 'success')
            else:
                flash('User already collaborating on this trip.', 'info')
        else:
            flash('User not found.', 'error')
        
        return redirect(url_for('collaboration', trip_id=trip_id))
    
    collaborators = Collaboration.query.filter_by(trip_id=trip_id).all()
    return render_template('collaboration.html', trip=trip, collaborators=collaborators)

@app.route('/remove-collaborator/<int:collab_id>', methods=['POST'])
@login_required
def remove_collaborator(collab_id):
    collab = Collaboration.query.get_or_404(collab_id)
    trip_id = collab.trip_id
    db.session.delete(collab)
    db.session.commit()
    flash('Collaborator removed!', 'success')
    return redirect(url_for('collaboration', trip_id=trip_id))

# Admin Dashboard
@app.route('/admin-dashboard')
@login_required
def admin_dashboard():
    # Simple admin check (in production, use proper role-based access)
    if current_user.email != 'admin@traveloop.com':
        flash('Access denied.', 'error')
        return redirect(url_for('dashboard'))
    
    total_users = User.query.count()
    total_trips = Trip.query.count()
    total_posts = CommunityPost.query.count()
    
    # Recent users
    recent_users = User.query.order_by(User.created_at.desc()).limit(10).all()
    
    # Popular destinations
    cities = {}
    for trip in Trip.query.all():
        for stop in trip.stops:
            if stop.city_name:
                cities[stop.city_name] = cities.get(stop.city_name, 0) + 1
    
    popular_cities = sorted(cities.items(), key=lambda x: x[1], reverse=True)[:10]
    
    return render_template('admin_dashboard.html', 
                         total_users=total_users,
                         total_trips=total_trips,
                         total_posts=total_posts,
                         recent_users=recent_users,
                         popular_cities=popular_cities)

# Export
@app.route('/export/<int:trip_id>')
@login_required
def export_trip(trip_id):
    trip = Trip.query.filter_by(id=trip_id, user_id=current_user.id).first_or_404()
    return render_template('export.html', trip=trip)
