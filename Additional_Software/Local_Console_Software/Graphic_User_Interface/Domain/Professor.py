import sys
from Domain.User import User

class Professor(User):

    def __init__(self, professorData):
        super(Professor,self).__init__(professorData)
        self.title = ""
        self.grade = ""
        self.reservesQuantity = 0

    def getFormalTitleAbreviation(self):
        titleAbreviation = "Tec."
        if(self.title=="Doctorate"):
            titleAbreviation = "Dr."
        if(self.title=="Master"):
            titleAbreviation = "Mag."
        if(self.title=="Engineer"):
            titleAbreviation = "Eng."
        if(self.title=="Licenciate"):
            titleAbreviation = "Lic."
        return titleAbreviation

    def getIdentifiedForFermentation(self):
        titleFormal = self.getFormalTitleAbreviation()
        return titleFormal+" "+self.name+" "+self.surname+" (ORT PROFESSOR)"

    def initiateSession(self, controller):
        controller.show_frameProfessor()

    def showParticularInitialData(self):
        return "\nTitle: "+self.title+" in Biotechonolgy\nProfessor Grade: "+self.grade

    def configureTitle(self, indexOfTitle):
        if(indexOfTitle==0):
            self.title = "Licenciate"
        if(indexOfTitle==1):
            self.title = "Engineer"
        if(indexOfTitle==2):
            self.title = "Master"
        if(indexOfTitle==3):
            self.title = "Doctorate"

    def getJSONData(self):
        professorData = {
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
            "title": self.title,
            "grade": self.grade,
            "reserves": self.reservesQuantity
         }
        return professorData
