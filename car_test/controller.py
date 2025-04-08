import pygame
import time
import sys
import car_test.motors as motors

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
    left_motor = motors.ThreePinMotor(forward_pin=17, backward_pin=27, speed_pin=12)
    # Physical pins: forward=11, backward=13, speed=32
    right_motor = motors.ThreePinMotor(forward_pin=22, backward_pin=23, speed_pin=13)
    # Physical pins: forward=15, backward=16, speed=33

    # Track the last hat state to detect changes
    last_hat_y = 0
    # Speed adjustment amount 
    speed_increment = 0.05
    
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

            # Control the car based on controller inputs
            # Get joystick values (assuming left stick is used for driving)
            left_stick_y = -inputs['axes'][1]  # Y-axis: forward (-1) / backward (1)
            left_stick_x = inputs['axes'][0]   # X-axis: left (-1) / right (1)
            right_stick_x = inputs['axes'][3]  # X-axis: left (-1) / right (1)

            # Convert joystick position to motor commands for differential drive
            # Invert Y because joystick forward is negative
            throttle = -left_stick_y  # Range: -1 (full backward) to 1 (full forward)
            steering = left_stick_x   # Range: -1 (full left) to 1 (full right)

            # Calculate motor speeds for differential steering
            left_motor_speed = 0
            right_motor_speed = 0

            # Right stick is higher priority, used for tank steering
            if abs(right_stick_x) > 0.1:
                # Use steering magnitude for both motors' speed
                turn_speed = abs(right_stick_x) * left_motor.max_speed
                
                if right_stick_x < 0:  # Steering left
                    left_motor.forward.off()
                    left_motor.backward.on()
                    left_motor.set_speed(turn_speed)
                    
                    right_motor.forward.on()
                    right_motor.backward.off()
                    right_motor.set_speed(turn_speed)
                    
                    # Display values
                    print(f"Tank steering LEFT {turn_speed}")
                    
                else:  # Steering right
                    left_motor.forward.on()
                    left_motor.backward.off()
                    left_motor.set_speed(turn_speed)
                    
                    right_motor.forward.off()
                    right_motor.backward.on()
                    right_motor.set_speed(turn_speed)
                    
                    print(f"Tank steering RIGHT {turn_speed}")
            elif abs(throttle) > 0.05 or abs(steering) > 0.05:
                # Calculate left/right motor speeds (ranges from -1 to 1)
                left_motor_speed = throttle + steering
                right_motor_speed = throttle - steering

                # Normalize speeds if they exceed limits (-1 to 1)
                max_magnitude = max(abs(left_motor_speed), abs(right_motor_speed))
                if max_magnitude > 1:
                    left_motor_speed /= max_magnitude
                    right_motor_speed /= max_magnitude
                
                # Apply max_speed scaling
                left_motor_speed *= left_motor.max_speed
                right_motor_speed *= right_motor.max_speed

                # Apply motor commands based on calculated speeds
                if left_motor_speed > 0:
                    left_motor.forward.on()
                    left_motor.backward.off()
                    left_motor.set_speed(left_motor_speed)
                elif left_motor_speed < 0:
                    left_motor.forward.off()
                    left_motor.backward.on()
                    left_motor.set_speed(abs(left_motor_speed))
                else:
                    left_motor.stop()

                if right_motor_speed > 0:
                    right_motor.forward.on()
                    right_motor.backward.off()
                    right_motor.set_speed(right_motor_speed)
                elif right_motor_speed < 0:
                    right_motor.forward.off()
                    right_motor.backward.on()
                    right_motor.set_speed(abs(right_motor_speed))
                else:
                    right_motor.stop()

            else:
                # No throttle input, stop both motors
                left_motor.stop()
                right_motor.stop()

            if len(inputs['hats']) > 0:
                hat_x, hat_y = inputs['hats'][0]

                # Only process if D-pad is pressed and it's a new press
                if hat_y != last_hat_y:
                    if hat_y == 1:  # D-pad Up pressed
                        new_max = min(left_motor.max_speed + speed_increment, 1.0)
                        left_motor.set_max_speed(new_max)
                        right_motor.set_max_speed(new_max)
                        print(f"\nMax speed increased to {new_max:.2f}")
                    elif hat_y == -1:  # D-pad Down pressed
                        new_max = max(left_motor.max_speed - speed_increment, 0.1)
                        left_motor.set_max_speed(new_max)
                        right_motor.set_max_speed(new_max)
                        print(f"\nMax speed decreased to {new_max:.2f}")

                # Save current hat state
                last_hat_y = hat_y


            # Display calculated values
            print(f"\nThrottle: {throttle:.2f}, Steering: {steering:.2f}")
            print(f"Left Motor: {left_motor_speed:.2f}, Right Motor: {right_motor_speed:.2f}")

            time.sleep(0.1)  # Prevent excessive CPU usage
            
    except KeyboardInterrupt:
        print("\nExiting controller monitor")
        
    finally:
        pygame.quit()
        

def main():
    monitor_controller()
    return
    left_motor = motors.ThreePinMotor(forward_pin=17, backward_pin=27, speed_pin=12)
    # Physical pins: forward=11, backward=13, speed=32
    right_motor = motors.ThreePinMotor(forward_pin=22, backward_pin=23, speed_pin=13)
    # Physical pins: forward=15, backward=16, speed=33
    while True:
        left_motor.forward_motion()
        time.sleep(2)
        left_motor.stop()
        time.sleep(2)
        left_motor.backward_motion()
        time.sleep(2)
        left_motor.stop()
        time.sleep(2)

if __name__ == "__main__":
    main()