from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    city = db.Column(db.String(50))
    country = db.Column(db.String(50))
    password = db.Column(db.String(256), nullable=False)
    additional_info = db.Column(db.Text)
    profile_picture = db.Column(db.String(256))
    language = db.Column(db.String(10), default='en')
    dark_mode = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    trips = db.relationship('Trip', backref='user', lazy=True, cascade='all, delete-orphan')
    saved_destinations = db.relationship('SavedDestination', backref='user', lazy=True, cascade='all, delete-orphan')

class Trip(db.Model):
    __tablename__ = 'trips'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    trip_name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.String(20))
    end_date = db.Column(db.String(20))
    description = db.Column(db.Text)
    destination_country = db.Column(db.String(100))
    status = db.Column(db.String(20), default='upcoming')
    is_archived = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    stops = db.relationship('Stop', backref='trip', lazy=True, cascade='all, delete-orphan')
    expenses = db.relationship('Expense', backref='trip', lazy=True, cascade='all, delete-orphan')

class Stop(db.Model):
    __tablename__ = 'stops'
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    city_name = db.Column(db.String(100))
    section_title = db.Column(db.String(100))
    start_date = db.Column(db.String(20))
    end_date = db.Column(db.String(20))
    budget = db.Column(db.Float, default=0)
    activities = db.relationship('Activity', backref='stop', lazy=True, cascade='all, delete-orphan')

class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True)
    stop_id = db.Column(db.Integer, db.ForeignKey('stops.id'), nullable=False)
    activity_name = db.Column(db.String(100))
    activity_description = db.Column(db.Text)
    activity_cost = db.Column(db.Float, default=0)
    category = db.Column(db.String(50))
    duration = db.Column(db.String(50))

class Expense(db.Model):
    __tablename__ = 'expenses'
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    expense_date = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SavedDestination(db.Model):
    __tablename__ = 'saved_destinations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    city_name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100))
    cost_index = db.Column(db.Float)
    popularity = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# Phase 3 Models

class PackingItem(db.Model):
    __tablename__ = 'packing_items'
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    item_name = db.Column(db.String(100), nullable=False)
    is_packed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class CommunityPost(db.Model):
    __tablename__ = 'community_posts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    post_content = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(256))
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'))
    likes_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref='posts')
    comments = db.relationship('Comment', backref='post', lazy=True, cascade='all, delete-orphan')
    likes = db.relationship('PostLike', backref='post', lazy=True, cascade='all, delete-orphan')

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('community_posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comment_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref='comments')

class PostLike(db.Model):
    __tablename__ = 'post_likes'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('community_posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TripNote(db.Model):
    __tablename__ = 'trip_notes'
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    note_title = db.Column(db.String(200))
    note_content = db.Column(db.Text, nullable=False)
    note_date = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    notification_text = db.Column(db.String(256), nullable=False)
    notification_type = db.Column(db.String(50))
    is_read = db.Column(db.Boolean, default=False)
    link = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Invoice(db.Model):
    __tablename__ = 'invoices'
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    invoice_number = db.Column(db.String(50), unique=True)
    total_amount = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.String(20), default='unpaid')
    generated_date = db.Column(db.DateTime, default=datetime.utcnow)
    trip = db.relationship('Trip', backref='invoices')

class Collaboration(db.Model):
    __tablename__ = 'collaborations'
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    collaborator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    role = db.Column(db.String(20), default='viewer')
    invited_at = db.Column(db.DateTime, default=datetime.utcnow)
    collaborator = db.relationship('User', backref='collaborations')


# Phase 4 Models

class AIRecommendation(db.Model):
    __tablename__ = 'ai_recommendations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recommendation_type = db.Column(db.String(50), nullable=False)
    recommendation_data = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class WeatherCache(db.Model):
    __tablename__ = 'weather_cache'
    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(100), nullable=False)
    temperature = db.Column(db.Float)
    weather_condition = db.Column(db.String(50))
    forecast_data = db.Column(db.Text)
    cached_at = db.Column(db.DateTime, default=datetime.utcnow)

class Achievement(db.Model):
    __tablename__ = 'achievements'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    badge_name = db.Column(db.String(100), nullable=False)
    badge_description = db.Column(db.String(256))
    unlocked_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref='achievements')
