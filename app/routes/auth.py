# app/routes/auth.py
from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash
from app.models import User, ActivityLog
from app import db, login_manager
from app.utils.logs import log_action

auth_bp = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_bp.route('/')
def home():
    if current_user.is_authenticated:
        if current_user.user_role == 'admin':
            return redirect(url_for('admin.dashboard'))
        elif current_user.user_role == 'donor':
            return redirect(url_for('donor.dashboard'))
        elif current_user.user_role == 'recipient':
            return redirect(url_for('recipient.dashboard'))
    return render_template('home.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.home'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Please fill in all fields', 'danger')
            return redirect(url_for('auth.home') + '#login-section')

        user = User.query.filter_by(username=username).first()

        #  Plaintext password check
        if user and user.password_hash == password:
            login_user(user)
            log_action(user.user_id, f"Logged in as {user.user_role}")
            flash('Login successful!', 'success')

            # Redirect based on user role
            if user.user_role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif user.user_role == 'donor':
                return redirect(url_for('donor.dashboard'))
            elif user.user_role == 'recipient':
                return redirect(url_for('recipient.dashboard'))
            else:
                return redirect(url_for('auth.home'))
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.home') + '#login-section')

    return redirect(url_for('auth.home') + '#login-section')

@auth_bp.route('/logout')
@login_required
def logout():
    log_action(current_user.user_id, "Logged out")
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.home'))


# For About Us page
@auth_bp.route('/about')
def about():
    return render_template('about.html')

# For Contact Us page
@auth_bp.route('/contact')
def contact():
    return render_template('contactus.html')

# For handling form submission (Contact Us form)
@auth_bp.route('/submit_contact_form', methods=['POST'])
def submit_contact_form():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    # Save to database or send via email
    flash('Your message has been sent successfully!', 'success')

    return redirect(url_for('auth.contact'))
