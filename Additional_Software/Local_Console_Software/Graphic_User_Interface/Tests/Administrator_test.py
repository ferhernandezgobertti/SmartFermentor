import unittest
from Domain.Administrator import Administrator

class AdministratorTest(unittest.TestCase):

    def testAddUsersAdded(self):
        self.adminReference = Administrator()
        self.adminReference.addUsersAdded()
        self.assertEqual(self.adminReference.usersAdded, 1)

    def testAddUsersDeleted(self):
        self.adminReference = Administrator()
        self.adminReference.addUsersDeleted()
        self.assertEqual(self.adminReference.usersDeleted, 1)

    def testIsAdminDataRightWhenTrue(self):
        self.adminReference = Administrator()
        self.assertEqual(self.adminReference.isAdminDataRight(["BiotecORT", "Smart.1450"]), 1)

    def testIsAdminDataRightWhenWrongUsernumber(self):
        self.adminReference = Administrator()
        self.adminReference.usernumber = "NOTADMIN"
        self.assertEqual(self.adminReference.isAdminDataRight(["BiotecORT", "Smart.1450"]), 0)

    def testIsAdminDataRightWhenWrongPassword(self):
        self.adminReference = Administrator()
        self.adminReference.password = "SmartORT"
        self.assertEqual(self.adminReference.isAdminDataRight(["BiotecORT", "Smart.1450"]), 0)

    def testShowParticularInitialData(self):
        self.adminReference = Administrator()
        self.assertEqual(self.adminReference.showParticularInitialData(), "ID: BiotecORT and Psw: Smart.1450")

    def testGetJSONDataWhenAdministrator(self):
        self.adminReference = Administrator()
        jsonToVerify = { 'admin' : { 'usernumber': "BiotecORT", 'password': "Smart.1450", 'registration': self.adminReference.registrationDate, 'lastEntry': self.adminReference.lastEntryDate, 'usersAdded': 0, 'usersDeleted': 0 } }
        self.assertEqual(self.adminReference.getJSONData(), jsonToVerify)
