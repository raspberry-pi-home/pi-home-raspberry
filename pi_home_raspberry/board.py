import logging

from pi_home_raspberry.pins import (
    DigitalOutputPin,
    PinFactory,
)


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Board:

    def __init__(self, config):
        # create pins
        self._pins = PinFactory.create_pins(
            pin_settings=config['pin_settings'],
        )

        # configure pins
        for pin in self.pins:
            pin.configure()

        # set pin dependencies
        pin_dependencies = config['pin_dependencies']
        for pin_dependency in pin_dependencies:
            input_pin = self._pins[pin_dependency['input_pin']]
            output_pin = self._pins[pin_dependency['output_pin']]
            dependency_type = pin_dependency['type']

            input_pin.add_dependency(output_pin, dependency_type)

    @property
    def pins(self):
        return [pin_setting for _, pin_setting in self._pins.items()]

    def action_set_value(self, data):
        if 'pin' not in data:
            return False, False

        if 'value' not in data:
            return False, False

        pin = data['pin']
        value = data['value']

        if not pin:
            return False, False

        # validate value
        if not isinstance(value, bool):
            return False, False

        # validate pin
        try:
            pin = int(pin)
        except ValueError:
            return False, False

        # validate pin range
        try:
            output_pin = self._pins[pin]
        except KeyError:
            return False, False

        # only we are suppose to change output pins
        if not isinstance(output_pin, DigitalOutputPin):
            return False, False

        logger.info('Previous pin value: %s', output_pin)
        output_pin.value = value
        logger.info('New pin value: %s', output_pin)

        return False, True