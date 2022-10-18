import unittest
from Domain.Velocity import Velocity

class VelocityTest(unittest.TestCase):

    def configureCorrectVelocityData(self):
        velocityData = ["400", "10", "15", "20"]
        self.velocityReference = Velocity(velocityData)

    def testIsObjectiveRightWhenTrue(self):
        self.configureCorrectVelocityData()
        self.assertTrue(self.velocityReference.isObjectiveRight())

    def testIsObjectiveRightWhenFalseWithLess(self):
        self.configureCorrectVelocityData()
        self.velocityReference.valueObjective = 100.0
        self.assertFalse(self.velocityReference.isObjectiveRight())

    def testIsObjectiveRightWhenFalseWithMore(self):
        self.configureCorrectVelocityData()
        self.velocityReference.valueObjective = 900.0
        self.assertFalse(self.velocityReference.isObjectiveRight())

    def testIsUnitRightWhenTrueWithUnitA(self):
        self.configureCorrectVelocityData()
        self.velocityReference.unit = "RPM"
        self.assertTrue(self.velocityReference.isUnitRight())

    def testIsUnitRightWhenTrueWithUnitB(self):
        self.configureCorrectVelocityData()
        self.velocityReference.unit = "RAD/S"
        self.assertTrue(self.velocityReference.isUnitRight())

    def testIsUnitRightWhenTrueWithUnitC(self):
        self.configureCorrectVelocityData()
        self.velocityReference.unit = "M/S"
        self.assertTrue(self.velocityReference.isUnitRight())

    def testIsUnitRightWhenFalse(self):
        self.configureCorrectVelocityData()
        self.velocityReference.unit = "C"
        self.assertFalse(self.velocityReference.isUnitRight())

    def testIsPrecisionRightWhenTrue(self):
        self.configureCorrectVelocityData()
        self.velocityReference.precision = 1.0
        self.assertTrue(self.velocityReference.isPrecisionRight())

    def testIsPrecisionRightWhenFalseWithLess(self):
        self.configureCorrectVelocityData()
        self.velocityReference.precision = 0.2
        self.assertFalse(self.velocityReference.isPrecisionRight())

    def testIsPrecisionRightWhenFalseWithMore(self):
        self.configureCorrectVelocityData()
        self.velocityReference.precision = 10.0
        self.assertFalse(self.velocityReference.isPrecisionRight())

    def testIsDirectionRightWhenTrueWitCLK(self):
        self.configureCorrectVelocityData()
        self.assertTrue(self.velocityReference.isDirectionRight())

    def testIsDirectionRightWhenTrueWithAntiCLK(self):
        self.configureCorrectVelocityData()
        self.velocityReference.direction = "AntiCLK"
        self.assertTrue(self.velocityReference.isDirectionRight())

    def testIsDirectionRightWhenFalse(self):
        self.configureCorrectVelocityData()
        self.velocityReference.direction = "C"
        self.assertFalse(self.velocityReference.isDirectionRight())

    def testSetCustomizationWhenCheckingUnit(self):
        self.configureCorrectVelocityData()
        self.velocityReference.setCustomization(["RPM", 1.0, "Normal", "AntiCLK", 10])
        self.assertEqual(self.velocityReference.unit, "RPM")

    def testSetCustomizationWhenCheckingPrecision(self):
        self.configureCorrectVelocityData()
        self.velocityReference.setCustomization(["RPM", 1.0, "Normal", "AntiCLK", 10])
        self.assertEqual(self.velocityReference.precision, 1.0)

    def testSetCustomizationWhenCheckingEvolutionSlope(self):
        self.configureCorrectVelocityData()
        self.velocityReference.setCustomization(["RPM", 1.0, "Normal", "AntiCLK", 10])
        self.assertEqual(self.velocityReference.evolutionSlope, "Normal")

    def testSetCustomizationWhenCheckingDirection(self):
        self.configureCorrectVelocityData()
        self.velocityReference.setCustomization(["RPM", 1.0, "Normal", "AntiCLK", 10])
        self.assertEqual(self.velocityReference.direction, "AntiCLK")

    def testSetCustomizationWhenCheckingDataInterval(self):
        self.configureCorrectVelocityData()
        self.velocityReference.setCustomization(["RPM", 1.0, "Normal", "AntiCLK", 10])
        self.assertEqual(self.velocityReference.dataInterval, 10)

    def testShowInformation(self):
        self.configureCorrectVelocityData()
        self.assertEqual(self.velocityReference.showInformation(), " spin at 400.0 RPM for 10 hours, 15 min, 20 sec")
