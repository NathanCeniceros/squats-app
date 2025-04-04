import threading
import tkinter as tk
from tkinter import ttk
import random
from src.tracker import update_progress

def schedule_next_reminder(delay):
    threading.Timer(delay, popup).start()

def popup():
    reminder_window = tk.Tk()
    reminder_window.title("Reminder")
    reminder_window.geometry("300x150")
    reminder_window.configure(bg="#fff0e0")

    label = ttk.Label(reminder_window, text="Time to take a break and do some squats!", font=("Helvetica", 12), wraplength=250)
    label.pack(pady=20)

    ok_button = ttk.Button(reminder_window, text="OK", command=reminder_window.destroy)
    ok_button.pack(pady=10)

    reminder_window.mainloop()

def show_congratulatory_message():
    congrats_window = tk.Tk()
    congrats_window.title("Good Job!")
    congrats_window.geometry("300x150")
    congrats_window.configure(bg="#e0ffe0")

    messages = [
        "Keep up the fantastic effort!",
        "Way to go! You’re doing great!",
        "Your body thanks you for staying active!",
        "Amazing! You're hitting your goals!",
        "Fantastic progress—keep crushing it!"
    ]

    message = random.choice(messages)

    label = ttk.Label(congrats_window, text=message, font=("Helvetica", 14, "bold"), foreground="#006600", wraplength=250)
    label.pack(pady=20)

    ok_button = ttk.Button(congrats_window, text="OK", command=congrats_window.destroy)
    ok_button.pack(pady=10)

    congrats_window.mainloop()
