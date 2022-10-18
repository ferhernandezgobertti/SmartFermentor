import unittest
from Domain.Student import Student

class StudentTest(unittest.TestCase):

    def configureCorrectStudentData(self):
        studentData = ["181201", "HarryPott.1", "Roberto", "Rodriguez", "ferhernagu@gmail.com", "99640088", "Maldonado 3211", "1.231.392-1", "17/08/1999"]
        self.studentReference = Student(studentData)

    def testGetIdentifiedForFermentation(self):
        self.configureCorrectStudentData()
        self.studentReference.semester = 3
        self.assertEqual(self.studentReference.getIdentifiedForFermentation(), "Roberto Rodriguez (STUDENT from Sem 3)")

    def testShowParticularInitialData(self):
        self.configureCorrectStudentData()
        self.studentReference.career = "Engineer in Biotec"
        self.studentReference.semester = 6
        self.assertEqual(self.studentReference.showParticularInitialData(), "\nCareer: Engineer in Biotec\Student of Semester: 6")

    def testConfigureCareerWhenTechnician(self):
        self.configureCorrectStudentData()
        self.studentReference.configureCareer(0)
        self.assertEqual(self.studentReference.career, "Technician in Biotec")

    def testConfigureCareerWhenLicenciate(self):
        self.configureCorrectStudentData()
        self.studentReference.configureCareer(1)
        self.assertEqual(self.studentReference.career, "Licenciate in Biotec")

    def testConfigureCareerWhenEngineer(self):
        self.configureCorrectStudentData()
        self.studentReference.configureCareer(2)
        self.assertEqual(self.studentReference.career, "Engineer in Biotec")

    def testConfigureCareerWhenPosgraduate(self):
        self.configureCorrectStudentData()
        self.studentReference.configureCareer(3)
        self.assertEqual(self.studentReference.career, "Posgraduate in Biotec")

    def testGetJSONData(self):
        self.configureCorrectStudentData()
        self.studentReference.career = "Licenciate in Biotec"
        self.studentReference.semester = 8
        jsonToVerify = { "usernumber": "181201", "password": "HarryPott.1", "name": "Roberto", "surname": "Rodriguez", "email": "ferhernagu@gmail.com", "telephone": "99640088", "address": "Maldonado 3211", "birthDate": "17/08/1999", "idNumber": "1.231.392-1", "registration": self.studentReference.registrationDate, "lastEntry": self.studentReference.lastEntryDate, "fermentsQuantity": 0, "career": "Licenciate in Biotec", "semester": 8
         }
        self.assertEqual(self.studentReference.getJSONData(), jsonToVerify)
