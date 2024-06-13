from datetime import datetime, timedelta, timezone


def format_timestamp(datetime_str):
    dt_part = datetime.strptime(datetime_str[:19], "%Y-%m-%dT%H:%M:%S")

    # Parse the timezone part
    tz_sign = datetime_str[19]
    tz_hours = int(datetime_str[20:22])
    tz_minutes = int(datetime_str[23:])

    # Calculate the timezone offset
    tz_offset = timedelta(hours=tz_hours, minutes=tz_minutes)
    if tz_sign == '-':
        tz_offset = -tz_offset

    # Add the timezone info to the datetime object
    dt_with_tz = dt_part.replace(tzinfo=timezone(tz_offset))

    return dt_with_tz
