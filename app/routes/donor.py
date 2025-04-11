from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Donor, BloodUnit, MedicalHistory, BloodBank
from datetime import date, timedelta
from app.utils.roles import role_required
from app.utils.logs import log_action

donor_bp = Blueprint('donor', __name__, url_prefix='/donor')

@donor_bp.route('/dashboard')
@login_required
@role_required('donor')
def dashboard():
    return render_template('donor_dashboard.html', user=current_user)

@donor_bp.route('/donate', methods=['GET', 'POST'])
@login_required
@role_required('donor')
def donate():
    donor = Donor.query.filter_by(user_id=current_user.user_id).first()
    if not donor:
        flash("No donor record found for this user.", "danger")
        return redirect(url_for('donor.dashboard'))

    blood_banks = BloodBank.query.all()

    if request.method == 'POST':
        blood_bank_id = request.form['blood_bank_id']
        donation_date = date.today()
        # expiry_date = donation_date + timedelta(days=42)

        # # Add to blood_units
        # new_unit = BloodUnit(
        #     donor_id=donor.donor_id,
        #     blood_bank_id=blood_bank_id,
        #     blood_type=donor.blood_type,
        #     donated_date=donation_date,
        #     expiry=expiry_date,
        #     status='available'
        # )

        new_unit = BloodUnit(
            donor_id=donor.donor_id,
            blood_bank_id=blood_bank_id,
            blood_type=donor.blood_type,
            donated_date=donation_date,
            status='available'
        )
        db.session.add(new_unit)

        # Add to medical_history
        donation_record = MedicalHistory(
            user_id=current_user.user_id,
            date1=donation_date,
            donate_taken='donate'
        )
        db.session.add(donation_record)

        db.session.commit()
        log_action(current_user.user_id, f"Donated blood to bank ID {blood_bank_id}")
        flash("Donation recorded successfully!", "success")
        return redirect(url_for('donor.dashboard'))

    return render_template('donate.html', user=current_user, blood_banks=blood_banks)
