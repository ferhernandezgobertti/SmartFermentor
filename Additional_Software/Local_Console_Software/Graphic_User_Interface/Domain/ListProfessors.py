import sys
import time
from Domain.Professor import Professor

class ListProfessors():

    professors = []

    def addProfessor(self, professorToAdd):
        self.professors.append(professorToAdd)

    def removeProfessor(self, indexOfProfessorToRemove):
        del self.professors[indexOfProfessorToRemove]

    def isProfessorRegistered(self, professorToCheck):
        professorRegistered = [-1, -1]
        for position in range(0,len(self.professors)):
            if(professorToCheck.usernumber==self.professors[position].usernumber):
                professorRegistered[0] = position
            if(professorToCheck.areEqual(self.professors[position])):
                professorRegistered[1] = position
                break
        return professorRegistered

    def clearProfessorsList(self):
        del self.professors[:]

    def orderList(self):
        self.professors = sorted(self.professors, key=lambda professor: professor.surname)

    def getAllMailFromList(self):
        userMails = []
        for eachUser in self.professors:
            userMails.append(eachUser.email)
        return userMails

    def loadJSONData(self, dataToLoad):
        professorUser = Professor(["","","","","","","","",""])
        professorUser.usernumber = dataToLoad['usernumber']
        professorUser.password = dataToLoad['password']
        professorUser.name = dataToLoad['name']
        professorUser.surname = dataToLoad['surname']
        professorUser.email = dataToLoad['email']
        professorUser.telephone = dataToLoad['telephone']
        professorUser.address = dataToLoad['address']
        professorUser.birthDate = dataToLoad['birthDate']
        professorUser.idNumber = dataToLoad['idNumber']
        professorUser.registrationDate = dataToLoad['registration']
        professorUser.lastEntryDate = dataToLoad['lastEntry']
        professorUser.fermentationsQuantity = dataToLoad['fermentsQuantity']
        professorUser.title = dataToLoad['title']
        professorUser.grade = dataToLoad['grade']
        professorUser.reservesQuantity = dataToLoad['reserves']
        self.professors.append(professorUser)
