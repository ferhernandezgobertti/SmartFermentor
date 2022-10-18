import unittest
from Domain.User import User
from Domain.Game import Game

class GameTest(unittest.TestCase):

    def configureInterestedUserData(self):
        userData = ["173631", "HerisHisis.2", "Fernando", "Hernandez", "ferhernagu@gmail.com", "98742547", "Canelones 1267", "4.851.112-6", "04/04/1996"]
        self.interestedUser = User(userData)
        self.interestedUser.gamesScore = [50, 50, 50]

    def testSetRandomPositionOfListWhenLess(self):
        self.gameReference = Game()
        self.gameReference.setRandomPositionOfList(50)
        self.assertLess(self.gameReference.selectedWord, 50)

    def testSetRandomPositionOfListWhenMore(self):
        self.gameReference = Game()
        self.gameReference.setRandomPositionOfList(50)
        self.assertGreater(self.gameReference.selectedWord, 0)

    def testIsScoreOnePersonalRecordWhenTrue(self):
        self.gameReference = Game()
        self.configureInterestedUserData()
        self.assertTrue(self.gameReference.isScoreOnePersonalRecord(self.interestedUser, 0, 100))

    def testIsScoreOnePersonalRecordWhenFalse(self):
        self.gameReference = Game()
        self.configureInterestedUserData()
        self.assertFalse(self.gameReference.isScoreOnePersonalRecord(self.interestedUser, 0, 0))

    def testIsScoreOneGlobalRecordWhenTrue(self):
        self.gameReference = Game()
        self.configureInterestedUserData()
        self.assertTrue(self.gameReference.isScoreOneGlobalRecord(self.interestedUser, 0))

    def testIsScoreOneGlobalRecordWhenFalse(self):
        self.gameReference = Game()
        self.gameReference.currentRecord = [200, 100, 90, 80, 70]
        self.configureInterestedUserData()
        self.assertFalse(self.gameReference.isScoreOneGlobalRecord(self.interestedUser, 0))

    def testGetPositionOfScoreWhenMiddleArray(self):
        self.gameReference = Game()
        self.gameReference.currentRecord = [200, 100, 90, 40, 20]
        self.configureInterestedUserData()
        self.assertEqual(self.gameReference.getPositionOfScore(self.interestedUser, 0), 3)

    def testGetPositionOfScoreWhenBeginArray(self):
        self.gameReference = Game()
        self.gameReference.currentRecord = [40, 30, 20, 10, 0]
        self.configureInterestedUserData()
        self.assertEqual(self.gameReference.getPositionOfScore(self.interestedUser, 0), 0)

    def testGetPositionOfScoreWhenEndArray(self):
        self.gameReference = Game()
        self.gameReference.currentRecord = [200, 100, 90, 60, 0]
        self.configureInterestedUserData()
        self.assertEqual(self.gameReference.getPositionOfScore(self.interestedUser, 0), 4)

    def testGetJSONDataWhenGame(self):
        self.gameReference = Game()
        jsonToVerify = { "records":[0, 0, 0, 0, 0], "recordsUsers":["NO PLAYER", "NO PLAYER", "NO PLAYER", "NO PLAYER", "NO PLAYER"] }
        self.assertEqual(self.gameReference.getJSONData(), jsonToVerify)
