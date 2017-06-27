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

    def set_pin_value(self, pin, value):
        if not pin or not value:
            # TODO: return an error or something
            return

        # only we are suppose to change output pins
        output_pin = self._pins[int(pin)]
        print(output_pin)
        output_pin.value = value
        print(output_pin)
