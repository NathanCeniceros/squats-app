"""
Module for handling the user interface of the squats app.
"""

import threading
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from src.tracker import Tracker, time_slots
import os

# Initialize global variables
ROOT = None
PROGRESS_BAR = None
STATUS_LABEL = None
TIME_SLOTS_FRAME = None
CALENDAR = None

# Create a global instance of Tracker
tracker = Tracker()

PROGRESS_LABEL = None
CURRENT_TIME_LABEL = None


def update_calendar(date, progress_label, status_label, progress_bar, root=None):
    """
    Update the calendar UI with the progress for the given date.
    """
    if date not in tracker.tracker_data:
        progress_label.config(text="No data available for this date.")
        progress_bar.config(value=0)
        status_label.config(text="No progress yet.", foreground="#333")
        return

    completed_count = sum(1 for completed in tracker.tracker_data[date] if completed)
    progress_text = f"Progress: {completed_count}/{len(time_slots)}"
    status_text = (
        "Way to go! You completed your squats for today!"
        if completed_count == len(time_slots)
        else "Keep going!"
    )
    status_color = "#006600" if completed_count == len(time_slots) else "#333"

    progress_percentage = (completed_count / len(time_slots)) * 100

    def update_ui():
        progress_label.config(text=progress_text)
        status_label.config(text=status_text, foreground=status_color)
        progress_bar.config(value=progress_percentage)

    if root:
        root.after(0, update_ui)
    else:
        update_ui()


def update_current_time():
    """
    Updates the current time label every second.
    """
    now = datetime.now().strftime("%I:%M:%S %p")
    if CURRENT_TIME_LABEL:
        CURRENT_TIME_LABEL.config(text=f"Current Time: {now}")
    if ROOT:
        ROOT.after(1000, update_current_time)  # Ensure this runs on the main thread
    else:
        print("Warning: root is not initialized. Skipping update_current_time.")


def update_time_slots_list(date, mock_style=None, mock_time_slots_frame=None):
    """
    Updates the time slots list for the given date.
    """
    if threading.current_thread() != threading.main_thread():
        print("Warning: update_time_slots_list called from a non-main thread. Scheduling on the main thread.")
        ROOT.after(0, lambda: update_time_slots_list(date, mock_style, mock_time_slots_frame))
        return

    if date not in tracker.tracker_data:
        print(f"Warning: No data found for date {date}.")
        return

    current_time = datetime.now()
    current_hour = current_time.hour
    current_minute = current_time.minute

    style = mock_style or ttk.Style()  # Use mock style if provided
    style.configure("Completed.TButton", foreground="#006600")
    style.configure("Missed.TButton", foreground="#990000")
    style.configure("Current.TButton", foreground="#3333FF", font=("Helvetica", 10, "bold"))

    frame = mock_time_slots_frame or TIME_SLOTS_FRAME  # Use mock frame if provided
    for widget in frame.winfo_children():
        widget.destroy()

    for index, slot_completed in enumerate(tracker.tracker_data[date]):
        slot = time_slots[index]
        slot_time = datetime.strptime(slot, "%I:%M %p")
        slot_hour = slot_time.hour
        slot_minute = slot_time.minute

        if slot_completed:
            status = "✔"
            button_style = "Completed.TButton"
        elif (slot_hour < current_hour) or (slot_hour == current_hour and slot_minute <= current_minute):
            status = "✗"
            button_style = "Missed.TButton"
        else:
            status = ""
            button_style = "TButton"

        if slot_hour == current_hour and current_minute >= slot_minute:
            button_style = "Current.TButton"
            status = "⏳"

        button = ttk.Button(
            frame,
            text=f"{slot} {status}",
            command=lambda idx=index: mark_squat_as_completed(date, idx),
            style=button_style
        )
        button.pack(fill="x", pady=2, padx=5)


def mark_squat_as_completed(date, slot_index):
    """
    Toggles the completion status of a squat for the given date and time slot.
    """
    tracker.tracker_data[date][slot_index] = not tracker.tracker_data[date][slot_index]
    update_time_slots_list(date)
    update_calendar(date, PROGRESS_LABEL, STATUS_LABEL, PROGRESS_BAR, ROOT)
    status = "completed" if tracker.tracker_data[date][slot_index] else "not completed"
    messagebox.showinfo("Status Updated", f"Time slot {time_slots[slot_index]} marked as {status}.")


