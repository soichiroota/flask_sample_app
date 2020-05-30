# project/server/tests/test_static_pages.py


import unittest

from base import BaseTestCase


class TestStaticPagesBlueprint(BaseTestCase):
    def setUp(self):
        super().__init__()
        self.base_title = "Flask Sample App"

    def test_home(self):
        # Ensure Flask is setup.
        response = self.client.get(
            "/static_pages/home",
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Sample App", response.data)
        self.assertIn(b"Login", response.data)
        self.assertIn(
            f"{self.base_title} | Home".encode(),
            response.data
        )

    def test_help(self):
        # Ensure help route behaves correctly.
        response = self.client.get(
            "/static_pages/help",
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Help", response.data)
        self.assertIn(
            f"{self.base_title} | Help".encode(),
            response.data
        )

    def test_about(self):
        # Ensure about route behaves correctly.
        response = self.client.get(
            "/static_pages/about",
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"About", response.data)
        self.assertIn(
            f"{self.base_title} | About".encode(),
            response.data
        )

    def test_contact(self):
        # Ensure contact route behaves correctly.
        response = self.client.get(
            "/static_pages/contact",
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Contact", response.data)
        self.assertIn(
            f"{self.base_title} | Contact".encode(),
            response.data
        )


if __name__ == "__main__":
    unittest.main()
