from datetime import datetime


def obtain_time():
    now = datetime.now()
    year = str(now.year)
    month = str(now.month) if len(str(now.month)) == 2 else '0' + str(now.month)
    day = str(now.day) if len(str(now.day)) == 2 else '0' + str(now.day)
    hour = str(now.hour) if len(str(now.hour)) == 2 else '0' + str(now.hour)
    minute = str(now.minute) if len(str(now.minute)) == 2 else '0' + str(now.minute)
    current_time = year + month + day + hour + minute
    return current_time
