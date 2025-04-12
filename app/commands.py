from flask import current_app
from app import db
from app.models import BloodUnit
from datetime import date

def expire_old_units():
    units = BloodUnit.query.filter(BloodUnit.expiry < date.today(), BloodUnit.status != 'expired').all()
    for unit in units:
        unit.status = 'expired'
    db.session.commit()
    print(f"{len(units)} blood units marked as expired.")
