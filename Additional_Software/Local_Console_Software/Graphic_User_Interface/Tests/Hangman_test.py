import unittest
from Domain.Hangman import Hangman

class HangmanTest(unittest.TestCase):

    def testIsWholeAnswerRightWhenTrue(self):
        self.hangmanReference = Hangman()
        self.assertTrue(self.hangmanReference.isWholeAnswerRight('ESCHERICHIA COLI'))

    def testIsWholeAnswerRightWhenFalse(self):
        self.hangmanReference = Hangman()
        self.assertFalse(self.hangmanReference.isWholeAnswerRight('ACTINOMYCES'))

    def testGetCurrentSolution(self):
        self.hangmanReference = Hangman()
        self.hangmanReference.getCurrentSolution()
        self.assertEqual(self.hangmanReference.lettersCorrect, ['E','S','C','H','E','R','I','C','H','I','A',' ','C','O','L','I'])

    def testGetCurrentImageName(self):
        self.hangmanReference = Hangman()
        self.assertEqual(self.hangmanReference.getCurrentImageName(), 'initGame')

    def testSetWordState(self):
        self.hangmanReference = Hangman()
        self.hangmanReference.setWordState()
        self.assertEqual(self.hangmanReference.wordState, "_ _ _ _ _ _ _ _ _ _ _ / \n_ _ _ _ / \n")

    def testGetHintOfCurrentWordToGuess(self):
        self.hangmanReference = Hangman()
        self.assertEqual(self.hangmanReference.getHintOfCurrentWordToGuess(), 'Enterobacteriaceae')

    def testGetLettersMistakenWhenEmpty(self):
        self.hangmanReference = Hangman()
        self.assertEqual(self.hangmanReference.getLettersMistaken(), "")

    def testGetLettersMistakenWhenNotEmpty(self):
        self.hangmanReference = Hangman()
        self.hangmanReference.lettersMistaken = ["D", "Q", "Y"]
        self.assertEqual(self.hangmanReference.getLettersMistaken(), "D, Q, Y, ")

    def testUpdateWordState(self):
        self.hangmanReference = Hangman()
        self.hangmanReference.updateWordState()
        self.assertEqual(self.hangmanReference.wordState, "_ _ _ _ _ _ _ _ _ _ _ / \n_ _ _ _ ")

    def testIsLetterTypedCorrectWhenCorrect(self):
        self.hangmanReference = Hangman()
        self.assertTrue(self.hangmanReference.isLetterTypedCorrect("E"))

    def testIsLetterTypedCorrectWhenMultipleLetters(self):
        self.hangmanReference = Hangman()
        self.assertFalse(self.hangmanReference.isLetterTypedCorrect("ABCD"))

    def testIsLetterTypedCorrectWhenLetterNotAlphabetic(self):
        self.hangmanReference = Hangman()
        self.assertFalse(self.hangmanReference.isLetterTypedCorrect("9"))

    def testIsLetterTypedCorrectWhenNotInSolution(self):
        self.hangmanReference = Hangman()
        self.assertFalse(self.hangmanReference.isLetterTypedCorrect("W"))

    def testIsEveryLetterGuessedWhenTrue(self):
        self.hangmanReference = Hangman()
        self.hangmanReference.wordState = "E S C H E R I C H I A / \nC O L I / \n"
        self.assertTrue(self.hangmanReference.isEveryLetterGuessed())

    def testIsEveryLetterGuessedWhenFalse(self):
        self.hangmanReference = Hangman()
        self.hangmanReference.wordState = "E _ C _ E _ I C _ I A / \nC _ _ I / \n"
        self.assertFalse(self.hangmanReference.isEveryLetterGuessed())

    def testAddIncorrectLetter(self):
        self.hangmanReference = Hangman()
        self.hangmanReference.addIncorrectLetter("P")
        self.assertIn("P", self.hangmanReference.lettersMistaken)

    def testIsGameOverWhenTrue(self):
        self.hangmanReference = Hangman()
        self.hangmanReference.lettersMistaken = ["D", "W", "Z", "Y", "Q", "N"]
        self.assertTrue(self.hangmanReference.isGameOver())

    def testIsGameOverWhenFalse(self):
        self.hangmanReference = Hangman()
        self.assertFalse(self.hangmanReference.isGameOver())

    def testStartHangmanSequenceWhenCheckingWordState(self):
        self.hangmanReference = Hangman()
        sequenceInformation = self.hangmanReference.startHangmanSequence()
        self.assertIn("_ ", sequenceInformation[0])

    def testStartHangmanSequenceWhenCheckingHint(self):
        self.hangmanReference = Hangman()
        sequenceInformation = self.hangmanReference.startHangmanSequence()
        self.assertIn(sequenceInformation[1], self.hangmanReference.hints)