def on_date_selected(event):
    """
    Handles the event when a date is selected in the calendar.
    """
    selected_date = CALENDAR.selection_get().strftime("%Y-%m-%d")
    update_calendar(selected_date, PROGRESS_LABEL, STATUS_LABEL, PROGRESS_BAR, ROOT)
    update_time_slots_list(selected_date)


def change_calendar_view(*args):
    """
    Changes the calendar view mode based on the dropdown selection.
    """
    view_mode = VIEW_MODE.get()
    if view_mode == "day":
        CALENDAR.config(selectmode="day")
    elif view_mode == "week":
        messagebox.showinfo("Info", "Week view is not implemented yet.")
    elif view_mode == "month":
        messagebox.showinfo("Info", "Month view is not implemented yet.")
    elif view_mode == "year":
        messagebox.showinfo("Info", "Year view is not implemented yet.")
    else:
        messagebox.showerror("Error", f"Unknown view mode: {view_mode}")
    print(f"Changed calendar view to: {view_mode}")


def build_main_screen():
    """
    Builds the main screen for the squats tracker application.
    """
    global ROOT, CURRENT_TIME_LABEL, PROGRESS_BAR, PROGRESS_LABEL, STATUS_LABEL, TIME_SLOTS_FRAME, CALENDAR, VIEW_MODE
    ROOT = tk.Tk()
    ROOT.title("Squats Tracker")
    ROOT.configure(bg="#f0f8ff")  # Light blue background for a fun and approachable look

    # Set the application icon to the squatting person icon if it exists
    icon_path = "squat-icon.ico"
    if os.path.exists(icon_path):
        ROOT.iconbitmap(icon_path)
    else:
        print(f"Warning: Icon file '{icon_path}' not found. Skipping icon setup.")

    # Initialize VIEW_MODE after ROOT is created
    VIEW_MODE = tk.StringVar(value="day")  # Default calendar view mode

    title_label = ttk.Label(
        ROOT, text="Daily Squats Progress", font=("Helvetica", 16, "bold"), foreground="#333"
    )
    title_label.pack(pady=10)

    # Dropdown menu for calendar view
    view_menu = ttk.OptionMenu(ROOT, VIEW_MODE, "day", "day", "week", "month", "year", command=change_calendar_view)
    view_menu.pack(pady=5)

    calendar_frame = ttk.Frame(ROOT)
    calendar_frame.pack(pady=10)
    CALENDAR = Calendar(calendar_frame, selectmode="day", date_pattern="yyyy-mm-dd")
    CALENDAR.pack()
    CALENDAR.bind("<<CalendarSelected>>", on_date_selected)

    CURRENT_TIME_LABEL = ttk.Label(
        ROOT, text="Current Time: ", font=("Helvetica", 12), foreground="#333"
    )
    CURRENT_TIME_LABEL.pack(pady=5)

    PROGRESS_BAR = ttk.Progressbar(ROOT, orient="horizontal", length=500, mode="determinate")
    PROGRESS_BAR.pack(pady=10)
    PROGRESS_LABEL = ttk.Label(
        ROOT, text="Today's Progress: 0/13", font=("Helvetica", 12), foreground="#333"
    )
    PROGRESS_LABEL.pack(pady=5)

    STATUS_LABEL = ttk.Label(
        ROOT, text="Keep going!", font=("Helvetica", 14, "bold"), foreground="#333"
    )
    STATUS_LABEL.pack(pady=10)

    TIME_SLOTS_FRAME = ttk.Frame(ROOT)
    TIME_SLOTS_FRAME.pack(fill="x", pady=10)

    # Pass required arguments to update_calendar
    today = datetime.now().strftime("%Y-%m-%d")
    update_calendar(today, PROGRESS_LABEL, STATUS_LABEL, PROGRESS_BAR, ROOT)
    update_time_slots_list(today)
    update_current_time()
    return ROOT


def schedule_next_reminder(delay_minutes, mock_status_label=None):
    """
    Schedules the next reminder after a specified delay in minutes.
    """
    print(f"Debug: Scheduling next reminder in {delay_minutes} minutes.")
    # Add logic to schedule the reminder (e.g., using a timer or external service)
    threading.Timer(delay_minutes * 60, lambda: print("Reminder triggered!")).start()

    # Update the status label if provided
    if status:
        status = mock_status_label or STATUS_LABEL  # Use mock_status_label if provided
        status.config(text="Way to go! You completed your squats for today!", foreground="#006600")
