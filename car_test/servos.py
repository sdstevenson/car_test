from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
factory = PiGPIOFactory()
import time

class CustomServo:
    def __init__(self, pin:int, angle:float = 0):
        self.servo:Servo = Servo(pin, pin_factory=factory)
        self.set_angle(angle)

    def set_angle(self, angle:float):
        """Acceptable inputs from -1 to 1"""
        # Make sure angle is within acceptable ranges
        if angle < -1:
            angle = -1
        elif angle > 1:
            angle = 1
        self.servo.value = angle
    
    def decrease_angle(self):
        self.set_angle(self.servo.value - 0.1)
    
    def increase_angle(self):
        self.set_angle(self.servo.value + 0.1)

def main():
    left_servo = CustomServo(pin=18)
    right_servo = CustomServo(pin=19)
    while True:
        print("Left")
        left_servo.set_angle(-1)
        right_servo.set_angle(-1)
        time.sleep(1)
        print("Middle")
        left_servo.set_angle(0)
        right_servo.set_angle(0)
        time.sleep(1)
        print("Right")
        left_servo.set_angle(1)
        right_servo.set_angle(1)
        time.sleep(1)