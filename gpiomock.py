# this file is a fake copy of gpiozero in where you can interact with
# without the need of having a raspberry-pi while developing the features


class PIN:

    def __init__(self, pin, *args, **kwars):
        self._pin = pin

    @property
    def pin(self):
        return self._pin


class LED(PIN):

    def __init__(self, pin, *args, **kwars):
        super(LED, self).__init__(pin, *args, **kwars)

        self._value = False

    @property
    def value(self):
        return self._value

    def on(self):
        self._value = True

    def off(self):
        self._value = False

    def toggle(self):
        self._value = not self._value


class Button(PIN):

    def __init__(self, pin, *args, **kwars):
        super(Button, self).__init__(pin, *args, **kwars)

        self._values = False
        self.when_pressed = self._pin_pressed
        self.when_released = self._pin_released

    @property
    def values(self):
        return self._values

    def _pin_pressed(self):
        pass

    def _pin_released(self):
        pass
