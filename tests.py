"""
Unit Tests for Traveloop Application
"""
import unittest
from app_new import create_app
from models import db, User, Trip
from config import TestingConfig

class TraveloopTestCase(unittest.TestCase):
    """Base test case for Traveloop"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        """Tear down test fixtures"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

class AuthTestCase(TraveloopTestCase):
    """Test authentication functionality"""
    
    def test_register(self):
        """Test user registration"""
        response = self.client.post('/register', data={
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        user = User.query.filter_by(email='test@example.com').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.first_name, 'Test')
    
    def test_login(self):
        """Test user login"""
        # Create user
        user = User(
            first_name='Test',
            last_name='User',
            email='test@example.com',
            password='pbkdf2:sha256:260000$test$test'
        )
        db.session.add(user)
        db.session.commit()
        
        response = self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_logout(self):
        """Test user logout"""
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

class TripTestCase(TraveloopTestCase):
    """Test trip functionality"""
    
    def setUp(self):
        """Set up test fixtures with user"""
        super().setUp()
        self.user = User(
            first_name='Test',
            last_name='User',
            email='test@example.com',
            password='pbkdf2:sha256:260000$test$test'
        )
        db.session.add(self.user)
        db.session.commit()
    
    def test_create_trip(self):
        """Test trip creation"""
        trip = Trip(
            user_id=self.user.id,
            trip_name='Test Trip',
            start_date='2024-01-01',
            end_date='2024-01-10',
            description='Test description'
        )
        db.session.add(trip)
        db.session.commit()
        
        saved_trip = Trip.query.filter_by(trip_name='Test Trip').first()
        self.assertIsNotNone(saved_trip)
        self.assertEqual(saved_trip.user_id, self.user.id)
    
    def test_trip_relationships(self):
        """Test trip relationships"""
        trip = Trip(
            user_id=self.user.id,
            trip_name='Test Trip'
        )
        db.session.add(trip)
        db.session.commit()
        
        self.assertEqual(trip.user.email, 'test@example.com')
        self.assertEqual(len(self.user.trips), 1)

class ModelTestCase(TraveloopTestCase):
    """Test database models"""
    
    def test_user_model(self):
        """Test User model"""
        user = User(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            password='hashed_password'
        )
        db.session.add(user)
        db.session.commit()
        
        self.assertIsNotNone(user.id)
        self.assertEqual(user.email, 'john@example.com')
    
    def test_trip_model(self):
        """Test Trip model"""
        user = User(
            first_name='Test',
            last_name='User',
            email='test@example.com',
            password='password'
        )
        db.session.add(user)
        db.session.commit()
        
        trip = Trip(
            user_id=user.id,
            trip_name='Paris Adventure',
            start_date='2024-06-01',
            end_date='2024-06-15'
        )
        db.session.add(trip)
        db.session.commit()
        
        self.assertIsNotNone(trip.id)
        self.assertEqual(trip.trip_name, 'Paris Adventure')

if __name__ == '__main__':
    unittest.main()
