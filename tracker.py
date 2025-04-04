import os

LOG_FILE = os.path.join(os.getcwd(), "squats_log.txt")
TRACKER_FILE = os.path.join(os.getcwd(), "squats_tracker.txt")

tracker_data = {}

def initialize_tracker():
    global tracker_data
    # Initialize tracker data...

def save_tracker():
    # Save tracker data to a file...

def load_tracker():
    # Load tracker data from a file...

def update_progress(date, slot_index):
    tracker_data[date][slot_index] = True
    save_tracker()
