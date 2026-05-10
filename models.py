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
