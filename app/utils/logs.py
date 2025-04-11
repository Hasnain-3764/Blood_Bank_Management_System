from app.models import ActivityLog
from app import db

def log_action(user_id, action):
    log = ActivityLog(user_id=user_id, action=action)
    db.session.add(log)
    db.session.commit()
