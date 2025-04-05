"""
Module for handling reminders and notifications in the squats app.
"""

import logging
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import random
from src.tracker import Tracker

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Create a global instance of Tracker
tracker = Tracker()

class ReminderConfig:
    """
    Configuration for reminders, including test messages.
    """
    TEST_CONGRATULATORY_MESSAGE = None

    @staticmethod
    def reset():
        """
        Resets the configuration to default values.
        """
        ReminderConfig.TEST_CONGRATULATORY_MESSAGE = None


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
    # Allow popup to be mocked during tests
    if hasattr(popup, "trigger_mock"):
        popup.trigger_mock()  # Trigger mock if set
        return

    if threading.current_thread() != threading.main_thread():
        print("Warning: popup called from a non-main thread. Scheduling on the main thread.")
        tk.Tk().after(0, popup)  # Schedule popup on the main thread using a temporary Tk instance
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
    popup.trigger_mock = mock_call  # Use a public attribute instead of a protected member


def reset_popup_mock():
    """
    Resets the mock call for the popup function.
    """
    if hasattr(popup, "trigger_mock"):
        del popup.trigger_mock


def show_congratulatory_message(status_label=None):
    """
    Displays a congratulatory message on the banner.
    """
    messages = [
        "Your squats are shaping a masterpiece!",
        "Your glutes are the envy of the fitness world!",
        "You're building buns of steel!",
        "Your dedication is sculpting perfection!",
        "Your squats are a work of art!",
        "You're squatting your way to greatness!",
        "Your glutes deserve a standing ovation!",
        "You're creating a masterpiece with every squat!",
        "Your hard work is paying off beautifully!",
        "Your squats are poetry in motion!",
        "Your glutes are a testament to your effort!",
        "You're building a foundation of strength!",
        "Your squats are inspiring greatness!",
        "Your glutes are a symbol of determination!",
        "You're squatting your way to glory!",
        "Your dedication is shaping excellence!",
        "Your squats are a marvel to behold!",
        "Your glutes are a masterpiece in progress!",
        "You're creating a legacy with every squat!",
        "Your hard work is shaping brilliance!",
        "Your squats are a testament to your willpower!",
        "Your glutes are a reflection of your effort!",
        "You're building a monument to fitness!",
        "Your squats are a celebration of strength!",
        "Your glutes are a masterpiece of dedication!",
        "You're squatting your way to perfection!",
        "Your dedication is shaping greatness!",
        "Your squats are a triumph of willpower!",
        "Your glutes are a masterpiece of hard work!",
        "You're creating a legacy of strength!"
    ]

    # Use the test message if set, otherwise pick a random one
    message = ReminderConfig.TEST_CONGRATULATORY_MESSAGE or random.choice(messages)

    if status_label is not None:
        status_label.config(text=message, foreground="#006600")


def set_test_congratulatory_message(message):
    """
    Sets a test message for the congratulatory message.
    """
    ReminderConfig.TEST_CONGRATULATORY_MESSAGE = message


def reset_test_congratulatory_message():
    """
    Resets the test message for the congratulatory message.
    """
    ReminderConfig.TEST_CONGRATULATORY_MESSAGE = None


def configure_reminders():
    """
    Opens a GUI to configure reminder intervals.
    """
    config_window = tk.Tk()
    config_window.title("Configure Reminders")
    config_window.geometry("300x200")

    label = ttk.Label(config_window, text="Set Reminder Interval (minutes):", font=("Helvetica", 12))
    label.pack(pady=10)

    interval_var = tk.IntVar(value=30)
    interval_entry = ttk.Entry(config_window, textvariable=interval_var)
    interval_entry.pack(pady=5)

    def save_interval():
        interval = interval_var.get()
        schedule_next_reminder(interval)
        messagebox.showinfo("Success", f"Reminder interval set to {interval} minutes.")
        config_window.destroy()

    save_button = ttk.Button(config_window, text="Save", command=save_interval)
    save_button.pack(pady=10)

    config_window.mainloop()
