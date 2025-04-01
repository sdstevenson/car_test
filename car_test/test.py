from gpiozero import OutputDevice
import time

def main():
    # Use the same pin numbers you're using in your main code
    forward_pin = 17 # Physical pin 11
    backward_pin = 27 # Physical pin 13

    # Create output devices
    forward = OutputDevice(forward_pin)
    backward = OutputDevice(backward_pin)

    try:
        print("Starting test sequence")
        for i in range(3):
            print(f"\nCycle {i+1}:")
            
            print("Ensuring STOP state")
            forward.off()
            backward.off()
            time.sleep(1)
            
            print("Testing FORWARD (forward=ON, backward=OFF)")
            forward.on()
            backward.off()
            time.sleep(2)
            print("Current state: forward={}, backward={}".format(
                "ON" if forward.value else "OFF", 
                "ON" if backward.value else "OFF"))
            
            print("STOP (both OFF)")
            forward.off()
            backward.off()
            time.sleep(1)
            
            print("Testing BACKWARD (forward=OFF, backward=ON)")
            forward.off()
            backward.on()
            time.sleep(2)
            print("Current state: forward={}, backward={}".format(
                "ON" if forward.value else "OFF", 
                "ON" if backward.value else "OFF"))
            
            print("STOP (both OFF)")
            forward.off()
            backward.off()
            time.sleep(1)
        
    finally:
        # Cleanup
        forward.close()
        backward.close()