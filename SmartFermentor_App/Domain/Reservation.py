import sys, time, datetime
from datetime import date
from datetime import timedelta

class Reservation():

        def __init__(self, users, dates):
            self.professorResponsible = users[0]
            self.userToReserve = users[1]
            self.datesOfReservation = self.getDatesOfReservation(dates)
            self.notifyNow = False
            self.notifyNear = False
            self.precaution = ""

        def getDatesOfReservation(self, dates):
            datesOfReservation = []
            durationReservation = dates[1]-dates[0]
            print("DURATION RESERVATION: ", durationReservation)
            if(durationReservation.days>=0):
                datesOfReservation.append(dates[0])
                newDate = dates[0]
                duration = 1
                while(duration<=durationReservation.days):
                    newDate = newDate + timedelta(days=1)
                    datesOfReservation.append(newDate)
                    print("DATE ADDED: ", newDate)
                    duration = duration + 1
            return datesOfReservation

        def getJSONData(self):
            reservationData = {
                "professorResponsible":self.professorResponsible.getJSONData(),
                "userToReserve":self.userToReserve.getJSONData(),
                "dateBeginning":self.datesOfReservation[0].strftime("%d/%B/%Y"),
                "dateEnding":self.datesOfReservation[len(self.datesOfReservation)-1].strftime("%d/%B/%Y"),
                "notifyNow":self.notifyNow,
                "notifyNear": self.notifyNear,
                "precaution": self.precaution,
             }
            return reservationData

        def setAditionalInformation(self, notifications, precautionText):
            if(notifications[0]==1):
                self.notifyNow = True
            if(notifications[1]==1):
                self.notifyNear = True
            if(precautionText==""):
                precautionText="No Precaution Data Registered"
            self.precaution = precautionText

        def areDatesWithNoWeekendDay(self):
            datesWithNoWeekend = True
            for eachDate in self.datesOfReservation:
                if(eachDate.isoweekday()==6 or eachDate.isoweekday()==7):
                    datesWithNoWeekend = False
            return datesWithNoWeekend

        def areDatesInOrder(self):
            previousDay = 0
            datesInOrder = True
            for eachDate in self.datesOfReservation:
                if(eachDate.day < previousDay):
                    datesInOrder = False
                previousDay = eachDate.day
            return datesInOrder

        def areDatesOnOneMonth(self):
            currentMonth = self.datesOfReservation[0].month
            datesOnOneMonth = True
            for eachDate in self.datesOfReservation:
                if(eachDate.month != currentMonth):
                    datesOnOneMonth = False
            return datesOnOneMonth

        def areDatesOnOneWeek(self):
            currentWeek = self.datesOfReservation[0].isocalendar()[1]
            datesOnOneWeek = True
            for eachDate in self.datesOfReservation:
                if(eachDate.isocalendar()[1] != currentWeek):
                    datesOnOneWeek = False
            return datesOnOneWeek

        def areDatesRight(self):
            return [self.areDatesWithNoWeekendDay(), self.areDatesOnOneMonth(), self.areDatesInOrder(), self.areDatesOnOneWeek()]

        def isReservationRight(self):
            if(len(self.datesOfReservation)>0):
                return self.areDatesRight()
            else:
                return None

        def isTimeToNotificate(self):
            currentDate = date.today()
            #timeBeforeReservation = self.datesOfReservation[len(self.datesOfReservation)-1]-self.datesOfReservation[0]
            timeBeforeReservation = self.datesOfReservation[0] - currentDate
            print("TIMEBEFORERESERVATION: ", timeBeforeReservation)
            return timeBeforeReservation.days<=7 and timeBeforeReservation.days>0 #one week prior to reservation

        def isInNeedOfNotification(self):
            return self.notifyNear and self.isTimeToNotificate()

        def getWeekAndDayOfDate(self, numberOfWeek, monthNumber):
            blockPosition = [0, 0, 0, 0, 0]
            currentTime = date.today()
            firstOfMonth = date(currentTime.year, monthNumber, 1) #currentTime.month, 1)
            print("CURRENT MONTH: ", currentTime.month)
            firstWeekOfMonth = firstOfMonth.isocalendar()[1]
            print("FIRST WEEK OF MONTH: ", firstWeekOfMonth)
            for eachDateOfReservation in self.datesOfReservation:
                reservationOfMonth = eachDateOfReservation.isocalendar()
                print("RESERVATIONS OF MONTH: ", reservationOfMonth)
                print("DIFFERENCE: ", reservationOfMonth[1]-firstWeekOfMonth)
                print("NUMBER OF WEEK: ", numberOfWeek-1)
                if(reservationOfMonth[1]-firstWeekOfMonth==numberOfWeek-1):
                    blockPosition[reservationOfMonth[2]-1] = 1
                    print("PAINT: ", reservationOfMonth[2]-1)
            return blockPosition
