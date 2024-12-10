import os
import time
from gpiozero import Motor, Device, AngularServo, Servo  # type: ignore

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

    m_lift = Motor(20, 21)
    actuator = Motor(16, 26)

    servo_qr = AngularServo(13, min_angle=-180, max_angle=180)
    servo_platform = Servo(18)
    servo_grab = AngularServo(19, min_angle=-180, max_angle=180)

    def forward(self):
        [m.forward() for m in [self.m1, self.m2, self.m3, self.m4]]

    def backward(self):
        [m.backward() for m in [self.m1, self.m2, self.m3, self.m4]]

    def stop(self):
        [m.stop() for m in [self.m1, self.m2, self.m3, self.m4, self.m_lift, self.actuator]]

    def right(self):
        self.m2.forward()
        self.m4.forward()
        self.m1.backward()
        self.m3.backward()

    def left(self):
        self.m1.forward()
        self.m3.forward()
        self.m2.backward()
        self.m4.backward()

    def rotate(self):
        self.m1.forward()
        self.m4.forward()
        self.m2.backward()
        self.m3.backward()

    def scan_qr(self):
        self.servo_qr.value = 0
        time.sleep(0.5)
        self.servo_qr.value = -0.7
        time.sleep(1)
        self.servo_qr.value = 0.7
        time.sleep(1)
