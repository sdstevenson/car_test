from gpiozero import Servo
    # Default PWM period of 20 ms matches current servos
import time

class CustomServo:
    def __init__(self, pin:int):
        self.servo:Servo = Servo(pin)

    def set_angle(self, angle:float):
        """Acceptable inputs from -1 to 1"""
        # Make sure angle is within acceptable ranges
        if angle < -1:
            angle = -1
        elif angle > 1:
            angle = 1
        self.servo.value = angle

def main():
    servo = CustomServo(pin=18)
    while True:
        print("Left")
        servo.set_angle(-1)
        time.sleep(1)
        print("Middle")
        servo.set_angle(0)
        time.sleep(1)
        print("Right")
        servo.set_angle(1)
        time.sleep(1)