import time

LOG_FILE = "squats_log.txt"

def log_message(message):
    with open(LOG_FILE, "a") as log:
        log.write(f"{time.ctime()}: {message}\n")