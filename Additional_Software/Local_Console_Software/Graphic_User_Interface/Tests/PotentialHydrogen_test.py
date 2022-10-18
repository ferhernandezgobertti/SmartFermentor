import unittest
from Domain.PotentialHydrogen import PotentialHydrogen

class PotentialHydrogenTest(unittest.TestCase):

    def configureCorrectPotentialHydrogenData(self):
        potentialData = ["6.8", "1", "2", "30"]
        self.potentialReference = PotentialHydrogen(potentialData)

    def testIsObjectiveRightWhenTrue(self):
        self.configureCorrectPotentialHydrogenData()
        self.assertTrue(self.potentialReference.isObjectiveRight())

    def testIsObjectiveRightWhenFalseWithLess(self):
        self.configureCorrectPotentialHydrogenData()
        self.potentialReference.valueObjective = 1.0
        self.assertFalse(self.potentialReference.isObjectiveRight())

    def testIsObjectiveRightWhenFalseWithMore(self):
        self.configureCorrectPotentialHydrogenData()
        self.potentialReference.valueObjective = 14.0
        self.assertFalse(self.potentialReference.isObjectiveRight())

    def testIsUnitRightWhenTrueWithUnitA(self):
        self.configureCorrectPotentialHydrogenData()
        self.potentialReference.unit = "mL"
        self.assertTrue(self.potentialReference.isUnitRight())

    def testIsUnitRightWhenTrueWithUnitB(self):
        self.configureCorrectPotentialHydrogenData()
        self.potentialReference.unit = "cui"
        self.assertTrue(self.potentialReference.isUnitRight())

    def testIsUnitRightWhenTrueWithUnitC(self):
        self.configureCorrectPotentialHydrogenData()
        self.potentialReference.unit = "L"
        self.assertTrue(self.potentialReference.isUnitRight())

    def testIsUnitRightWhenFalse(self):
        self.configureCorrectPotentialHydrogenData()
        self.potentialReference.unit = "K"
        self.assertFalse(self.potentialReference.isUnitRight())

    def testIsPrecisionRightWhenTrue(self):
        self.configureCorrectPotentialHydrogenData()
        self.potentialReference.precision = 0.1
        self.assertTrue(self.potentialReference.isPrecisionRight())

    def testIsPrecisionRightWhenFalseWithLess(self):
        self.configureCorrectPotentialHydrogenData()
        self.potentialReference.precision = 0.02
        self.assertFalse(self.potentialReference.isPrecisionRight())

    def testIsPrecisionRightWhenFalseWithMore(self):
        self.configureCorrectPotentialHydrogenData()
        self.potentialReference.precision = 1.0
        self.assertFalse(self.potentialReference.isPrecisionRight())

    def testIsBurstModeRightWhenTrue(self):
        self.configureCorrectPotentialHydrogenData()
        self.assertTrue(self.potentialReference.isBurstModeRight())

    def testIsBurstModeRightWhenFalseWithLess(self):
        self.configureCorrectPotentialHydrogenData()
        self.potentialReference.burstMode = 0
        self.assertFalse(self.potentialReference.isBurstModeRight())

    def testIsBurstModeRightWhenFalseWithLess(self):
        self.configureCorrectPotentialHydrogenData()
        self.potentialReference.burstMode = 5
        self.assertFalse(self.potentialReference.isBurstModeRight())

    def testIsTimeBetweenDropsRightWhenTrue(self):
        self.configureCorrectPotentialHydrogenData()
        self.assertTrue(self.potentialReference.isTimeBetweenDropsRight())

    def testIsTimeBetweenDropsRightWhenFalseWithLess(self):
        self.configureCorrectPotentialHydrogenData()
        self.potentialReference.timeBetweenDrops = 0
        self.assertFalse(self.potentialReference.isTimeBetweenDropsRight())

    def testIsTimeBetweenDropsRightWhenFalseWithLess(self):
        self.configureCorrectPotentialHydrogenData()
        self.potentialReference.timeBetweenDrops = 3.0
        self.assertFalse(self.potentialReference.isTimeBetweenDropsRight())

    def testSetCustomizationWhenCheckingUnit(self):
        self.configureCorrectPotentialHydrogenData()
        self.potentialReference.setCustomization(["mL", 1.0, 1, 0.500, 10])
        self.assertEqual(self.potentialReference.unit, "mL")

    def testSetCustomizationWhenCheckingPrecision(self):
        self.configureCorrectPotentialHydrogenData()
        self.potentialReference.setCustomization(["mL", 1.0, 1, 0.500, 10])
        self.assertEqual(self.potentialReference.precision, 1.0)

    def testSetCustomizationWhenCheckingBurstMode(self):
        self.configureCorrectPotentialHydrogenData()
        self.potentialReference.setCustomization(["mL", 1.0, 1, 0.500, 10])
        self.assertEqual(self.potentialReference.burstMode, 1)

    def testSetCustomizationWhenCheckingTimeBetweenDrops(self):
        self.configureCorrectPotentialHydrogenData()
        self.potentialReference.setCustomization(["mL", 1.0, 1, 0.500, 10])
        self.assertEqual(self.potentialReference.timeBetweenDrops, 0.500)

    def testSetCustomizationWhenCheckingDataInterval(self):
        self.configureCorrectPotentialHydrogenData()
        self.potentialReference.setCustomization(["mL", 1.0, 1, 0.500, 10])
        self.assertEqual(self.potentialReference.dataInterval, 10)

    def testShowInformation(self):
        self.configureCorrectPotentialHydrogenData()
        self.assertEqual(self.potentialReference.showInformation(), " at 6.8 for 1 hours, 2 min, 30 sec")
