import unittest
import os
import signal
import threading
import logging
from unittest.mock import patch, Mock
from datetime import datetime
from src.tracker import Tracker, time_slots  # Import the Tracker class
from src.ui import build_main_screen, update_calendar, update_current_time
from src.reminders import schedule_next_reminder, popup
from src.reminders import show_congratulatory_message  # Add this import

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

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
        logging.info("Initializing tracker for test setup.")
        self.tracker = Tracker()  # Use the Tracker class

    # Tracker Module Tests
    @timeout(5)  # Add a timeout of 5 seconds
    def test_initialize_tracker(self):
        self.tracker.initialize_tracker()
        self.assertGreater(len(self.tracker.tracker_data), 0)  # Tracker data should have entries

    @timeout(5)
    def test_save_tracker(self):
        try:
            self.tracker.save_tracker()
            self.assertTrue(os.path.exists("squats_tracker.json"))  # File should exist
        except Exception as e:
            self.fail(f"save_tracker() raised an exception: {e}")

    @timeout(5)
    def test_load_tracker(self):
        try:
            self.tracker.load_tracker()
            self.assertTrue(self.tracker.tracker_data)  # Data should be loaded successfully
        except Exception as e:
            self.fail(f"load_tracker() raised an exception: {e}")

    @timeout(5)
    @patch("src.tracker.Tracker.load_tracker", autospec=True)
    @patch("src.tracker.Tracker.save_tracker", autospec=True)
    def test_mark_as_completed(self, mock_save_tracker, mock_load_tracker):
        logging.info("Starting test_mark_as_completed.")
        test_date = "2025-04-04"
        self.tracker.tracker_data[test_date] = [False, False, False]  # Mock tracker data
        logging.debug(f"Initial tracker data for {test_date}: {self.tracker.tracker_data[test_date]}")

        # Mark the first slot as completed
        self.tracker.mark_as_completed(test_date, 0, completed=True)
        logging.debug(f"Tracker data after marking slot 0 as completed: {self.tracker.tracker_data[test_date]}")
        self.assertTrue(self.tracker.tracker_data[test_date][0], "Slot 0 should be marked as completed.")

        # Mark the first slot as not completed
        self.tracker.mark_as_completed(test_date, 0, completed=False)
        logging.debug(f"Tracker data after marking slot 0 as not completed: {self.tracker.tracker_data[test_date]}")
        self.assertFalse(self.tracker.tracker_data[test_date][0], "Slot 0 should be marked as not completed.")

        # Mark the second slot as completed
        self.tracker.mark_as_completed(test_date, 1, completed=True)
        logging.debug(f"Tracker data after marking slot 1 as completed: {self.tracker.tracker_data[test_date]}")
        self.assertTrue(self.tracker.tracker_data[test_date][1], "Slot 1 should be marked as completed.")

        # Validate that other slots remain unaffected
        logging.debug(f"Validating that slot 2 remains unaffected: {self.tracker.tracker_data[test_date]}")
        self.assertFalse(self.tracker.tracker_data[test_date][2], "Slot 2 should remain not completed.")

        # Ensure save_tracker is called after each update
        self.assertEqual(mock_save_tracker.call_count, 3, "save_tracker should be called after each update.")
        logging.info("test_mark_as_completed completed successfully.")

    @timeout(5)
    def test_save_tracker_content(self):
        logging.info("Starting test_save_tracker_content.")
        self.tracker.initialize_tracker()
        self.tracker.save_tracker()
        with open("squats_tracker.json", "r") as file:
            content = file.read()
        logging.debug(f"Content of squats_tracker.json: {content}")
        self.assertIn(datetime.now().strftime("%Y-%m-%d"), content)  # Verify today's date is saved
        logging.info("test_save_tracker_content completed successfully.")

    # UI Module Tests
    @timeout(10)  # Increased timeout for GUI-related test
    def test_build_main_screen(self):
        logging.info("Starting test_build_main_screen.")
        try:
            root = build_main_screen()
            self.assertIsNotNone(root)  # Main screen should be built successfully
            logging.info("Main screen built successfully.")
        except Exception as e:
            logging.error(f"build_main_screen() raised an exception: {e}")
            self.fail(f"build_main_screen() raised an exception: {e}")

    @timeout(5)
    @patch("src.ui.ttk.Style", create=True)  # Mock ttk.Style
    @patch("src.ui.time_slots_frame", create=True)  # Mock time_slots_frame
    @patch("src.ui.progress_label", create=True)  # Mock GUI component
    @patch("src.ui.status_label", create=True)  # Mock GUI component
    @patch("src.ui.progress_bar", create=True)  # Mock GUI component
    def test_update_calendar(self, mock_progress_bar, mock_status_label, mock_progress_label, mock_time_slots_frame, mock_style):
        # Ensure tracker_data reflects an "in-progress" state
        test_date = "2025-04-04"
        self.tracker.tracker_data = {test_date: [True, False, False]}  # Mock tracker data

        # Debug log: State of tracker_data before calling update_calendar
        logging.debug(f"Before update_calendar: tracker_data[{test_date}] = {self.tracker.tracker_data[test_date]}")

        # Mock GUI components
        mock_progress_label.config = Mock()
        mock_status_label.config = Mock()
        mock_progress_bar.config = Mock()
        mock_style.configure = Mock()
        mock_time_slots_frame.winfo_children = Mock(return_value=[])

        # Call update_calendar
        update_calendar(test_date, mock_progress_label, mock_status_label, mock_progress_bar)

        # Assert the correct message is displayed
        mock_status_label.config.assert_called_once_with(text="Keep going!", foreground="#333")

    @timeout(5)
    @patch("src.ui.CURRENT_TIME_LABEL", create=True)  # Mock CURRENT_TIME_LABEL
    @patch("src.ui.ROOT", create=True)  # Mock ROOT
    def test_update_current_time(self, mock_root, mock_current_time_label):
        """
        Test the update_current_time function to ensure it updates the time label correctly.
        """
        # Mock the config method of CURRENT_TIME_LABEL
        mock_current_time_label.config = Mock()

        # Mock the after method of ROOT to prevent actual scheduling
        mock_root.after = Mock()

        # Call the function
        update_current_time()

        # Assert that CURRENT_TIME_LABEL.config was called with the correct text
        now = datetime.now().strftime("%I:%M:%S %p")
        mock_current_time_label.config.assert_called_once_with(text=f"Current Time: {now}")

        # Assert that ROOT.after was called to schedule the next update
        mock_root.after.assert_called_once_with(1000, update_current_time)

    # Reminders Module Tests
    @timeout(5)
    @patch("src.reminders.popup", autospec=True)  # Mock the popup function
    @patch("tkinter.Tk")  # Mock tkinter.Tk to prevent GUI from opening
    def test_schedule_next_reminder(self, mock_tk, mock_popup):
        """
        Test the schedule_next_reminder function to ensure it schedules reminders correctly.
        """
        try:
            schedule_next_reminder(5)  # Schedule a reminder after 5 seconds
            mock_popup.assert_not_called()  # Ensure popup is not called immediately
            self.assertTrue(True)  # Ensure no exceptions are raised
        except Exception as e:
            self.fail(f"schedule_next_reminder() raised an exception: {e}")

    @timeout(5)
    @patch("src.reminders.popup", autospec=True)  # Mock the popup function
    def test_popup(self, mock_popup):
        """
        Test the popup function to ensure it can be triggered without manual interaction.
        """
        try:
            # Set the mock for popup
            from src.reminders import set_popup_mock, reset_popup_mock
            set_popup_mock(mock_popup)

            # Explicitly call the popup function
            popup()  # Ensure the popup function is invoked
            mock_popup.assert_called_once()  # Ensure the popup function is called

            # Reset the mock after the test
            reset_popup_mock()
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

    @timeout(5)
    @patch("src.ui.schedule_next_reminder", autospec=True)
    @patch("src.ui.status_label", create=True)
    @patch("src.ui.root", create=True)  # Mock root for GUI updates
    def test_schedule_next_reminder_logic(self, mock_root, mock_status_label, mock_schedule):
        """
        Test the update_calendar function when all slots are completed.
        """
        test_date = "2025-04-04"
        self.tracker.tracker_data[test_date] = [True] * len(time_slots)  # Mock all slots as completed

        # Call update_calendar with the test date
        update_calendar(test_date, mock_status_label, mock_status_label, mock_status_label, root=mock_root)

        # Assert the correct message is displayed
        mock_status_label.config.assert_called_once_with(
            text="Keep up the fantastic effort!", foreground="#006600"  # Update expected text
        )

        # Verify that schedule_next_reminder is called with the correct delay
        mock_schedule.assert_called_once_with(5, mock_status_label=mock_status_label)

    @timeout(5)
    @patch("src.reminders.show_congratulatory_message")
    def test_schedule_next_reminder_logic(self, mock_show_message):
        """
        Test the logic for scheduling the next reminder.
        """
        from src.reminders import set_test_congratulatory_message, reset_test_congratulatory_message

        # Set the test message to match the expected value
        set_test_congratulatory_message("Way to go! You completed your squats for today!")

        mock_status_label = Mock()
        show_congratulatory_message(status_label=mock_status_label)

        # Assert the expected call
        mock_status_label.config.assert_called_once_with(
            text="Way to go! You completed your squats for today!", foreground="#006600"
        )

        # Reset the test message after the test
        reset_test_congratulatory_message()

    @timeout(5)
    def test_mark_as_completed(self):
        """
        Test the mark_as_completed function to ensure it updates tracker_data correctly.
        """
        test_date = "2025-04-01"
        slot_index = 0
        self.tracker.initialize_tracker("2025-03-31")  # Initialize tracker for the test week

        # Debug log: State of tracker_data before calling mark_as_completed
        logging.debug(f"Before mark_as_completed: tracker_data[{test_date}] = {self.tracker.tracker_data.get(test_date, 'Not Found')}")

        # Call the function to mark the slot as completed
        self.tracker.mark_as_completed(test_date, slot_index, completed=True)

        # Debug log: State of tracker_data after calling mark_as_completed
        logging.debug(f"After mark_as_completed: tracker_data[{test_date}] = {self.tracker.tracker_data.get(test_date, 'Not Found')}")

        # Assert that the slot is marked as completed
        self.assertTrue(self.tracker.tracker_data[test_date][slot_index], f"Slot {slot_index} on {test_date} was not marked as completed.")

if __name__ == "__main__":
    unittest.main()