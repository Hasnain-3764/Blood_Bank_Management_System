from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
from flask_login import login_required, current_user
from app import db
from app.models import Donor, BloodUnit, MedicalHistory, BloodBank, Feedback
from datetime import date, timedelta
from app.utils.roles import role_required
from app.utils.logs import log_action
from weasyprint import HTML
from io import BytesIO
import os

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
    blood_banks = BloodBank.query.all()
    if not donor:
        flash("No donor record found for this user.", "danger")
        return redirect(url_for('donor.dashboard'))
    
    # Check if the donor is eligible
    last_donation = MedicalHistory.query.filter_by(user_id=current_user.user_id, donate_taken='donate').order_by(MedicalHistory.date1.desc()).first()
    next_eligible_date = None
    ineligible = last_donation and (date.today() - last_donation.date1) < timedelta(days=90)

    if last_donation:
        days_since = (date.today() - last_donation.date1).days
        if days_since < 90:
            ineligible = True
            next_eligible_date = last_donation.date1 + timedelta(days=90)

    if request.method == 'POST':
        if ineligible:
            flash("⛔ You’ve already donated recently. Please wait 90 days between donations.", "danger")
            return redirect(url_for('donor.donate'))

    if request.method == 'POST':
        # Proceed with donation if eligible
        blood_bank_id = request.form['blood_bank_id']
        donation_date = date.today()

        new_unit = BloodUnit(
            donor_id=donor.donor_id,
            blood_bank_id=blood_bank_id,
            blood_type=donor.blood_type,
            donated_date=donation_date,
            status='available'
        )
        db.session.add(new_unit)

        # Add to medical history
        donation_record = MedicalHistory(
            user_id=current_user.user_id,
            date1=donation_date,
            donate_taken='donate'
        )
        db.session.add(donation_record)
        db.session.commit()
        
        # Log the action
        log_action(current_user.user_id, f"Donated blood to bank ID {blood_bank_id}")
        
        flash("Donation recorded successfully!", "success")
        return redirect(url_for('donor.dashboard'))

    return render_template('donate.html', user=current_user, blood_banks=blood_banks, ineligible=ineligible, next_eligible_date=next_eligible_date)


@donor_bp.route('/history')
@login_required
@role_required('donor')
def history():
    donor = Donor.query.filter_by(user_id=current_user.user_id).first()

    if not donor:
        flash("Donor record not found.", "danger")
        return redirect(url_for('donor.dashboard'))

    donations = BloodUnit.query.filter_by(donor_id=donor.donor_id).order_by(BloodUnit.donated_date.desc()).all()
    return render_template('donor_history.html', user=current_user, donations=donations)



@donor_bp.route('/profile', methods=['GET', 'POST'])
@login_required
@role_required('donor')
def profile():
    donor = Donor.query.filter_by(user_id=current_user.user_id).first()
    user = current_user

    if request.method == 'POST':
        user.name = request.form.get('name')
        user.phone_no = request.form.get('phone_no')
        user.location = request.form.get('location')
        user.gender = request.form.get('gender')
        user.dob = request.form.get('dob')

        db.session.commit()
        flash("✅ Profile updated successfully!", "success")
        return redirect(url_for('donor.profile'))

    return render_template('donor_profile.html', user=user, donor=donor)



@donor_bp.route('/feedback', methods=['GET', 'POST'])
@login_required
@role_required('donor')
def feedback():
    if request.method == 'POST':
        comments = request.form.get('message')
        rating = int(request.form.get('rating')) if request.form.get('rating') else None

        feedback = Feedback(user_id=current_user.user_id, comments=comments, rating=rating)
        db.session.add(feedback)
        db.session.commit()

        flash("✅ Thank you for your feedback!", "success")
        return redirect(url_for('donor.dashboard'))

    return render_template('donor_feedback.html', user=current_user)



@donor_bp.route('/certificate/<int:unit_id>')
@login_required
@role_required('donor')
def certificate(unit_id):
    unit = BloodUnit.query.get_or_404(unit_id)
    donor = Donor.query.get(unit.donor_id)

    if donor.user_id != current_user.user_id:
        flash("⛔ Unauthorized access.", "danger")
        return redirect(url_for('donor.dashboard'))

    bank = BloodBank.query.get(unit.blood_bank_id)

    # 👇 Render HTML as string
    html = render_template('certificate_template.html', unit=unit, user=current_user, bank=bank)

    # 👇 Build absolute base path
    base_path = os.path.abspath("app/static")

    # 👇 Generate PDF with proper static path
    pdf = HTML(string=html, base_url=f"file://{base_path}").write_pdf()

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=donation_certificate_{unit_id}.pdf'
    return response
