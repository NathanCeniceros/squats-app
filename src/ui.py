"""
Module for handling the user interface of the squats app.
"""

from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from src.tracker import Tracker, time_slots

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

    def update_ui():
        progress_label.config(text=progress_text)
        status_label.config(text=status_text, foreground=status_color)
        progress_bar.config(value=(completed_count / len(time_slots)) * 100)

    if root:
        root.after(0, update_ui)
    else:
        update_ui()


def update_current_time():
    """
    Updates the current time label every second.
    """
    now = datetime.now().strftime("%I:%M:%S %p")
    CURRENT_TIME_LABEL.config(text=f"Current Time: {now}")
    root.after(1000, update_current_time)


def update_time_slots_list(date, mock_style=None, mock_time_slots_frame=None):
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

    frame = mock_time_slots_frame or time_slots_frame  # Use mock frame if provided
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
            command=lambda idx=index: tracker.mark_as_completed(date, idx),
            style=button_style
        )
        button.pack(fill="x", pady=2, padx=5)


def on_date_selected(event):
    selected_date = calendar.selection_get().strftime("%Y-%m-%d")
    update_calendar(selected_date)


def build_main_screen():
    global root, CURRENT_TIME_LABEL, progress_bar, PROGRESS_LABEL, status_label, time_slots_frame, calendar
    root = tk.Tk()
    root.title("Squats Tracker")
    root.configure(bg="#f0f0f0")

    title_label = ttk.Label(root, text="Daily Squats Progress", font=("Helvetica", 16, "bold"), foreground="#333")
    title_label.pack(pady=10)

    calendar_frame = ttk.Frame(root)
    calendar_frame.pack(pady=10)
    calendar = Calendar(calendar_frame, selectmode="day", date_pattern="yyyy-mm-dd")
    calendar.pack()
    calendar.bind("<<CalendarSelected>>", on_date_selected)

    CURRENT_TIME_LABEL = ttk.Label(root, text="Current Time: ", font=("Helvetica", 12), foreground="#333")
    CURRENT_TIME_LABEL.pack(pady=5)

    progress_bar = ttk.Progressbar(root, orient="horizontal", length=500, mode="determinate")
    progress_bar.pack(pady=10)
    PROGRESS_LABEL = ttk.Label(root, text="Progress: 0/13", font=("Helvetica", 12), foreground="#333")
    PROGRESS_LABEL.pack(pady=5)
    status_label = ttk.Label(root, text="Keep going!", font=("Helvetica", 14, "bold"), foreground="#333")
    status_label.pack(pady=10)

    time_slots_frame = ttk.Frame(root)
    time_slots_frame.pack(fill="x", pady=10)

    # Pass required arguments to update_calendar
    update_calendar(datetime.now().strftime("%Y-%m-%d"), PROGRESS_LABEL, status_label, progress_bar, root)
    update_current_time()
    return root


def schedule_next_reminder(delay_minutes, mock_status_label=None):
    print(f"Debug: Scheduling next reminder in {delay_minutes} minutes.")
    status = mock_status_label or status_label  # Use mock_status_label if provided

    # Update the status label if provided
    if status:
        status.config(text="Way to go! You completed your squats for today!", foreground="#006600")

    # Add logic to schedule the reminder (e.g., using a timer or external service)
    threading.Timer(delay_minutes * 60, lambda: print("Reminder triggered!")).start()
