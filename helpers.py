from datetime import datetime, timedelta

TIMEFORMATTER = "%Y-%m-%d %H:%M:%S"

def write_to_csv(file, record):
    a_path = file + '.csv'
    with open(a_path, 'a+') as f:
        f.write(record)
        f.write("\n")
        f.close()

def get_time_string():
    current_time = datetime.now()
    return convert_to_time_string(current_time)

def convert_to_time_string(current_time):
    return datetime.strftime(current_time, TIMEFORMATTER)

def get_time_from_string(time):
    return datetime.strptime(time, TIMEFORMATTER)

def replace_h_m(dtime, h, m):
    return dtime.replace(hour=h, minute=m)
