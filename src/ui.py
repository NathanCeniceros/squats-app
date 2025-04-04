"""
Module for handling the user interface of the squats app.
"""

import threading
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from src.tracker import Tracker, time_slots
import os
import json  # Add for data persistence
from src.reminders import show_congratulatory_message  # Import the function

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
        def no_data_ui_update():
            progress_label.config(text="No data available for this date.")
            progress_bar.config(value=0)
            status_label.config(text="No progress yet.", foreground="#333")
        if root:
            root.after(0, no_data_ui_update)
        else:
            no_data_ui_update()
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

        # Update calendar colors for previous days
        for day, slots in tracker.tracker_data.items():
            if root:
                root.after(0, lambda d=day, s=slots: _update_calendar_event(d, s, root))
            else:
                _update_calendar_event(day, slots, root)

        # Highlight the current time slot with a blue hourglass
        today = datetime.now().strftime("%Y-%m-%d")
        if date == today:
            current_time = datetime.now()
            for index, slot in enumerate(time_slots):
                slot_time = datetime.strptime(slot, "%I:%M %p")
                if slot_time.hour == current_time.hour and slot_time.minute == current_time.minute:
                    def highlight_current_slot():
                        if root:
                            root.after(0, lambda: CALENDAR.calevent_create(current_time, "", "current"))
                            root.after(0, lambda: CALENDAR.tag_config("current", background="blue", foreground="white"))
                        else:
                            CALENDAR.calevent_create(current_time, "", "current")
                            CALENDAR.tag_config("current", background="blue", foreground="white")
                    highlight_current_slot()

    if root:
        root.after(0, update_ui)  # Schedule UI updates on the main thread
    else:
        update_ui()


