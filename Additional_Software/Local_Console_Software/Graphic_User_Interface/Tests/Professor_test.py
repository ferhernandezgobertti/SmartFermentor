import unittest
from Domain.Professor import Professor

class ProfessorTest(unittest.TestCase):

    def configureCorrectProfessorData(self):
        professorData = ["173630", "Fer.553", "Carlos", "Cigliutti", "cgcigliutti@gmail.com", "99323432", "Union 3232", "153.232-8", "12/10/1982"]
        self.professorReference = Professor(professorData)

    def testGetFormalTitleAbbreviationWhenDoctorate(self):
        self.configureCorrectProfessorData()
        self.professorReference.title = "Doctorate"
        self.assertEqual(self.professorReference.getFormalTitleAbreviation(), "Dr.")

    def testGetFormalTitleAbbreviationWhenMaster(self):
        self.configureCorrectProfessorData()
        self.professorReference.title = "Master"
        self.assertEqual(self.professorReference.getFormalTitleAbreviation(), "Mag.")

    def testGetFormalTitleAbbreviationWhenEngineer(self):
        self.configureCorrectProfessorData()
        self.professorReference.title = "Engineer"
        self.assertEqual(self.professorReference.getFormalTitleAbreviation(), "Eng.")

    def testGetFormalTitleAbbreviationWhenLicenciate(self):
        self.configureCorrectProfessorData()
        self.professorReference.title = "Licenciate"
        self.assertEqual(self.professorReference.getFormalTitleAbreviation(), "Lic.")

    def testGetFormalTitleAbbreviationWhenTechnician(self):
        self.configureCorrectProfessorData()
        self.professorReference.title = "Technician"
        self.assertEqual(self.professorReference.getFormalTitleAbreviation(), "Tec.")

    def testGetIdentifiedForFermentationWhenDoctorate(self):
        self.configureCorrectProfessorData()
        self.professorReference.title = "Doctorate"
        self.assertEqual(self.professorReference.getIdentifiedForFermentation(), "Dr. Carlos Cigliutti (ORT PROFESSOR)")

    def testGetIdentifiedForFermentationWhenMaster(self):
        self.configureCorrectProfessorData()
        self.professorReference.title = "Master"
        self.assertEqual(self.professorReference.getIdentifiedForFermentation(), "Mag. Carlos Cigliutti (ORT PROFESSOR)")

    def testGetIdentifiedForFermentationWhenEngineer(self):
        self.configureCorrectProfessorData()
        self.professorReference.title = "Engineer"
        self.assertEqual(self.professorReference.getIdentifiedForFermentation(), "Eng. Carlos Cigliutti (ORT PROFESSOR)")

    def testGetIdentifiedForFermentationWhenLicenciate(self):
        self.configureCorrectProfessorData()
        self.professorReference.title = "Licenciate"
        self.assertEqual(self.professorReference.getIdentifiedForFermentation(), "Lic. Carlos Cigliutti (ORT PROFESSOR)")

    def testGetIdentifiedForFermentationWhenTechnician(self):
        self.configureCorrectProfessorData()
        self.professorReference.title = "Technician"
        self.assertEqual(self.professorReference.getIdentifiedForFermentation(), "Tec. Carlos Cigliutti (ORT PROFESSOR)")

    def testShowParticularInitialData(self):
        self.configureCorrectProfessorData()
        self.professorReference.title = "Engineer"
        self.professorReference.grade = "B"
        self.assertEqual(self.professorReference.showParticularInitialData(), "\nTitle: Engineer in Biotechonolgy\nProfessor Grade: B")

    def testConfigureTitleWhenDoctorate(self):
        self.configureCorrectProfessorData()
        self.professorReference.configureTitle(3)
        self.assertEqual(self.professorReference.title, "Doctorate")

    def testConfigureTitleWhenMaster(self):
        self.configureCorrectProfessorData()
        self.professorReference.configureTitle(2)
        self.assertEqual(self.professorReference.title, "Master")

    def testConfigureTitleWhenEngineer(self):
        self.configureCorrectProfessorData()
        self.professorReference.configureTitle(1)
        self.assertEqual(self.professorReference.title, "Engineer")

    def testConfigureTitleWhenLicenciate(self):
        self.configureCorrectProfessorData()
        self.professorReference.configureTitle(0)
        self.assertEqual(self.professorReference.title, "Licenciate")

    def testGetJSONData(self):
        self.configureCorrectProfessorData()
        self.professorReference.title = "Engineer"
        self.professorReference.grade = "B"
        self.professorReference.reservesQuantity = 10
        jsonToVerify = { "usernumber":"173630", "password": "Fer.553", "name": "Carlos", "surname": "Cigliutti", "email": "cgcigliutti@gmail.com", "telephone": "99323432", "address": "Union 3232", "birthDate": "12/10/1982", "idNumber": "153.232-8", "registration": self.professorReference.registrationDate, "lastEntry": self.professorReference.lastEntryDate, "fermentsQuantity": 0, "title": "Engineer", "grade": "B", "reserves": 10 }
        self.assertEqual(self.professorReference.getJSONData(), jsonToVerify)
