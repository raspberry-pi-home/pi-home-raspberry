try:
    import gpiozero as gpio
except Exception:
    import gpiomock as gpio

import config as config_constants


class PinFactory:

    @staticmethod
    def create_pin(pin_type, pin_setting):
        if pin_type == config_constants.PIN_TYPE_INPUT_DIGITAL:
            return InputPin(pin_setting)
        if pin_type == config_constants.PIN_TYPE_OUTPUT_DIGITAL:
            return OutputPin(pin_setting)
        return EmptyPin(pin_setting)

    @staticmethod
    def create_pins(pin_settings):
        return {
            pin: PinFactory.create_pin(pin_setting.get('type'), pin_setting)
            for pin, pin_setting in pin_settings.items()
        }


class Pin:

    def __init__(self, settings):
        if type(self) == Pin:
            raise TypeError('\'Pin\' can not be instantiated')

        self._pin_number = settings['pin']
        self._pin = None

    def __str__(self):
        return '{class_name}({pin})'.format(
            class_name=self.__class__.__name__,
            pin=self.pin,
        )

    @property
    def pin(self):
        return self._pin_number

    def configure(self):
        raise NotImplementedError


class EmptyPin(Pin):

    def configure(self):
        pass


class ConfigurablePin(Pin):

    def __init__(self, settings):
        super(ConfigurablePin, self).__init__(settings)

        self.label = settings['label']
        self.type = settings['type']

    def __str__(self):
        return '{parent_name}({label})'.format(
            parent_name=super(ConfigurablePin, self).__str__(),
            label=self.label,
        )


class InputPin(ConfigurablePin):

    def __init__(self, settings):
        super(InputPin, self).__init__(settings)

        self._dependencies = []

    def __str__(self):
        return '{parent_name} > status: {status} > dependencies: {dependencies}'.format(
            parent_name=super(InputPin, self).__str__(),
            status=self.values,
            dependencies=[str(dependency) for dependency in self._dependencies],
        )

    # TODO: add this back (?)
    # @property
    # def values(self):
    #     return self._pin.values

    def configure(self):
        self._pin = gpio.Button(self.pin)
        self._pin.when_pressed = self._pin_pressed
        self._pin.when_released = self._pin_released

    def add_dependency(self, output_pin):
        self._dependencies.append(output_pin)

    def _pin_pressed(self):
        for dependency in self._dependencies:
            dependency.toggle()

    def _pin_released(self):
        pass


class OutputPin(ConfigurablePin):

    def __str__(self):
        return '{parent_name} > status: {status}'.format(
            parent_name=super(OutputPin, self).__str__(),
            status=self.value,
        )

    @property
    def value(self):
        return self._pin.value

    @value.setter
    def value(self, value):
        if value:
            self.on()
        else:
            self.off()

    def configure(self):
        self._pin = gpio.LED(self.pin)

    def on(self):
        self._pin.on()

    def off(self):
        self._pin.off()

    def toggle(self):
        self._pin.toggle()
