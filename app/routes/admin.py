from app.utils.roles import role_required
from flask import Blueprint, render_template, render_template_string
from flask import request, abort, redirect, flash, url_for, Response
from werkzeug.security import generate_password_hash
from flask_login import login_required, current_user
from app.models import User, Donor, Recipient, BloodUnit, BloodRequest, BloodBank, Feedback
from app import db
from app.models import ActivityLog
from app.utils.logs import log_action
from sqlalchemy import text

# from weasyprint import HTML
from io import BytesIO
from sqlalchemy import func
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/dashboard')
@login_required
@role_required('admin')
def dashboard():
    total_donors = Donor.query.count()
    total_recipients = Recipient.query.count()
    total_units = BloodUnit.query.count()
    total_requests = BloodRequest.query.count()

    # NEW: fetch recent activity logs
    logs = db.session.query(ActivityLog, User).join(User).order_by(ActivityLog.timestamp.desc()).limit(5).all()


    return render_template('admin_dashboard.html',
                           user=current_user,
                           total_donors=total_donors,
                           total_recipients=total_recipients,
                           total_units=total_units,
                           total_requests=total_requests,
                           logs=logs)


@admin_bp.route('/donations')
@login_required
@role_required('admin')
def donations():
    units = BloodUnit.query.order_by(BloodUnit.donated_date.desc()).all()
    return render_template('admin_donations.html', units=units)


@admin_bp.route('/requests')
@role_required('admin')
@login_required
def requests():
    requests = BloodRequest.query.order_by(BloodRequest.request_date.desc()).all()
    return render_template('admin_requests.html', requests=requests)



# View all users
@admin_bp.route('/users')
@login_required
@role_required('admin')
def users():
    donors = User.query.filter_by(user_role='donor').all()
    recipients = User.query.filter_by(user_role='recipient').all()
    return render_template('admin_users.html', donors=donors, recipients=recipients)


