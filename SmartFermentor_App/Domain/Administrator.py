import sys
from Domain.User import User
from MonitorConsole.AdminPage import AdminPage

class Administrator(User):

    def __init__(self):
        super(Administrator,self).__init__(["BiotecORT","Smart.1450","AdminSmart","BiotecORT","","","","",""])
        self.usersAdded = 0
        self.usersDeleted = 0

    def addUsersAdded(self):
        self.usersAdded = self.usersAdded + 1

    def addUsersDeleted(self):
        self.usersDeleted = self.usersDeleted + 1

    def isAdminDataRight(self, referenceData):
        dataRight = 0
        if (self.usernumber==referenceData[0] and self.password==referenceData[1]):
            dataRight = 1
        return dataRight

    def initiateSession(self, controller):
        controller.show_frameAdministrator()

    def showParticularInitialData(self):
        return "ID: "+self.usernumber+" and Psw: "+self.password

    def getJSONData(self):
        adminData = {}
        adminData['admin'] = {
            'usernumber': self.usernumber,
            'password': self.password,
            'registration': self.registrationDate,
            'lastEntry': self.lastEntryDate,
            'usersAdded': self.usersAdded,
            'usersDeleted': self.usersDeleted
        }
        return adminData

    def loadJSONData(self, adminData):
        self.usernumber = adminData['admin']['usernumber']
        self.password = adminData['admin']['password']
        self.registrationDate = adminData['admin']['registration']
        self.lastEntryDate = adminData['admin']['lastEntry']
        self.usersAdded = adminData['admin']['usersAdded']
        self.usersDeleted = adminData['admin']['usersDeleted']
