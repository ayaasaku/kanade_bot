# Format time in Dd Hh Mm Ss format
async def format_time(seconds: int):
    days = int(seconds // 86400)
    hours = int(seconds // 3600 % 24)
    minutes = int(seconds // 60 % 60)
    seconds = int(seconds % 60)
    output = f"{days}d {hours}h {minutes}m {seconds}s"
    return output

# Format date in YYYY-MM-DD HH:MM:SS UTC format
async def format_date_jp(seconds: int):
    from datetime import datetime, timedelta
    date = datetime.fromtimestamp(seconds / 1000)
    date = date-timedelta(hours=-1)
    date = date.strftime("%Y-%m-%d %H:%M:%S")
    return date

async def format_date(seconds: int):
    from datetime import datetime, timedelta
    date = datetime.fromtimestamp(seconds / 1000)
    date = date-timedelta(hours=0)
    date = date.strftime("%Y-%m-%d %H:%M:%S")
    return date

async def format_creation_date(seconds: int):
    from datetime import datetime, timedelta
    datetime.fromtimestamp(seconds)
    date = date-timedelta(hours=-1)
    date = date.strftime("%A, %B %d, %Y %I:%M:%S")
    return date
    

async def format_progress(end_time, start_time, current_time):
    event_length = end_time - start_time
    time_left = end_time - current_time
    event_prog = round((((event_length - time_left) / event_length) * 100), 2)
    return f"{event_prog}%"


