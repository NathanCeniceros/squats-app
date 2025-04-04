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