def _update_calendar_event(day, slots, root=None):
    """
    Helper function to update calendar events for a specific day.
    """
    def update_event():
        if not CALENDAR:
            print(f"Warning: CALENDAR is not initialized. Skipping update for {day}.")
            return

        if all(slots):
            CALENDAR.calevent_create(datetime.strptime(day, "%Y-%m-%d"), "", "completed")
            CALENDAR.tag_config("completed", background="green", foreground="white")
        elif any(slots):
            CALENDAR.calevent_create(datetime.strptime(day, "%Y-%m-%d"), "", "incomplete")
            CALENDAR.tag_config("incomplete", background="red", foreground="white")
        else:
            CALENDAR.calevent_create(datetime.strptime(day, "%Y-%m-%d"), "", "missed")
            CALENDAR.tag_config("missed", background="red", foreground="white")

    if threading.current_thread() != threading.main_thread():
        if root:
            root.after(0, update_event)  # Schedule on the main thread
        else:
            print(f"Warning: ROOT is not initialized. Skipping update for {day}.")
    else:
        update_event()


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

    today = datetime.now().strftime("%Y-%m-%d")  # Get today's date as a string

    for index, slot_completed in enumerate(tracker.tracker_data[date]):
        slot = time_slots[index]
        slot_time = datetime.strptime(slot, "%I:%M %p")
        slot_hour = slot_time.hour
        slot_minute = slot_time.minute

        if slot_completed:
            status = "✔"
            button_style = "Completed.TButton"
        elif date < today:  # For previous days, mark all missed slots
            status = "✗"
            button_style = "Missed.TButton"
        elif date == today:  # For today, check the current time
            if (slot_hour < current_hour) or (slot_hour == current_hour and slot_minute < current_minute):
                status = "✗"
                button_style = "Missed.TButton"
            elif slot_hour == current_hour and slot_minute == current_minute:
                button_style = "Current.TButton"
                status = "⏳"
            else:
                status = ""
                button_style = "TButton"
        else:  # For future dates
            status = ""
            button_style = "TButton"

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

    # Check if all squats for the day are completed
    if all(tracker.tracker_data[date]):
        show_congratulatory_message(STATUS_LABEL)  # Update banner with congratulatory message
    else:
        # Briefly show a congratulatory message for the individual time slot
        if tracker.tracker_data[date][slot_index]:  # If the slot was marked as completed
            original_text = STATUS_LABEL.cget("text")  # Save the original status text
            STATUS_LABEL.config(text="Great job! Keep going!", foreground="#006600")
            ROOT.after(2000, lambda: STATUS_LABEL.config(text=original_text, foreground="#333"))  # Revert after 2 seconds

    status = "completed" if tracker.tracker_data[date][slot_index] else "not completed"
    print(f"Time slot {time_slots[slot_index]} marked as {status}.")


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
    selected_date = CALENDAR.selection_get()
    today = datetime.now()

    if view_mode == "day":
        # Show progress for the selected day
        update_calendar(selected_date.strftime("%Y-%m-%d"), PROGRESS_LABEL, STATUS_LABEL, PROGRESS_BAR, ROOT)
        update_time_slots_list(selected_date.strftime("%Y-%m-%d"))

    elif view_mode == "week":
        # Calculate the start and end of the week
        start_of_week = selected_date - timedelta(days=selected_date.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        for current_date in (start_of_week + timedelta(days=i) for i in range(7)):
            update_calendar(current_date.strftime("%Y-%m-%d"), PROGRESS_LABEL, STATUS_LABEL, PROGRESS_BAR, ROOT)

    elif view_mode == "month":
        # Keep the existing behavior for month view
        start_of_month = selected_date.replace(day=1)
        next_month = (start_of_month + timedelta(days=31)).replace(day=1)
        end_of_month = next_month - timedelta(days=1)
        for current_date in (start_of_month + timedelta(days=i) for i in range((end_of_month - start_of_month).days + 1)):
            update_calendar(current_date.strftime("%Y-%m-%d"), PROGRESS_LABEL, STATUS_LABEL, PROGRESS_BAR, ROOT)

    elif view_mode == "year":
        # Keep the existing behavior for year view
        start_of_year = selected_date.replace(month=1, day=1)
        end_of_year = selected_date.replace(month=12, day=31)
        for current_date in (start_of_year + timedelta(days=i) for i in range((end_of_year - start_of_year).days + 1)):
            update_calendar(current_date.strftime("%Y-%m-%d"), PROGRESS_LABEL, STATUS_LABEL, PROGRESS_BAR, ROOT)

    else:
        print(f"Error: Unknown view mode {view_mode}")


def calculate_progress_for_range(start_date, end_date):
    """
    Calculates progress for a range of dates.
    """
    progress = {}
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        if date_str in tracker.tracker_data:
            completed_count = sum(1 for completed in tracker.tracker_data[date_str] if completed)
            progress[date_str] = f"{completed_count}/{len(time_slots)}"
        else:
            progress[date_str] = "No data"
        current_date += timedelta(days=1)
    return progress


def display_progress_summary(progress, title, date_range):
    """
    Displays a summary of progress for a given range.
    """
    summary_window = tk.Toplevel(ROOT)
    summary_window.title(title)
    summary_window.geometry("400x300")
    summary_window.configure(bg="#f0f8ff")

    title_label = ttk.Label(summary_window, text=f"{title}: {date_range}", font=("Helvetica", 14, "bold"))
    title_label.pack(pady=10)

    for date, progress_text in progress.items():
        progress_label = ttk.Label(summary_window, text=f"{date}: {progress_text}", font=("Helvetica", 12))
        progress_label.pack(anchor="w", padx=10, pady=2)


def save_progress():
    """
    Save the tracker data to a file.
    """
    with open("progress_data.json", "w") as file:
        json.dump(tracker.tracker_data, file)
    print("Progress saved.")


def load_progress():
    """
    Load the tracker data from a file.
    """
    if os.path.exists("progress_data.json"):
        with open("progress_data.json", "r") as file:
            tracker.tracker_data = json.load(file)
        print("Progress loaded.")
    else:
        print("No saved progress found.")


def notify_missed_slots(date):
    """
    Notify the user of missed slots for the given date.
    """
    missed_slots = [
        time_slots[i] for i, completed in enumerate(tracker.tracker_data.get(date, []))
        if not completed
    ]
    if missed_slots:
        messagebox.showwarning("Missed Slots", f"You missed the following slots: {', '.join(missed_slots)}")


def ensure_root_initialized():
    """
    Ensure that ROOT is initialized before performing any Tkinter operations.
    """
    if ROOT is None:
        raise RuntimeError("ROOT is not initialized. Call build_main_screen first.")


def safe_exit():
    """
    Save progress and exit the application gracefully.
    """
    try:
        save_progress()
    except Exception as e:
        print(f"Error saving progress: {e}")
    finally:
        if ROOT:
            ROOT.destroy()


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
    load_progress()  # Load progress on startup
    ROOT.protocol("WM_DELETE_WINDOW", safe_exit)  # Use safe_exit for graceful shutdown
    VIEW_MODE.trace_add("write", change_calendar_view)  # Trigger view change on dropdown selection
    return ROOT


def schedule_next_reminder(delay_minutes, mock_status_label=None):
    """
    Schedules the next reminder after a specified delay in minutes.
    """
    print(f"Debug: Scheduling next reminder in {delay_minutes} minutes.")
    # Add logic to schedule the reminder (e.g., using a timer or external service)
    threading.Timer(delay_minutes * 60, lambda: print("Reminder triggered!")).start()

    # Update the status label if provided
    if mock_status_label:
        status = mock_status_label or STATUS_LABEL  # Use mock_status_label if provided
        status.config(text="Way to go! You completed your squats for today!", foreground="#006600")
