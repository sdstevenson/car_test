Basic python script to read in input from a logitech game controller and output it to specific raspberry pi pins to control a simple car.

Installs:
Poetry [https://python-poetry.org/docs/]
sudo apt install python3-pigpio python3-rpi.gpio

Enable pigpio daemon: sudo pigpiod

Wiring (see controller.py)

Run with: poetry run controller
