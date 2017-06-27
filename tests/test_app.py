from unittest import TestCase

from app import App
from config import get_config


class TestApp(TestCase):

    def test_create_app(self):
        config = get_config()
        app = App(config)

        self.assertIsNotNone(app)
