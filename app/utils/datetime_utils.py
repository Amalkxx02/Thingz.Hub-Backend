from datetime import datetime, timedelta, timezone

def get_current_utc_time():
    return datetime.now(timezone.utc)

def get_future_utc_time(days: float = 0, minutes: float = 0):
    return datetime.now(timezone.utc) + timedelta(days=days, minutes=minutes)