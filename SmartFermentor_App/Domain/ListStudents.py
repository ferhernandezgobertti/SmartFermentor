import sys
import time
from Domain.Student import Student

class ListStudents():

    students = []

    def addStudent(self, studentToAdd):
        self.students.append(studentToAdd)

    def removeStudent(self, indexOfStudentToRemove):
        del self.students[indexOfStudentToRemove]

    def isStudentRegistered(self, studentToCheck):
        studentRegistered = [-1, -1]
        for position in range(0,len(self.students)):
            if(studentToCheck.usernumber==self.students[position].usernumber):
                studentRegistered[0] = position
            if(studentToCheck.areEqual(self.students[position])):
                studentRegistered[1] = position
                break
        return studentRegistered

    def clearStudentsList(self):
        del self.students[:]

    def getAllMailFromList(self):
        userMails = []
        for eachUser in self.students:
            userMails.append(eachUser.email)
        return userMails

    def orderList(self):
        self.students = sorted(self.students, key=lambda student: student.surname)

    def loadJSONData(self, dataToLoad):
        studentUser = Student(["","","","","","","","",""])
        studentUser.usernumber = dataToLoad['usernumber']
        studentUser.password = dataToLoad['password']
        studentUser.name = dataToLoad['name']
        studentUser.surname = dataToLoad['surname']
        studentUser.email = dataToLoad['email']
        studentUser.telephone = dataToLoad['telephone']
        studentUser.address = dataToLoad['address']
        studentUser.birthDate = dataToLoad['birthDate']
        studentUser.idNumber = dataToLoad['idNumber']
        studentUser.registrationDate = dataToLoad['registration']
        studentUser.lastEntryDate = dataToLoad['lastEntry']
        studentUser.fermentationsQuantity = dataToLoad['fermentsQuantity']
        studentUser.career = dataToLoad['career']
        studentUser.semester = dataToLoad['semester']
        self.students.append(studentUser)
