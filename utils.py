"""
Utility functions for Traveloop application
"""
import os
import logging
from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def setup_logging(app):
    """Setup application logging"""
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = logging.FileHandler('logs/traveloop.log')
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Traveloop startup')

def allowed_file(filename, allowed_extensions):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def admin_required(f):
    """Decorator to require admin access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.login'))
        if current_user.email != os.environ.get('ADMIN_EMAIL', 'admin@traveloop.com'):
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('trips.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def format_currency(amount):
    """Format amount as currency"""
    return f"${amount:,.2f}"

def calculate_trip_duration(start_date, end_date):
    """Calculate trip duration in days"""
    from datetime import datetime
    try:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
        return (end - start).days
    except:
        return 0

def get_trip_status(start_date, end_date):
    """Determine trip status based on dates"""
    from datetime import date
    today = date.today().isoformat()
    
    if not start_date or not end_date:
        return 'upcoming'
    
    if start_date <= today <= end_date:
        return 'ongoing'
    elif start_date > today:
        return 'upcoming'
    else:
        return 'completed'
