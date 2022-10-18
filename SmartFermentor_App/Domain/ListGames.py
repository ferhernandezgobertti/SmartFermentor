import sys, time
from datetime import datetime, date, timedelta
from Domain.Scrambled import Scrambled
from Domain.Hangman import Hangman
from Domain.Trivia import Trivia

class ListGames():

    def __init__(self):
        self.scrambledData = Scrambled()
        self.hangmanData = Hangman()
        self.triviaData = Trivia()

    def getJSONData(self):
        gamesData = {
            "scrambled":self.scrambledData.getJSONData(),
            "hangman":self.hangmanData.getJSONData(),
            "trivia":self.triviaData.getJSONData(),
         }
        return gamesData

    def loadJSONData(self, gamesData):
        self.scrambledData.loadJSONData(gamesData['scrambled'])
        self.hangmanData.loadJSONData(gamesData['hangman'])
        self.triviaData.loadJSONData(gamesData['trivia'])
        
