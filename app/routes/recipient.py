from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Recipient, BloodRequest, Feedback
from datetime import date
from app.utils.roles import role_required
from app.utils.logs import log_action
from app.utils.compatibility import is_compatible
from app.models import Donor, User, Recipient, BloodRequest

recipient_bp = Blueprint('recipient', __name__, url_prefix='/recipient')


@recipient_bp.route('/dashboard')
@login_required
@role_required('recipient')
def dashboard():
    recipient = Recipient.query.filter_by(user_id=current_user.user_id).first()
    if not recipient:
        flash("No recipient record found for this user.", "danger")
        return redirect(url_for('auth.login'))

    requests = BloodRequest.query.filter_by(recipient_id=recipient.recipient_id).all()
    return render_template('recipient_dashboard.html', user=current_user, requests=requests)


@recipient_bp.route('/request', methods=['GET', 'POST'])
@login_required
@role_required('recipient')
def request_blood():
    recipient = Recipient.query.filter_by(user_id=current_user.user_id).first()
    if not recipient:
        flash("No recipient record found for this user.", "danger")
        return redirect(url_for('recipient.dashboard'))

    if request.method == 'POST':
        print("Form submitted!")  # For debug
        blood_type = request.form['blood_type']
        quantity = int(request.form['quantity'])
        request_date = date.today()

        # Check compatibility before submitting request
        available_blood_units = BloodUnit.query.filter_by(blood_type=blood_type, status='available').all()
        compatible = any(is_compatible(unit.blood_type, recipient.blood_type) for unit in available_blood_units)

        if not compatible:
            flash(f"Sorry, no compatible blood type available for {blood_type}!", "danger")
            return redirect(url_for('recipient.request_blood'))

        new_request = BloodRequest(
            recipient_id=recipient.recipient_id,
            blood_type=blood_type,
            quantity=quantity,
            request_date=request_date,
            status='pending'
        )

        db.session.add(new_request)
        db.session.commit()
        log_action(current_user.user_id, f"Requested {quantity} unit(s) of {blood_type} blood")
        flash("Blood request submitted successfully!", "success")
        return redirect(url_for('recipient.dashboard'))

    return render_template('request_blood.html', user=current_user)


@recipient_bp.route('/search-donors', methods=['GET', 'POST'])
@login_required
@role_required('recipient')
def search_donors():
    donors = []
    selected_blood = None
    selected_location = None

    if request.method == 'POST':
        selected_blood = request.form.get('blood_type')
        selected_location = request.form.get('location')

        query = db.session.query(Donor, User).join(User)

        if selected_blood:
            query = query.filter(Donor.blood_type == selected_blood)
        if selected_location:
            query = query.filter(User.location.ilike(f"%{selected_location}%"))

        donors = query.all()

    return render_template('search_donors.html', user=current_user, donors=donors,
                           selected_blood=selected_blood, selected_location=selected_location)


@recipient_bp.route('/profile', methods=['GET', 'POST'])
@login_required
@role_required('recipient')
def profile():
    recipient = Recipient.query.filter_by(user_id=current_user.user_id).first()
    user = current_user

    if request.method == 'POST':
        user.name = request.form.get('name')
        user.phone_no = request.form.get('phone_no')
        user.location = request.form.get('location')
        user.gender = request.form.get('gender')
        user.dob = request.form.get('dob')

        db.session.commit()
        flash("✅ Profile updated successfully!", "success")
        return redirect(url_for('recipient.profile'))

    return render_template('profile.html', user=user, recipient=recipient)



@recipient_bp.route('/feedback', methods=['GET', 'POST'])
@login_required
@role_required('recipient')
def feedback():
    if request.method == 'POST':
        comments = request.form.get('message')  # still using `message` from form
        rating = int(request.form.get('rating')) if request.form.get('rating') else None

        feedback = Feedback(user_id=current_user.user_id, comments=comments, rating=rating)
        db.session.add(feedback)
        db.session.commit()

        flash("✅ Thank you for your feedback!", "success")
        return redirect(url_for('recipient.dashboard'))

    return render_template('feedback.html', user=current_user)
