import subprocess, time, serial

ser = serial.Serial()
ser.port = '/dev/ttyACM0'
ser.baudrate = 9600
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE
ser.bytesize = serial.EIGHTBITS
ser.timeout = 2

def configureStatusLeds():
    subprocess.call(['sudo /home/pi/Documents/ledStatusOn.sh PON'], shell=True)
    subprocess.call(['sudo /home/pi/Documents/ledStatusOff.sh ERR'], shell=True)
    subprocess.call(['sudo /home/pi/Documents/ledStatusOff.sh VEL'], shell=True)
    subprocess.call(['sudo /home/pi/Documents/ledStatusOff.sh TEM'], shell=True)
    subprocess.call(['sudo /home/pi/Documents/ledStatusOff.sh POT'], shell=True)
    subprocess.call(['sudo /home/pi/Documents/ledStatusOff.sh EXT'], shell=True)

def configureIdleState():
    subprocess.call(['sudo /home/pi/Documents/ledBarOn.sh BLUE'], shell=True)
    subprocess.call(['sudo /home/pi/Documents/ledBarOff.sh WHITE'], shell=True)
    subprocess.call(['sudo /home/pi/Documents/ledBarOff.sh RED'], shell=True)

def configureActiveState():
    subprocess.call(['sudo /home/pi/Documents/ledBarOff.sh BLUE'], shell=True)
    subprocess.call(['sudo /home/pi/Documents/ledBarOn.sh WHITE'], shell=True)
    subprocess.call(['sudo /home/pi/Documents/ledBarOff.sh RED'], shell=True)

def configureWarningState():
    subprocess.call(['sudo /home/pi/Documents/ledBarOff.sh BLUE'], shell=True)
    subprocess.call(['sudo /home/pi/Documents/ledBarOff.sh WHITE'], shell=True)
    subprocess.call(['sudo /home/pi/Documents/ledBarOn.sh RED'], shell=True)

def configureInitiationAnimation():
    configureIdleState()
    time.sleep(1)
    configureActiveState()
    time.sleep(1)
    configureWarningState()
    time.sleep(1)

if __name__ == "__main__":
    ser.open()
    ser.close()
    configureStatusLeds()
    configureInitiationAnimation()
    configureInitiationAnimation()
    configureIdleState()