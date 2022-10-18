import sys, random
from datetime import date
from datetime import datetime

class Game():

    def __init__(self):
        self.currentRecord = [0, 0, 0, 0, 0]
        self.recordsUsersNames = ["NO PLAYER", "NO PLAYER", "NO PLAYER", "NO PLAYER", "NO PLAYER"]
        self.selectedWord = 0

    def setRandomPositionOfList(self, maxNumber):
        self.selectedWord = random.randint(0,maxNumber-1)
        print("RANDOM WORD: ", self.selectedWord)

    def isScoreOnePersonalRecord(self, interestedUser, gameNumber, gamePoints):
        return gamePoints > interestedUser.gamesScore[gameNumber]

    def isScoreOneGlobalRecord(self, interestedUser, gameNumber):
        return interestedUser.gamesScore[gameNumber] > self.currentRecord[len(self.currentRecord)-1]

    def getPositionOfScore(self, interestedUser, gameNumber):
        position = 0
        for eachRecord in self.currentRecord:
            if(interestedUser.gamesScore[gameNumber] > eachRecord):
                break
            position = position + 1
        return position

    def setRecordData(self, interestedUser, gameNumber):
        if(self.isScoreOneGlobalRecord(interestedUser, gameNumber)):
            position = self.getPositionOfScore(interestedUser, gameNumber)
            self.currentRecord.insert(position, interestedUser.gamesScore[gameNumber])
            self.currentRecord.remove(self.currentRecord[len(self.currentRecord)-1])
            self.recordsUserNames.insert(position, interestedUser.getCompleteNameSurname())
            self.recordsUserNames.remove(self.recordsUserNames[len(self.recordsUserNames)-1])

    def getJSONData(self):
        gameData = {
            "records":self.currentRecord,
            "recordsUsers":self.recordsUsersNames,
         }
        return gameData

    def loadJSONData(self, gameData):
        self.currentRecord = gameData['records']
        self.recordsUserNames = gameData['recordsUsers']
