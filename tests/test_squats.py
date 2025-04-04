import unittest
from src.tracker import initialize_tracker, save_tracker, load_tracker, tracker_data

class TestSquatsApp(unittest.TestCase):

    def test_initialize_tracker(self):
        initialize_tracker()
        self.assertGreater(len(tracker_data), 0)  # Tracker data should have entries

    def test_save_tracker(self):
        try:
            save_tracker()
            self.assertTrue(True)  # File should save successfully
        except Exception as e:
            self.fail(f"save_tracker() raised an exception: {e}")

    def test_load_tracker(self):
        try:
            load_tracker()
            self.assertTrue(tracker_data)  # Data should be loaded successfully
        except Exception as e:
            self.fail(f"load_tracker() raised an exception: {e}")

if __name__ == "__main__":
    unittest.main()
