import sys, time
from datetime import datetime, date, timedelta
from Domain.Information import Information

class ListInformations():

    def __init__(self):
        self.informations = []


    def initializeInformationData(self):
        self.informations.append(Information())
        self.informations.append(Information())
        self.informations.append(Information())
        self.informations.append(Information())
        self.informations.append(Information())
        self.informations.append(Information())

    def loadJSONData(self, dataToLoad):
        self.informations.append(Information())
        self.informations[len(self.informations)-1].usersRegistered = dataToLoad['usersRegistered']
        self.informations[len(self.informations)-1].fermentationsDone = dataToLoad['fermentationsDone']
        self.informations[len(self.informations)-1].timesControlsRealized = dataToLoad['controlsRealized']
        self.informations[len(self.informations)-1].timesVerificationsDone = dataToLoad['verificationsDone']
        self.informations[len(self.informations)-1].timesGamesPlayed = dataToLoad['gamesPlayed']
        self.informations[len(self.informations)-1].informationDate = datetime.strptime(dataToLoad['date'],"%m/%y")
        #print("USERS REGISTERED: ", self.informations[len(self.informations)-1].usersRegistered)

    def collectGeneralInformation(self):
        generalInformation = ""
        for eachInformation in self.informations:
            generalInformation = generalInformation + eachInformation.getParticularInformation()
        return generalInformation

    def updateInformationsHistory(self):
        del self.informations[0]
        self.informations.append(Information())
        self.informations[5].usersRegistered = self.informations[4].usersRegistered
        #self.informations[5].fermentationsDone = self.informations[4].fermentationsDone

    def getDatesConsidered(self):
        return [self.informations[0].getDateIdentifier(), self.informations[1].getDateIdentifier(), self.informations[2].getDateIdentifier(), self.informations[3].getDateIdentifier(), self.informations[4].getDateIdentifier(), self.informations[5].getDateIdentifier()]

    def getProfessorsQuantityHistory(self):
        return [self.informations[0].usersRegistered[0], self.informations[1].usersRegistered[0], self.informations[2].usersRegistered[0], self.informations[3].usersRegistered[0], self.informations[4].usersRegistered[0], self.informations[5].usersRegistered[0]]

    def getStudentsQuantityHistory(self):
        return [self.informations[0].usersRegistered[1], self.informations[1].usersRegistered[1], self.informations[2].usersRegistered[1], self.informations[3].usersRegistered[1], self.informations[4].usersRegistered[1], self.informations[5].usersRegistered[1]]

    def getFermentationsInitiatedQuantityHistory(self):
        return [self.informations[0].fermentationsDone[0], self.informations[1].fermentationsDone[0], self.informations[2].fermentationsDone[0], self.informations[3].fermentationsDone[0], self.informations[4].fermentationsDone[0], self.informations[5].fermentationsDone[0]]

    def getFermentationsContinuedQuantityHistory(self):
        return [self.informations[0].fermentationsDone[1], self.informations[1].fermentationsDone[1], self.informations[2].fermentationsDone[1], self.informations[3].fermentationsDone[1], self.informations[4].fermentationsDone[1], self.informations[5].fermentationsDone[1]]

    def getCurrentMonthControlsInformation(self):
        totalFermentationsMonth = self.informations[5].getTotalFermentationsOfMonth()
        if(totalFermentationsMonth==0):
            controlsInformation = [0, 0, 0, 0, 0, 0, 0]
        else:
            controlsInformation = [round(float(100*self.informations[5].timesControlsRealized[0]/totalFermentationsMonth),2), round(float(100*self.informations[5].timesControlsRealized[1]/totalFermentationsMonth),2), round(float(100*self.informations[5].timesControlsRealized[2]/totalFermentationsMonth),2), round(float(100*self.informations[5].timesControlsRealized[3]/totalFermentationsMonth),2), round(float(100*self.informations[5].timesControlsRealized[4]/totalFermentationsMonth),2), round(float(100*self.informations[5].timesControlsRealized[5]/totalFermentationsMonth),2), round(float(100*self.informations[5].timesControlsRealized[6]/totalFermentationsMonth),2)]
        return controlsInformation

    def getCurrentMonthVerificationsInformation(self):
        totalFermentationsInitiatedOnMonth = self.informations[5].fermentationsDone[0]
        if(totalFermentationsInitiatedOnMonth==0):
            verificationsInformation = [0, 0, 0, 0]
        else:
            verificationsInformation = [round(float(100*self.informations[5].timesVerificationsDone[0]/totalFermentationsInitiatedOnMonth),2), round(float(100*self.informations[5].timesVerificationsDone[1]/totalFermentationsInitiatedOnMonth),2), round(float(100*self.informations[5].timesVerificationsDone[2]/totalFermentationsInitiatedOnMonth),2), round(float(100*self.informations[5].timesVerificationsDone[3]/totalFermentationsInitiatedOnMonth),2)]
        return verificationsInformation

    def getCurrentMonthGamesInformation(self):
        return [self.informations[5].timesGamesPlayed[0], self.informations[5].timesGamesPlayed[1], self.informations[5].timesGamesPlayed[2]]
