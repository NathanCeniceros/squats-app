import unittest
import os
import json
from flask import Flask
from src.backend import app  # Import the Flask app
from src.tracker import Tracker

class TestSquatsApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()  # Create a test client for the Flask app
        self.app.testing = True
        self.tracker = Tracker()

    # Test API: Get all progress
    def test_get_progress(self):
        response = self.app.get('/api/progress')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)  # Ensure the response is a dictionary

    # Test API: Get progress by date
    def test_get_progress_by_date(self):
        test_date = "2025-04-04"
        self.tracker.tracker_data[test_date] = [False, True, False]
        response = self.app.get(f'/api/progress/{test_date}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data, [False, True, False])  # Ensure the correct data is returned

    # Test API: Update progress
    def test_update_progress(self):
        test_date = "2025-04-04"
        self.tracker.tracker_data[test_date] = [False, False, False]
        response = self.app.post(f'/api/progress/{test_date}/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])  # Ensure the update was successful
        self.assertTrue(self.tracker.tracker_data[test_date][1])  # Ensure the slot was toggled

    # Test Tracker: Save and load tracker
    def test_save_and_load_tracker(self):
        self.tracker.tracker_data = {"2025-04-04": [True, False, True]}
        self.tracker.save_tracker()
        self.assertTrue(os.path.exists("progress_data.json"))
        self.tracker.tracker_data = {}
        self.tracker.load_tracker()
        self.assertIn("2025-04-04", self.tracker.tracker_data)

if __name__ == "__main__":
    unittest.main()