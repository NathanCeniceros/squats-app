import tkinter as tk
from tkinter import ttk
from tracker import update_calendar, update_current_time

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

    # Create other UI elements...
    update_calendar()
    update_current_time()
    return root
