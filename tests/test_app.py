from unittest import TestCase

from pi_home_raspberry.app import App


class FakeClient:

    def send_json(self, data):
        pass


class TestApp(TestCase):

    def setUp(self):
        self.config = {
            'pin_settings': {
                2: {
                    'pin': 2,
                    'label': 'Led 2',
                    'type': 'digital_output'
                },
                3: {
                    'pin': 3,
                    'label': 'Led 3',
                    'type': 'digital_output'
                },
                4: {
                    'pin': 4,
                    'label': 'Button 4',
                    'type': 'digital_input'
                },
                5: {
                    'pin': 5,
                    'label': 'Led 5',
                    'type': 'digital_input'
                }
            },
            'pin_dependencies': [
                {
                    'output_pin': 2,
                    'input_pin': 4,
                    'type': 'toggle'
                },
                {
                    'output_pin': 3,
                    'input_pin': 5,
                    'type': 'direct'
                }
            ]
        }
        self.app = App(self.config, 1234)
        self.client = FakeClient()

    def test_create_app(self):
        self.assertIsNotNone(self.app)

    def test_set_value(self):
        self.assertEqual(self.app.board._pins[2].value, False)

        action_name, result = self.app.process_message({
            'action': 'set_value',
            'data': {
                'pin': 2,
                'value': True,
            },
        }, self.client)
        self.assertEqual(action_name, 'set_value')
        self.assertTrue(result)
        self.assertEqual(self.app.board._pins[2].value, True)

        should_notify_self, should_notify_others = self.app.process_message({
            'action': 'set_value',
            'data': {
                'pin': 2,
                'value': False,
            },
        }, self.client)
        self.assertEqual(action_name, 'set_value')
        self.assertTrue(result)
        self.assertEqual(self.app.board._pins[2].value, False)