# Edit user (only donor or recipient)
@admin_bp.route('/user/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_user(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        user.name = request.form['name']
        user.phone_no = request.form['phone']
        user.location = request.form['location']
        if request.form['password']:
            user.password_hash = generate_password_hash(request.form['password'])

        user.gender = request.form['gender']
        user.dob = request.form['dob']
        db.session.commit()
        log_action(current_user.user_id, f"Edited user ID #{user_id}")

        flash("User updated successfully", "success")
        return redirect(url_for('admin.users'))

    return render_template('admin_edit_user.html', user=user)


# Delete user
@admin_bp.route('/user/<int:user_id>/delete', methods=['POST'])
@login_required
@role_required('admin')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    log_action(current_user.user_id, f"Deleted user ID #{user_id}")
    flash("User deleted successfully", "info")
    return redirect(url_for('admin.users'))


from app.models import Donor, Recipient

@admin_bp.route('/user/add', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        phone = request.form['phone']
        location = request.form['location']
        password = generate_password_hash(request.form['password'])
        gender = request.form['gender']
        dob = request.form['dob']
        role = request.form['role']
        blood_type = request.form['blood_type']

        # Create basic user record
        new_user = User(
            username=username,
            password_hash=password,
            user_role=role,
            name=name,
            phone_no=phone,
            location=location,
            gender=gender,
            dob=dob
        )
        db.session.add(new_user)
        db.session.commit()

        # Add to donor or recipient table
        if role == 'donor':
            donor = Donor(
                user_id=new_user.user_id,
                blood_type=blood_type
            )
            db.session.add(donor)
        elif role == 'recipient':
            recipient = Recipient(
                user_id=new_user.user_id,
                blood_type=blood_type
            )
            db.session.add(recipient)

        db.session.commit()
        log_action(current_user.user_id, f"Added new {role} user '{username}'")
        flash("User added successfully!", "success")
        return redirect(url_for('admin.users'))

    return render_template('admin_add_user.html')


# View blood units with edit/delete options
@admin_bp.route('/units')
@login_required
@role_required('admin')
def units():
    units = BloodUnit.query.order_by(BloodUnit.donated_date.desc()).all()
    return render_template('admin_units.html', units=units)


# Edit a unit
@admin_bp.route('/unit/<int:unit_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_unit(unit_id):
    unit = BloodUnit.query.get_or_404(unit_id)
    banks = BloodBank.query.all()

    if request.method == 'POST':
        unit.blood_bank_id = request.form['blood_bank_id']
        unit.donated_date = request.form['donated_date']
        unit.status = request.form['status']
        db.session.commit()
        log_action(current_user.user_id, f"Edited blood unit ID #{unit.unit_id}")
        flash("Blood unit updated.", "success")
        return redirect(url_for('admin.units'))

    return render_template('admin_edit_unit.html', unit=unit, banks=banks)


# Delete a unit
@admin_bp.route('/unit/<int:unit_id>/delete', methods=['POST'])
@login_required
@role_required('admin')
def delete_unit(unit_id):
    unit = BloodUnit.query.get_or_404(unit_id)
    db.session.delete(unit)
    db.session.commit()
    log_action(current_user.user_id, f"Edited blood unit ID #{unit.unit_id}")
    flash("Blood unit deleted.", "info")
    log_action(current_user.user_id, f"Deleted blood unit #{unit.unit_id}")
    return redirect(url_for('admin.units'))


# View all requests with edit/delete options
@admin_bp.route('/requests/manage')
@login_required
@role_required('admin')
def manage_requests():
    requests = BloodRequest.query.order_by(BloodRequest.request_date.desc()).all()
    return render_template('admin_manage_requests.html', requests=requests)


# Edit request status
@admin_bp.route('/request/<int:request_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_request(request_id):
    request_obj = BloodRequest.query.get_or_404(request_id)

    if request.method == 'POST':
        request_obj.status = request.form['status']
        db.session.commit()
        log_action(current_user.user_id, f"Updated request ID #{request_id} to status '{request_obj.status}'")

        flash("Request status updated.", "success")
        return redirect(url_for('admin.manage_requests'))

    return render_template('admin_edit_request.html', request_obj=request_obj)


# Delete a request
@admin_bp.route('/request/<int:request_id>/delete', methods=['POST'])
@login_required
@role_required('admin')
def delete_request(request_id):
    request_obj = BloodRequest.query.get_or_404(request_id)
    db.session.delete(request_obj)
    db.session.commit()
    log_action(current_user.user_id, f"Deleted blood request ID #{request_id}")

    flash("Request deleted.", "info")
    return redirect(url_for('admin.manage_requests'))


@admin_bp.route('/feedback')
@login_required
@role_required('admin')
def feedback():
    feedbacks = db.session.query(Feedback, User).join(User).order_by(Feedback.submission_date.desc()).all()
    return render_template('admin_feedback.html', feedbacks=feedbacks)

@admin_bp.route('/logs')
@login_required
@role_required('admin')
def logs():
    logs = db.session.query(ActivityLog, User).join(User).order_by(ActivityLog.timestamp.desc()).all()
    return render_template('admin_logs.html', logs=logs)


# @admin_bp.route('/report/donations/pdf')
# @login_required
# @role_required('admin')
# def export_donations_pdf():
#     units = BloodUnit.query.all()

#     html_template = render_template('pdf_donations_report.html', units=units)
#     pdf_file = BytesIO()
#     HTML(string=html_template).write_pdf(pdf_file)
#     pdf_file.seek(0)

#     return Response(pdf_file, mimetype='application/pdf',
#                     headers={'Content-Disposition': 'attachment; filename=blood_donations_report.pdf'})


@admin_bp.route('/charts')
@login_required
@role_required('admin')
def charts():
    # Blood type counts
    type_counts = db.session.query(
        BloodUnit.blood_type,
        func.count(BloodUnit.unit_id)
    ).group_by(BloodUnit.blood_type).all()

    # Status counts
    status_counts = db.session.query(
        BloodUnit.status,
        func.count(BloodUnit.unit_id)
    ).group_by(BloodUnit.status).all()

    # Monthly donations (last 6 months)
    six_months_ago = datetime.today().replace(day=1) - timedelta(days=180)
    monthly_donations = db.session.query(
        func.date_format(BloodUnit.donated_date, "%Y-%m"),
        func.count(BloodUnit.unit_id)
    ).filter(BloodUnit.donated_date >= six_months_ago).group_by(
        func.date_format(BloodUnit.donated_date, "%Y-%m")
    ).all()

    # Blood bank unit distribution
    bank_distribution = db.session.query(
        BloodBank.name,
        func.count(BloodUnit.unit_id)
    ).join(BloodUnit, BloodUnit.blood_bank_id == BloodBank.bank_id
    ).group_by(BloodBank.name).all()

    # Request status pie
    request_status = db.session.query(
        BloodRequest.status,
        func.count(BloodRequest.request_id)
    ).group_by(BloodRequest.status).all()

    return render_template('admin_charts.html',
                           type_counts=type_counts,
                           status_counts=status_counts,
                           monthly_donations=monthly_donations,
                           bank_distribution=bank_distribution,
                           request_status=request_status)


from sqlalchemy import text

@admin_bp.route('/queries', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def queries():
    queries_list = [
        {
            'id': 1,
            'query': text("""
                SELECT br.request_id,
                       br.recipient_id,
                       br.blood_type AS requested_type,
                       br.quantity AS requested_quantity,
                       bu.unit_id,
                       bu.donated_date,
                       bu.expiry
                FROM blood_requests br
                JOIN blood_units bu ON br.blood_type = bu.blood_type
                WHERE br.status = 'pending' 
                  AND bu.status = 'available';
            """),
            'description': "List of pending blood requests with available blood units."
        },
        {
            'id': 2,
            'query': text("""
                SELECT unit_id,
                       blood_type,
                       donated_date,
                       expiry,
                       status
                FROM blood_units
                WHERE expiry < CURRENT_DATE
                  AND status IN ('expired');
            """),
            'description': "List of expired blood units."
        },
        {
            'id': 3,
            'query': text("""
                SELECT b.name AS blood_bank,
                       bu.blood_type,
                       COUNT(bu.unit_id) AS available_units
                FROM blood_units bu
                JOIN blood_banks b ON bu.blood_bank_id = b.bank_id
                WHERE bu.status = 'available'
                GROUP BY b.name, bu.blood_type
                HAVING COUNT(bu.unit_id) < 12;
            """),
            'description': "Blood banks with less than 10 available units."
        },
        {
            'id': 4,
            'query': text("""
                SELECT b.name AS blood_bank,
                       bu.blood_type,
                       COUNT(bu.unit_id) AS total_units
                FROM blood_units bu
                JOIN blood_banks b ON bu.blood_bank_id = b.bank_id
                GROUP BY b.name, bu.blood_type;
            """),
            'description': "Total blood units in each blood bank."
        },
        {
            'id': 5,
            'query': text("""
                SELECT ROUND(AVG(donation_count), 2) AS avg_donations_per_donor
                FROM (
                    SELECT d.donor_id, COUNT(bu.unit_id) AS donation_count
                    FROM donors d
                    LEFT JOIN blood_units bu ON d.donor_id = bu.donor_id
                    GROUP BY d.donor_id
                ) AS donor_donations;
            """),
            'description': "The average number of blood donations per donor.."
        }
    ]

    if request.method == 'POST':
        query_id = request.form.get('query_id')
        query = next((q for q in queries_list if q['id'] == int(query_id)), None)
        
        if query:
            # Execute the query and fetch the result
            result = db.session.execute(query['query']).fetchall()

            # Convert the result from SQLAlchemy Row to dictionary using _mapping
            result_dict = [dict(row._mapping) for row in result]  # Convert to dictionary
            return render_template('query_results.html', query=query, result=result_dict)
    
    return render_template('queries.html', queries=queries_list)
