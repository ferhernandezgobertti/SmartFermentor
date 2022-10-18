import unittest
from Domain.Settings import Settings

class SettingsTest(unittest.TestCase):

    def testIsAllPreparationDoneWhenTrue(self):
        self.settingsReference = Settings()
        self.settingsReference.isConnectionChecked = True
        self.settingsReference.isCalibrated = True
        self.settingsReference.isLiquidExpulsed = True
        self.assertTrue(self.settingsReference.isAllPreparationDone())

    def testIsAllPreparationDoneWhenFalseWithSomeDone(self):
        self.settingsReference = Settings()
        self.settingsReference.isConnectionChecked = False
        self.settingsReference.isCalibrated = True
        self.settingsReference.isLiquidExpulsed = True
        self.assertFalse(self.settingsReference.isAllPreparationDone())

    def testIsAllPreparationDoneWhenFalseWithNoneDone(self):
        self.settingsReference = Settings()
        self.assertFalse(self.settingsReference.isAllPreparationDone())

    def testIsAllControlDoneWhenTrue(self):
        self.settingsReference = Settings()
        self.settingsReference.isVelocityControlOnFreeWheel = True
        self.settingsReference.isTemperatureControlOnFreeWheel = True
        self.settingsReference.isPotentialHydrogenControlOnFreeWheel = True
        self.assertTrue(self.settingsReference.isAllControlOnFreeWheel())

    def testIsAllControlDoneWhenFalseWithSomeDone(self):
        self.settingsReference = Settings()
        self.settingsReference.isVelocityControlOnFreeWheel = False
        self.settingsReference.isTemperatureControlOnFreeWheel = True
        self.settingsReference.isPotentialHydrogenControlOnFreeWheel = True
        self.assertFalse(self.settingsReference.isAllControlOnFreeWheel())

    def testIsAllControlDoneWhenFalseWithNoneDone(self):
        self.settingsReference = Settings()
        self.assertFalse(self.settingsReference.isAllControlOnFreeWheel())

    def testGetJSONDataSettings(self):
        self.settingsReference = Settings()
        jsonToVerify = { "connectionStatus": False, "calibrationStatus": False, "liquidStatus": False, "velocityFreeWheel": False, "temperatureFreeWheel": False, "potentialHydrogenFreeWheel": False, }
        self.assertEqual(self.settingsReference.getJSONData(), jsonToVerify)
