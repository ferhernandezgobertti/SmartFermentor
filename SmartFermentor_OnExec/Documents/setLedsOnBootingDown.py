import subprocess, time

def configureStatusLeds():
    subprocess.call([“sudo /home/pi/Documents/ledStatusOff.sh PON“], shell=True)
    subprocess.call([“sudo /home/pi/Documents/ledStatusOff.sh ERR“], shell=True)
    subprocess.call([“sudo /home/pi/Documents/ledStatusOff.sh VEL“], shell=True)
    subprocess.call([“sudo /home/pi/Documents/ledStatusOff.sh TEM“], shell=True)
    subprocess.call([“sudo /home/pi/Documents/ledStatusOff.sh POT“], shell=True)
    subprocess.call([“sudo /home/pi/Documents/ledStatusOff.sh EXT“], shell=True)

def configureBarsState():
    subprocess.call([“sudo /home/pi/Documents/ledBarOff.sh BLUE“], shell=True)
    subprocess.call([“sudo /home/pi/Documents/ledBarOff.sh WHITE“], shell=True)
    subprocess.call([“sudo /home/pi/Documents/ledBarOff.sh RED“], shell=True)

if __name__ == "__main__":
    configureStatusLeds()
    configureBarsState()
    



