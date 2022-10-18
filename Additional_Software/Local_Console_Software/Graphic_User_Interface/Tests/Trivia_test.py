import unittest
from Domain.Trivia import Trivia

class TriviaTest(unittest.TestCase):

    def testIsOptionCorrectWhenTrue(self):
        self.triviaReference = Trivia()
        self.assertTrue(self.triviaReference.isOptionCorrect("Genes of another organism"), "Genes of another organism")

    def testIsOptionCorrectWhenFalse(self):
        self.triviaReference = Trivia()
        self.assertFalse(self.triviaReference.isOptionCorrect("Genes with no function to perform"), "Genes of another organism")

    def testGetOptionDataWhenCorrect(self):
        self.triviaReference = Trivia()
        self.assertEqual(self.triviaReference.getOptionData(1), "Genes of another organism")

    def testGetOptionDataWhenIncorrectA(self):
        self.triviaReference = Trivia()
        self.assertEqual(self.triviaReference.getOptionData(2), "Genes with no function to perform")

    def testGetOptionDataWhenIncorrectB(self):
        self.triviaReference = Trivia()
        self.assertEqual(self.triviaReference.getOptionData(3), "Genes in transposition")

    def testGetOptionDataWhenIncorrectC(self):
        self.triviaReference = Trivia()
        self.assertEqual(self.triviaReference.getOptionData(4), "No gene")

    def testGetRandomOrderOptionsWhenCheckingCorrectAnswer(self):
        self.triviaReference = Trivia()
        self.assertIn("Genes of another organism", self.triviaReference.getRandomOrderOfOptions())

    def testGetRandomOrderOptionsWhenCheckingIncorrectA(self):
        self.triviaReference = Trivia()
        self.assertIn("Genes with no function to perform", self.triviaReference.getRandomOrderOfOptions())

    def testGetRandomOrderOptionsWhenCheckingIncorrectB(self):
        self.triviaReference = Trivia()
        self.assertIn("Genes in transposition", self.triviaReference.getRandomOrderOfOptions())

    def testGetRandomOrderOptionsWhenCheckingIncorrectC(self):
        self.triviaReference = Trivia()
        self.assertIn("No gene", self.triviaReference.getRandomOrderOfOptions())

    def testGetCurrentQuestion(self):
        self.triviaReference = Trivia()
        self.assertEqual(self.triviaReference.getCurrentQuestion(), "Transgenic plants are plants having:")

    def testStartTriviaSequenceWhenCheckingQuestion(self):
        self.triviaReference = Trivia()
        gameInformation = self.triviaReference.startTriviaSequence()
        self.assertEqual(self.triviaReference.questionsToAsk[self.triviaReference.selectedWord], gameInformation[0])

    def testStartTriviaSequenceWhenCheckingCorrectAnswer(self):
        self.triviaReference = Trivia()
        gameInformation = self.triviaReference.startTriviaSequence()
        self.assertIn(self.triviaReference.correctOption[self.triviaReference.selectedWord], gameInformation)

    def testStartTriviaSequenceWhenCheckingIncorrectA(self):
        self.triviaReference = Trivia()
        gameInformation = self.triviaReference.startTriviaSequence()
        self.assertIn(self.triviaReference.wrongOptionA[self.triviaReference.selectedWord], gameInformation)

    def testStartTriviaSequenceWhenCheckingIncorrectB(self):
        self.triviaReference = Trivia()
        gameInformation = self.triviaReference.startTriviaSequence()
        self.assertIn(self.triviaReference.wrongOptionB[self.triviaReference.selectedWord], gameInformation)

    def testStartTriviaSequenceWhenCheckingIncorrectC(self):
        self.triviaReference = Trivia()
        gameInformation = self.triviaReference.startTriviaSequence()
        self.assertIn(self.triviaReference.wrongOptionC[self.triviaReference.selectedWord], gameInformation)
