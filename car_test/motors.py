from gpiozero import OutputDevice

leftMotor = OutputDevice(17)
rightMotor = OutputDevice(18)

def turnLeft():
    leftMotor.on()
    rightMotor.off()

def turnRight():
    leftMotor.off()
    rightMotor.on()

def forward():
    leftMotor.on()
    rightMotor.on()

def stop():
    leftMotor.off()
    rightMotor.off()
