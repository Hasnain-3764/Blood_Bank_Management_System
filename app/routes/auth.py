from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash
from app.models import User
from app import db, login_manager
from app.models import ActivityLog
from app.utils.logs import log_action

auth_bp = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and user.password_hash == password:
            login_user(user)
            log_action(user.user_id, f"Logged in as {user.user_role}")
            flash('Login successful!', 'success')

            # Role-based redirect
            if user.user_role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif user.user_role == 'donor':
                return redirect(url_for('donor.dashboard'))
            elif user.user_role == 'recipient':
                return redirect(url_for('recipient.dashboard'))
            else:
                return redirect(url_for('auth.login'))  # fallback
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    log_action(current_user.user_id, "Logged out")
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
