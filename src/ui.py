import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar  # Add tkcalendar for calendar widget
from src.tracker import time_slots, tracker_data, mark_as_completed, update_progress, initialize_tracker
from datetime import datetime

def update_calendar(selected_date=None):
    date = selected_date or datetime.now().strftime("%Y-%m-%d")
    if date not in tracker_data:
        print(f"Warning: No data found for date {date}.")
        progress_label.config(text="No data available for this date.")
        progress_bar["value"] = 0
        status_label.config(text="No progress yet.", foreground="#333")
        return

    completed_count = sum(tracker_data[date])
    progress_label.config(text=f"Progress: {completed_count}/{len(time_slots)}")
    progress_bar["value"] = (completed_count / len(time_slots)) * 100

    if completed_count == len(time_slots):
        status_label.config(text="Way to go! You completed your squats for today!", foreground="#006600")
    else:
        status_label.config(text="Keep going!", foreground="#333")
    update_time_slots_list(date)

def update_current_time():
    now = datetime.now().strftime("%I:%M:%S %p")
    current_time_label.config(text=f"Current Time: {now}")
    root.after(1000, update_current_time)

def update_time_slots_list(date):
    if date not in tracker_data:
        print(f"Warning: No data found for date {date}.")
        return

    current_time = datetime.now()
    current_hour = current_time.hour
    current_minute = current_time.minute

    style = ttk.Style()
    style.configure("Completed.TButton", foreground="#006600")
    style.configure("Missed.TButton", foreground="#990000")
    style.configure("Current.TButton", foreground="#3333FF", font=("Helvetica", 10, "bold"))

    for widget in time_slots_frame.winfo_children():
        widget.destroy()

    for index, slot_completed in enumerate(tracker_data[date]):
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
            time_slots_frame,
            text=f"{slot} {status}",
            command=lambda idx=index: mark_as_completed(date, idx),
            style=button_style
        )
        button.pack(fill="x", pady=2, padx=5)

def on_date_selected(event):
    selected_date = calendar.selection_get().strftime("%Y-%m-%d")
    update_calendar(selected_date)

def build_main_screen():
    global root, current_time_label, progress_bar, progress_label, status_label, time_slots_frame, calendar
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

    current_time_label = ttk.Label(root, text="Current Time: ", font=("Helvetica", 12), foreground="#333")
    current_time_label.pack(pady=5)

    progress_bar = ttk.Progressbar(root, orient="horizontal", length=500, mode="determinate")
    progress_bar.pack(pady=10)
    progress_label = ttk.Label(root, text="Progress: 0/13", font=("Helvetica", 12), foreground="#333")
    progress_label.pack(pady=5)
    status_label = ttk.Label(root, text="Keep going!", font=("Helvetica", 14, "bold"), foreground="#333")
    status_label.pack(pady=10)

    time_slots_frame = ttk.Frame(root)
    time_slots_frame.pack(fill="x", pady=10)

    update_calendar()
    update_current_time()
    return root
