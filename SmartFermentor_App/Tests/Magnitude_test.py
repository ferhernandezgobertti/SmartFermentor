import unittest
from Domain.Magnitude import Magnitude

class MagnitudeTest(unittest.TestCase):

    def configureCorrectMagnitudeData(self):
        magnitudeData = ["150", "10", "15", "20"]
        self.magnitudeReference = Magnitude(magnitudeData)

    def configureComparissonMagnitudeData(self):
        magnitudeData = ["150", "10", "15", "20"]
        self.magnitudeComparison = Magnitude(magnitudeData)

    def testGetDuration(self):
        self.configureCorrectMagnitudeData()
        self.assertEqual(self.magnitudeReference.getDuration(), 36920)

    def testIsDurationWithinLimitsWhenTrue(self):
        self.configureCorrectMagnitudeData()
        self.assertTrue(self.magnitudeReference.isDurationWithinLimits([200, 100000]))

    def testIsDurationWithinLimitsWhenFalseWithLess(self):
        self.configureCorrectMagnitudeData()
        self.magnitudeReference.duration = [0, 2, 20]
        self.assertFalse(self.magnitudeReference.isDurationWithinLimits([200, 100000]))

    def testIsDurationWithinLimitsWhenFalseWithMore(self):
        self.configureCorrectMagnitudeData()
        self.magnitudeReference.duration = [50, 50, 10]
        self.assertFalse(self.magnitudeReference.isDurationWithinLimits([200, 100000]))

    def testIsDurationConfigurationCorrectWhenTrue(self):
        self.configureCorrectMagnitudeData()
        self.assertTrue(self.magnitudeReference.isDurationConfigurationCorrect())

    def testIsDurationConfigurationCorrectWhenFalseWithWrongHours(self):
        self.configureCorrectMagnitudeData()
        self.magnitudeReference.duration = [99, 2, 20]
        self.assertFalse(self.magnitudeReference.isDurationConfigurationCorrect())

    def testIsDurationConfigurationCorrectWhenFalseWithWrongMinutes(self):
        self.configureCorrectMagnitudeData()
        self.magnitudeReference.duration = [2, 200, 10]
        self.assertFalse(self.magnitudeReference.isDurationConfigurationCorrect())

    def testIsDurationConfigurationCorrectWhenFalseWithWrongSeconds(self):
        self.configureCorrectMagnitudeData()
        self.magnitudeReference.duration = [5, 30, 100]
        self.assertFalse(self.magnitudeReference.isDurationConfigurationCorrect())

    def testIsDurationRightWhenTrue(self):
        self.configureCorrectMagnitudeData()
        self.assertTrue(self.magnitudeReference.isDurationRight([200, 100000]))

    def testIsDurationConfigurationCorrectWhenFalseWithWrongConfiguration(self):
        self.configureCorrectMagnitudeData()
        self.magnitudeReference.duration = [2, 200, 10]
        self.assertFalse(self.magnitudeReference.isDurationRight([200, 100000]))

    def testIsDurationConfigurationCorrectWhenFalseWithWrongWithinLimits(self):
        self.configureCorrectMagnitudeData()
        self.magnitudeReference.duration = [50, 30, 100]
        self.assertFalse(self.magnitudeReference.isDurationRight([200, 100000]))

    def testIsEqualMagnitudeWhenTrue(self):
        self.configureCorrectMagnitudeData()
        self.configureComparissonMagnitudeData()
        self.magnitudeReference.unit = "C"
        self.magnitudeComparison.unit = "C"
        self.assertTrue(self.magnitudeReference.isEqualMagnitude(self.magnitudeComparison))

    def testIsEqualMagnitudeWhenFalseWithDifferentObjective(self):
        self.configureCorrectMagnitudeData()
        self.configureComparissonMagnitudeData()
        self.magnitudeReference.valueObjective = 100
        self.magnitudeReference.unit = "C"
        self.magnitudeComparison.unit = "C"
        self.assertFalse(self.magnitudeReference.isEqualMagnitude(self.magnitudeComparison))

    def testIsEqualMagnitudeWhenFalseWithDifferentDuration(self):
        self.configureCorrectMagnitudeData()
        self.configureComparissonMagnitudeData()
        self.magnitudeReference.duration[0] = 20
        self.magnitudeReference.unit = "C"
        self.magnitudeComparison.unit = "C"
        self.assertFalse(self.magnitudeReference.isEqualMagnitude(self.magnitudeComparison))

    def testIsEqualMagnitudeWhenFalseWithDifferentUnit(self):
        self.configureCorrectMagnitudeData()
        self.configureComparissonMagnitudeData()
        self.magnitudeReference.unit = "C"
        self.magnitudeComparison.unit = "K"
        self.assertFalse(self.magnitudeReference.isEqualMagnitude(self.magnitudeComparison))

    def testIsUnitSelectedWhenTrue(self):
        self.configureCorrectMagnitudeData()
        self.magnitudeReference.unit = "C"
        self.assertTrue(self.magnitudeReference.isUnitSelected("C"))

    def testIsUnitSelectedWhenFalse(self):
        self.configureCorrectMagnitudeData()
        self.magnitudeReference.unit = "C"
        self.assertFalse(self.magnitudeReference.isUnitSelected("K"))

    def testIsDataIntervalRightWhenTrue(self):
        self.configureCorrectMagnitudeData()
        self.assertTrue(self.magnitudeReference.isDataIntervalRight())

    def testIsDataIntervalRightWhenFalseWithLess(self):
        self.configureCorrectMagnitudeData()
        self.magnitudeReference.dataInterval = 0
        self.assertFalse(self.magnitudeReference.isDataIntervalRight())

    def testIsDataIntervalRightWhenFalseWithMore(self):
        self.configureCorrectMagnitudeData()
        self.magnitudeReference.dataInterval = 30
        self.assertFalse(self.magnitudeReference.isDataIntervalRight())

    def testGetInformationMagnitude(self):
        self.configureCorrectMagnitudeData()
        self.assertEqual(self.magnitudeReference.getInformationMagnitude(), "Objective: 150.0 during 36920 seconds")
