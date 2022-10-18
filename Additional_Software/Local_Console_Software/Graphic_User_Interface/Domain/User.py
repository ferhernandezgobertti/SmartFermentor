import sys
from datetime import date
from datetime import datetime

class User():

    entryTime = datetime.today()
    registrationDate = entryTime.strftime("%b %d %Y %H:%M:%S")
    lastEntryDate = entryTime.strftime("%b %d %Y %H:%M:%S")

    def __init__(self, userData):
        self.usernumber = str(userData[0])
        self.password = str(userData[1])
        self.name = str(userData[2])
        self.surname = str(userData[3])
        self.email = str(userData[4])
        self.telephone = str(userData[5])
        self.address = str(userData[6])
        self.idNumber = str(userData[7])
        self.birthDate = str(userData[8])
        self.gamesScore = [0, 0, 0]
        self.fermentationsQuantity = 0

    def updateLastEntry(self):
        newEntryTime = datetime.today()
        self.lastEntryDate = newEntryTime.strftime("%b %d %Y %H:%M:%S")

    def addFermentation(self):
        self.fermentationsQuantity = self.fermentationsQuantity + 1

    def isPasswordCorrect(self, passwordInput):
        passwordCorrect = 0
        if(passwordInput==self.password):
            passwordCorrect = 1
        return passwordCorrect

    def checkUserData(self):
        return str(self.isUsernumberRight()) + str(self.isPasswordRight()) + str(self.isNameSurnameRight()) + str(self.isEmailRight()) + str(self.isAddressRight()) + str(self.isTelephoneRight()) + str(self.isIdNumberRight())

    def checkEditionData(self):
        return str(self.isPasswordRight()) + str(self.isEmailRight()) + str(self.isAddressRight()) + str(self.isTelephoneRight())

    def isUserWellRegistered(self):
        if(self.isUsernumberRight()==1 and self.isPasswordRight()==1 and self.isNameSurnameRight()==1 and self.isEmailRight()==1 and self.isAddressRight()==1 and self.isTelephoneRight()==1 and self.isIdNumberRight()==1):
            return True
        else:
            return False

    def isDataToEditRight(self):
        if(self.isPasswordRight()==1 and self.isEmailRight()==1 and self.isAddressRight()==1 and self.isTelephoneRight()==1):
            return True
        else:
            return False

    def isUsernumberRight(self):
        usernameRight = 0
        if(len(self.usernumber)<=6 and len(self.usernumber)>=4 and self.isContentNumber(self.usernumber)):
            usernameRight = 1
        return usernameRight

    def isContentNumber(self, content):
        try:
            int(content)
            return True
        except ValueError:
            return False

    def isPasswordRight(self):
        passwordRight = 0
        if(len(self.password)>=6 and len(self.password)<=12 and self.isPasswordWithUpper()==1 and self.isWordWithSymbol(self.password, "0123456789")==1 and self.isWordWithSymbol(self.password, ".,;<>|/%&^!")==1):
            passwordRight = 1
        return passwordRight

    def isNameSurnameRight(self):
        nameSurnameRight = 0
        if(len(self.name)>=1 and len(self.surname)>=1 and len(self.name)<=10 and len(self.surname)<=12 and self.isNameSurnameWithUpper()==1 and self.isNameSurnameWithSymbol()==0):
            nameSurnameRight = 1
        return nameSurnameRight

    def isNameSurnameWithSymbol(self):
        nameSurnameWithSymbol = 0
        if(self.isWordWithSymbol(self.name, "0123456789")==1 or self.isWordWithSymbol(self.surname, "0123456789")==1 or self.isWordWithSymbol(self.name, ".,;<>|/%&^!")==1 or self.isWordWithSymbol(self.surname, ".,;<>|/%&^!")==1):
            nameSurnameWithSymbol = 1
        return nameSurnameWithSymbol

    def isNameSurnameWithUpper(self):
        nameSurnameWithUpper = 0
        if(not self.name.islower() and not self.name.isupper() and not self.surname.islower() and not self.surname.isupper()):
            nameSurnameWithUpper = 1
        return nameSurnameWithUpper

    def isPasswordWithUpper(self):
        passwordWithUpper = 0
        if(not self.password.islower() and not self.password.isupper()):
            passwordWithUpper = 1
        return passwordWithUpper

    def isWordWithSymbol(self, word, symbolPossibilities):
        wordWithSymbol = 0
        interval = 0
        while(interval<len(word)-1):
            if(word.find(symbolPossibilities[interval])!=-1):
                wordWithSymbol = 1
                break
            interval = interval + 1
        return wordWithSymbol

    def isEmailRight(self):
        emailRight = 0
        if(self.isEmailWithUsername() and self.isEmailEndingCorrect() and (self.isEmailwithExtension("@gmail.com") or self.isEmailwithExtension("@adinet.com") or self.isEmailwithExtension("@vera.com") or self.isEmailwithExtension("@yahoo.com") or self.isEmailwithExtension("@ort.edu.uy"))):
            emailRight = 1
        return emailRight

    def isEmailWithUsername(self):
        lettersRead = 0
        while(lettersRead<len(self.email)):
            if(self.email[lettersRead]=='@'):
                break
            lettersRead = lettersRead + 1
        if(lettersRead<len(self.email)):
            return True
        else:
            return False

    def isEmailEndingCorrect(self):
        endingCharactersCommercial = self.email[len(self.email)-4:len(self.email)]
        endingCharactersEducational = self.email[len(self.email)-7:len(self.email)]
        if(endingCharactersCommercial==".com" or endingCharactersEducational==".edu.uy"):
            return True
        else:
            return False

    def isEmailwithExtension(self, extension):
        if(extension in self.email):
            return True
        else:
            return False

    def isTelephoneRight(self):
        telephoneRight = 0
        if(len(self.telephone)==8 and self.isContentNumber(self.telephone) and self.hasTelephoneCorrectNumber()):
            telephoneRight = 1
        return telephoneRight

    def hasTelephoneCorrectNumber(self):
        beginningNumbers = self.telephone[0:2]
        if(beginningNumbers=="94" or beginningNumbers=="95" or beginningNumbers=="96" or beginningNumbers=="98" or beginningNumbers=="99"):
            return True
        else:
            return False

    def isAddressRight(self):
        addressRight = 0
        if(self.address[len(self.address)-3:len(self.address)].isdigit() or self.address[len(self.address)-4:len(self.address)].isdigit()):
            addressRight = 1
        return addressRight

    def isIdNumberRight(self):
        idNumberRight = 0
        if(len(self.idNumber)==11 and self.hasIdNumberNewFormat()):
            idNumberRight = 1
        if(len(self.idNumber)==9 and self.hasIdNumberOldFormat()):
            idNumberRight = 1
        return idNumberRight

    def hasIdNumberNewFormat(self):
        if(self.isNumberNewFormatRight() and self.areSymbolsNewPositionRight()):
            return True
        else:
            return False

    def isNumberNewFormatRight(self):
        return self.idNumber[0:1].isdigit() and self.idNumber[2:5].isdigit() and self.idNumber[6:9].isdigit() and self.idNumber[10:11].isdigit()

    def areSymbolsNewPositionRight(self):
        return self.idNumber[1:2]=='.' and self.idNumber[5:6]=='.' and self.idNumber[9:10]=='-'

    def hasIdNumberOldFormat(self):
        if(self.isNumberOldFormatRight() and self.areSymbolsOldPositionRight()):
            return True
        else:
            return False

    def isNumberOldFormatRight(self):
        return self.idNumber[0:3].isdigit() and self.idNumber[4:7].isdigit() and self.idNumber[8:9].isdigit()

    def areSymbolsOldPositionRight(self):
        return self.idNumber[3:4]=='.' and self.idNumber[7:8]=='-'

    def getCompleteNameSurname(self):
        return self.name+" "+self.surname

    def showParticularInitialData(self):
        return ""

    def showInitialData(self):
        return "\n\nUsernumber: "+self.usernumber+"\nPassword: "+self.password+"\nTelephone: +598"+self.telephone+"\nAddress: "+self.address+"\nID Number: "+self.idNumber+"\nBirthdate: "+self.birthDate+self.showParticularInitialData()

    def showUserInfo(self):
        return self.usernumber + ' ~ ' + self.surname.upper()+', '+self.name+' ~ Contact: '+ self.email + "/0" + self.telephone

    def areEqual(self, otherUser):
        if(self.usernumber==otherUser.usernumber and self.password==otherUser.password):
            return True
        else:
            return False

    def showUserRegistry(self):
        return "REGISTRATION: " + self.registrationDate + ' :::: LAST LOGIN: ' + self.lastEntryDate
