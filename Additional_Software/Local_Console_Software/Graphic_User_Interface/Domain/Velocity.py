import sys
from Domain.Magnitude import Magnitude

class Velocity(Magnitude):

    def __init__(self, velocityData):
        super(Velocity,self).__init__(velocityData)
        self.direction = "AntiCLK"
        # RPM

    def isObjectiveRight(self):
        return self.valueObjective >= 180 and self.valueObjective <=800

    def isUnitRight(self):
        return self.unit == "RPM" or self.unit == "RAD/S" or self.unit == "M/S"

    def isPrecisionRight(self):
        return self.precision >= 1.0 and self.precision <= 5.0

    def isDirectionRight(self):
        return self.direction == "AntiCLK" or self.direction == "CLK"

    def setCustomization(self, customizationData):
        self.unit = customizationData[0]
        self.precision = customizationData[1]
        self.evolutionSlope = customizationData[2]
        self.direction = customizationData[3]
        self.dataInterval = customizationData[4]

    def showInformation(self):
        return " spin at "+str(self.valueObjective)+" RPM for "+str(self.duration[0])+" hours, "+str(self.duration[1])+" min, "+str(self.duration[2])+" sec" #(Total: "+str(int(self.getDuration()))+" sec)"
