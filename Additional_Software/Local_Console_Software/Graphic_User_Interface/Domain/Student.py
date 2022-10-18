import sys
from Domain.User import User
from MonitorConsole.StudentPage import StudentPage

class Student(User):

    def __init__(self, studentData):
        super(Student,self).__init__(studentData)
        self.career = ""
        self.semester = 0
        self.gameRecords = [0, 0]

    def getIdentifiedForFermentation(self):
        return self.name+" "+self.surname+" (STUDENT from Sem "+str(self.semester)+")"

    def initiateSession(self, controller):
        controller.show_frameStudent()

    def showParticularInitialData(self):
        return "\nCareer: "+self.career+"\Student of Semester: "+str(self.semester)

    def configureCareer(self, indexOfCareer):
        if(indexOfCareer==0):
            self.career = "Technician in Biotec"
        if(indexOfCareer==1):
            self.career = "Licenciate in Biotec"
        if(indexOfCareer==2):
            self.career = "Engineer in Biotec"
        if(indexOfCareer==3):
            self.career = "Posgraduate in Biotec"

    def getJSONData(self):
        studentData = {
            "usernumber":self.usernumber,
            "password":self.password,
            "name":self.name,
            "surname":self.surname,
            "email": self.email,
            "telephone": self.telephone,
            "address": self.address,
            "birthDate": self.birthDate,
            "idNumber": self.idNumber,
            "registration": self.registrationDate,
            "lastEntry": self.lastEntryDate,
            "fermentsQuantity": self.fermentationsQuantity,
            "career": self.career,
            "semester": self.semester
         }
        return studentData
