import pygame
import time
import sys

def initialize_controller():
    """Initialize pygame and set up controller detection."""
    pygame.init()
    pygame.joystick.init()
    
    # Wait for controller to be connected
    controller = None
    while not controller:
        try:
            # Check how many joysticks/controllers are connected
            joystick_count = pygame.joystick.get_count()
            
            if joystick_count == 0:
                print("No controllers found. Please connect a Logitech controller.")
                time.sleep(2)
                continue
                
            # Initialize the first controller found
            controller = pygame.joystick.Joystick(0)
            controller.init()
            
            # Verify it's a Logitech controller (may not be 100% accurate)
            controller_name = controller.get_name()
            print(f"Controller connected: {controller_name}")
            
            if "logitech" not in controller_name.lower() and "logicool" not in controller_name.lower():
                print("Warning: This may not be a Logitech controller.")
                
            # Display controller information
            print(f"Number of axes: {controller.get_numaxes()}")
            print(f"Number of buttons: {controller.get_numbuttons()}")
            print(f"Number of hats: {controller.get_numhats()}")
            
        except pygame.error as e:
            print(f"Controller error: {e}")
            controller = None
            time.sleep(2)
    
    return controller

def read_controller_input(controller):
    """Read and return all controller inputs."""
    # Need to call event pump to update controller state
    pygame.event.pump()
    
    # Read all axes (joysticks, triggers)
    axes = [controller.get_axis(i) for i in range(controller.get_numaxes())]
    
    # Read all buttons
    buttons = [controller.get_button(i) for i in range(controller.get_numbuttons())]
    
    # Read all hats (D-pads, typically returns tuple of (-1,0,1) for each direction)
    hats = [controller.get_hat(i) for i in range(controller.get_numhats())]
    
    return {
        'axes': axes,
        'buttons': buttons,
        'hats': hats
    }

def monitor_controller():
    """Main function to continuously monitor controller input."""
    controller = initialize_controller()
    
    print("\nController monitoring started. Press Ctrl+C to exit.")
    print("Reading controller inputs... (3 seconds)")
    
    try:
        while True:
            inputs = read_controller_input(controller)
            
            # Format the output 
            print("\033[H\033[J", end="")  # Clear screen (might not work in all terminals)
            print("Controller inputs:")
            print(f"Axes (joysticks/triggers): {inputs['axes']}")
            print(f"Buttons: {inputs['buttons']}")
            print(f"Hats (D-pad): {inputs['hats']}")
            
            time.sleep(0.1)  # Prevent excessive CPU usage
            
    except KeyboardInterrupt:
        print("\nExiting controller monitor")
        
    finally:
        pygame.quit()
        
if __name__ == "__main__":
    monitor_controller()