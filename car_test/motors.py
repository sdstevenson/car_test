from gpiozero import OutputDevice, PWMOutputDevice
# from gpiozero.pins.mock import MockFactory, MockPWMPin
# from gpiozero import Device

# No GPIO pins on windows, use MockFactory
# Device.pin_factory = MockFactory(pin_class=MockPWMPin)

class ThreePinMotor:
    def __init__(self, forward_pin:int, backward_pin:int, speed_pin:int):
        self.forward = OutputDevice(forward_pin)
        self.backward = OutputDevice(backward_pin)
        self.speed = PWMOutputDevice(speed_pin, active_high=True, initial_value=0.5)
        self.max_speed = 0.5

    def forward_motion(self):
        """Move motor forward at specified speed (0.0 to 1.0)"""
        self.backward.off()
        self.forward.on()
        self.speed.value = self.max_speed

    def backward_motion(self):
        """Move motor backward at specified speed (0.0 to 1.0)"""
        self.forward.off()
        self.backward.on()
        self.speed.value = self.max_speed

    def stop(self):
        """Stop the motor"""
        self.forward.off()
        self.backward.off()
        self.speed.value = self.max_speed

    def set_speed(self, speed):
        """Set the speed of the motor by adjusting duty cycle (0.0 to 1.0)"""
        if speed < 0:
            self.speed.value = 0
        elif speed > self.max_speed:
            self.speed.value = self.max_speed
        else:
            self.speed.value = speed
    
    def set_max_speed(self, speed):
        """Set the maximum speed of the motor"""
        if speed < 0:
            self.max_speed = 0
        elif speed > 1:
            self.max_speed = 1
        else:
            self.max_speed = speed
