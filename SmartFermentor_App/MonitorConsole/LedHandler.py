import sys, os, subprocess, time

class LedHandler():

    def __init__(self):
        self.setErrorFixed()
        self.configureInitiationAnimation()
        self.setIdleState()
        self.isControlExecuting = [False, False, False]
    
    def configureInitiationAnimation(self):
        count = 0
        while(count<2):
            self.setVelocityControlLedOn()
            time.sleep(0.5)
            self.setTemperatureControlLedOn()
            time.sleep(0.5)
            self.setPotentialControlLedOn()
            time.sleep(0.5)
            self.setExtractionControlLedOn()
            time.sleep(1)
            self.configureStopAllControl()
            self.setExtractionControlLedOff()
            time.sleep(0.5)
            count = count + 1

    def configureVelocityLeds(self, isControlRunning):
        if(isControlRunning):
            self.setActiveState()
            self.setVelocityControlLedOn()
        else:
            self.setVelocityControlLedOff()
        self.isControlExecuting[0] = isControlRunning

    def configureTemperatureLeds(self, isControlRunning):
        if(isControlRunning):
            self.setActiveState()
            self.setTemperatureControlLedOn()
        else:
            self.setTemperatureControlLedOff()
        self.isControlExecuting[1] = isControlRunning

    def configurePotentialLeds(self, isControlRunning):
        if(isControlRunning):
            self.setActiveState()
            self.setPotentialControlLedOn()
        else:
            self.setPotentialControlLedOff()
        self.isControlExecuting[2] = isControlRunning

    def verifyLedsState(self):
        if(not self.isControlExecuting[0] and not self.isControlExecuting[1] and not self.isControlExecuting[2]):
            self.setIdleState()

    def setIdleState(self):
        subprocess.call(['sudo /home/pi/Documents/ledBarOn.sh BLUE'], shell=True)
        subprocess.call(['sudo /home/pi/Documents/ledBarOff.sh WHITE'], shell=True)
        subprocess.call(['sudo /home/pi/Documents/ledBarOff.sh RED'], shell=True)

    def setActiveState(self):
        subprocess.call(['sudo /home/pi/Documents/ledBarOff.sh BLUE'], shell=True)
        subprocess.call(['sudo /home/pi/Documents/ledBarOn.sh WHITE'], shell=True)
        subprocess.call(['sudo /home/pi/Documents/ledBarOff.sh RED'], shell=True)

    def setWarningState(self):
        subprocess.call(['sudo /home/pi/Documents/ledBarOff.sh BLUE'], shell=True)
        subprocess.call(['sudo /home/pi/Documents/ledBarOff.sh WHITE'], shell=True)
        subprocess.call(['sudo /home/pi/Documents/ledBarOn.sh RED'], shell=True)

    def setAllBarsOff(self):
        subprocess.call(['sudo /home/pi/Documents/ledBarOff.sh BLUE'], shell=True)
        subprocess.call(['sudo /home/pi/Documents/ledBarOff.sh WHITE'], shell=True)
        subprocess.call(['sudo /home/pi/Documents/ledBarOff.sh RED'], shell=True)

    def setAllBarsOn(self):
        subprocess.call(['sudo /home/pi/Documents/ledBarOn.sh BLUE'], shell=True)
        subprocess.call(['sudo /home/pi/Documents/ledBarOn.sh WHITE'], shell=True)
        subprocess.call(['sudo /home/pi/Documents/ledBarOn.sh RED'], shell=True)

    def configureFinishedRoutineAnimation(self):
        count = 0
        while(count<5):
            self.setAllBarsOff()
            time.sleep(1)
            self.setAllBarsOn()
            time.sleep(1)
            count = count+1
        self.setIdleState()
    
    def setErrorDetected(self):
        subprocess.call(['sudo /home/pi/Documents/ledStatusOn.sh ERR'], shell=True)
    
    def setErrorFixed(self):
        subprocess.call(['sudo /home/pi/Documents/ledStatusOff.sh ERR'], shell=True)

    def configureErrorAnimation(self):
        count = 0
        while(count<10):
            self.setErrorDetected()
            time.sleep(1)
            self.setErrorFixed()
            time.sleep(1)
            count = count+1
        self.setErrorDetected()
        
    def setVelocityControlLedOn(self):
        subprocess.call(['sudo /home/pi/Documents/ledStatusOn.sh VEL'], shell=True)

    def setVelocityControlLedOff(self):
        subprocess.call(['sudo /home/pi/Documents/ledStatusOff.sh VEL'], shell=True)

    def setTemperatureControlLedOn(self):
        subprocess.call(['sudo /home/pi/Documents/ledStatusOn.sh TEM'], shell=True)
    
    def setTemperatureControlLedOff(self):
        subprocess.call(['sudo /home/pi/Documents/ledStatusOff.sh TEM'], shell=True)

    def setPotentialControlLedOn(self):
        subprocess.call(['sudo /home/pi/Documents/ledStatusOn.sh POT'], shell=True)

    def setPotentialControlLedOff(self):
        subprocess.call(['sudo /home/pi/Documents/ledStatusOff.sh POT'], shell=True)

    def setExtractionControlLedOn(self):
        subprocess.call(['sudo /home/pi/Documents/ledStatusOn.sh EXT'], shell=True)

    def setExtractionControlLedOff(self):
        subprocess.call(['sudo /home/pi/Documents/ledStatusOff.sh EXT'], shell=True)

    def configureRunAllControl(self):
        self.setVelocityControlLedOn()
        self.setTemperatureControlLedOn()
        self.setPotentialControlLedOn()
        
    def configureStopAllControl(self):
        self.setVelocityControlLedOff()
        self.setTemperatureControlLedOff()
        self.setPotentialControlLedOff()

    def setAllLedsOn(self):
        subprocess.call(['sudo /home/pi/Documents/ledStatusOn PON'], shell=True)
        subprocess.call(['sudo /home/pi/Documents/ledStatusOn ERR'], shell=True)
        subprocess.call(['sudo /home/pi/Documents/ledStatusOn VEL'], shell=True)
        subprocess.call(['sudo /home/pi/Documents/ledStatusOn TEM'], shell=True)
        subprocess.call(['sudo /home/pi/Documents/ledStatusOn POT'], shell=True)
        subprocess.call(['sudo /home/pi/Documents/ledStatusOn EXT'], shell=True)
        
    def setAllLedsOff(self):
        subprocess.call(['sudo /home/pi/Documents/ledStatusOff PON'], shell=True)
        subprocess.call(['sudo /home/pi/Documents/ledStatusOff ERR'], shell=True)
        subprocess.call(['sudo /home/pi/Documents/ledStatusOff VEL'], shell=True)
        subprocess.call(['sudo /home/pi/Documents/ledStatusOff TEM'], shell=True)
        subprocess.call(['sudo /home/pi/Documents/ledStatusOff POT'], shell=True)
        subprocess.call(['sudo /home/pi/Documents/ledStatusOff EXT'], shell=True)
        
    def configurePowerDown(self):
        self.setAllBarsOff()
        self.setAllLedsOff()
        