import tkinter as tk
from tkinter import ttk
import threading
import time
from datetime import datetime, timedelta
import random

LOG_FILE = "squats_log.txt"
TRACKER_FILE = "squats_tracker.txt"
time_slots = ["8:00 AM", "8:45 AM", "9:30 AM", "10:15 AM", "11:00 AM", "11:45 AM", 
              "12:30 PM", "1:15 PM", "2:00 PM", "2:45 PM", "3:30 PM", "4:15 PM", "5:00 PM"]
tracker_data = {}  # Dictionary to store daily progress


# Initialize tracker data for the week
def initialize_tracker():
    global tracker_data
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    tracker_data = {
        (start_of_week + timedelta(days=i)).strftime("%Y-%m-%d"): [False] * len(time_slots)
        for i in range(7)
    }

initialize_tracker()


# Save tracker data to a file
def save_tracker():
    with open(TRACKER_FILE, "w") as f:
        for date, progress in tracker_data.items():
            progress_str = ",".join(map(str, progress))
            f.write(f"{date}:{progress_str}\n")


# Load tracker data from a file
def load_tracker():
    global tracker_data
    try:
        with open(TRACKER_FILE, "r") as f:
            for line in f:
                date, progress_str = line.strip().split(":")
                tracker_data[date] = list(map(lambda x: x == "True", progress_str.split(",")))
    except FileNotFoundError:
        save_tracker()  # Create tracker file if it doesn't exist

load_tracker()


# Function to log activity
def log_message(message):
    with open(LOG_FILE, "a") as log:
        log.write(f"{time.ctime()}: {message}\n")


# Update tracker and progress bars
def update_progress(date, slot_index):
    tracker_data[date][slot_index] = True
    save_tracker()
    update_calendar()


def update_calendar():
    today = datetime.now().strftime("%Y-%m-%d")
    if today in tracker_data:
        completed_count = sum(tracker_data[today])
        progress_label.config(text=f"Progress: {completed_count}/{len(time_slots)}")
        progress_bar["value"] = (completed_count / len(time_slots)) * 100
        if completed_count == len(time_slots):
            status_label.config(text="Way to go! You completed your squats for today!", foreground="#006600")
        else:
            status_label.config(text="Keep going!", foreground="#333")
        update_time_slots_list(today)


def update_time_slots_list(date):
    current_time = datetime.now()
    current_hour = current_time.hour
    current_minute = current_time.minute

    style = ttk.Style()
    style.configure("Completed.TButton", foreground="#006600")  # Green for completed
    style.configure("Missed.TButton", foreground="#990000")  # Red for missed
    style.configure("Current.TButton", foreground="#3333FF", font=("Helvetica", 10, "bold"))  # Blue for current

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


def show_congratulatory_message():
    # Pop-up window for motivational message
    congrats_window = tk.Tk()
    congrats_window.title("Good Job!")
    congrats_window.geometry("300x150")
    congrats_window.configure(bg="#e0ffe0")  # Light green background

    # List of motivational messages
    messages = [
        "Keep up the fantastic effort!",
        "Way to go! You’re doing great!",
        "Your body thanks you for staying active!",
        "Amazing! You're hitting your goals!",
        "Fantastic progress—keep crushing it!"
    ]

    # Choose a random message
    message = random.choice(messages)

    # Display the message
    label = ttk.Label(
        congrats_window,
        text=message,
        font=("Helvetica", 14, "bold"),
        foreground="#006600",
        wraplength=250  # Wrap text to fit window
    )
    label.pack(pady=20)

    # Add OK button to close the window
    ok_button = ttk.Button(congrats_window, text="OK", command=congrats_window.destroy)
    ok_button.pack(pady=10)

    congrats_window.mainloop()

def mark_as_completed(date, slot_index):
    # Toggle the completion status for the selected time slot
    if tracker_data[date][slot_index]:  # If marked completed
        tracker_data[date][slot_index] = False  # Undo completion
        log_message(f"User undid squats for {time_slots[slot_index]}.")
    else:  # Mark as completed
        tracker_data[date][slot_index] = True
        log_message(f"User completed squats for {time_slots[slot_index]}.")
        show_congratulatory_message()  # Celebrate progress

    save_tracker()
    update_calendar()


# Function to display and dynamically update the current time
def update_current_time():
    # Get the current time
    now = datetime.now().strftime("%I:%M:%S %p")  # Format: HH:MM:SS AM/PM
    current_time_label.config(text=f"Current Time: {now}")

    # Schedule this function to run again in 1 second
    root.after(1000, update_current_time)


# Function to handle the reminder pop-up
def popup():
    def on_complete():
        current_date = datetime.now().strftime("%Y-%m-%d")
        next_slot_index = next((i for i, v in enumerate(tracker_data[current_date]) if not v), None)
        if next_slot_index is not None:
            update_progress(current_date, next_slot_index)
            log_message(f"User completed squats for {time_slots[next_slot_index]}.")
        reminder_window.destroy()
        schedule_next_reminder(45 * 60)

    def on_skip():
        log_message("User skipped this set of squats.")
        reminder_window.destroy()
        schedule_next_reminder(45 * 60)

    reminder_window = tk.Tk()
    reminder_window.title("Squat Reminder")
    reminder_window.configure(bg="#f0f0f0")  # Background color

    title_label = ttk.Label(
        reminder_window,
        text="Time to Move!",
        font=("Helvetica", 16, "bold"),
        foreground="#333",
        anchor="center"
    )
    title_label.pack(pady=10)

    # Include the specific time slot in the message
    current_date = datetime.now().strftime("%Y-%m-%d")
    next_slot_index = next((i for i, v in enumerate(tracker_data[current_date]) if not v), None)
    current_slot = time_slots[next_slot_index] if next_slot_index is not None else "Unknown"

    message_label = ttk.Label(
        reminder_window,
        text=f"Did you complete your squats for {current_slot}?",
        font=("Helvetica", 12),
        foreground="#555",
        wraplength=280  # Dynamically wrap text within 280px width
    )
    message_label.pack(pady=10)

    # Button frame to align buttons
    button_frame = ttk.Frame(reminder_window)
    button_frame.pack(pady=20)

    # Add "Yes" and "Skip" buttons
    complete_button = ttk.Button(button_frame, text="Yes", command=on_complete)
    complete_button.pack(side=tk.LEFT, padx=10)

    skip_button = ttk.Button(button_frame, text="Skip", command=on_skip)
    skip_button.pack(side=tk.RIGHT, padx=10)

    # Allow the window to dynamically adjust to content
    reminder_window.update_idletasks()
    reminder_window.mainloop()


# Schedule the next reminder
def schedule_next_reminder(delay):
    threading.Timer(delay, popup).start()


# Build the main app screen
def build_main_screen():
    global root, current_time_label, progress_bar, progress_label, status_label, time_slots_frame
    root = tk.Tk()
    root.title("Squats Tracker")
    root.configure(bg="#f0f0f0")

    title_label = ttk.Label(
        root,
        text="Daily Squats Progress",
        font=("Helvetica", 16, "bold"),
        foreground="#333"
    )
    title_label.pack(pady=10)

    # Display current time
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


# Main function to start everything
def main():
    log_message("Squat reminder program started.")
    root = build_main_screen()
    schedule_next_reminder(5)  # Start the first reminder after 5 seconds
    root.mainloop()  # Keeps the app running
if __name__ == "__main__":
    main()