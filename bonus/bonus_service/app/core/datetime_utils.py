from datetime import datetime

import holidays


def is_weekend_or_holiday(dt: datetime) -> bool:
    return dt.weekday() >= 5 or dt.date() in holidays.RU()
