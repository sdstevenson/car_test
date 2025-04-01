from gpiozero import OutputDevice
import time

def main():
    # Use the same pin numbers you're using in your main code
    forward_pin = 3
    backward_pin = 5

    # Create output devices
    forward = OutputDevice(forward_pin)
    backward = OutputDevice(backward_pin)

    try:
        for i in range(5):
            print("Testing FORWARD (forward=ON, backward=OFF)")
            forward.on()
            backward.off()
            time.sleep(2)
            
            print("STOP (both OFF)")
            forward.off()
            backward.off()
            time.sleep(2)
            
            print("Testing BACKWARD (forward=OFF, backward=ON)")
            forward.off()
            backward.on()
            time.sleep(2)
            
            print("STOP (both OFF)")
            forward.off()
            backward.off()
        
    finally:
        # Cleanup
        forward.close()
        backward.close()