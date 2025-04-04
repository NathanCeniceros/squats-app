import os
import json
from datetime import datetime, timedelta

# Constants
TRACKER_FILE = "squats_tracker.json"
LOG_FILE = "squats_log.txt"  # Add this constant to define the log file path
time_slots = [
    "8:00 AM", "8:45 AM", "9:30 AM", "10:15 AM", "11:00 AM", "11:45 AM",
    "12:30 PM", "1:15 PM", "2:00 PM", "2:45 PM", "3:30 PM", "4:15 PM", "5:00 PM"
]
tracker_data = {}

# Function to initialize tracker
def initialize_tracker(start_date=None):
    """
    Initializes the tracker data for the current week or a given start_date.
    """
    global tracker_data
    if start_date is None:
        today = datetime.now().date()
        start_date = today - timedelta(days=today.weekday())
    else:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()

    tracker_data = {
        (start_date + timedelta(days=i)).strftime("%Y-%m-%d"): [False] * len(time_slots)
        for i in range(7)
    }
    log_message(f"Initialized tracker data starting from {start_date}.")
    print(f"Initialized tracker data starting from {start_date}: {tracker_data}")

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
    if date not in tracker_data:
        print(f"Error: Date {date} is not in the tracker data.")
        return
    if not (0 <= slot_index < len(time_slots)):
        print(f"Error: Slot index {slot_index} is out of range.")
        return

    tracker_data[date][slot_index] = True  # Mark the slot as completed
    log_message(f"Progress updated for {date}, slot {slot_index}.")
    save_tracker()

# Function to toggle completion status for a time slot
def mark_as_completed(date, slot_index):
    """
    Toggles the completion status of a specific time slot for the given date.
    """
    global tracker_data
    if date not in tracker_data:
        print(f"Date {date} not found in tracker data. Initializing data for this date.")
        tracker_data[date] = [False] * len(time_slots)  # Initialize data for the date

    if not (0 <= slot_index < len(time_slots)):
        print(f"Error: Slot index {slot_index} is out of range.")
        return

    print(f"Before modification - Date: {date}, Slot index: {slot_index}")
    print(f"Tracker Data: {tracker_data}")

    tracker_data[date][slot_index] = not tracker_data[date][slot_index]  # Toggle completion status
    action = "completed" if tracker_data[date][slot_index] else "undid"
    log_message(f"User {action} squats for {time_slots[slot_index]} on {date}.")

    save_tracker()  # Save changes to the tracker file

    print(f"After modification - Tracker Data: {tracker_data}")

# Function to save tracker data to a JSON file
def save_tracker():
    """
    Saves the tracker data to a JSON file for persistence.
    """
    try:
        with open(TRACKER_FILE, "w") as f:
            json.dump(tracker_data, f, indent=4)
        print(f"Tracker data saved to file: {TRACKER_FILE}")
    except PermissionError:
        print(f"Error: Permission denied when trying to save to {TRACKER_FILE}.")
    except Exception as e:
        print(f"Error saving tracker data: {e}")

# Function to load tracker data from a JSON file
def load_tracker():
    """
    Loads tracker data from a JSON file for persistence.
    """
    global tracker_data
    try:
        if os.path.exists(TRACKER_FILE):
            with open(TRACKER_FILE, "r") as f:
                tracker_data = json.load(f)
            print(f"Tracker data loaded from file: {tracker_data}")
        else:
            print("Tracker file not found, initializing and saving new tracker data.")
            initialize_tracker()
            save_tracker()
    except json.JSONDecodeError:
        print("Error: Tracker file is corrupted. Reinitializing tracker data.")
        initialize_tracker()
        save_tracker()
    except Exception as e:
        print(f"Error loading tracker data: {e}")
        initialize_tracker()  # Fallback to reinitialize tracker data

# Function to reset tracker data for a new week
def reset_weekly_data(start_date=None):
    """
    Resets the tracker data for a new week starting from the given start_date.
    If no start_date is provided, it defaults to the current week.
    """
    global tracker_data
    try:
        if start_date is None:
            start_date = datetime.now().date() - timedelta(days=datetime.now().date().weekday())
        else:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()

        tracker_data = {
            (start_date + timedelta(days=i)).strftime("%Y-%m-%d"): [False] * len(time_slots)
            for i in range(7)
        }
        log_message(f"Tracker data reset for the week starting {start_date}.")
        save_tracker()
        print(f"Tracker data reset for the week starting {start_date}.")
    except ValueError:
        print(f"Error: Invalid start_date format '{start_date}'. Expected format: YYYY-MM-DD.")

def print_tracker_data():
    """
    Prints the current tracker data for debugging purposes.
    """
    print("Current Tracker Data:")
    for date, slots in tracker_data.items():
        print(f"{date}: {slots}")

# Initialize and load tracker data at startup
initialize_tracker()
load_tracker()