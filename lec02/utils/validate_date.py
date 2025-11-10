from datetime import datetime


def valid_date(date_str: str) -> datetime.date:
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        if date > datetime.now().date():
            raise ValueError("Date cannot be in future")
        return date
    except ValueError:
        raise ValueError("Date %s is not valid", date_str)
