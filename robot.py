import os
from gpiozero import Motor, Device  # type: ignore

if os.environ.get("DEV"):
    from gpiozero.pins.mock import MockFactory, MockPWMPin  # type: ignore

    Device.pin_factory = MockFactory(pin_class=MockPWMPin)


class Robot:
    m1 = Motor(2, 3)
    """ Левый сзади """

    m2 = Motor(17, 27)
    """ Правый сзади """

    m4 = Motor(24, 23)
    """ Левый спереди """

    m3 = Motor(15, 14)
    """ Правый спереди """

    def forward(self):
        [m.forward() for m in [self.m1, self.m2, self.m3, self.m4]]

    def backward(self):
        [m.backward() for m in [self.m1, self.m2, self.m3, self.m4]]

    def stop(self):
        [m.stop() for m in [self.m1, self.m2, self.m3, self.m4]]
