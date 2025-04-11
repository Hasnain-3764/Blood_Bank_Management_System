from . import db
from flask_login import UserMixin
from datetime import date, timedelta
from sqlalchemy import Computed

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    user_role = db.Column(db.Enum('admin', 'donor', 'recipient'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    phone_no = db.Column(db.String(20))
    gender = db.Column(db.Enum('male', 'female', 'other'))
    dob = db.Column(db.Date)
    location = db.Column(db.String(255))

    def get_id(self):
        return str(self.user_id)


class BloodBank(db.Model):
    __tablename__ = 'blood_banks'
    bank_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255))
    contact = db.Column(db.String(20))
    storage_capacity = db.Column(db.Integer)


class Donor(db.Model):
    __tablename__ = 'donors'
    donor_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    blood_sugar = db.Column(db.Integer)
    blood_pressure_systolic = db.Column(db.Integer)
    blood_pressure_diastolic = db.Column(db.Integer)
    disease_history = db.Column(db.Text)
    medications = db.Column(db.Text)
    allergies = db.Column(db.Text)
    blood_type = db.Column(db.Enum('A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-'), nullable=False)


class Recipient(db.Model):
    __tablename__ = 'recipients'
    recipient_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    blood_sugar = db.Column(db.Integer)
    blood_pressure_systolic = db.Column(db.Integer)
    blood_pressure_diastolic = db.Column(db.Integer)
    disease_history = db.Column(db.Text)
    medications = db.Column(db.Text)
    allergies = db.Column(db.Text)
    blood_type = db.Column(db.Enum('A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-'), nullable=False)


class Admin(db.Model):
    __tablename__ = 'admins'
    admin_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    blood_bank_id = db.Column(db.Integer, db.ForeignKey('blood_banks.bank_id'), nullable=False)


class MedicalHistory(db.Model):
    __tablename__ = 'medical_history'
    medical_history_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    date1 = db.Column(db.Date)
    donate_taken = db.Column(db.Enum('donate', 'taken'))


# class BloodUnit(db.Model):
#     __tablename__ = 'blood_units'
#     unit_id = db.Column(db.Integer, primary_key=True)
#     donor_id = db.Column(db.Integer, db.ForeignKey('donors.donor_id'), nullable=False)
#     blood_bank_id = db.Column(db.Integer, db.ForeignKey('blood_banks.bank_id'), nullable=False)
#     blood_type = db.Column(db.Enum('A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-'), nullable=False)
#     donated_date = db.Column(db.Date)
#     expiry = db.Column(db.Date)
#     status = db.Column(db.Enum('available', 'assigned', 'transfused', 'expired', 'discarded'), default='available')


class BloodUnit(db.Model):
    __tablename__ = 'blood_units'
    unit_id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('donors.donor_id'), nullable=False)
    blood_bank_id = db.Column(db.Integer, db.ForeignKey('blood_banks.bank_id'), nullable=False)
    blood_type = db.Column(db.Enum('A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-'), nullable=False)
    donated_date = db.Column(db.Date)
    expiry = db.Column(db.Date, Computed("DATE_ADD(donated_date, INTERVAL 42 DAY)"))
    status = db.Column(db.Enum('available', 'assigned', 'transfused', 'expired', 'discarded'), default='available')


class BloodRequest(db.Model):
    __tablename__ = 'blood_requests'
    request_id = db.Column(db.Integer, primary_key=True)
    recipient_id = db.Column(db.Integer, db.ForeignKey('recipients.recipient_id'), nullable=False)
    blood_type = db.Column(db.Enum('A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+','AB-'), nullable=False)
    quantity = db.Column(db.Integer)
    request_date = db.Column(db.Date)
    status = db.Column(db.Enum('pending', 'fulfilled', 'cancelled'))


class RequestFulfillment(db.Model):
    __tablename__ = 'request_fulfillment'
    fulfillment_id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('blood_requests.request_id'), nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey('blood_units.unit_id'), nullable=False)
    fulfillment_date = db.Column(db.Date)


class Feedback(db.Model):
    __tablename__ = 'feedback_and_reviews'
    feedback_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text)
    submission_date = db.Column(db.Date)

class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    action = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.now())
