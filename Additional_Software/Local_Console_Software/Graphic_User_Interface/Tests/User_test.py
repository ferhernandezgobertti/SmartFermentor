import unittest, time
#import sys
#sys.path.insert(0, '/C:/PYfiles/LAST_VERSION/html/')
#print(sys.path)
from Domain.User import User

class UserTest(unittest.TestCase):

    def configureCorrectUserData(self):
        userData = ["173631", "HerisHisis.2", "Fernando", "Hernandez", "ferhernagu@gmail.com", "98742547", "Canelones 1267", "4.851.112-6", "04/04/1996"]
        self.userReference = User(userData)

    def configureUserToCompareData(self):
        userData = ["173631", "HerisHisis.2", "Fernando", "Hernandez", "ferhernagu@gmail.com", "98742547", "Canelones 1267", "4.851.112-6", "04/04/1996"]
        self.userComparisson = User(userData)

    def testUpdateLastEntryWhenCorrect(self):
        self.configureCorrectUserData()
        initialLastEntry = self.userReference.lastEntryDate
        time.sleep(1)
        self.userReference.updateLastEntry()
        updatedLastEntry = self.userReference.lastEntryDate
        self.assertNotEqual(initialLastEntry, updatedLastEntry)

    def testAddFermentationWhenCorrect(self):
        self.configureCorrectUserData()
        initialFermentationsQuantity = self.userReference.fermentationsQuantity
        self.userReference.addFermentation()
        self.assertEqual(self.userReference.fermentationsQuantity, initialFermentationsQuantity+1)

    def testIsUsernumberRightWhenAllCorrect(self):
        self.configureCorrectUserData()
        self.assertEqual(self.userReference.isUsernumberRight(), 1)

    def testIsUsernumberRightWhenNoNumber(self):
        self.configureCorrectUserData()
        self.userReference.usernumber = "NONUMBER"
        self.assertEqual(self.userReference.isUsernumberRight(), 0)

    def testIsUsernumberRightWhenTooShort(self):
        self.configureCorrectUserData()
        self.userReference.usernumber = "123"
        self.assertEqual(self.userReference.isUsernumberRight(), 0)

    def testIsUsernumberRightWhenTooLarge(self):
        self.configureCorrectUserData()
        self.userReference.usernumber = "123456789"
        self.assertEqual(self.userReference.isUsernumberRight(), 0)

    def testIsContentNumberWhenTrue(self):
        self.configureCorrectUserData()
        self.assertTrue(self.userReference.isContentNumber("12345"))

    def testIsContentNumberWhenFalse(self):
        self.configureCorrectUserData()
        self.assertFalse(self.userReference.isContentNumber("NONUM"))

    def testIsPasswordCorrectWhenCorrect(self):
        self.configureCorrectUserData()
        self.assertTrue(self.userReference.isPasswordCorrect("HerisHisis.2"))

    def testIsPasswordCorrectWhenIncorrect(self):
        self.configureCorrectUserData()
        self.assertFalse(self.userReference.isPasswordCorrect("HarryPott.2"))

    def testIsPasswordRightWhenCorrect(self):
        self.configureCorrectUserData()
        self.assertEqual(self.userReference.isPasswordRight(), 1)

    def testIsPasswordRightWhenTooShort(self):
        self.configureCorrectUserData()
        self.userReference.password = "aaa"
        self.assertEqual(self.userReference.isPasswordRight(), 0)

    def testIsPasswordRightWhenTooLarge(self):
        self.configureCorrectUserData()
        self.userReference.password = "aaaaaaaaaaaaaaaaaaaaaaaa"
        self.assertEqual(self.userReference.isPasswordRight(), 0)

    def testIsPasswordRightWhenNoUpper(self):
        self.configureCorrectUserData()
        self.userReference.password = "fercar.23"
        self.assertEqual(self.userReference.isPasswordRight(), 0)

    def testIsPasswordRightWhenNoNumber(self):
        self.configureCorrectUserData()
        self.userReference.password = "Up.And.Down"
        self.assertEqual(self.userReference.isPasswordRight(), 0)

    def testIsPasswordRightWhenNoSymbol(self):
        self.configureCorrectUserData()
        self.userReference.password = "CarlosFer2"
        self.assertEqual(self.userReference.isPasswordRight(), 0)

    def testIsNameSurnameRightWhenCorrect(self):
        self.configureCorrectUserData()
        self.assertEqual(self.userReference.isNameSurnameRight(), 1)

    def testIsNameSurnameRightWhenNameTooShort(self):
        self.configureCorrectUserData()
        self.userReference.name = "A"
        self.assertEqual(self.userReference.isNameSurnameRight(), 0)

    def testIsNameSurnameRightWhenSurnameTooShort(self):
        self.configureCorrectUserData()
        self.userReference.surname = "CarlosFernando"
        self.assertEqual(self.userReference.isNameSurnameRight(), 0)

    def testIsNameSurnameRightWhenNoUpper(self):
        self.configureCorrectUserData()
        self.userReference.name = "fernando"
        self.assertEqual(self.userReference.isNameSurnameRight(), 0)

    def testIsNameSurnameRightWhenWithSymbol(self):
        self.configureCorrectUserData()
        self.userReference.surname = "Her.23dez"
        self.assertEqual(self.userReference.isNameSurnameRight(), 0)

    def testIsNameSurnameWithSymbolWhenCorrect(self):
        self.configureCorrectUserData()
        self.assertEqual(self.userReference.isNameSurnameWithSymbol(), 0)

    def testIsNameSurnameWithSymbolWhenNameWithNumber(self):
        self.configureCorrectUserData()
        self.userReference.name = "With23Nam"
        self.assertEqual(self.userReference.isNameSurnameWithSymbol(), 1)

    def testIsNameSurnameWithSymbolWhenSurnameWithNumber(self):
        self.configureCorrectUserData()
        self.userReference.surname = "With23Sur"
        self.assertEqual(self.userReference.isNameSurnameWithSymbol(), 1)

    def testIsNameSurnameWithSymbolWhenNameWithSymbol(self):
        self.configureCorrectUserData()
        self.userReference.name = "With2;,Nam"
        self.assertEqual(self.userReference.isNameSurnameWithSymbol(), 1)

    def testIsNameSurnameWithSymbolWhenSurnameWithSymbol(self):
        self.configureCorrectUserData()
        self.userReference.surname = "With./Sur"
        self.assertEqual(self.userReference.isNameSurnameWithSymbol(), 1)

    def testIsNameSurnameWithUpperWhenCorrect(self):
        self.configureCorrectUserData()
        self.assertEqual(self.userReference.isNameSurnameWithUpper(), 1)

    def testIsNameSurnameWithUpperWhenNameAllLower(self):
        self.configureCorrectUserData()
        self.userReference.name = "carlos"
        self.assertEqual(self.userReference.isNameSurnameWithUpper(), 0)

    def testIsNameSurnameWithUpperWhenNameAllUpper(self):
        self.configureCorrectUserData()
        self.userReference.name = "CARLOS"
        self.assertEqual(self.userReference.isNameSurnameWithUpper(), 0)

    def testIsNameSurnameWithUpperWhenSurnameAllLower(self):
        self.configureCorrectUserData()
        self.userReference.surname = "cigliutti"
        self.assertEqual(self.userReference.isNameSurnameWithUpper(), 0)

    def testIsNameSurnameWithUpperWhenSurnameAllUpper(self):
        self.configureCorrectUserData()
        self.userReference.surname = "CIGLIUTTI"
        self.assertEqual(self.userReference.isNameSurnameWithUpper(), 0)

    def testIsPasswordWithUpperWhenCorrect(self):
        self.configureCorrectUserData()
        self.assertEqual(self.userReference.isPasswordWithUpper(), 1)

    def testIsPasswordWithUpperWhenAllLower(self):
        self.configureCorrectUserData()
        self.userReference.password = "her.22his"
        self.assertEqual(self.userReference.isPasswordWithUpper(), 0)

    def testIsPasswordWithUpperWhenAllUpper(self):
        self.configureCorrectUserData()
        self.userReference.password = "HER.22HIS"
        self.assertEqual(self.userReference.isPasswordWithUpper(), 0)

    def testIsWordWithSymbolWhenCorrect(self):
        self.configureCorrectUserData()
        self.assertEqual(self.userReference.isWordWithSymbol('Fer.an,o', ".,;<>|/%&^!"), 1)

    def testIsWordWithSymbolWhenIncorrect(self):
        self.configureCorrectUserData()
        self.assertEqual(self.userReference.isWordWithSymbol('Fernando', ".,;<>|/%&^!"), 0)

    def testIsEmailRightWhenCorrect(self):
        self.configureCorrectUserData()
        self.assertEqual(self.userReference.isEmailRight(), 1)

    def testIsEmailRightWhenWrongUsername(self):
        self.configureCorrectUserData()
        self.userReference.email = "ferhernagugmail.com"
        self.assertEqual(self.userReference.isEmailRight(), 0)

    def testIsEmailRightWhenWrongEnding(self):
        self.configureCorrectUserData()
        self.userReference.email = "ferhernagu@gmailcom"
        self.assertEqual(self.userReference.isEmailRight(), 0)

    def testIsEmailRightWhenWrongExtension(self):
        self.configureCorrectUserData()
        self.userReference.email = "ferhernagu@gmal.com"
        self.assertEqual(self.userReference.isEmailRight(), 0)

    def testIsEmailWithUsernameWhenTrue(self):
        self.configureCorrectUserData()
        self.assertTrue(self.userReference.isEmailWithUsername())

    def testIsEmailWithUsernameWhenFalse(self):
        self.configureCorrectUserData()
        self.userReference.email = "smartfermentoredu.uy"
        self.assertFalse(self.userReference.isEmailWithUsername())

    def testIsEmailEndingCorrectWhenTrueIfCommercial(self):
        self.configureCorrectUserData()
        self.userReference.email = "smartfermentor@gmail.com"
        self.assertTrue(self.userReference.isEmailEndingCorrect())

    def testIsEmailEndingCorrectWhenTrueIfEducational(self):
        self.configureCorrectUserData()
        self.userReference.email = "smartfermentor@ort.edu.uy"
        self.assertTrue(self.userReference.isEmailEndingCorrect())

    def testIsEmailEndingCorrectWhenFalse(self):
        self.configureCorrectUserData()
        self.userReference.email = "smartfermentor@edu.org"
        self.assertFalse(self.userReference.isEmailEndingCorrect())

    def testIsEmailWithExtensionWhenTrue(self):
        self.configureCorrectUserData()
        self.assertTrue(self.userReference.isEmailwithExtension("gmail"))

    def testIsEmailWithExtensionWhenFalse(self):
        self.configureCorrectUserData()
        self.userReference.email = "smartfermentor@edu.uy"
        self.assertFalse(self.userReference.isEmailwithExtension("gmail"))

    def testIsTelephoneRightWhenCorrect(self):
        self.configureCorrectUserData()
        self.assertEqual(self.userReference.isTelephoneRight(), 1)

    def testIsTelephoneRightWhenWrongLength(self):
        self.configureCorrectUserData()
        self.userReference.telephone = "983232"
        self.assertEqual(self.userReference.isTelephoneRight(), 0)

    def testIsTelephoneRightWhenNotNumbers(self):
        self.configureCorrectUserData()
        self.userReference.telephone = "983SD2332"
        self.assertEqual(self.userReference.isTelephoneRight(), 0)

    def testIsTelephoneRightWhenWrongFormat(self):
        self.configureCorrectUserData()
        self.userReference.telephone = "098233232"
        self.assertEqual(self.userReference.isTelephoneRight(), 0)

    def testHasTelephoneCorrectNumberWhenTrue(self):
        self.configureCorrectUserData()
        self.assertTrue(self.userReference.hasTelephoneCorrectNumber())

    def testHasTelephoneCorrectNumberWhenFalse(self):
        self.configureCorrectUserData()
        self.userReference.telephone = "23233232"
        self.assertFalse(self.userReference.hasTelephoneCorrectNumber())

    def testIsAddressRightWhenCorrectWhen3DoorNumbers(self):
        self.configureCorrectUserData()
        self.userReference.address = "Canelones 898"
        self.assertEqual(self.userReference.isAddressRight(), 1)

    def testIsAddressRightWhenCorrectWhen4DoorNumbers(self):
        self.configureCorrectUserData()
        self.assertEqual(self.userReference.isAddressRight(), 1)

    def testIsAddressRightWhenWrongFormat(self):
        self.configureCorrectUserData()
        self.userReference.address = "1267 Canelones"
        self.assertEqual(self.userReference.isAddressRight(), 0)

    def testIsAddressRightWhenWrongNoDoorNumbers(self):
        self.configureCorrectUserData()
        self.userReference.address = "Canelones"
        self.assertEqual(self.userReference.isAddressRight(), 0)

    def testIsIdNumberRightWhenCorrectWhenOldFormat(self):
        self.configureCorrectUserData()
        self.userReference.idNumber = "123.456-3"
        self.assertEqual(self.userReference.isIdNumberRight(), 1)

    def testIsIdNumberRightWhenCorrectWhenNewFormat(self):
        self.configureCorrectUserData()
        self.assertEqual(self.userReference.isIdNumberRight(), 1)

    def testIsIdNumberRightWhenWrongOldFormat(self):
        self.configureCorrectUserData()
        self.userReference.idNumber = "1234563"
        self.assertEqual(self.userReference.isIdNumberRight(), 0)

    def testIsIdNumberRightWhenWrongNewFormat(self):
        self.configureCorrectUserData()
        self.userReference.idNumber = "48511126"
        self.assertEqual(self.userReference.isIdNumberRight(), 0)

    def testIsIdNumberRightWhenWrongLength(self):
        self.configureCorrectUserData()
        self.userReference.idNumber = "123"
        self.assertEqual(self.userReference.isIdNumberRight(), 0)

    def testHasIdNumberNewFormatWhenTrue(self):
        self.configureCorrectUserData()
        self.assertTrue(self.userReference.hasIdNumberNewFormat())

    def testHasIdNumberNewFormatWhenFalse(self):
        self.configureCorrectUserData()
        self.userReference.idNumber = "123.456-3"
        self.assertFalse(self.userReference.hasIdNumberNewFormat())

    def testIsNumberNewFormatRightWhenTrue(self):
        self.configureCorrectUserData()
        self.assertTrue(self.userReference.isNumberNewFormatRight())

    def testIsNumberNewFormatRightWhenFalse(self):
        self.configureCorrectUserData()
        self.userReference.idNumber = "48511126"
        self.assertFalse(self.userReference.isNumberNewFormatRight())

    def testAreSymbolsNewPositionRightWhenTrue(self):
        self.configureCorrectUserData()
        self.assertTrue(self.userReference.areSymbolsNewPositionRight())

    def testAreSymbolsNewPositionRightWhenFalse(self):
        self.configureCorrectUserData()
        self.userReference.idNumber = "4-851.112.6"
        self.assertFalse(self.userReference.areSymbolsNewPositionRight())

    def testHasIdNumberOldFormatWhenTrue(self):
        self.configureCorrectUserData()
        self.userReference.idNumber = "123.456-3"
        self.assertTrue(self.userReference.hasIdNumberOldFormat())

    def testHasIdNumberOldFormatWhenFalse(self):
        self.configureCorrectUserData()
        self.assertFalse(self.userReference.hasIdNumberOldFormat())

    def testIsNumberOldFormatRightWhenTrue(self):
        self.configureCorrectUserData()
        self.userReference.idNumber = "123.456-3"
        self.assertTrue(self.userReference.isNumberOldFormatRight())

    def testIsNumberOldFormatRightWhenFalse(self):
        self.configureCorrectUserData()
        self.userReference.idNumber = "1234563"
        self.assertFalse(self.userReference.isNumberOldFormatRight())

    def testAreSymbolsOldPositionRightWhenTrue(self):
        self.configureCorrectUserData()
        self.userReference.idNumber = "123.456-3"
        self.assertTrue(self.userReference.areSymbolsOldPositionRight())

    def testAreSymbolsOldPositionRightWhenFalse(self):
        self.configureCorrectUserData()
        self.userReference.idNumber = "123-456.3"
        self.assertFalse(self.userReference.areSymbolsOldPositionRight())

    def testGetCompleteNameSurname(self):
        self.configureCorrectUserData()
        self.assertEqual(self.userReference.getCompleteNameSurname(), "Fernando Hernandez")

    def testShowInitialData(self):
        self.configureCorrectUserData()
        self.assertEqual(self.userReference.showInitialData(), "\n\nUsernumber: 173631\nPassword: HerisHisis.2\nTelephone: +59898742547\nAddress: Canelones 1267\nID Number: 4.851.112-6\nBirthdate: 04/04/1996")

    def testShowUserInfo(self):
        self.configureCorrectUserData()
        self.assertEqual(self.userReference.showUserInfo(), "173631 ~ HERNANDEZ, Fernando ~ Contact: ferhernagu@gmail.com/098742547")

    def testAreEqualWhenTrue(self):
        self.configureCorrectUserData()
        self.configureUserToCompareData()
        self.assertTrue(self.userReference.areEqual(self.userComparisson))

    def testAreEqualWhenFalseWithDifferentUsernumber(self):
        self.configureCorrectUserData()
        self.configureUserToCompareData()
        self.userComparisson.usernumber = "181201"
        self.assertFalse(self.userReference.areEqual(self.userComparisson))

    def testAreEqualWhenFalseWithDifferentPassword(self):
        self.configureCorrectUserData()
        self.configureUserToCompareData()
        self.userComparisson.password = "HarryPott.2"
        self.assertFalse(self.userReference.areEqual(self.userComparisson))

    def testShowUserRegistry(self):
        self.configureCorrectUserData()
        self.assertEqual(self.userReference.showUserRegistry(), "REGISTRATION: " + self.userReference.registrationDate + ' :::: LAST LOGIN: ' + self.userReference.lastEntryDate)

    def testCheckUserDataWhenAllCorrect(self):
        self.configureCorrectUserData()
        self.assertEqual(self.userReference.checkUserData(), "1111111")

    def testCheckUserDataWhenUsernumberWrong(self):
        self.configureCorrectUserData()
        self.userReference.usernumber = "18AB"
        self.assertEqual(self.userReference.checkUserData(), "0111111")

    def testCheckUserDataWhenPasswordWrong(self):
        self.configureCorrectUserData()
        self.userReference.password = "32Asds"
        self.assertEqual(self.userReference.checkUserData(), "1011111")

    def testCheckUserDataWhenNameSurnameWrong(self):
        self.configureCorrectUserData()
        self.userReference.name = "?aa."
        self.assertEqual(self.userReference.checkUserData(), "1101111")

    def testCheckUserDataWhenEmailWrong(self):
        self.configureCorrectUserData()
        self.userReference.email = "fer@pepito.jpg"
        self.assertEqual(self.userReference.checkUserData(), "1110111")

    def testCheckUserDataWhenAddressWrong(self):
        self.configureCorrectUserData()
        self.userReference.address = "Murcielago"
        self.assertEqual(self.userReference.checkUserData(), "1111011")

    def testCheckUserDataWhenTelephoneWrong(self):
        self.configureCorrectUserData()
        self.userReference.telephone = "NoTelephone"
        self.assertEqual(self.userReference.checkUserData(), "1111101")

    def testCheckUserDataWhenIdNumberWrong(self):
        self.configureCorrectUserData()
        self.userReference.idNumber = "32.54"
        self.assertEqual(self.userReference.checkUserData(), "1111110")

    def testCheckEditionDataWhenAllCorrect(self):
        self.configureCorrectUserData()
        self.userReference.password = "HarryPott.2"
        self.userReference.email = "f_hernandez@ort.edu.uy"
        self.userReference.telephone = "99342145"
        self.userReference.address = "Malvin 3333"
        self.assertEqual(self.userReference.checkEditionData(), "1111")

    def testCheckEditionDataWhenPasswordWrong(self):
        self.configureCorrectUserData()
        self.userReference.password = "Montevideo2"
        self.userReference.email = "f_hernandez@ort.edu.uy"
        self.userReference.telephone = "99342145"
        self.userReference.address = "Malvin 3333"
        self.assertEqual(self.userReference.checkEditionData(), "0111")

    def testCheckEditionDataWhenEmailWrong(self):
        self.configureCorrectUserData()
        self.userReference.password = "HarryPott.2"
        self.userReference.email = "f_hernandez@mile.not"
        self.userReference.telephone = "99342145"
        self.userReference.address = "Malvin 3333"
        self.assertEqual(self.userReference.checkEditionData(), "1011")

    def testCheckEditionDataWhenAddressWrong(self):
        self.configureCorrectUserData()
        self.userReference.password = "HarryPott.2"
        self.userReference.email = "f_hernandez@ort.edu.uy"
        self.userReference.telephone = "99342145"
        self.userReference.address = "NotAddress"
        self.assertEqual(self.userReference.checkEditionData(), "1101")

    def testCheckEditionDataWhenTelephoneWrong(self):
        self.configureCorrectUserData()
        self.userReference.password = "HarryPott.2"
        self.userReference.email = "f_hernandez@ort.edu.uy"
        self.userReference.telephone = "9AS45"
        self.userReference.address = "Malvin 3333"
        self.assertEqual(self.userReference.checkEditionData(), "1110")

    def testIsUserWellRegisteredWhenAllCorrect(self):
        self.configureCorrectUserData()
        self.assertTrue(self.userReference.isUserWellRegistered())

    def testIsUserWellRegisteredWhenUsernumberWrong(self):
        self.configureCorrectUserData()
        self.userReference.usernumber = "18AB"
        self.assertFalse(self.userReference.isUserWellRegistered())

    def testIsUserWellRegisteredWhenPasswordWrong(self):
        self.configureCorrectUserData()
        self.userReference.password = "32Asds"
        self.assertFalse(self.userReference.isUserWellRegistered())

    def testIsUserWellRegisteredWhenNameSurnameWrong(self):
        self.configureCorrectUserData()
        self.userReference.name = "?aa."
        self.assertFalse(self.userReference.isUserWellRegistered())

    def testIsUserWellRegisteredWhenEmailWrong(self):
        self.configureCorrectUserData()
        self.userReference.email = "fer@pepito.jpg"
        self.assertFalse(self.userReference.isUserWellRegistered())

    def testIsUserWellRegisteredWhenAddressWrong(self):
        self.configureCorrectUserData()
        self.userReference.address = "Murcielago"
        self.assertFalse(self.userReference.isUserWellRegistered())

    def testIsUserWellRegisteredWhenTelephoneWrong(self):
        self.configureCorrectUserData()
        self.userReference.telephone = "NoTelephone"
        self.assertFalse(self.userReference.isUserWellRegistered())

    def testIsUserWellRegisteredWhenIdNumberWrong(self):
        self.configureCorrectUserData()
        self.userReference.idNumber = "32.54"
        self.assertFalse(self.userReference.isUserWellRegistered())

    def testisDataToEditRightWhenAllCorrect(self):
        self.configureCorrectUserData()
        self.userReference.password = "HarryPott.2"
        self.userReference.email = "f_hernandez@ort.edu.uy"
        self.userReference.telephone = "99342145"
        self.userReference.address = "Malvin 3333"
        self.assertTrue(self.userReference.isDataToEditRight())

    def testisDataToEditRightWhenPasswordWrong(self):
        self.configureCorrectUserData()
        self.userReference.password = "Montevideo2"
        self.userReference.email = "f_hernandez@ort.edu.uy"
        self.userReference.telephone = "99342145"
        self.userReference.address = "Malvin 3333"
        self.assertFalse(self.userReference.isDataToEditRight())

    def testisDataToEditRightWhenEmailWrong(self):
        self.configureCorrectUserData()
        self.userReference.password = "HarryPott.2"
        self.userReference.email = "f_hernandez@mile.not"
        self.userReference.telephone = "99342145"
        self.userReference.address = "Malvin 3333"
        self.assertFalse(self.userReference.isDataToEditRight())

    def testisDataToEditRightWhenAddressWrong(self):
        self.configureCorrectUserData()
        self.userReference.password = "HarryPott.2"
        self.userReference.email = "f_hernandez@ort.edu.uy"
        self.userReference.telephone = "99342145"
        self.userReference.address = "NotAddress"
        self.assertFalse(self.userReference.isDataToEditRight())

    def testisDataToEditRightWhenTelephoneWrong(self):
        self.configureCorrectUserData()
        self.userReference.password = "HarryPott.2"
        self.userReference.email = "f_hernandez@ort.edu.uy"
        self.userReference.telephone = "9AS45"
        self.userReference.address = "Malvin 3333"
        self.assertFalse(self.userReference.isDataToEditRight())
