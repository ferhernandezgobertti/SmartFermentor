import sys

class Magnitude():

    def __init__(self, magnitudeData):
        self.valueObjective = float(magnitudeData[0])
        self.duration = [int(magnitudeData[1]), int(magnitudeData[2]), int(magnitudeData[3])]
        self.unit = ""
        self.evolutionSlope = "Nominal"
        self.dataInterval = 10
        self.precision = 1.0

    def getDuration (self):
        return self.duration[0]*60*60+self.duration[1]*60+self.duration[2]

    def isDurationConfigurationCorrect(self):
        return self.duration[0]<=90 and self.duration[1]<=59 and self.duration[2]<=59

    def isDurationWithinLimits(self, durationLimits):
        currentDuration = self.getDuration()
        return currentDuration >= durationLimits[0] and currentDuration <= durationLimits[1]

    def isDurationRight(self, durationLimits):
        return self.isDurationWithinLimits(durationLimits) and self.isDurationConfigurationCorrect()

    def isEqualMagnitude(self, magnitudeToCompare):
        return self.valueObjective == magnitudeToCompare.valueObjective and self.duration == magnitudeToCompare.duration and self.unit == magnitudeToCompare.unit

    def isUnitSelected(self, unitSelected):
        return self.unit == str(unitSelected)

    def isDataIntervalRight(self):
        return self.dataInterval >= 1 and self.dataInterval <= 20

    def getInformationMagnitude(self):
        return "Objective: "+str(self.valueObjective)+" during "+str(self.getDuration())+" seconds"

    def loadJSONMagnitude(self, dataToLoad):
        print("CARGADO")
        #self.unit = dataToLoad['unit']
        #self.evolutionSlope = dataToLoad['evolutionSlope']
        #self.dataInterval = dataToLoad['dataInterval']
        #self.precision = dataToLoad['precision']
