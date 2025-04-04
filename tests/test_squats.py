import unittest
import os
from datetime import datetime
from src.tracker import initialize_tracker, save_tracker, load_tracker, mark_as_completed, tracker_data, time_slots
from src.ui import build_main_screen, update_calendar, update_current_time
from src.reminders import schedule_next_reminder, popup

class TestSquatsApp(unittest.TestCase):

    # Tracker Module Tests
    def test_initialize_tracker(self):
        initialize_tracker()
        self.assertGreater(len(tracker_data), 0)  # Tracker data should have entries

    def test_save_tracker(self):
        try:
            save_tracker()
            self.assertTrue(os.path.exists("squats_tracker.txt"))  # File should exist
        except Exception as e:
            self.fail(f"save_tracker() raised an exception: {e}")

    def test_load_tracker(self):
        try:
            load_tracker()
            self.assertTrue(tracker_data)  # Data should be loaded successfully
        except Exception as e:
            self.fail(f"load_tracker() raised an exception: {e}")

    def test_mark_as_completed(self):
        initialize_tracker()
        test_date = datetime.now().strftime("%Y-%m-%d")
        self.assertIn(test_date, tracker_data)  # Tracker data has today's date
        mark_as_completed(test_date, 0)  # Mark first time slot as completed
        self.assertTrue(tracker_data[test_date][0])  # Slot should be marked as completed
        mark_as_completed(test_date, 0)  # Undo completion
        self.assertFalse(tracker_data[test_date][0])  # Slot should be marked as incomplete

    # UI Module Tests
    def test_build_main_screen(self):
        try:
            root = build_main_screen()
            self.assertIsNotNone(root)  # Main screen should be built successfully
        except Exception as e:
            self.fail(f"build_main_screen() raised an exception: {e}")

    def test_update_calendar(self):
        try:
            initialize_tracker()
            update_calendar()  # Call calendar update
            self.assertTrue(True)  # Ensure no exceptions are raised
        except Exception as e:
            self.fail(f"update_calendar() raised an exception: {e}")

    def test_update_current_time(self):
        try:
            update_current_time()  # Call current time update
            self.assertTrue(True)  # Ensure no exceptions are raised
        except Exception as e:
            self.fail(f"update_current_time() raised an exception: {e}")

    # Reminders Module Tests
    def test_schedule_next_reminder(self):
        try:
            schedule_next_reminder(5)  # Schedule a reminder after 5 seconds
            self.assertTrue(True)  # Ensure no exceptions are raised
        except Exception as e:
            self.fail(f"schedule_next_reminder() raised an exception: {e}")

    def test_popup(self):
        try:
            popup()  # Trigger the popup window
            self.assertTrue(True)  # Ensure no exceptions are raised
        except Exception as e:
            self.fail(f"popup() raised an exception: {e}")

if __name__ == "__main__":
    unittest.main()
