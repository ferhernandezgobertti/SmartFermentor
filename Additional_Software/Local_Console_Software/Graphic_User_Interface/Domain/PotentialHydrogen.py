import sys
from Domain.Magnitude import Magnitude

class PotentialHydrogen(Magnitude):

    def __init__(self, potentialHydrogenData):
        super(PotentialHydrogen,self).__init__(potentialHydrogenData)
        self.burstMode = 1
        self.timeBetweenDrops = 0.500

    def isObjectiveRight(self):
        return self.valueObjective >= 2.0 and self.valueObjective <= 12.0

    def isUnitRight(self):
        return self.unit == "mL" or self.unit == "cui" or self.unit == "L"

    def isPrecisionRight(self):
        return self.precision >= 0.05 and self.precision <= 0.2

    def isBurstModeRight(self):
        return self.burstMode >= 1 and self.burstMode <= 4

    def isTimeBetweenDropsRight(self):
        return self.timeBetweenDrops >= 0.500 and self.timeBetweenDrops <= 2.0

    def setCustomization(self, customizationData):
        self.unit = customizationData[0]
        self.precision = customizationData[1]
        self.burstMode = customizationData[2]
        self.timeBetweenDrops = customizationData[3]
        self.dataInterval = customizationData[4]


    def showInformation(self):
        return " at "+str(self.valueObjective)+" for "+str(self.duration[0])+" hours, "+str(self.duration[1])+" min, "+str(self.duration[2])+" sec" #(Total: "+str(int(self.getDuration()))+" sec)"
