import unittest
import os
import signal
from unittest.mock import patch
from datetime import datetime
from src.tracker import (
    initialize_tracker,
    save_tracker,
    load_tracker,
    mark_as_completed,
    tracker_data,
    time_slots,
)
from src.ui import build_main_screen, update_calendar, update_current_time
from src.reminders import schedule_next_reminder, popup


class TimeoutException(Exception):
    pass

def timeout(seconds=5):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutException(f"Test timed out after {seconds} seconds")

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                return func(*args, **kwargs)
            finally:
                signal.alarm(0)  # Disable the alarm
        return wrapper
    return decorator

class TestSquatsApp(unittest.TestCase):
    # Tracker Module Tests
    @timeout(5)  # Add a timeout of 5 seconds
    def test_initialize_tracker(self):
        initialize_tracker()
        self.assertGreater(len(tracker_data), 0)  # Tracker data should have entries

    @timeout(5)
    def test_save_tracker(self):
        try:
            save_tracker()
            self.assertTrue(os.path.exists("squats_tracker.json"))  # File should exist
        except Exception as e:
            self.fail(f"save_tracker() raised an exception: {e}")

    @timeout(5)
    def test_load_tracker(self):
        try:
            load_tracker()
            self.assertTrue(tracker_data)  # Data should be loaded successfully
        except Exception as e:
            self.fail(f"load_tracker() raised an exception: {e}")

    @timeout(5)
    def test_mark_as_completed(self):
        initialize_tracker()
        test_date = datetime.now().strftime("%Y-%m-%d")
        
        if test_date not in tracker_data:
            tracker_data[test_date] = [False] * len(time_slots)
        
        mark_as_completed(test_date, 0)
        self.assertTrue(tracker_data[test_date][0])  # Assert slot is marked completed

    @timeout(5)
    def test_save_tracker_content(self):
        initialize_tracker()
        save_tracker()
        with open("squats_tracker.json", "r") as file:
            content = file.read()
        self.assertIn(datetime.now().strftime("%Y-%m-%d"), content)  # Verify today's date is saved

    # UI Module Tests
    @timeout(5)
    def test_build_main_screen(self):
        try:
            root = build_main_screen()
            self.assertIsNotNone(root)  # Main screen should be built successfully
        except Exception as e:
            self.fail(f"build_main_screen() raised an exception: {e}")

    @timeout(5)
    def test_update_calendar(self):
        initialize_tracker()
        update_calendar()
        # Add assertions to verify calendar updates (mock UI components if necessary)
        self.assertTrue(True)  # Placeholder for actual verification logic

    @timeout(5)
    def test_update_current_time(self):
        update_current_time()
        # Add assertions to verify time updates (mock UI components if necessary)
        self.assertTrue(True)  # Placeholder for actual verification logic

    # Reminders Module Tests
    @timeout(5)
    @patch("tkinter.Tk")  # Mock tkinter.Tk to prevent GUI from opening
    def test_schedule_next_reminder(self, mock_tk):
        try:
            schedule_next_reminder(5)  # Schedule a reminder after 5 seconds
            self.assertTrue(True)  # Ensure no exceptions are raised
        except Exception as e:
            self.fail(f"schedule_next_reminder() raised an exception: {e}")

    @timeout(5)
    @patch("tkinter.Tk")  # Mock tkinter.Tk to prevent GUI from opening
    def test_popup(self, mock_tk):
        try:
            popup()  # Trigger the popup window
            mock_tk.assert_called_once()  # Ensure tkinter.Tk is called
        except Exception as e:
            self.fail(f"popup() raised an exception: {e}")

    @timeout(5)
    @patch("src.reminders.schedule_next_reminder")
    def test_schedule_next_reminder_logic(self, mock_schedule):
        schedule_next_reminder(5)
        mock_schedule.assert_called_once_with(5)  # Verify reminder is scheduled with correct delay


if __name__ == "__main__":
    unittest.main()