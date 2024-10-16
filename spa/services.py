from django.utils import timezone


def get_next_minute_date(date_time_start_sent, now_time):
    if now_time > date_time_start_sent:
        new_time = now_time + timezone.timedelta(minutes=1)
    else:
        new_time = date_time_start_sent

    return new_time.replace(second=0, microsecond=0)


def get_next_hour_date(date_time_start_sent, now_time):
    # К дате/времени начала рассылки прибавляются недостающие дни
    # к текущей дате плюс один час на следующую рассылку
    if now_time > date_time_start_sent:
        next_date_time_diff = (
            now_time - date_time_start_sent
        ).total_seconds() // (60 * 60) + 1
        delta = timezone.timedelta(hours=next_date_time_diff)
        new_time = date_time_start_sent + delta
    else:
        new_time = date_time_start_sent

    return new_time.replace(second=0, microsecond=0)


def get_next_day_date(date_time_start_sent, now_time):
    # К дате/времени начала рассылки прибавляются недостающие дни
    # к текущей дате плюс один день на следующую рассылку
    if now_time > date_time_start_sent:
        next_date_time_diff = (now_time - date_time_start_sent).days + 1
        delta = timezone.timedelta(days=next_date_time_diff)
        new_time = date_time_start_sent + delta
    else:
        new_time = date_time_start_sent

    return new_time.replace(second=0, microsecond=0)


def get_next_week_date(date_time_start_sent, now_time):
    # К дате/времени начала рассылки прибавляются недостающие дни
    # к текущей дате плюс разница до следующей недели на следующую рассылку
    if now_time > date_time_start_sent:
        now_start_delta = (now_time - date_time_start_sent).days
        delta = now_start_delta + (7 - now_start_delta % 7)
        new_time = date_time_start_sent + timezone.timedelta(days=delta)
    else:
        new_time = date_time_start_sent

    return new_time.replace(second=0, microsecond=0)
