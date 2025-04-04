from ui import build_main_screen
from reminders import schedule_next_reminder
from utils import log_message

if __name__ == "__main__":
    log_message("Squat reminder program started.")
    root = build_main_screen()
    schedule_next_reminder(5)  # Start the first reminder after 5 seconds
    root.mainloop()
