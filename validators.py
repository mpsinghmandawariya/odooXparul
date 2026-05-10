"""
Input Validation and Sanitization for Traveloop
"""
import re
from flask import flash

class Validator:
    """Input validation class"""
    
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_password(password):
        """Validate password strength"""
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        if not re.search(r'[A-Za-z]', password):
            return False, "Password must contain at least one letter"
        if not re.search(r'[0-9]', password):
            return False, "Password must contain at least one number"
        return True, "Valid password"
    
    @staticmethod
    def validate_phone(phone):
        """Validate phone number format"""
        if not phone:
            return True  # Phone is optional
        pattern = r'^\+?[0-9]{10,15}$'
        return re.match(pattern, phone.replace('-', '').replace(' ', '')) is not None
    
    @staticmethod
    def validate_date(date_string):
        """Validate date format (YYYY-MM-DD)"""
        if not date_string:
            return True  # Date is optional
        pattern = r'^\d{4}-\d{2}-\d{2}$'
        return re.match(pattern, date_string) is not None
    
    @staticmethod
    def sanitize_string(text, max_length=None):
        """Sanitize string input"""
        if not text:
            return ''
        
        # Remove leading/trailing whitespace
        text = text.strip()
        
        # Remove potentially dangerous characters
        text = re.sub(r'[<>]', '', text)
        
        # Limit length if specified
        if max_length and len(text) > max_length:
            text = text[:max_length]
        
        return text
    
    @staticmethod
    def validate_trip_data(data):
        """Validate trip creation data"""
        errors = []
        
        if not data.get('trip_name'):
            errors.append('Trip name is required')
        elif len(data.get('trip_name', '')) > 100:
            errors.append('Trip name must be less than 100 characters')
        
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        if start_date and not Validator.validate_date(start_date):
            errors.append('Invalid start date format')
        
        if end_date and not Validator.validate_date(end_date):
            errors.append('Invalid end date format')
        
        if start_date and end_date and start_date > end_date:
            errors.append('End date must be after start date')
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_expense_data(data):
        """Validate expense data"""
        errors = []
        
        if not data.get('category'):
            errors.append('Category is required')
        
        try:
            amount = float(data.get('amount', 0))
            if amount <= 0:
                errors.append('Amount must be greater than 0')
        except ValueError:
            errors.append('Invalid amount')
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_post_data(data):
        """Validate community post data"""
        errors = []
        
        if not data.get('title'):
            errors.append('Title is required')
        elif len(data.get('title', '')) > 200:
            errors.append('Title must be less than 200 characters')
        
        if not data.get('content'):
            errors.append('Content is required')
        elif len(data.get('content', '')) > 5000:
            errors.append('Content must be less than 5000 characters')
        
        return len(errors) == 0, errors

def validate_file_upload(file, allowed_extensions, max_size_mb=16):
    """Validate file upload"""
    if not file or not file.filename:
        return False, "No file selected"
    
    # Check file extension
    if '.' not in file.filename:
        return False, "Invalid file format"
    
    ext = file.filename.rsplit('.', 1)[1].lower()
    if ext not in allowed_extensions:
        return False, f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}"
    
    # Check file size
    file.seek(0, 2)  # Seek to end
    size = file.tell()
    file.seek(0)  # Reset to beginning
    
    if size > max_size_mb * 1024 * 1024:
        return False, f"File size exceeds {max_size_mb}MB limit"
    
    return True, "Valid file"
