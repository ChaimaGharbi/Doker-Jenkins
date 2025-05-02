import unittest
import json
from app.app import app


class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_hello_word(self):
        response = self.client.get("/")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn("Bienvenue", data["message"])

    def test_health_check(self):
        response = self.client.get("/health")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["status"], "healthy")


if __name__ == "__main__":
    unittest.main()
