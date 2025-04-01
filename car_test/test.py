from gpiozero import OutputDevice
import time

def main():
    # Use the same pin numbers you're using in your main code
    forward_pin = 17 # Physical pin 11
    backward_pin = 27 # Physical pin 13
    forward_pin_r = 22 # Physical pin 15
    backward_pin_r = 23 # Physical pin 16

    # Create output devices
    forward = OutputDevice(forward_pin)
    backward = OutputDevice(backward_pin)
    forward_r = OutputDevice(forward_pin_r)
    backward_r = OutputDevice(backward_pin_r)

    try:
        print("Starting test sequence")
        for i in range(3):
            print(f"\nCycle {i+1}:")
            
            print("Ensuring STOP state")
            forward.off()
            backward.off()
            forward_r.off()
            backward_r.off()
            time.sleep(1)
            
            print("Testing FORWARD (forward=ON, backward=OFF)")
            forward.on()
            backward.off()
            forward_r.on()
            backward_r.off()
            time.sleep(2)
            print("Current state: forward={}, backward={}, forward_r={}, backward_r={}".format(
                "ON" if forward.value else "OFF", 
                "ON" if backward.value else "OFF",
                "ON" if forward_r.value else "OFF",
                "ON" if backward_r.value else "OFF"))
            
            print("STOP (both OFF)")
            forward.off()
            backward.off()
            forward_r.off()
            backward_r.off()
            time.sleep(1)
            
            print("Testing BACKWARD (forward=OFF, backward=ON)")
            forward.off()
            backward.on()
            forward_r.off()
            backward_r.on()
            time.sleep(2)
            print("Current state: forward={}, backward={}, forward_r={}, backward_r={}".format(
                "ON" if forward.value else "OFF", 
                "ON" if backward.value else "OFF",
                "ON" if forward_r.value else "OFF",
                "ON" if backward_r.value else "OFF"))
            
            print("STOP (both OFF)")
            forward.off()
            backward.off()
            forward_r.off()
            backward_r.off()
            time.sleep(1)
        
    finally:
        # Cleanup
        forward.close()
        backward.close()