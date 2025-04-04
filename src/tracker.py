import os
from datetime import datetime, timedelta

# Constants
LOG_FILE = "squats_log.txt"
TRACKER_FILE = "squats_tracker.txt"
time_slots = [
    "8:00 AM", "8:45 AM", "9:30 AM", "10:15 AM", "11:00 AM", "11:45 AM",
    "12:30 PM", "1:15 PM", "2:00 PM", "2:45 PM", "3:30 PM", "4:15 PM", "5:00 PM"
]
tracker_data = {}

# Function to initialize tracker
def initialize_tracker():
    global tracker_data
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    tracker_data = {
        (start_of_week + timedelta(days=i)).strftime("%Y-%m-%d"): [False] * len(time_slots)
        for i in range(7)
    }
    print("Initialized tracker data:", tracker_data)

# Function to log messages to a file
def log_message(message):
    """
    Logs a message to the log file with a timestamp.
    """
    try:
        with open(LOG_FILE, "a") as log:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log.write(f"{timestamp}: {message}\n")
        print(f"Log message written: {message}")
    except Exception as e:
        print(f"Error writing to log file: {e}")

# Function to update progress for a specific time slot
def update_progress(date, slot_index):
    """
    Updates the progress for a specific time slot on the given date.
    """
    if date in tracker_data and 0 <= slot_index < len(time_slots):
        tracker_data[date][slot_index] = True  # Mark the slot as completed
        print(f"Updated progress for {date}, slot {slot_index}: {tracker_data[date]}")
        save_tracker()  # Save progress to the tracker file

# Function to toggle completion status for a time slot
def mark_as_completed(date, slot_index):
    """
    Toggles the completion status of a specific time slot for the given date.
    """
    print(f"Before modification - Date: {date}, Slot index: {slot_index}")
    print(f"Tracker Data: {tracker_data}")
    
    if date in tracker_data and 0 <= slot_index < len(time_slots):
        if tracker_data[date][slot_index]:  # Undo completion
            tracker_data[date][slot_index] = False
            log_message(f"User undid squats for {time_slots[slot_index]}.")
        else:  # Mark as completed
            tracker_data[date][slot_index] = True
            log_message(f"User completed squats for {time_slots[slot_index]}.")
        
        save_tracker()  # Save changes to the tracker file
    
    print(f"After modification - Tracker Data: {tracker_data}")

# Function to save tracker data to a file
def save_tracker():
    """
    Saves the tracker data to a file for persistence.
    """
    try:
        with open(TRACKER_FILE, "w") as f:
            for date, progress in tracker_data.items():
                progress_str = ",".join(map(str, progress))
                f.write(f"{date}:{progress_str}\n")
        print(f"Tracker data saved to file: {TRACKER_FILE}")
    except Exception as e:
        print(f"Error saving tracker data: {e}")

# Function to load tracker data from a file
def load_tracker():
    """
    Loads tracker data from a file for persistence.
    """
    global tracker_data
    try:
        with open(TRACKER_FILE, "r") as f:
            for line in f:
                date, progress_str = line.strip().split(":")
                tracker_data[date] = list(map(lambda x: x == "True", progress_str.split(",")))
        print(f"Tracker data loaded from file: {tracker_data}")
    except FileNotFoundError:
        print("Tracker file not found, initializing and saving new tracker data.")
        save_tracker()
    except Exception as e:
        print(f"Error loading tracker data: {e}")

# Initialize and load tracker data at startup
initialize_tracker()
load_tracker()