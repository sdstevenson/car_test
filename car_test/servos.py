from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
factory = PiGPIOFactory()
import time

class CustomServo:
    def __init__(self, pin:int, angle:int = 135):
        self.servo:AngularServo = AngularServo(pin, pin_factory=factory, min_angle=-135, max_angle=135)
        self.set_angle(angle)

    def set_angle(self, angle:int):
        self.servo.value = angle
    
    def decrease_angle(self):
        self.set_angle(self.servo.value - 1)
    
    def increase_angle(self):
        self.set_angle(self.servo.value + 1)

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