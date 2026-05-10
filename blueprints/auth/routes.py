from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
import os

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('trips.dashboard'))
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('trips.dashboard'))
        flash('Invalid email or password.', 'error')
    return render_template('login_premium.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('trips.dashboard'))
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')
        
        if not email or not password:
            flash('Email and password are required.', 'error')
            return render_template('register.html')
        
        if password != confirm:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
            return render_template('register.html')
        
        try:
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
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('Error during registration. Please try again.', 'error')
            return render_template('register.html')
    return render_template('register.html')

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
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
            return redirect(url_for('auth.forgot_password'))
        elif step == 2:
            email = session.get('reset_email')
            password = request.form.get('password', '')
            confirm = request.form.get('confirm_password', '')
            if password != confirm:
                flash('Passwords do not match.', 'error')
                return redirect(url_for('auth.forgot_password'))
            user = User.query.filter_by(email=email).first()
            if user:
                try:
                    user.password = generate_password_hash(password)
                    db.session.commit()
                    session.pop('reset_email', None)
                    session.pop('reset_step', None)
                    flash('Password reset successful! Please log in.', 'success')
                    return redirect(url_for('auth.login'))
                except Exception as e:
                    db.session.rollback()
                    flash('Error resetting password. Please try again.', 'error')
    return render_template('forgot_password.html', step=step)

@auth_bp.route('/google-login', methods=['POST'])
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
    
    try:
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
        return jsonify({'success': True, 'redirect': url_for('trips.dashboard')})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Login failed'}), 500

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        try:
            current_user.first_name = request.form.get('first_name', '').strip()
            current_user.last_name = request.form.get('last_name', '').strip()
            current_user.phone = request.form.get('phone', '').strip()
            current_user.city = request.form.get('city', '').strip()
            current_user.country = request.form.get('country', '').strip()
            current_user.language = request.form.get('language', 'en')
            db.session.commit()
            flash('Profile updated!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error updating profile. Please try again.', 'error')
        return redirect(url_for('auth.profile'))
    return render_template('profile.html')

@auth_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    current_pw = request.form.get('current_password', '')
    new_pw = request.form.get('new_password', '')
    confirm_pw = request.form.get('confirm_password', '')
    
    if not check_password_hash(current_user.password, current_pw):
        flash('Current password is incorrect.', 'error')
        return redirect(url_for('auth.profile'))
    
    if new_pw != confirm_pw:
        flash('New passwords do not match.', 'error')
        return redirect(url_for('auth.profile'))
    
    try:
        current_user.password = generate_password_hash(new_pw)
        db.session.commit()
        flash('Password changed successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error changing password. Please try again.', 'error')
    
    return redirect(url_for('auth.profile'))
