# app/tests/test_sessions.py

import uuid
from datetime import datetime, timedelta
from app.models.user import User
from app.models.session import Session

def test_create_session(db_session):
    unique_email = f"{uuid.uuid4()}@example.com"
    user = User(username="User Session", email=unique_email, password="123456")
    db_session.add(user)
    db_session.commit()

    start_time = datetime.now()
    end_time = start_time + timedelta(hours=1)
    duration = int((end_time - start_time).total_seconds() / 60)

    sessao = Session(user_id=user.id, start_time=start_time, end_time=end_time, duration=duration)
    db_session.add(sessao)
    db_session.commit()

    db_sessao = db_session.query(Session).filter_by(user_id=user.id).first()
    assert db_sessao is not None
    assert db_sessao.user_id == user.id
    assert db_sessao.start_time == start_time
    assert db_sessao.end_time == end_time
    assert db_sessao.duration == duration
