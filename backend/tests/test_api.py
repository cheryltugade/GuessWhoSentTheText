import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api import app, update_game, get_messages

''''
Sets up
'''
class TestApp(unittest.TestCase):
    def setUp(self):
        app = self.app.test_client()  # Use Flask's test client
        app.testing = True  # Propagate exceptions to the test client

    def test_update_game_success(self):
        # Mock data for the request
        data = {
            "phone_number": "1234567890",
            "user_name": "test_user",
            "contact_name": "test_contact"
        }

        # Simulate a PUT request
        response = self.app.put('/api/update_game', json=data)

        # Assert response
        self.assertEqual(response.status_code, 200)
        self.assertIn("Game updated successfully!", response.json.get("message"))

    def test_update_game_missing_fields(self):
        # Mock data with missing fields
        data = {
            "phone_number": "1234567890",
            "user_name": "test_user"
        }

        # Simulate a PUT request
        response = self.app.put('/api/update_game', json=data)

        # Assert response
        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing required fields", response.json.get("error"))

    def test_update_game_exception(self):
        # Simulate an invalid request to cause an exception
        response = self.app.put('/api/update_game', json=None)

        # Assert response
        self.assertEqual(response.status_code, 500)
        self.assertIn("error", response.json)

'''
This class checks that the get_messages endpoint works correctly.
'''
# class TestGetMessages(unittest.TestCase):
#     def test_get_messages(self):


if __name__ == '__main__':
    unittest.main()