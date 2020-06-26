from helpers import *

def serialize_sleep(sleep_type):
    current_time = get_time_string()
    record = ";".join([current_time, sleep_type])
    write_to_csv("sleep", record)
    return 0, [current_time, sleep_type]