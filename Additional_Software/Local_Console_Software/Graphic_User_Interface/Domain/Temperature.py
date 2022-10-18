import sys
from Domain.Magnitude import Magnitude

class Temperature(Magnitude):

    def __init__(self, temperatureData):
        super(Temperature,self).__init__(temperatureData)
        self.pumpStep = 5

    def isObjectiveRight(self):
        return self.valueObjective >= 10.0 and self.valueObjective <= 95.0

    def isUnitRight(self):
        return self.unit == "C" or self.unit == "K" or self.unit == "F"

    def isPrecisionRight(self):
        return self.precision >= 0.5 and self.precision <= 5.0

    def isPumpStepRight(self):
        return self.pumpStep >= 1 and self.pumpStep <= 5

    def setCustomization(self, customizationData):
        self.unit = customizationData[0]
        self.precision = customizationData[1]
        self.pumpStep = customizationData[2]
        self.evolutionSlope = customizationData[3]
        self.dataInterval = customizationData[4]

    def showInformation(self):
        return " at "+str(self.valueObjective)+" "+self.unit+" for "+str(self.duration[0])+" hours, "+str(self.duration[1])+" min, "+str(self.duration[2])+" sec"#(Total: "+str(int(self.getDuration()))+" sec)"
