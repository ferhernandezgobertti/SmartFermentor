import unittest
from Domain.Information import Information

class InformationTest(unittest.TestCase):

    def configureInstanceOfInformation(self):
        self.informationReference = Information()
        self.informationReference.usersRegistered = [10, 20] # [PROFESSORS, STUDENTS]
        self.informationReference.fermentationsDone = [30, 5] # [Fermentations Initiated, Fermentations Continued]
        self.informationReference.timesControlsRealized = [10, 5, 5, 5, 5, 2, 3] # [VEL Control, TEM Control, POT Control, VEL+TEM Control, TEM+POT Control, VEL+POT Control, VEL+TEM+POT Control]
        self.informationReference.timesVerificationsDone = [20, 4, 2, 4] # [NONE Verified, CON Verified, CAL Verified, CON+CAL Verified]
        self.informationReference.timesGamesPlayed = [10, 5, 12] # [GAME Played, GAME2 Played, GAME3 Played]

    def testUpdateInformationTimesVerificationsDoneWhenNothingVerified(self):
        self.configureInstanceOfInformation()
        self.informationReference.updateInformationTimesVerificationsDone([False, False])
        self.assertEqual(self.informationReference.timesVerificationsDone[0], 21)

    def testUpdateInformationTimesVerificationsDoneWhenConnectionVerified(self):
        self.configureInstanceOfInformation()
        self.informationReference.updateInformationTimesVerificationsDone([True, False])
        self.assertEqual(self.informationReference.timesVerificationsDone[1], 5)

    def testUpdateInformationTimesVerificationsDoneWhenCalibrationVerified(self):
        self.configureInstanceOfInformation()
        self.informationReference.updateInformationTimesVerificationsDone([False, True])
        self.assertEqual(self.informationReference.timesVerificationsDone[2], 3)

    def testUpdateInformationTimesVerificationsDoneWhenAllVerified(self):
        self.configureInstanceOfInformation()
        self.informationReference.updateInformationTimesVerificationsDone([True, True])
        self.assertEqual(self.informationReference.timesVerificationsDone[3], 5)

    def testGetParticularInformation(self):
        self.configureInstanceOfInformation()
        self.assertEqual(self.informationReference.getParticularInformation(), "\nDATE: "+self.informationReference.informationDate.strftime("%m/%y")+"\nUsers Registered: 10 Professors and 20 Students.\nFermentations: 30 Initiated and 5 Continued.\nFrom those Fermentations: 10 only controlled Velocity, 5 only controlled Temperature, 5 only controlled Potential Hydrogen.\nLikewise, 5 controlled Velocity&Temperature, 5 controlled Velocity&Potential, 2 controlled Temperature&Potential. The other 3 Fermentations controlled ALL Magnitudes.\nConsidering the Fermentations that where initialized, 4 had only the Connection verified, while 2 had only the Calibration verified. However, 4 Fermentations verified both Connection and Calibration.\nRegarding the Entertainment, this month the Scrambled Game was played 10 times, meanwhile the Hangman Game was played 5 times and the Trivia Game was played 12 times.\n")

    def testGetDateIdentifier(self): #CHECK CURRENT DATE
        self.informationReference = Information()
        self.assertEqual(self.informationReference.getDateIdentifier(), "February\n2019")

    def testAddProfessorRegistered(self):
        self.configureInstanceOfInformation()
        self.informationReference.addProfessorRegistered()
        self.assertEqual(self.informationReference.usersRegistered[0], 11)

    def testAddStudentRegistered(self):
        self.configureInstanceOfInformation()
        self.informationReference.addStudentRegistered()
        self.assertEqual(self.informationReference.usersRegistered[1], 21)

    def testAddFermentationInitiated(self):
        self.configureInstanceOfInformation()
        self.informationReference.addFermentationInitiated()
        self.assertEqual(self.informationReference.fermentationsDone[0], 31)

    def testAddFermentationContinued(self):
        self.configureInstanceOfInformation()
        self.informationReference.addFermentationContinued()
        self.assertEqual(self.informationReference.fermentationsDone[1], 6)

    def testAddFermentationWithOnlyVelocityControl(self):
        self.configureInstanceOfInformation()
        self.informationReference.addFermentationWithOnlyVelocityControl()
        self.assertEqual(self.informationReference.timesControlsRealized[0], 11)

    def testAddFermentationWithOnlyTemperatureControl(self):
        self.configureInstanceOfInformation()
        self.informationReference.addFermentationWithOnlyTemperatureControl()
        self.assertEqual(self.informationReference.timesControlsRealized[1], 6)

    def testAddFermentationWithOnlyPotentialControl(self):
        self.configureInstanceOfInformation()
        self.informationReference.addFermentationWithOnlyPotentialControl()
        self.assertEqual(self.informationReference.timesControlsRealized[2], 6)

    def testAddFermentationWithOnlyVelocityAndTemperatureControl(self):
        self.configureInstanceOfInformation()
        self.informationReference.addFermentationWithVelocityAndTemperatureControl()
        self.assertEqual(self.informationReference.timesControlsRealized[3], 6)

    def testAddFermentationWithOnlyVelocityAndPotentialControl(self):
        self.configureInstanceOfInformation()
        self.informationReference.addFermentationWithVelocityAndPotentialControl()
        self.assertEqual(self.informationReference.timesControlsRealized[4], 6)

    def testAddFermentationWithOnlyTemperatureAndPotentialControl(self):
        self.configureInstanceOfInformation()
        self.informationReference.addFermentationWithTemperatureAndPotentialControl()
        self.assertEqual(self.informationReference.timesControlsRealized[5], 3)

    def testAddFermentationWithAllControls(self):
        self.configureInstanceOfInformation()
        self.informationReference.addFermentationWithAllControls()
        self.assertEqual(self.informationReference.timesControlsRealized[6], 4)

    def testAddFermentationWithNothingVerified(self):
        self.configureInstanceOfInformation()
        self.informationReference.addFermentationWithNothingVerified()
        self.assertEqual(self.informationReference.timesVerificationsDone[0], 21)

    def testAddFermentationWithOnlyConnectionVerified(self):
        self.configureInstanceOfInformation()
        self.informationReference.addFermentationWithOnlyConnectionVerified()
        self.assertEqual(self.informationReference.timesVerificationsDone[1], 5)

    def testAddFermentationWithOnlyCalibrationVerified(self):
        self.configureInstanceOfInformation()
        self.informationReference.addFermentationWithOnlyCalibrationVerified()
        self.assertEqual(self.informationReference.timesVerificationsDone[2], 3)

    def testAddFermentationWithOnlyConnectionAndCalibrationVerified(self):
        self.configureInstanceOfInformation()
        self.informationReference.addFermentationWithConnectionAndCalibrationVerified()
        self.assertEqual(self.informationReference.timesVerificationsDone[3], 5)

    def testAddTimesScrambledPlayed(self):
        self.configureInstanceOfInformation()
        self.informationReference.addTimesScrambledPlayed()
        self.assertEqual(self.informationReference.timesGamesPlayed[0], 11)

    def testAddTimesHangmanPlayed(self):
        self.configureInstanceOfInformation()
        self.informationReference.addTimesHangmanPlayed()
        self.assertEqual(self.informationReference.timesGamesPlayed[1], 6)

    def testAddTimesTriviaPlayed(self):
        self.configureInstanceOfInformation()
        self.informationReference.addTimesTriviaPlayed()
        self.assertEqual(self.informationReference.timesGamesPlayed[2], 13)

    def testGetTotalFermentationsOfMonth(self):
        self.configureInstanceOfInformation()
        self.assertEqual(self.informationReference.getTotalFermentationsOfMonth(), 35)

    def testGetJSONData(self):
        self.configureInstanceOfInformation()
        jsonToVerify = { "usersRegistered": [10, 20], "fermentationsDone": [30, 5], "controlsRealized": [10, 5, 5, 5, 5, 2, 3], "verificationsDone": [20, 4, 2, 4], "gamesPlayed": [10, 5, 12], "date": self.informationReference.informationDate.strftime("%m/%y") }
        self.assertEqual(self.informationReference.getJSONData(), jsonToVerify)
