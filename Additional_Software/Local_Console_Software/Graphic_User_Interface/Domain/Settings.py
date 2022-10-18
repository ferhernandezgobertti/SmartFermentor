import sys

class Settings():

    def __init__(self):
        self.isConnectionChecked = False
        self.isCalibrated = False
        self.isLiquidExpulsed = False
        self.isVelocityControlOnFreeWheel = False
        self.isTemperatureControlOnFreeWheel = False
        self.isPotentialHydrogenControlOnFreeWheel = False
        self.isFermentationContinuing = False

    def isAllPreparationDone(self):
        return self.isConnectionChecked and self.isCalibrated and self.isLiquidExpulsed

    def isAllControlOnFreeWheel(self):
        return self.isVelocityControlOnFreeWheel and self.isTemperatureControlOnFreeWheel and self.isPotentialHydrogenControlOnFreeWheel

    def getJSONData(self):
        settingsData = {
            "connectionStatus": self.isConnectionChecked,
            "calibrationStatus": self.isCalibrated,
            "liquidStatus": self.isLiquidExpulsed,
            "velocityFreeWheel": self.isVelocityControlOnFreeWheel,
            "temperatureFreeWheel": self.isTemperatureControlOnFreeWheel,
            "potentialHydrogenFreeWheel": self.isPotentialHydrogenControlOnFreeWheel,
         }
        return settingsData

    def loadJSONData(self, dataToLoad):
        self.isConnectionChecked = dataToLoad['connectionStatus']
        self.isCalibrated = dataToLoad['calibrationStatus']
        self.isLiquidExpulsed = dataToLoad['liquidStatus']
        self.isVelocityControlOnFreeWheel = dataToLoad['velocityFreeWheel']
        self.isTemperatureControlOnFreeWheel = dataToLoad['temperatureFreeWheel']
        self.isPotentialHydrogenControlOnFreeWheel = dataToLoad['potentialHydrogenFreeWheel']
