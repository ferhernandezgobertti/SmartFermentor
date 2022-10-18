import unittest
from Domain.Temperature import Temperature

class TemperatureTest(unittest.TestCase):

    def configureCorrectTemperatureData(self):
        temperatureData = ["42", "3", "10", "20"]
        self.temperatureReference = Temperature(temperatureData)

    def testIsObjectiveRightWhenTrue(self):
        self.configureCorrectTemperatureData()
        self.assertTrue(self.temperatureReference.isObjectiveRight())

    def testIsObjectiveRightWhenFalseWithLess(self):
        self.configureCorrectTemperatureData()
        self.temperatureReference.valueObjective = 1.0
        self.assertFalse(self.temperatureReference.isObjectiveRight())

    def testIsObjectiveRightWhenFalseWithMore(self):
        self.configureCorrectTemperatureData()
        self.temperatureReference.valueObjective = 100.0
        self.assertFalse(self.temperatureReference.isObjectiveRight())

    def testIsUnitRightWhenTrueWithUnitA(self):
        self.configureCorrectTemperatureData()
        self.temperatureReference.unit = "C"
        self.assertTrue(self.temperatureReference.isUnitRight())

    def testIsUnitRightWhenTrueWithUnitB(self):
        self.configureCorrectTemperatureData()
        self.temperatureReference.unit = "K"
        self.assertTrue(self.temperatureReference.isUnitRight())

    def testIsUnitRightWhenTrueWithUnitC(self):
        self.configureCorrectTemperatureData()
        self.temperatureReference.unit = "F"
        self.assertTrue(self.temperatureReference.isUnitRight())

    def testIsUnitRightWhenFalse(self):
        self.configureCorrectTemperatureData()
        self.temperatureReference.unit = "RPM"
        self.assertFalse(self.temperatureReference.isUnitRight())

    def testIsPrecisionRightWhenTrue(self):
        self.configureCorrectTemperatureData()
        self.temperatureReference.precision = 1.0
        self.assertTrue(self.temperatureReference.isPrecisionRight())

    def testIsPrecisionRightWhenFalseWithLess(self):
        self.configureCorrectTemperatureData()
        self.temperatureReference.precision = 0.2
        self.assertFalse(self.temperatureReference.isPrecisionRight())

    def testIsPrecisionRightWhenFalseWithMore(self):
        self.configureCorrectTemperatureData()
        self.temperatureReference.precision = 10.0
        self.assertFalse(self.temperatureReference.isPrecisionRight())

    def testIsPumpStepRightWhenTrue(self):
        self.configureCorrectTemperatureData()
        self.assertTrue(self.temperatureReference.isPumpStepRight())

    def testIsPumpStepRightWhenFalseWithLess(self):
        self.configureCorrectTemperatureData()
        self.temperatureReference.pumpStep = 0
        self.assertFalse(self.temperatureReference.isPumpStepRight())

    def testIsPumpStepRightWhenFalseWithLess(self):
        self.configureCorrectTemperatureData()
        self.temperatureReference.pumpStep = 10
        self.assertFalse(self.temperatureReference.isPumpStepRight())

    def testSetCustomizationWhenCheckingUnit(self):
        self.configureCorrectTemperatureData()
        self.temperatureReference.setCustomization(["K", 1.0, 5, "Normal", 10])
        self.assertEqual(self.temperatureReference.unit, "K")

    def testSetCustomizationWhenCheckingPrecision(self):
        self.configureCorrectTemperatureData()
        self.temperatureReference.setCustomization(["K", 1.0, 5, "Normal", 10])
        self.assertEqual(self.temperatureReference.precision, 1.0)

    def testSetCustomizationWhenCheckingPumpStep(self):
        self.configureCorrectTemperatureData()
        self.temperatureReference.setCustomization(["K", 1.0, 5, "Normal", 10])
        self.assertEqual(self.temperatureReference.pumpStep, 5)

    def testSetCustomizationWhenCheckingEvolutionSlope(self):
        self.configureCorrectTemperatureData()
        self.temperatureReference.setCustomization(["K", 1.0, 5, "Normal", 10])
        self.assertEqual(self.temperatureReference.evolutionSlope, "Normal")

    def testSetCustomizationWhenCheckingDataInterval(self):
        self.configureCorrectTemperatureData()
        self.temperatureReference.setCustomization(["K", 1.0, 5, "Normal", 10])
        self.assertEqual(self.temperatureReference.dataInterval, 10)

    def testShowInformation(self):
        self.configureCorrectTemperatureData()
        self.temperatureReference.unit = "C"
        self.assertEqual(self.temperatureReference.showInformation(), " at 42.0 C for 3 hours, 10 min, 20 sec")
