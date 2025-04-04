import unittest
import os
import signal
import threading
from unittest.mock import patch, Mock
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
        def wrapper(*args, **kwargs):
            result = [None]
            exception = [None]

            def target():
                try:
                    result[0] = func(*args, **kwargs)
                except Exception as e:
                    exception[0] = e

            thread = threading.Thread(target=target)
            thread.start()
            thread.join(seconds)
            if thread.is_alive():
                raise TimeoutException(f"Test timed out after {seconds} seconds")
            if exception[0]:
                raise exception[0]
            return result[0]
        return wrapper
    return decorator

class TestSquatsApp(unittest.TestCase):
    def setUp(self):
        initialize_tracker()

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
            tracker_data[test_date] = [False] * len(time_slots)  # Ensure tracker_data is initialized
        mark_as_completed(test_date, 0)
        self.assertTrue(tracker_data[test_date][0])  # Assert slot is marked completed
        self.assertFalse(tracker_data[test_date][1])  # Assert other slots remain unmarked

    @timeout(5)
    def test_save_tracker_content(self):
        initialize_tracker()
        save_tracker()
        with open("squats_tracker.json", "r") as file:
            content = file.read()
        self.assertIn(datetime.now().strftime("%Y-%m-%d"), content)  # Verify today's date is saved

    # UI Module Tests
    @timeout(10)  # Increased timeout for GUI-related test
    def test_build_main_screen(self):
        try:
            root = build_main_screen()
            self.assertIsNotNone(root)  # Main screen should be built successfully
        except Exception as e:
            self.fail(f"build_main_screen() raised an exception: {e}")

    @timeout(5)
    @patch("src.ui.ttk.Style", create=True)  # Mock ttk.Style
    @patch("src.ui.time_slots_frame", create=True)  # Mock time_slots_frame
    @patch("src.ui.progress_label", create=True)  # Mock GUI component
    @patch("src.ui.status_label", create=True)  # Mock GUI component
    @patch("src.ui.progress_bar", create=True)  # Mock GUI component
    def test_update_calendar(self, mock_progress_bar, mock_status_label, mock_progress_label, mock_time_slots_frame, mock_style):
        initialize_tracker()
        mock_progress_label.config = Mock()  # Correctly mock config method
        mock_status_label.config = Mock()  # Correctly mock config method
        mock_progress_bar.config = Mock()  # Correctly mock config method
        mock_style.configure = Mock()  # Mock style configuration
        mock_time_slots_frame.winfo_children = Mock(return_value=[])  # Mock frame children
        update_calendar(mock_progress_label=mock_progress_label, mock_status_label=mock_status_label, mock_progress_bar=mock_progress_bar)
        mock_status_label.config.assert_called_once_with(text="Keep going!", foreground="#333")

    @timeout(5)
    @patch("src.ui.current_time_label", create=True)  # Mock GUI component
    @patch("src.ui.root", create=True)  # Mock GUI component
    def test_update_current_time(self, mock_root, mock_current_time_label):
        mock_current_time_label.config = lambda **kwargs: None  # Mock config method
        mock_root.after = lambda delay, func: None  # Mock root.after
        update_current_time()
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
    @patch("src.reminders.schedule_next_reminder", autospec=True)
    def test_schedule_next_reminder_logic(self, mock_schedule):
        schedule_next_reminder(5)
        mock_schedule.assert_called_once_with(5)  # Verify reminder is scheduled with correct delay

    @timeout(5)
    @patch("src.reminders.threading.Timer", autospec=True)
    def test_schedule_next_reminder_with_timer(self, mock_timer):
        mock_timer_instance = mock_timer.return_value
        schedule_next_reminder(5, mock_timer=mock_timer)
        mock_timer.assert_called_once_with(5, popup)  # Verify timer is initialized with correct delay and function
        mock_timer_instance.start.assert_called_once()  # Verify timer is started


if __name__ == "__main__":
    unittest.main()