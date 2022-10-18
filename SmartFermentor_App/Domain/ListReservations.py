import sys
import time
import datetime
from datetime import date
from Domain.Reservation import Reservation
from Domain.Professor import Professor
from Domain.Student import Student

class ListReservations():

    reservations = []

    def addReservation(self, reservationToAdd):
        self.reservations.append(reservationToAdd)

    def removeReservation(self, indexOfReservationToRemove):
        del self.reservations[indexOfReservationToRemove]

    def removeReservationByDate(self, dateOfReservation):
        reservationToRemove = None
        position = 0
        reservationRemoved = False
        for eachReservation in self.reservations:
            for eachDateOfReservation in eachReservation.datesOfReservation:
                if(eachDateOfReservation==dateOfReservation):
                    reservationToRemove = eachReservation
                    del self.reservations[position]
                    reservationRemoved = True
                    break
            if(reservationRemoved):
                break
            position = position + 1
        return reservationToRemove

    def isReservationPeriodAvailable(self, reservationToCheck):
        reservationAvailable = True
        for eachReservation in self.reservations:
            for eachDateRegistered in eachReservation.datesOfReservation:
                for eachDate in reservationToCheck.datesOfReservation:
                    if(eachDate == eachDateRegistered):
                        reservationAvailable = False
                        break
                if (not reservationAvailable):
                    break
            if (not reservationAvailable):
                break
        return reservationAvailable

    def getInformationOfDate(self, dateToCheck):
        informationText = []
        informationFound = False
        for eachReservation in self.reservations:
            for eachDateRegistered in eachReservation.datesOfReservation:
                if(eachDateRegistered == dateToCheck):
                    informationText = [eachReservation.professorResponsible, eachReservation.userToReserve, eachReservation.precaution]
                    informationFound = True
                    break
            if(informationFound):
                break
        return informationText

    def loadJSONData(self, dataToLoad):
        userResponsible = Professor(["","","","","","","","",""])
        userResponsible.usernumber = dataToLoad['professorResponsible']['usernumber']
        userResponsible.password = dataToLoad['professorResponsible']['password']
        userResponsible.name = dataToLoad['professorResponsible']['name']
        userResponsible.surname = dataToLoad['professorResponsible']['surname']
        userResponsible.email = dataToLoad['professorResponsible']['email']
        userResponsible.telephone = dataToLoad['professorResponsible']['telephone']
        userResponsible.address = dataToLoad['professorResponsible']['address']
        userResponsible.birthDate = dataToLoad['professorResponsible']['birthDate']
        userResponsible.idNumber = dataToLoad['professorResponsible']['idNumber']
        userResponsible.registrationDate = dataToLoad['professorResponsible']['registration']
        userResponsible.lastEntryDate = dataToLoad['professorResponsible']['lastEntry']
        userResponsible.fermentationsQuantity = dataToLoad['professorResponsible']['fermentsQuantity']
        userResponsible.title = dataToLoad['professorResponsible']['title']
        userResponsible.grade = dataToLoad['professorResponsible']['grade']
        try:
            userToReserve = Student(["","","","","","","","",""])
            userToReserve.usernumber = dataToLoad['userToReserve']['usernumber']
            userToReserve.password = dataToLoad['userToReserve']['password']
            userToReserve.name = dataToLoad['userToReserve']['name']
            userToReserve.surname = dataToLoad['userToReserve']['surname']
            userToReserve.email = dataToLoad['userToReserve']['email']
            userToReserve.telephone = dataToLoad['userToReserve']['telephone']
            userToReserve.address = dataToLoad['userToReserve']['address']
            userToReserve.birthDate = dataToLoad['userToReserve']['birthDate']
            userToReserve.idNumber = dataToLoad['userToReserve']['idNumber']
            userToReserve.registrationDate = dataToLoad['userToReserve']['registration']
            userToReserve.lastEntryDate = dataToLoad['userToReserve']['lastEntry']
            userToReserve.fermentationsQuantity = dataToLoad['userToReserve']['fermentsQuantity']
            userToReserve.career = dataToLoad['userToReserve']['career']
            userToReserve.semester = dataToLoad['userToReserve']['semester']
        except KeyError:
            userToReserve = Professor(["","","","","","","","",""])
            userToReserve.usernumber = dataToLoad['userToReserve']['usernumber']
            userToReserve.password = dataToLoad['userToReserve']['password']
            userToReserve.name = dataToLoad['userToReserve']['name']
            userToReserve.surname = dataToLoad['userToReserve']['surname']
            userToReserve.email = dataToLoad['userToReserve']['email']
            userToReserve.telephone = dataToLoad['userToReserve']['telephone']
            userToReserve.address = dataToLoad['userToReserve']['address']
            userToReserve.birthDate = dataToLoad['userToReserve']['birthDate']
            userToReserve.idNumber = dataToLoad['userToReserve']['idNumber']
            userToReserve.registrationDate = dataToLoad['userToReserve']['registration']
            userToReserve.lastEntryDate = dataToLoad['userToReserve']['lastEntry']
            userToReserve.fermentationsQuantity = dataToLoad['userToReserve']['fermentsQuantity']
            userToReserve.title = dataToLoad['userToReserve']['title']
            userToReserve.grade = dataToLoad['userToReserve']['grade']

        beginning = time.strptime(dataToLoad['dateBeginning'], "%d/%B/%Y")
        reservationBegin = date(beginning.tm_year, beginning.tm_mon, beginning.tm_mday)
        ending = time.strptime(dataToLoad['dateEnding'], "%d/%B/%Y")
        reservationEnd = date(ending.tm_year, ending.tm_mon, ending.tm_mday)
        reservation = Reservation([userResponsible, userToReserve],[reservationBegin, reservationEnd])
        reservation.notifyNow = dataToLoad['notifyNow']
        reservation.notifyNear = dataToLoad['notifyNear']
        reservation.precaution = dataToLoad['precaution']
        self.reservations.append(reservation)
