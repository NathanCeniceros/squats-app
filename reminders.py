import threading
from tracker import update_progress, log_message

def schedule_next_reminder(delay):
    threading.Timer(delay, show_reminder).start()

def show_reminder():
    # Logic for reminder pop-up
    pass
