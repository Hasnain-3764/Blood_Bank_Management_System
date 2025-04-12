from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Recipient, BloodRequest
from datetime import date
from app.utils.roles import role_required
from app.utils.logs import log_action
from app.utils.compatibility import is_compatible

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
