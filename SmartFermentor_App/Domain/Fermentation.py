import sys
from datetime import date
from datetime import datetime
from Domain.User import User
from Domain.ListMagnitude import ListMagnitude
#from ListPotentialHydrogen import ListPotentialHydrogen

class Fermentation():

    def __init__(self, userResponsible, fermentationData):
        self.user = userResponsible
        entryTime = datetime.today()
        self.dateBeginning = entryTime.strftime("%b/%d/%Y - %H:%M:%S")
        self.dateEnding = ''
        self.sustance = fermentationData[0]
        self.objective = fermentationData[1]
        self.motive = fermentationData[2]
        self.description = self.checkDescriptionData(fermentationData[3])
        self.magnitudesToControl = ListMagnitude()
        self.dataFilenames = []
        self.isConnectionChecked = False
        self.isCalibrated = False
        self.isLiquidExpulsed = False
        self.isVelocityControlOnFreeWheel = False
        self.isTemperatureControlOnFreeWheel = False
        self.isPotentialHydrogenControlOnFreeWheel = False
        self.isFermentationContinuing = False
        #self.potentialHydrogenControl = ListPotentialHydrogen()
        #self.extractionControl = ListExtraction()

    def checkDescriptionData(self, descriptionData):
        information = descriptionData
        if(not self.hasContent(descriptionData)):
            information = "No Description Added"
        return information

    def isDataCorrect(self):
        return self.hasContent(self.sustance) and self.hasContent(self.objective) and self.hasContent(self.motive) and self.hasContent(self.description)

    def hasContent(self, contentToCheck):
        return contentToCheck!=''

    def showProcessRegistry(self):
        return "BEGINNING: "+self.dateBeginning

    def showInformation(self):
        responsibleData = self.user.getIdentifiedForFermentation()
        return self.objective.upper()+"; Responsible: "+responsibleData

    def isDescriptionRight(self):
        return self.description!="No Description Added" and self.description!="" and self.description!=" " and self.description!="\n" and not self.description.isdigit()

    def getDescriptiveInformation(self):
        descriptiveInformation = "Sustance: "+self.sustance+"\nObjective: "+self.objective+"\nMotive: "+self.motive+"\nVelocity Control Duration: "+self.magnitudesToControl.getMagnitudeDuration(self.magnitudesToControl.velocities)+"\nTemperature Control Duration: "+self.magnitudesToControl.getMagnitudeDuration(self.magnitudesToControl.temperatures)+"\nPH Control Duration: "+self.magnitudesToControl.getMagnitudeDuration(self.magnitudesToControl.potentialsHydrogen)+self.magnitudesToControl.getConditions()+"\nDescription: " #400 rpm, 37℃ (190hs), 90℃ (10hs:20m), pH 7"
        if(self.isDescriptionRight()):
            descriptiveInformation = descriptiveInformation+self.description
        else:
            descriptiveInformation = descriptiveInformation+"NO DESCRIPTION AVAILABLE"
        print("DESCRIPTION: ", self.description)
        print("DESCRIPTION RIGHT: ", self.description.isalpha())
        print("DESCRIPTIVE INFORMAITON: ", descriptiveInformation)
        return descriptiveInformation

    #def getDescriptiveInformation(self):
    #    return "Sustance: "+self.sustance+"\nObjective: "+self.objective+"\nMotive: "+self.motive+"\nVelocity Control Duration: 200hs:20m:00s\nTemperature Control Duration: 200hs:20m:00s\nPH Control Duration: 200hs:20m:00s\nConditions: 400 rpm, 37℃ (190hs), 90℃ (10hs:20m), pH 7"

    def logFilenamesInformation(self):
        return self.sustance+', OBJECTIVE: '+self.objective+', FILES: '+self.getFilesList()+'\n'

    def getFilesList(self):
        filenames = ""
        for eachFile in self.dataFilenames:
            filenames = filenames+" - "+eachFile
        return filenames

    def initiateFermentation(self, controller):
        controller.show_frameFermentation()

    def getJSONData(self):
        fermentationData = {
            "user":self.user.getJSONData(),
            "sustance":self.sustance,
            "objective": self.objective,
            "motive": self.motive,
            "description": self.description,
            "connectionStatus": self.isConnectionChecked,
            "calibrationStatus": self.isCalibrated,
            "liquidStatus": self.isLiquidExpulsed,
            "velocityFreeWheel": self.isVelocityControlOnFreeWheel,
            "temperatureFreeWheel": self.isTemperatureControlOnFreeWheel,
            "potentialHydrogenFreeWheel": self.isPotentialHydrogenControlOnFreeWheel,
            "beginning":self.dateBeginning,
            "ending":self.dateEnding,
            "magnitudes":self.magnitudesToControl.getJSONData(),
            "filenames":self.dataFilenames
         }
        return fermentationData
