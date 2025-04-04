"""
Utility functions for the squats app.
"""

import time

LOG_FILE = "squats_log.txt"

def log_message(message):
    """
    Logs a message to the log file with a timestamp.
    """
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(f"{time.ctime()}: {message}\n")

def read_file(file_path):
    """
    Reads the content of a file.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()
