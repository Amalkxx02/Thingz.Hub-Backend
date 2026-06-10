from datetime import datetime, timedelta, timezone


def get_current_utc_time() -> datetime:
    return datetime.now(timezone.utc)


def get_future_utc_time(days: float = 0, minutes: float = 0) -> datetime:
    return get_current_utc_time() + timedelta(days=days, minutes=minutes)


def add_time(dt: datetime, minutes: float = 0) -> datetime:
    return dt + timedelta(minutes=minutes)
