from helpers import *

def serialize_sleep(sleep_type):
    utc_time = datetime.utcnow()
    record = ";".join([convert_to_time_string(utc_time), sleep_type])
    write_to_csv("sleep", record)
    current_time = datetime.now()
    return 0, [current_time, sleep_type]

def serialize_event(intensity):
    utc_time = datetime.utcnow()
    record = ";".join([convert_to_time_string(utc_time), intensity])
    write_to_csv("event", record)
    current_time = datetime.now()
    return intensity, [current_time, intensity]
