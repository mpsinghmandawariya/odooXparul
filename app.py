from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_file
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from models import db, User, Trip, Stop, Activity, Expense, SavedDestination, PackingItem, CommunityPost, Comment, PostLike, TripNote, Notification, Invoice, Collaboration
from datetime import datetime, date
import os, secrets
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_DIR = os.path.join(BASE_DIR, 'database')
os.makedirs(DB_DIR, exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(DB_DIR, "traveloop.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Context processor for notifications
@app.context_processor
def utility_processor():
    def unread_notifications_count():
        try:
            if current_user.is_authenticated:
                return Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
        except:
            pass
        return 0
    return dict(unread_notifications_count=unread_notifications_count)

with app.app_context():
    db.create_all()

# Register Blueprints
from blueprints.auth.routes import auth_bp
from blueprints.trips.routes import trips_bp
from blueprints.community.routes import community_bp
from blueprints.admin.routes import admin_bp

app.register_blueprint(auth_bp)
app.register_blueprint(trips_bp)
app.register_blueprint(community_bp)
app.register_blueprint(admin_bp)

# ── Auth Routes ──────────────────────────────────────────────────────────────

@app.route('/test')
def test_route():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test - Traveloop</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; background: #f5f5f5; }
            .success { background: #d4edda; border: 1px solid #c3e6cb; color: #155724; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
            .info { background: #d1ecf1; border: 1px solid #bee5eb; color: #0c5460; padding: 20px; border-radius: 8px; }
            h1 { color: #333; }
            ul { line-height: 1.8; }
            a { color: #007bff; text-decoration: none; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="success">
            <h1>Server is Running!</h1>
            <p>Flask application is working correctly.</p>
        </div>
        <div class="info">
            <h2>Available Routes:</h2>
            <ul>
                <li><a href="/">Home (redirects to login/dashboard)</a></li>
                <li><a href="/login">Login Page</a></li>
                <li><a href="/register">Register Page</a></li>
                <li><a href="/dashboard">Dashboard (requires login)</a></li>
                <li><a href="/search-city">Search Cities (requires login)</a></li>
                <li><a href="/search-activity">Search Activities (requires login)</a></li>
            </ul>
            <h2>Next Steps:</h2>
            <ol>
                <li>Go to <a href="/login">/login</a> to sign in</li>
                <li>Or go to <a href="/register">/register</a> to create an account</li>
                <li>After login, you'll be redirected to the dashboard</li>
            </ol>
        </div>
    </body>
    </html>
    '''

@app.route('/')
def index():
    return redirect(url_for('trips.dashboard') if current_user.is_authenticated else url_for('auth.login'))


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('403.html'), 403

if __name__ == '__main__':
    app.run(debug=True)
