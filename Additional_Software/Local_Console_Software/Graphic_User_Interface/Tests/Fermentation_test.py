import unittest
from datetime import date, datetime
from Domain.Fermentation import Fermentation
from Domain.Student import Student

class FermentationTest(unittest.TestCase):

    def configureCorrectFermentationData(self):
        userData = ["173631", "HerisHisis.2", "Fernando", "Hernandez", "ferhernagu@gmail.com", "98742547", "Canelones 1267", "4.851.112-6", "04/04/1996"]
        userResponsible = Student(userData)
        fermentationData = ["Escherichia Coli", "Study of Genetic Recombination in Alpha Variety", "Agro Investigation", "Higiene matters"]
        self.fermentationReference = Fermentation(userResponsible, fermentationData)

    def testHasContentWhenTrue(self):
        self.configureCorrectFermentationData()
        self.assertTrue(self.fermentationReference.hasContent("Content"))

    def testHasContentWhenFalse(self):
        self.configureCorrectFermentationData()
        self.assertFalse(self.fermentationReference.hasContent(""))

    def testCheckDescriptionDataWhenHasContent(self):
        self.configureCorrectFermentationData()
        self.assertEqual(self.fermentationReference.checkDescriptionData("Some Description"), "Some Description")

    def testCheckDescriptionDataWhenHasNoContent(self):
        self.configureCorrectFermentationData()
        self.assertEqual(self.fermentationReference.checkDescriptionData(""), "No Description Added")

    def testIsDataCorrectWhenTrue(self):
        self.configureCorrectFermentationData()
        self.assertTrue(self.fermentationReference.isDataCorrect())

    def testIsDataCorrectWhenFalseWithNoSustance(self):
        self.configureCorrectFermentationData()
        self.fermentationReference.sustance = ""
        self.assertFalse(self.fermentationReference.isDataCorrect())

    def testIsDataCorrectWhenFalseWithNoObjective(self):
        self.configureCorrectFermentationData()
        self.fermentationReference.objective = ""
        self.assertFalse(self.fermentationReference.isDataCorrect())

    def testIsDataCorrectWhenFalseWithNoMotive(self):
        self.configureCorrectFermentationData()
        self.fermentationReference.motive = ""
        self.assertFalse(self.fermentationReference.isDataCorrect())

    def testIsDataCorrectWhenFalseWithNoDescription(self):
        self.configureCorrectFermentationData()
        self.fermentationReference.description = ""
        self.assertFalse(self.fermentationReference.isDataCorrect())

    def testShowProcessRegistry(self):
        self.configureCorrectFermentationData()
        self.fermentationReference.dateBeginning = datetime(2010, 9, 12, 4, 19, 54).strftime("%b/%d/%Y - %H:%M:%S")
        self.assertEqual(self.fermentationReference.showProcessRegistry(), "BEGINNING: Sep/12/2010 - 04:19:54")

    def testShowInformation(self):
        self.configureCorrectFermentationData()
        self.assertEqual(self.fermentationReference.showInformation(), "STUDY OF GENETIC RECOMBINATION IN ALPHA VARIETY; Responsible: "+self.fermentationReference.user.getIdentifiedForFermentation())

    def testIsDescriptionRightWhenTrue(self):
        self.configureCorrectFermentationData()
        self.assertTrue(self.fermentationReference.isDescriptionRight())

    def testIsDescriptionRightWhenFalseWithNoDescriptionAdded(self):
        self.configureCorrectFermentationData()
        self.fermentationReference.description = "No Description Added"
        self.assertFalse(self.fermentationReference.isDescriptionRight())

    def testIsDescriptionRightWhenFalseWithNoContent(self):
        self.configureCorrectFermentationData()
        self.fermentationReference.description = ""
        self.assertFalse(self.fermentationReference.isDescriptionRight())

    def testIsDescriptionRightWhenFalseWithSpaceContent(self):
        self.configureCorrectFermentationData()
        self.fermentationReference.description = " "
        self.assertFalse(self.fermentationReference.isDescriptionRight())

    def testIsDescriptionRightWhenFalseWithLineReturnContent(self):
        self.configureCorrectFermentationData()
        self.fermentationReference.description = "\n"
        self.assertFalse(self.fermentationReference.isDescriptionRight())

    def testIsDescriptionRightWhenFalseWithNoAlphabetic(self):
        self.configureCorrectFermentationData()
        self.fermentationReference.description = "32323423565645"
        self.assertFalse(self.fermentationReference.isDescriptionRight())

    def testGetDescriptiveInformationWhenDescriptionRight(self):
        self.configureCorrectFermentationData()
        self.assertEqual(self.fermentationReference.getDescriptiveInformation(), "Sustance: Escherichia Coli\nObjective: Study of Genetic Recombination in Alpha Variety\nMotive: Agro Investigation\nVelocity Control Duration: "+self.fermentationReference.magnitudesToControl.getMagnitudeDuration(self.fermentationReference.magnitudesToControl.velocities)+"\nTemperature Control Duration: "+self.fermentationReference.magnitudesToControl.getMagnitudeDuration(self.fermentationReference.magnitudesToControl.temperatures)+"\nPH Control Duration: "+self.fermentationReference.magnitudesToControl.getMagnitudeDuration(self.fermentationReference.magnitudesToControl.potentialsHydrogen)+self.fermentationReference.magnitudesToControl.getConditions()+"\nDescription: Higiene matters")

    def testGetDescriptiveInformationWhenDescriptionNotRight(self):
        self.configureCorrectFermentationData()
        self.fermentationReference.description = ""
        self.assertEqual(self.fermentationReference.getDescriptiveInformation(), "Sustance: Escherichia Coli\nObjective: Study of Genetic Recombination in Alpha Variety\nMotive: Agro Investigation\nVelocity Control Duration: "+self.fermentationReference.magnitudesToControl.getMagnitudeDuration(self.fermentationReference.magnitudesToControl.velocities)+"\nTemperature Control Duration: "+self.fermentationReference.magnitudesToControl.getMagnitudeDuration(self.fermentationReference.magnitudesToControl.temperatures)+"\nPH Control Duration: "+self.fermentationReference.magnitudesToControl.getMagnitudeDuration(self.fermentationReference.magnitudesToControl.potentialsHydrogen)+self.fermentationReference.magnitudesToControl.getConditions()+"\nDescription: NO DESCRIPTION AVAILABLE")

    def testLogFilenamesInformation(self):
        self.configureCorrectFermentationData()
        self.fermentationReference.dataFilenames = ["20180302_193245_VEL.txt", "20180302_173642_TEM.txt", "20180302_133133_POT.txt"]
        self.assertEqual(self.fermentationReference.logFilenamesInformation(), 'Escherichia Coli, OBJECTIVE: Study of Genetic Recombination in Alpha Variety, FILES:  - 20180302_193245_VEL.txt - 20180302_173642_TEM.txt - 20180302_133133_POT.txt\n')

    def testGetFilesList(self):
        self.configureCorrectFermentationData()
        self.fermentationReference.dataFilenames = ["20180302_193245_VEL.txt", "20180302_173642_TEM.txt", "20180302_133133_POT.txt"]
        self.assertEqual(self.fermentationReference.getFilesList(), ' - 20180302_193245_VEL.txt - 20180302_173642_TEM.txt - 20180302_133133_POT.txt')

    def testGetJSONDataFermentation(self):
        self.configureCorrectFermentationData()
        self.fermentationReference.dataFilenames = ["20180302_193245_VEL.txt", "20180302_173642_TEM.txt", "20180302_133133_POT.txt"]
        jsonToVerify = { "user":self.fermentationReference.user.getJSONData(), "sustance": "Escherichia Coli", "objective": "Study of Genetic Recombination in Alpha Variety", "motive": "Agro Investigation", "description": "Higiene matters", "settingsConfigured": self.fermentationReference.settingsConfigured.getJSONData(), "beginning": self.fermentationReference.dateBeginning, "ending": '', "magnitudes":self.fermentationReference.magnitudesToControl.getJSONData(), "filenames": ["20180302_193245_VEL.txt", "20180302_173642_TEM.txt", "20180302_133133_POT.txt"] }
        self.assertEqual(self.fermentationReference.getJSONData(), jsonToVerify)
