from unittest import TestCase

from pi_home.app import App


class TestApp(TestCase):

    def setUp(self):
        self.config = {
            "pin_settings": {
                2: {
                    "pin": 2,
                    "label": "Led 2",
                    "type": "digital_output"
                },
                2: {
                    "pin": 2,
                    "label": "Led 2",
                    "type": "digital_output"
                },
                4: {
                    "pin": 4,
                    "label": "Button 4",
                    "type": "digital_input"
                },
                5: {
                    "pin": 5,
                    "label": "Led 5",
                    "type": "digital_output"
                }
            },
            "pin_dependencies": [
                {
                    "output_pin": 2,
                    "input_pin": 4
                },
                {
                    "output_pin": 2,
                    "input_pin": 4
                }
            ]
        }

    def test_create_app(self):
        app = App(self.config)

        self.assertIsNotNone(app)
