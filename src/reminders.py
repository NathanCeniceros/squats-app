import threading
import tkinter as tk
from tkinter import ttk
import random
from src.tracker import Tracker
import logging

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Create a global instance of Tracker
tracker = Tracker()

def schedule_next_reminder(delay, mock_timer=None):
    """
    Schedules the next reminder after a specified delay.
    """
    timer = mock_timer or threading.Timer
    timer(delay, popup).start()  # Use popup directly instead of a lambda

def popup():
    # Allow popup to be mocked during tests
    if hasattr(popup, "_mock_call"):
        popup._mock_call()  # Trigger mock if set
        return

    reminder_window = tk.Tk()
    reminder_window.title("Reminder")
    reminder_window.geometry("300x150")
    reminder_window.configure(bg="#fff0e0")

    label = ttk.Label(
        reminder_window, 
        text="Time to take a break and do some squats!", 
        font=("Helvetica", 12), 
        wraplength=250
    )
    label.pack(pady=20)

    # Add a fun animation effect
    def bounce_window():
        for i in range(5):
            reminder_window.geometry(f"300x{150 + i * 5}")
            reminder_window.update_idletasks()
            reminder_window.after(50)
        for i in range(5):
            reminder_window.geometry(f"300x{175 - i * 5}")
            reminder_window.update_idletasks()
            reminder_window.after(50)

    bounce_window()

    def snooze():
        reminder_window.destroy()
        schedule_next_reminder(300)  # Snooze for 5 minutes

    ok_button = ttk.Button(reminder_window, text="OK", command=reminder_window.destroy)
    ok_button.pack(side="left", padx=10, pady=10)

    snooze_button = ttk.Button(reminder_window, text="Snooze", command=snooze)
    snooze_button.pack(side="right", padx=10, pady=10)

    reminder_window.mainloop()

# Add a method to set a mock call for popup
def set_popup_mock(mock_call):
    popup._mock_call = mock_call
    popup._mock_call_set = True  # Track if mock is set

# Ensure popup mock is resettable
def reset_popup_mock():
    if hasattr(popup, "_mock_call"):
        del popup._mock_call
        del popup._mock_call_set

# Add a global variable to override the congratulatory message for testing
test_congratulatory_message = None

def show_congratulatory_message(status_label=None):
    """
    Displays a congratulatory message. If a status_label is provided, updates it instead of creating a new window.
    """
    messages = [
        "Way to go! You completed your squats for today!",  # Ensure this matches the test expectation
        "Keep up the fantastic effort!",
        "Your body thanks you for staying active!",
        "Amazing! You're hitting your goals!",
        "Fantastic progress—keep crushing it!"
    ]

    # Use the test message if set, otherwise pick a random one
    message = test_congratulatory_message or random.choice(messages)

    # Debug log to check if status_label is passed
    logging.debug(f"Received status_label: {status_label} (type: {type(status_label)})")

    if status_label is not None:  # Explicitly check for None
        # Debug log to verify status_label is being updated
        logging.debug(f"Updating status_label with message: {message}")
        status_label.config(text=message, foreground="#006600")  # Ensure this matches the test expectation
        return

    congrats_window = tk.Tk()
    congrats_window.title("Good Job!")
    congrats_window.geometry("300x150")
    congrats_window.configure(bg="#e0ffe0")

    label = ttk.Label(
        congrats_window, 
        text=message, 
        font=("Helvetica", 14, "bold"), 
        foreground="#006600", 
        wraplength=250
    )
    label.pack(pady=20)

    # Add auto-sizing for better appearance
    congrats_window.update_idletasks()
    width = congrats_window.winfo_reqwidth()
    height = congrats_window.winfo_reqheight()
    congrats_window.geometry(f"{width}x{height}")

    ok_button = ttk.Button(congrats_window, text="OK", command=congrats_window.destroy)
    ok_button.pack(pady=10)

    congrats_window.mainloop()

# Add a function to set the test message
def set_test_congratulatory_message(message):
    global test_congratulatory_message
    test_congratulatory_message = message

# Add a function to reset the test message
def reset_test_congratulatory_message():
    global test_congratulatory_message
    test_congratulatory_message = None
