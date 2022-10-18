import sys
from Domain.Fermentation import Fermentation
from Domain.Student import Student
from Domain.Professor import Professor
from Domain.ListMagnitude import ListMagnitude

class ListFermentations():

    fermentations = []

    def addFermentation(self, fermentationToAdd):
        self.fermentations.append(fermentationToAdd)

    def removeFermentation(self, indexOfFermentationToRemove):
        del self.fermentations[indexOfFermentationToRemove]

    def loadJSONData(self, dataToLoad):
        try:
            userResponsible = Student(["","","","","","","","",""])
            userResponsible.usernumber = dataToLoad['user']['usernumber']
            userResponsible.password = dataToLoad['user']['password']
            userResponsible.name = dataToLoad['user']['name']
            userResponsible.surname = dataToLoad['user']['surname']
            userResponsible.email = dataToLoad['user']['email']
            userResponsible.telephone = dataToLoad['user']['telephone']
            userResponsible.address = dataToLoad['user']['address']
            userResponsible.birthDate = dataToLoad['user']['birthDate']
            userResponsible.idNumber = dataToLoad['user']['idNumber']
            userResponsible.registrationDate = dataToLoad['user']['registration']
            userResponsible.lastEntryDate = dataToLoad['user']['lastEntry']
            userResponsible.fermentationsQuantity = dataToLoad['user']['fermentsQuantity']
            userResponsible.career = dataToLoad['user']['career']
            userResponsible.semester = dataToLoad['user']['semester']
        except KeyError:
            userResponsible = Professor(["","","","","","","","",""])
            userResponsible.usernumber = dataToLoad['user']['usernumber']
            userResponsible.password = dataToLoad['user']['password']
            userResponsible.name = dataToLoad['user']['name']
            userResponsible.surname = dataToLoad['user']['surname']
            userResponsible.email = dataToLoad['user']['email']
            userResponsible.telephone = dataToLoad['user']['telephone']
            userResponsible.address = dataToLoad['user']['address']
            userResponsible.birthDate = dataToLoad['user']['birthDate']
            userResponsible.idNumber = dataToLoad['user']['idNumber']
            userResponsible.registrationDate = dataToLoad['user']['registration']
            userResponsible.lastEntryDate = dataToLoad['user']['lastEntry']
            userResponsible.fermentationsQuantity = dataToLoad['user']['fermentsQuantity']
            userResponsible.title = dataToLoad['user']['title']
            userResponsible.grade = dataToLoad['user']['grade']
        fermentationData = Fermentation(userResponsible, ["", "", "", ""])
        fermentationData.sustance = dataToLoad['sustance']
        fermentationData.objective = dataToLoad['objective']
        fermentationData.motive = dataToLoad['motive']
        fermentationData.description = dataToLoad['description']
        fermentationData.magnitudesToControl.loadJSONData(dataToLoad['magnitudes'])
        fermentationData.dataFilenames = dataToLoad['filenames']
        fermentationData.settingsConfigured.loadJSONData(dataToLoad['settingsConfigured'])
        self.fermentations.append(fermentationData)
