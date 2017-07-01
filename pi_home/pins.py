from addict import Dict
try:
    import gpiozero as gpio
except Exception:
    import pi_home.gpiomock as gpio

import pi_home.config as config_constants


class PinFactory:

    @staticmethod
    def create_pin(pin_type, pin_setting):
        if pin_type == config_constants.PIN_TYPE_INPUT_DIGITAL:
            return DigitalInputPin(pin_setting)
        if pin_type == config_constants.PIN_TYPE_OUTPUT_DIGITAL:
            return DigitalOutputPin(pin_setting)
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


class DigitalInputPin(ConfigurablePin):

    def __init__(self, settings):
        super(DigitalInputPin, self).__init__(settings)

        self._dependencies = Dict({
            config_constants.PIN_DEPENDENCY_TYPE_TOGGLE: [],
            config_constants.PIN_DEPENDENCY_TYPE_DIRECT: [],
        })

    def __str__(self):
        dependency_str = '\'{type_1}\': {dependencies_1}, \'{type_2}\': {dependencies_2}'.format(
            type_1=config_constants.PIN_DEPENDENCY_TYPE_TOGGLE,
            dependencies_1=[str(dependency) for dependency in self._dependencies[config_constants.PIN_DEPENDENCY_TYPE_TOGGLE]],
            type_2=config_constants.PIN_DEPENDENCY_TYPE_DIRECT,
            dependencies_2=[str(dependency) for dependency in self._dependencies[config_constants.PIN_DEPENDENCY_TYPE_DIRECT]],
        )
        return '{parent_name} > status: {status} > dependencies: {dependencies}'.format(
            parent_name=super(DigitalInputPin, self).__str__(),
            status=self.values,
            dependencies=dependency_str,
        )

    @property
    def values(self):
        return self._pin.values

    def configure(self):
        self._pin = gpio.Button(self.pin)
        self._pin.when_pressed = self._pin_pressed
        self._pin.when_released = self._pin_released

    def add_dependency(self, output_pin, dependency_type):
        self._dependencies[dependency_type].append(output_pin)

    def _pin_pressed(self):
        for dependency in self._dependencies[config_constants.PIN_DEPENDENCY_TYPE_TOGGLE]:
            dependency.toggle()
        for dependency in self._dependencies[config_constants.PIN_DEPENDENCY_TYPE_DIRECT]:
            dependency.on()

    def _pin_released(self):
        for dependency in self._dependencies[config_constants.PIN_DEPENDENCY_TYPE_DIRECT]:
            dependency.off()


class DigitalOutputPin(ConfigurablePin):

    def __str__(self):
        return '{parent_name} > status: {status}'.format(
            parent_name=super(DigitalOutputPin, self).__str__(),
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
