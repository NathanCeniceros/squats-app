import os
from datetime import datetime, timedelta

LOG_FILE = "squats_log.txt"
TRACKER_FILE = "squats_tracker.txt"
time_slots = ["8:00 AM", "8:45 AM", "9:30 AM", "10:15 AM", "11:00 AM", "11:45 AM", 
              "12:30 PM", "1:15 PM", "2:00 PM", "2:45 PM", "3:30 PM", "4:15 PM", "5:00 PM"]
tracker_data = {}

def initialize_tracker():
    global tracker_data
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    tracker_data = {
        (start_of_week + timedelta(days=i)).strftime("%Y-%m-%d"): [False] * len(time_slots)
        for i in range(7)
    }
def log_message(message):
    """
    Logs a message to the log file with a timestamp.
    """
    with open(LOG_FILE, "a") as log:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log.write(f"{timestamp}: {message}\n")

# Modify mark_as_completed to use log_message

def update_progress(date, slot_index):
    """
    Updates the progress for a specific time slot on the given date.
    """
    if date in tracker_data and 0 <= slot_index < len(time_slots):
        tracker_data[date][slot_index] = True  # Mark the slot as completed
        save_tracker()  # Save progress to the tracker file

def mark_as_completed(date, slot_index):
    """
    Toggles the completion status of a specific time slot for the given date.
    """
    if date in tracker_data and 0 <= slot_index < len(time_slots):
        if tracker_data[date][slot_index]:  # If marked completed
            tracker_data[date][slot_index] = False  # Undo completion
            log_message(f"User undid squats for {time_slots[slot_index]}.")
        else:  # Mark as completed
            tracker_data[date][slot_index] = True
            log_message(f"User completed squats for {time_slots[slot_index]}.")
        
        # Save the updated tracker data to the file
        save_tracker()

def save_tracker():
    with open(TRACKER_FILE, "w") as f:
        for date, progress in tracker_data.items():
            progress_str = ",".join(map(str, progress))
            f.write(f"{date}:{progress_str}\n")

def load_tracker():
    global tracker_data
    try:
        with open(TRACKER_FILE, "r") as f:
            for line in f:
                date, progress_str = line.strip().split(":")
                tracker_data[date] = list(map(lambda x: x == "True", progress_str.split(",")))
    except FileNotFoundError:
        save_tracker()

initialize_tracker()
load_tracker()
