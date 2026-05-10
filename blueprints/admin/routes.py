from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from models import db, User, Trip, CommunityPost
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.email != current_app.config.get('ADMIN_EMAIL'):
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('trips.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def admin_dashboard():
    total_users = User.query.count()
    total_trips = Trip.query.count()
    total_posts = CommunityPost.query.count()
    
    recent_users = User.query.order_by(User.created_at.desc()).limit(10).all()
    
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
