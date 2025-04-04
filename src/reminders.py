"""
Module for handling reminders and notifications in the squats app.
"""

import logging
import threading
import tkinter as tk
from tkinter import ttk
import random
from src.tracker import Tracker

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Create a global instance of Tracker
tracker = Tracker()

TEST_CONGRATULATORY_MESSAGE = None  # Global variable for testing purposes


def schedule_next_reminder(delay, mock_timer=None):
    """
    Schedules the next reminder after a specified delay.
    """
    timer = mock_timer or threading.Timer
    timer(delay, popup).start()


def popup():
    """
    Displays a popup reminder window.
    """
    if hasattr(popup, "_mock_call"):
        popup._mock_call()
        return

    reminder_window = tk.Tk()
    reminder_window.title("Reminder")
    reminder_window.geometry("300x150")
    reminder_window.configure(bg="#fff0e0")

    label = ttk.Label(
        reminder_window,
        text="Time to take a break and do some squats!",
        font=("Helvetica", 12),
        wraplength=250,
    )
    label.pack(pady=20)

    def snooze():
        reminder_window.destroy()
        schedule_next_reminder(300)

    ok_button = ttk.Button(reminder_window, text="OK", command=reminder_window.destroy)
    ok_button.pack(side="left", padx=10, pady=10)

    snooze_button = ttk.Button(reminder_window, text="Snooze", command=snooze)
    snooze_button.pack(side="right", padx=10, pady=10)

    reminder_window.mainloop()


def set_popup_mock(mock_call):
    """
    Sets a mock call for the popup function.
    """
    popup._mock_call = mock_call


def reset_popup_mock():
    """
    Resets the mock call for the popup function.
    """
    if hasattr(popup, "_mock_call"):
        del popup._mock_call


def show_congratulatory_message(status_label=None):
    """
    Displays a congratulatory message.
    """
    messages = [
        "Way to go! You completed your squats for today!",
        "Keep up the fantastic effort!",
        "Your body thanks you for staying active!",
        "Amazing! You're hitting your goals!",
        "Fantastic progress—keep crushing it!",
    ]

    message = TEST_CONGRATULATORY_MESSAGE or random.choice(messages)

    if status_label is not None:
        status_label.config(text=message, foreground="#006600")
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
        wraplength=250,
    )
    label.pack(pady=20)

    ok_button = ttk.Button(congrats_window, text="OK", command=congrats_window.destroy)
    ok_button.pack(pady=10)

    congrats_window.mainloop()


def set_test_congratulatory_message(message):
    """
    Sets a test message for the congratulatory message.
    """
    global TEST_CONGRATULATORY_MESSAGE
    TEST_CONGRATULATORY_MESSAGE = message


def reset_test_congratulatory_message():
    """
    Resets the test message for the congratulatory message.
    """
    global TEST_CONGRATULATORY_MESSAGE
    TEST_CONGRATULATORY_MESSAGE = None
