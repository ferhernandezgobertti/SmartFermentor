import unittest, time
from datetime import datetime, date, timedelta
from Domain.Status import Status

class StatusTest(unittest.TestCase):

    def testBlockUserEntry(self):
        self.statusReference = Status()
        initialBlockedEntryTime = self.statusReference.blockedEntryTime
        self.statusReference.blockUserEntry()
        self.assertNotEqual(self.statusReference.blockedEntryTime, initialBlockedEntryTime)

    def testGetTimeEntryBlockRemaining(self):
        self.statusReference = Status()
        self.statusReference.blockedEntryTime = datetime.today()
        self.assertEqual(self.statusReference.getTimeEntryBlockRemaining(), datetime.today() - self.statusReference.blockedEntryTime)

    def testIsUserEntryBlockedWhenTrue(self):
        self.statusReference = Status()
        self.statusReference.blockedEntryTime = datetime.today()
        time.sleep(1)
        self.assertTrue(self.statusReference.isUserEntryBlocked())

    def testIsUserEntryBlockedWhenFalse(self):
        self.statusReference = Status()
        self.assertFalse(self.statusReference.isUserEntryBlocked())

    def testSetStatusStudentLoggedWhenCheckingUserLogged(self):
        self.statusReference = Status()
        self.statusReference.setStatusStudentLogged(1)
        self.assertEqual(self.statusReference.userLogged, 1)

    def testSetStatusStudentLoggedWhenCheckingIsUserLogged(self):
        self.statusReference = Status()
        self.statusReference.setStatusStudentLogged(1)
        self.assertEqual(self.statusReference.isUserLogged, [True, True])

    def testSetStatusProfessorLoggedWhenCheckingUserLogged(self):
        self.statusReference = Status()
        self.statusReference.setStatusProfessorLogged(1)
        self.assertEqual(self.statusReference.userLogged, 1)

    def testSetStatusProfessorLoggedWhenCheckingIsUserLogged(self):
        self.statusReference = Status()
        self.statusReference.setStatusProfessorLogged(1)
        self.assertEqual(self.statusReference.isUserLogged, [True, False])

    def testUpdateMagnitudeStepWhenVelocity(self):
        self.statusReference = Status()
        self.statusReference.updateMagnitudeStep(3, 0)
        self.assertEqual(self.statusReference.currentControlSteps, [3, 0, 0])

    def testUpdateMagnitudeStepWhenTemperature(self):
        self.statusReference = Status()
        self.statusReference.updateMagnitudeStep(3, 1)
        self.assertEqual(self.statusReference.currentControlSteps, [0, 3, 0])

    def testUpdateMagnitudeStepWhenPotential(self):
        self.statusReference = Status()
        self.statusReference.updateMagnitudeStep(3, 2)
        self.assertEqual(self.statusReference.currentControlSteps, [0, 0, 3])

    def testUpdateControlPorts(self):
        self.statusReference = Status()
        self.statusReference.updateControlPorts(["/dev/ttyACM0","/dev/ttyACM1","/dev/ttyACM2","/dev/ttyAMA0","/dev/ttyAMA1","/dev/ttyUSB0","/dev/ttyUSB1"])
        self.assertEqual(self.statusReference.currentControlPorts, ["/dev/ttyACM0","/dev/ttyACM1","/dev/ttyACM2","/dev/ttyAMA0","/dev/ttyAMA1","/dev/ttyUSB0","/dev/ttyUSB1"])

    def testUpdateControlServerDataWhenVelocityData(self):
        self.statusReference = Status()
        self.statusReference.updateControlServerData(0, ["ControlData/Velocity/DATA_Log/20190306_115003_VEL.txt", 1, "Running", "Started now"])
        self.assertEqual(self.statusReference.velocityControlData, ["ControlData/Velocity/DATA_Log/20190306_115003_VEL.txt", 1, "Running", "Started now"])

    def testUpdateControlServerDataWhenTemperatureData(self):
        self.statusReference = Status()
        self.statusReference.updateControlServerData(1, ["ControlData/Temperature/DATA_Log/20190306_115003_TEM.txt", 1, "Running", "Started now"])
        self.assertEqual(self.statusReference.temperatureControlData, ["ControlData/Temperature/DATA_Log/20190306_115003_TEM.txt", 1, "Running", "Started now"])

    def testUpdateControlServerDataWhenVelocityData(self):
        self.statusReference = Status()
        self.statusReference.updateControlServerData(2, ["ControlData/PotentialHydrogen/DATA_Log/20190306_115003_POT.txt", 1, "Running", "Started now"])
        self.assertEqual(self.statusReference.potentialControlData, ["ControlData/PotentialHydrogen/DATA_Log/20190306_115003_POT.txt", 1, "Running", "Started now"])

    def testGetJSONDataStatus(self):
        self.statusReference = Status()
        jsonToVerify = { "userLogged": 0, "fermentationActual": 0, "isUserLogged": [False, False], "controlSteps": [0, 0, 0], "controlPorts": ["", "", "", "", "", "", ""], "blockedEntryTime": "19:04-12/09/10", "velocityControl": ["ControlData/Velocity/DATA_Log/20181109_115003_VEL.txt", 0, "", ""], "temperatureControl": ["ControlData/Temperature/DATA_Log/20181109_115003_VEL.txt", 0, "", ""], "potentialControl": ["ControlData/PotentialHydrogen/DATA_Log/20181109_115003_VEL.txt", 0, "", ""] }
        self.maxDiff = None
        self.assertEqual(self.statusReference.getJSONData(), jsonToVerify)
