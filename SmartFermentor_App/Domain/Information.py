import sys, time
from datetime import datetime, date, timedelta

class Information():

    def __init__(self):
        self.usersRegistered = [10, 20] # [PROFESSORS, STUDENTS]
        self.fermentationsDone = [30, 5] # [Fermentations Initiated, Fermentations Continued]
        self.timesControlsRealized = [10, 5, 5, 5, 5, 2, 3] # [VEL Control, TEM Control, POT Control, VEL+TEM Control, TEM+POT Control, VEL+POT Control, VEL+TEM+POT Control]
        self.timesVerificationsDone = [20, 4, 2, 4] # [NONE Verified, CON Verified, CAL Verified, CON+CAL Verified]
        self.timesGamesPlayed = [0, 0, 0] # [GAME Played, GAME2 Played, GAME3 Played]
        self.informationDate = date.today()

    def getJSONData(self):
        informationData = {
            "usersRegistered":self.usersRegistered,
            "fermentationsDone":self.fermentationsDone,
            "controlsRealized":self.timesControlsRealized,
            "verificationsDone":self.timesVerificationsDone,
            "gamesPlayed": self.timesGamesPlayed,
            "date": self.informationDate.strftime("%m/%y")
         }
        return informationData

    def updateInformationTimesVerificationsDone(self, currentVerifications):
        if(currentVerifications[0] and currentVerifications[1]):
            self.addFermentationWithConnectionAndCalibrationVerified()
        if(not currentVerifications[0] and currentVerifications[1]):
            self.addFermentationWithOnlyCalibrationVerified()
        if(currentVerifications[0] and not currentVerifications[1]):
            self.addFermentationWithOnlyConnectionVerified()
        if(not currentVerifications[0] and not currentVerifications[1]):
            self.addFermentationWithNothingVerified()

    def getParticularInformation(self):
        return "\nDATE: "+self.informationDate.strftime("%m/%y")+"\nUsers Registered: "+str(self.usersRegistered[0])+" Professors and "+str(self.usersRegistered[1])+" Students.\nFermentations: "+str(self.fermentationsDone[0])+" Initiated and "+str(self.fermentationsDone[1])+" Continued.\nFrom those Fermentations: "+str(self.timesControlsRealized[0])+" only controlled Velocity, "+str(self.timesControlsRealized[1])+" only controlled Temperature, "+str(self.timesControlsRealized[2])+" only controlled Potential Hydrogen.\nLikewise, "+str(self.timesControlsRealized[3])+" controlled Velocity&Temperature, "+str(self.timesControlsRealized[4])+" controlled Velocity&Potential, "+str(self.timesControlsRealized[5])+" controlled Temperature&Potential. The other "+str(self.timesControlsRealized[6])+" Fermentations controlled ALL Magnitudes.\nConsidering the Fermentations that where initialized, "+str(self.timesVerificationsDone[1])+" had only the Connection verified, while "+str(self.timesVerificationsDone[2])+" had only the Calibration verified. However, "+str(self.timesVerificationsDone[3])+" Fermentations verified both Connection and Calibration.\nRegarding the Entertainment, this month the Scrambled Game was played "+str(self.timesGamesPlayed[0])+" times, meanwhile the Hangman Game was played "+str(self.timesGamesPlayed[1])+" times and the Trivia Game was played "+str(self.timesGamesPlayed[2])+" times.\n"

    def getDateIdentifier(self):
        monthsName = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        return monthsName[self.informationDate.month-1]+"\n"+str(self.informationDate.year)

    def addProfessorRegistered (self):
        self.usersRegistered[0] = self.usersRegistered[0] + 1

    def addStudentRegistered (self):
        self.usersRegistered[1] = self.usersRegistered[1] + 1

    def addFermentationInitiated (self):
        self.fermentationsDone[0] = self.fermentationsDone[0] + 1

    def addFermentationContinued (self):
        self.fermentationsDone[1] = self.fermentationsDone[1] + 1

    def addFermentationWithOnlyVelocityControl (self):
        self.timesControlsRealized[0] = self.timesControlsRealized[0] + 1

    def addFermentationWithOnlyTemperatureControl (self):
        self.timesControlsRealized[1] = self.timesControlsRealized[1] + 1

    def addFermentationWithOnlyPotentialControl (self):
        self.timesControlsRealized[2] = self.timesControlsRealized[2] + 1

    def addFermentationWithVelocityAndTemperatureControl (self):
        self.timesControlsRealized[3] = self.timesControlsRealized[3] + 1

    def addFermentationWithVelocityAndPotentialControl (self):
        self.timesControlsRealized[4] = self.timesControlsRealized[4] + 1

    def addFermentationWithTemperatureAndPotentialControl (self):
        self.timesControlsRealized[5] = self.timesControlsRealized[5] + 1

    def addFermentationWithAllControls (self):
        self.timesControlsRealized[6] = self.timesControlsRealized[6] + 1

    def addFermentationWithNothingVerified(self):
        self.timesVerificationsDone[0] = self.timesVerificationsDone[0] + 1

    def addFermentationWithOnlyConnectionVerified(self):
        self.timesVerificationsDone[1] = self.timesVerificationsDone[1] + 1

    def addFermentationWithOnlyCalibrationVerified(self):
        self.timesVerificationsDone[2] = self.timesVerificationsDone[2] + 1

    def addFermentationWithConnectionAndCalibrationVerified(self):
        self.timesVerificationsDone[3] = self.timesVerificationsDone[3] + 1

    def addTimesScrambledPlayed(self):
        self.timesGamesPlayed[0] = self.timesGamesPlayed[0] + 1

    def addTimesHangmanPlayed(self):
        self.timesGamesPlayed[1] = self.timesGamesPlayed[1] + 1

    def addTimesTriviaPlayed(self):
        self.timesGamesPlayed[2] = self.timesGamesPlayed[2] + 1

    def getTotalFermentationsOfMonth(self):
        return self.fermentationsDone[0] + self.fermentationsDone[1]
