import unittest
import datetime
from datetime import date, datetime, timedelta
from Domain.Professor import Professor
from Domain.Student import Student
from Domain.Reservation import Reservation

class ReservationTest(unittest.TestCase):

    def configureCorrectReservationData(self):
        professorResponsibleData = ["173630", "Fer.553", "Carlos", "Cigliutti", "cgcigliutti@gmail.com", "99323432", "Union 3232", "153.232-8", "12/10/1982"]
        professorResponsible = Professor(professorResponsibleData)
        userToReserveData = ["173631", "HerisHisis.2", "Fernando", "Hernandez", "ferhernagu@gmail.com", "98742547", "Canelones 1267", "4.851.112-6", "04/04/1996"]
        userToReserve = Student(userToReserveData)
        dateBeginning = date(2019, 2, 11)
        dateEnding = date(2019, 2, 15)
        self.reservationReference = Reservation([professorResponsible, userToReserve], [dateBeginning, dateEnding])

    def testGetDatesOfReservation(self):
        self.configureCorrectReservationData()
        datesToVerify = [date(2019, 2, 11), date(2019, 2, 12), date(2019, 2, 13), date(2019, 2, 14), date(2019, 2, 15)]
        self.assertEqual(self.reservationReference.getDatesOfReservation([self.reservationReference.datesOfReservation[0], self.reservationReference.datesOfReservation[len(self.reservationReference.datesOfReservation)-1]]), datesToVerify)

    def testGetJSONDataReservation(self):
        self.configureCorrectReservationData()
        jsonToVerify = { "professorResponsible": self.reservationReference.professorResponsible.getJSONData(), "userToReserve": self.reservationReference.userToReserve.getJSONData(), "dateBeginning": "11/February/2019", "dateEnding": "15/February/2019", "notifyNow": False, "notifyNear": False, "precaution": "", }
        self.maxDiff = None
        self.assertEqual(self.reservationReference.getJSONData(), jsonToVerify)

    def testSetAditionalInformationWhenCheckingNotifyNow(self):
        self.configureCorrectReservationData()
        self.reservationReference.setAditionalInformation([True, False], "")
        self.assertTrue(self.reservationReference.notifyNow)

    def testSetAditionalInformationWhenCheckingNotifyNear(self):
        self.configureCorrectReservationData()
        self.reservationReference.setAditionalInformation([False, True], "")
        self.assertTrue(self.reservationReference.notifyNear)

    def testSetAditionalInformationWhenCheckingPrecaution(self):
        self.configureCorrectReservationData()
        self.reservationReference.setAditionalInformation([False, False], "PRECAUTION")
        self.assertEqual(self.reservationReference.precaution, "PRECAUTION")

    def testAreDatesWithNoWeekendDayWhenTrue(self):
        self.configureCorrectReservationData()
        self.assertTrue(self.reservationReference.areDatesWithNoWeekendDay())

    def testAreDatesWithNoWeekendDayWhenFalse(self):
        self.configureCorrectReservationData()
        self.reservationReference.datesOfReservation = self.reservationReference.getDatesOfReservation([date(2019, 2, 11), date(2019, 2, 17)])
        self.assertFalse(self.reservationReference.areDatesWithNoWeekendDay())

    def testAreDatesInOrderWhenTrue(self):
        self.configureCorrectReservationData()
        self.assertTrue(self.reservationReference.areDatesInOrder())

    def testAreDatesInOrderWhenFalse(self):
        self.configureCorrectReservationData()
        self.reservationReference.datesOfReservation = self.reservationReference.getDatesOfReservation([date(2019, 2, 11), date(2019, 4, 28)])
        self.assertFalse(self.reservationReference.areDatesInOrder())

    def testAreDatesOnOneMonthWhenTrue(self):
        self.configureCorrectReservationData()
        self.assertTrue(self.reservationReference.areDatesOnOneMonth())

    def testAreDatesOnOneMonthWhenFalse(self):
        self.configureCorrectReservationData()
        self.reservationReference.datesOfReservation = self.reservationReference.getDatesOfReservation([date(2019, 2, 25), date(2019, 3, 2)])
        self.assertFalse(self.reservationReference.areDatesOnOneMonth())

    def testAreDatesOnOneWeekWhenTrue(self):
        self.configureCorrectReservationData()
        self.assertTrue(self.reservationReference.areDatesOnOneWeek())

    def testAreDatesOnOneWeekWhenFalse(self):
        self.configureCorrectReservationData()
        self.reservationReference.datesOfReservation = self.reservationReference.getDatesOfReservation([date(2019, 2, 11), date(2019, 2, 20)])
        self.assertFalse(self.reservationReference.areDatesOnOneWeek())

    def testAreDatesRightWhenTrue(self):
        self.configureCorrectReservationData()
        self.assertEqual(self.reservationReference.areDatesRight(), [True, True, True, True])

    def testAreDatesRightWhenFalse(self):
        self.configureCorrectReservationData()
        self.reservationReference.datesOfReservation = self.reservationReference.getDatesOfReservation([date(2019, 2, 11), date(2019, 4, 28)])
        self.assertEqual(self.reservationReference.areDatesRight(), [False, False, False, False])

    def testIsReservationRightWhenTrue(self):
        self.configureCorrectReservationData()
        self.assertEqual(self.reservationReference.isReservationRight(), [True, True, True, True])

    def testIsReservationRightWhenFalse(self):
        self.configureCorrectReservationData()
        self.reservationReference.datesOfReservation = self.reservationReference.getDatesOfReservation([date(2019, 4, 11), date(2019, 2, 28)])
        self.assertFalse(self.reservationReference.isReservationRight())

    def testIsTimeToNotificateWhenTrue(self):
        self.configureCorrectReservationData()
        currentDate = date.today()
        oneWeekLater = currentDate + timedelta(days=7)
        oneWeekLaterPlusSomeDays = currentDate + timedelta(days=8)
        self.reservationReference.datesOfReservation = self.reservationReference.getDatesOfReservation([oneWeekLater, oneWeekLaterPlusSomeDays])
        self.assertTrue(self.reservationReference.isTimeToNotificate())

    def testIsTimeToNotificateWhenFalse(self):
        self.configureCorrectReservationData()
        currentDate = date.today()
        oneWeekLater = currentDate + timedelta(days=21)
        oneWeekLaterPlusSomeDays = currentDate + timedelta(days=22)
        self.reservationReference.datesOfReservation = self.reservationReference.getDatesOfReservation([oneWeekLater, oneWeekLaterPlusSomeDays])
        self.assertFalse(self.reservationReference.isTimeToNotificate())

    def testIsInNeedOfNotificationWhenTrue(self):
        self.configureCorrectReservationData()
        self.reservationReference.notifyNear = True
        currentDate = date.today()
        oneWeekLater = currentDate + timedelta(days=7)
        oneWeekLaterPlusSomeDays = currentDate + timedelta(days=8)
        self.reservationReference.datesOfReservation = self.reservationReference.getDatesOfReservation([oneWeekLater, oneWeekLaterPlusSomeDays])
        self.assertTrue(self.reservationReference.isInNeedOfNotification())

    def testIsInNeedOfNotificationWhenFalseWithNotifyNearTrue(self):
        self.configureCorrectReservationData()
        self.reservationReference.notifyNear = True
        currentDate = date.today()
        oneWeekLater = currentDate + timedelta(days=21)
        oneWeekLaterPlusSomeDays = currentDate + timedelta(days=22)
        self.reservationReference.datesOfReservation = self.reservationReference.getDatesOfReservation([oneWeekLater, oneWeekLaterPlusSomeDays])
        self.assertFalse(self.reservationReference.isInNeedOfNotification())

    def testIsInNeedOfNotificationWhenFalseWithNotifyNearFalse(self):
        self.configureCorrectReservationData()
        self.reservationReference.notifyNear = False
        currentDate = date.today()
        oneWeekLater = currentDate + timedelta(days=7)
        oneWeekLaterPlusSomeDays = currentDate + timedelta(days=8)
        self.reservationReference.datesOfReservation = self.reservationReference.getDatesOfReservation([oneWeekLater, oneWeekLaterPlusSomeDays])
        self.assertFalse(self.reservationReference.isInNeedOfNotification())

    def testGetWeekAndDayOfDateWhenCorrectWeek(self):
        self.configureCorrectReservationData()
        self.assertEqual(self.reservationReference.getWeekAndDayOfDate(3, 2), [1, 1, 1, 1, 1])

    def testGetWeekAndDayOfDateWhenIncorrectWeek(self):
        self.configureCorrectReservationData()
        self.assertEqual(self.reservationReference.getWeekAndDayOfDate(2, 2), [0, 0, 0, 0, 0])
