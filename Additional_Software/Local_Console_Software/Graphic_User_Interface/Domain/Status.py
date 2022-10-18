import sys, time
from datetime import datetime, date, timedelta

class Status():

    def __init__(self):
        self.userLogged = 0
        self.fermentationActual = 0
        self.isUserLogged = [False, False] # [UserLogged, StudnetLogged]
        self.currentControlSteps = [0, 0, 0] # [Velocity Control, Temperature Control, Potential Control]
        self.currentControlPorts = ["", "", "", "", "", "", ""] # [Velocity Arduino Port, Temperature Arduino Port, Potential Hydrogen Port, Motor Port, Bath Port, Screens Port]
        self.blockedEntryTime = datetime(2010, 9, 12, 4, 19, 54)
        self.velocityControlData = ["ControlData/Velocity/DATA_Log/20181109_115003_VEL.txt", 0, "", ""]
        self.temperatureControlData = ["ControlData/Temperature/DATA_Log/20181109_115003_VEL.txt", 0, "", ""]
        self.potentialControlData = ["ControlData/PotentialHydrogen/DATA_Log/20181109_115003_VEL.txt", 0, "", ""]

    def blockUserEntry(self):
        self.blockedEntryTime = datetime.today()

    def getTimeEntryBlockRemaining(self):
        nowTime = datetime.today()
        #self.blockedEntryTime = datetime(2010, 9, 12, 11, 19, 54)
        print("NOW TIME: ", nowTime)
        print("BLOCKED ENTRY TIME: ", self.blockedEntryTime)
        print("TIME DIFFERENCE (seconds): ", (nowTime - self.blockedEntryTime).seconds)
        return nowTime - self.blockedEntryTime

    def isUserEntryBlocked(self):
        isEntryBlocked = False
        timeRemaining = self.getTimeEntryBlockRemaining()
        if(timeRemaining.seconds<=(20*60) and timeRemaining.seconds>0):
            self.blockUserEntry()
            isEntryBlocked = True
        print("ISENTRYBLOCKED: ", isEntryBlocked)
        return isEntryBlocked

    def setStatusStudentLogged(self, studentBeingLogged):
        self.userLogged = studentBeingLogged
        self.isUserLogged[0] = True
        self.isUserLogged[1] = True

    def setStatusProfessorLogged(self, professorBeingLogged):
        self.userLogged = professorBeingLogged
        self.isUserLogged[0] = True
        self.isUserLogged[1] = False

    def updateMagnitudeStep(self, stepToUpdate, magnitudeToUpdate):
        self.currentControlSteps[magnitudeToUpdate] = stepToUpdate

    def updateControlPorts(self, newControlPorts):
        position = 0
        for eachPort in newControlPorts:
            self.currentControlPorts[position] = eachPort
            position = position + 1

    def updateControlServerData(self, idControl, controlData):
        if(idControl==0):
            self.velocityControlData = controlData
        if(idControl==1):
            self.temperatureControlData = controlData
        if(idControl==2):
            self.potentialControlData = controlData

    def getJSONData(self):
        statusData = {
            "userLogged": self.userLogged,
            "fermentationActual": self.fermentationActual,
            "isUserLogged": self.isUserLogged,
            "controlSteps": self.currentControlSteps,
            "controlPorts": self.currentControlPorts,
            "blockedEntryTime": self.blockedEntryTime.strftime("%M:%H-%d/%m/%y"),
            "velocityControl": self.velocityControlData,
            "temperatureControl": self.temperatureControlData,
            "potentialControl": self.potentialControlData
         }
        return statusData

    def loadJSONData(self, statusData):
        self.userLogged = statusData['userLogged']
        self.fermentationActual = statusData['fermentationActual']
        self.isUserLogged = statusData['isUserLogged']
        self.currentControlSteps = statusData['controlSteps']
        self.currentControlPorts = statusData['controlPorts']
        self.blockedEntryTime = datetime.strptime(statusData['blockedEntryTime'], "%M:%H-%d/%m/%y")
        self.velocityControlData = statusData['velocityControl']
        self.temperatureControlData = statusData['temperatureControl']
        self.potentialControlData = statusData['potentialControl']
