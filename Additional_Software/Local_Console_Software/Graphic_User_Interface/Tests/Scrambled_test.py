import unittest
from Domain.Scrambled import Scrambled

class ScrambledTest(unittest.TestCase):

    def testScrambleSelectedWord(self):
        self.scrambledReference = Scrambled()
        self.assertNotEqual(self.scrambledReference.scrambleSelectedWord(self.scrambledReference.organismsWords[self.scrambledReference.selectedWord]), self.scrambledReference.organismsWords[self.scrambledReference.selectedWord])

    def testGetSelectedImageName(self):
        self.scrambledReference = Scrambled()
        self.assertEqual(self.scrambledReference.getSelectedImageName(), 'Image01')

    def testGetScrambledRegisteredDataWhenCheckingOrganismsWord(self):
        self.scrambledReference = Scrambled()
        self.assertNotEqual(self.scrambledReference.getScrambledRegisteredData()[0], self.scrambledReference.organismsWords[self.scrambledReference.selectedWord])

    def testGetScrambledRegisteredDataWhenCheckingFamiliesWord(self):
        self.scrambledReference = Scrambled()
        self.assertNotEqual(self.scrambledReference.getScrambledRegisteredData()[1], self.scrambledReference.familiesWords[self.scrambledReference.selectedWord])

    def testGetScrambledSolutionWordsWhenCheckingOrganismsSolution(self):
        self.scrambledReference = Scrambled()
        self.assertEqual(self.scrambledReference.getScrambledSolutionWords()[0], self.scrambledReference.organismsWords[self.scrambledReference.selectedWord])

    def testGetScrambledSolutionWordsWhenCheckingFamiliesSolution(self):
        self.scrambledReference = Scrambled()
        self.assertEqual(self.scrambledReference.getScrambledSolutionWords()[1], self.scrambledReference.familiesWords[self.scrambledReference.selectedWord])

    def testVerifyOrganismsEntryWhenTrue(self):
        self.scrambledReference = Scrambled()
        self.assertTrue(self.scrambledReference.verifyOrganismsEntry('Escherichia Coli'))

    def testVerifyOrganismsEntryWhenFalse(self):
        self.scrambledReference = Scrambled()
        self.assertFalse(self.scrambledReference.verifyOrganismsEntry('Actinomyces'))

    def testVerifyFamiliesEntryWhenTrue(self):
        self.scrambledReference = Scrambled()
        self.assertTrue(self.scrambledReference.verifyFamiliesEntry('Enterobacteriaceae'))

    def testVerifyFamiliesEntryWhenFalse(self):
        self.scrambledReference = Scrambled()
        self.assertFalse(self.scrambledReference.verifyFamiliesEntry('Actinomycetaceae'))

    def testStartScrambledSequenceWhenCheckingOrganismsWord(self):
        self.scrambledReference = Scrambled()
        self.assertNotEqual(self.scrambledReference.startScrambledSequence()[0], self.scrambledReference.organismsWords[self.scrambledReference.selectedWord])

    def testStartScrambledSequenceWhenCheckingFamiliesWord(self):
        self.scrambledReference = Scrambled()
        self.assertNotEqual(self.scrambledReference.startScrambledSequence()[1], self.scrambledReference.familiesWords[self.scrambledReference.selectedWord])
