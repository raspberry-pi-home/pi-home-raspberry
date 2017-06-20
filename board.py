from pins import PinFactory


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

            input_pin.add_dependency(output_pin)

    @property
    def pins(self):
        return [pin_setting for _, pin_setting in self._pins.items()]

    def change_pin_status(self, pin, status):
        # TODO: validate pin, status and pin-status relation
        input_pin = self._pins[pin]
        input_pin.value = status
