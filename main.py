from gpiozero import Servo, AngularServo, Motor  # type: ignore
import time


class Robot:
    manipulator_horizontal = Servo(17)
    manipulator_grab = AngularServo(15, min_angle=-180, max_angle=180)

    motor_lf = Motor(19, 16)
    """Мотор впереди слева"""

    motor_rf = Motor(24, 25)
    """Мотор впереди справа"""

    motor_lb = Motor(14, 13)
    """Мотор сзади слева"""

    motor_rb = Motor(10, 9)
    """Мотор сзади справа"""

    def __init__(self) -> None:
        pass

    def right(self) -> None:
        self.motor_lf.forward()
        self.motor_lb.forward()

        self.motor_rf.backward()
        self.motor_rb.backward()

    def left(self) -> None:
        self.motor_lf.backward()
        self.motor_lb.backward()

        self.motor_rf.forward()
        self.motor_rb.forward()

    def forward(self) -> None:
        self.motor_lf.forward()
        self.motor_lb.forward()

        self.motor_rf.forward()
        self.motor_rb.forward()

    def backward(self) -> None:
        self.motor_lf.backward()
        self.motor_lb.backward()

        self.motor_rf.backward()
        self.motor_rb.backward()

    def stop(self) -> None:
        self.motor_lf.stop()
        self.motor_lb.stop()

        self.motor_rf.stop()
        self.motor_rb.stop()


if __name__ == "__main__":
    robot = Robot()

    robot.forward()
    time.sleep(1)

    robot.stop()
    time.sleep(1)

    robot.backward()
    time.sleep(1)

    robot.stop()
    time.sleep(1)

    robot.right()
    time.sleep(1)

    robot.stop()
    time.sleep(1)

    robot.left()
    time.sleep(1)

    robot.stop()
    time.sleep(1)
