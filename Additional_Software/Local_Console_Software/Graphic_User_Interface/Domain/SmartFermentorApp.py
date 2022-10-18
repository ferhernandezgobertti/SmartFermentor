import sys, os, json, base64, smtplib
from datetime import date, datetime
from Domain.Administrator import Administrator
from Domain.Student import Student
from Domain.Professor import Professor
from Domain.User import User
from Domain.ListProfessors import ListProfessors
from Domain.ListStudents import ListStudents
from Domain.ListFermentations import ListFermentations
from Domain.ListReservations import ListReservations
from Domain.ListVersions import ListVersions
from Domain.ListInformations import ListInformations
from Domain.Status import Status
from Domain.ListGames import ListGames
from pathlib import Path
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import hmac, hashlib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from os.path import basename

class SmartFermentorApp():

    def __init__(self):
        self.rootDirectory = "SystemData/"
        self.controlDirectory = "ControlData/"
        self.admin = Administrator()
        self.listProfessors = ListProfessors()
        self.listStudents = ListStudents()
        self.systemCurrentStatus = Status()
        self.listFermentations = ListFermentations()
        self.listReservations = ListReservations()
        self.systemData = ListInformations()
        self.versionsHistory = ListVersions()
        self.gamesEntertainment = ListGames()
        self.loadSmartData()
        self.checkReservationNotification()
        self.updateSystemDataHistory()
        #self.versionNumber = [0.0, 0.0, 0.0]
        #self.versionCommentary = ["", "", ""]
        print("SMART FERMENTOR CARGADO !!!!!!!!!!!!!!!!!")

    def isUserDataRight(self, userToCheck):
        studentPosition = self.listStudents.isStudentRegistered(userToCheck)
        professorPosition = self.listProfessors.isProfessorRegistered(userToCheck)
        userData = 0
        if(studentPosition[0]!=-1):
            userData = 1
        if(studentPosition[1]!=-1):
            userData = 2
            self.systemCurrentStatus.setStatusStudentLogged(studentPosition[1])
        if(professorPosition[0]!=-1):
            userData = 3
        if(professorPosition[1]!=-1):
            userData = 4
            self.systemCurrentStatus.setStatusProfessorLogged(professorPosition[1])
        print("USER DATA: ", userData)
        return userData

    def doesFileExist(self, filename):
        filePath = Path(filename)
        return filePath.exists()

    def eraseDataFile(self, filename):
        if(self.doesFileExist(filename)):
            os.remove(filename)

    def getDayTimeMomentMessage(self, listOfTimeMoments):
        currentTime = datetime.today()
        timeMoment = listOfTimeMoments[0]
        if(currentTime.hour<=6):
            timeMoment = listOfTimeMoments[1]
        if(currentTime.hour>=18):
            timeMoment = listOfTimeMoments[2]
        elif(currentTime.hour>=12):
            timeMoment = listOfTimeMoments[3]
        return timeMoment

    def sendEmail(self, destinataries, mailInformation):
        from_addr = 'Smart Fermentor - Universidad ORT Uruguay'
        to_addr = destinataries
        mailToSend = MIMEMultipart()
        mailToSend['From'] = from_addr
        mailToSend['To'] = "undisclosed-recipient"
        mailToSend['Subject'] = mailInformation[0] #'Registration Notice'
        attachment =  mailInformation[1] #'mailPresentation.png'
        body =  mailInformation[2] #"Your Password: "

        if(mailInformation[3]=="IMAGE"):
            imageBytes = open(attachment, 'rb')
            imageMIME = MIMEImage(imageBytes.read())
            imageBytes.close()
            imageMIME.add_header('Content-ID', '<{}>'.format(attachment))
            mailToSend.attach(imageMIME)

        mailToSend.attach(MIMEText(body, 'plain'))

        if(mailInformation[3]=="FILE"):
            with open(attachment, "rb") as fileToSend:
                fileContent = MIMEApplication( fileToSend.read(), Name=basename(attachment) )
            fileContent['Content-Disposition'] = 'attachment; filename="%s"' % basename(attachment)
            mailToSend.attach(fileContent)

        smtp_server = smtplib.SMTP('smtp.gmail.com', 587) #Specify Gmail Mail server
        smtp_server.ehlo() #Send mandatory 'hello' message to SMTP server
        smtp_server.starttls() #Start TLS Encryption as we're not using SSL.
        smtp_server.login('smartfermentor@gmail.com', 'Smart.1450') #Login to gmail: Account | Password
        smtp_server.sendmail(from_addr, to_addr, mailToSend.as_string()) #Compile email: From, To, Email body
        smtp_server.quit()

    def updateSystemDataHistory(self):
        currentDate = date.today()
        if(currentDate.month != self.systemData.informations[5].informationDate.month or currentDate.year != self.systemData.informations[5].informationDate.year):
            systemDataBodyMail = "\n\nAdministrator :\n\n    Following is a summary of the statistics this Platform has been collecting regarding administrative issues such as Number of Users Registerered, Number of Fermentations Done and so on. We hope you found this information particularly useful for the days to come.\n\n"+self.systemData.collectGeneralInformation()+"\n\nBy all means if you have any doubt, consult Carlos Sanguinetti and Felipe Machado.\n\nThank you for your preference,\n        Smart Fermentor Team"
            #self.sendEmail(['smartfermentor@gmail.com'], ['Your Monthly Summmary: The System Usage so far', 'Images/MailContent/summaryInformationMail.png', systemDataBodyMail, "IMAGE"])
        self.systemData.updateInformationsHistory()

    def updateFermentationControlsData(self):
        currentFermentation = self.listFermentations.fermentations[self.systemCurrentStatus.fermentationActual]
        velocityControlQuantity = len(currentFermentation.magnitudesToControl.velocities)
        temperatureControlQuantity = len(currentFermentation.magnitudesToControl.temperatures)
        potentialControlQuantity = len(currentFermentation.magnitudesToControl.potentialsHydrogen)
        if(velocityControlQuantity>0 and temperatureControlQuantity==0 and potentialControlQuantity==0):
            self.systemData.informations[4].addFermentationWithOnlyVelocityControl()
        if(velocityControlQuantity==0 and temperatureControlQuantity>0 and potentialControlQuantity==0):
            self.systemData.informations[4].addFermentationWithOnlyTemperatureControl()
        if(velocityControlQuantity==0 and temperatureControlQuantity==0 and potentialControlQuantity>0):
            self.systemData.informations[4].addFermentationWithOnlyPotentialControl()
        if(velocityControlQuantity>0 and temperatureControlQuantity>0 and potentialControlQuantity==0):
            self.systemData.informations[4].addFermentationWithVelocityAndTemperatureControl()
        if(velocityControlQuantity>0 and temperatureControlQuantity==0 and potentialControlQuantity>0):
            self.systemData.informations[4].addFermentationWithVelocityAndPotentialControl()
        if(velocityControlQuantity==0 and temperatureControlQuantity>0 and potentialControlQuantity>0):
            self.systemData.informations[4].addFermentationWithTemperatureAndPotentialControl()
        if(velocityControlQuantity>0 and temperatureControlQuantity>0 and potentialControlQuantity>0):
            self.systemData.informations[4].addFermentationWithAllControls()

    def updateFermentationVerificationsData(self):
        currentFermentation = self.listFermentations.fermentations[self.systemCurrentStatus.fermentationActual]
        if(not currentFermentation.isFermentationContinuing):
            if(not currentFermentation.isConnectionChecked and not currentFermentation.isCalibrated):
                self.systemData.informations[4].addFermentationWithNothingVerified()
            if(currentFermentation.isConnectionChecked and not currentFermentation.isCalibrated):
                self.systemData.informations[4].addFermentationWithOnlyConnectionVerified()
            if(not currentFermentation.isConnectionChecked and currentFermentation.isCalibrated):
                self.systemData.informations[4].addFermentationWithOnlyCalibrationVerified()
            if(currentFermentation.isConnectionChecked and currentFermentation.isCalibrated):
                self.systemData.informations[4].addFermentationWithConnectionAndCalibrationVerified()

    def checkReservationNotification(self):
        position = 0
        for eachReservation in self.listReservations.reservations:
            if(eachReservation.isInNeedOfNotification()):
                reservationReminderBodyMail = "\n\nDear Professor "+eachReservation.professorResponsible.getCompleteNameSurname()+" and Student "+eachReservation.userToReserve.getCompleteNameSurname()+",\n\n    We would like to remind you that you soon have a Reservation to use our System. This Reservation is from "+eachReservation.datesOfReservation[0].strftime("%d/%B/%Y")+" to "+eachReservation.datesOfReservation[len(eachReservation.datesOfReservation)-1].strftime("%d/%B/%Y")+" and can still be removed and changed. \n\nBy all means if you have any doubt, consult Carlos Sanguinetti and Felipe Machado.\n\nThank you for your preference,\n        Smart Fermentor Team"
                self.sendEmail([eachReservation.professorResponsible.email, eachReservation.userToReserve.email], ['Reminder: Your RESERVATION is NEARBY', 'Images/MailContent/reservationInformationMail.png', reservationReminderBodyMail, "IMAGE"])
                self.listReservations.reservations[position] = False
            position = position + 1

    def encryptAES256(self, interestedData, key, initVector):
        keyByte = key.encode('utf-8')
        keyByte = keyByte.ljust(32, "\0".encode('utf-8'))
        if (len(keyByte)>32):
            keyByte = keyByte[:32]
        initVectorByte = initVector.encode('utf-8')
        initVectorByte = initVectorByte.ljust(16, "\0".encode('utf-8'))
        if (len(initVectorByte)>16):
            initVectorByte = initVectorByte[:16]

        paddingLength = 16 - len(interestedData)%16
        padding = chr(paddingLength)*paddingLength
        interestedData += padding
        cryptor = AES.new(keyByte, AES.MODE_CBC, initVectorByte)
        print("INTERESTED DATA: ", interestedData)
        dataEncrypted = cryptor.encrypt(interestedData.encode('utf-8'))
        dataEncrypted64 = base64.b64encode(dataEncrypted).decode('utf-8')
        return dataEncrypted64

    def encryptData(self, filenamesEncryption):
        key = "Biotec.ORT1450"
        initVector = "CB+I_OrtURU"
        fileInput = open(self.rootDirectory+filenamesEncryption[1], 'r+')
        data = fileInput.read()
        fileInput.close()
        dataEncrypted = self.encryptAES256(data, key, initVector)
        digestedData = hmac.new(b"my_secret", data.encode("utf-8"), digestmod=hashlib.sha256).digest()
        dataHash = base64.b64encode(digestedData).decode()
        jsonDataProtected = {"info": dataEncrypted, "hash": dataHash}
        particularJsonDataProtected = json.dumps(jsonDataProtected)
        fileOutput = open(self.rootDirectory+filenamesEncryption[0], 'w')
        dataJson = fileOutput.write(particularJsonDataProtected)
        fileOutput.close()
        print("ENCRYPTED: ", data)
        self.eraseDataFile(filenamesEncryption[1])

    def decryptAES256(self, interestedEncryptedData, key, initVector):
        dataByte = base64.b64decode(interestedEncryptedData.encode('utf-8'))
        keyByte = key.encode('utf-8')
        keyByte = keyByte.ljust(32, "\0".encode('utf-8'))
        if (len(keyByte)>32):
            keyByte = keyByte[:32]
        initVectorByte = initVector.encode('utf-8')
        initVectorByte = initVectorByte.ljust(16, "\0".encode('utf-8'))
        if (len(initVectorByte)>16):
            initVectorByte = initVectorByte[:16]
        cryptor = AES.new(keyByte, AES.MODE_CBC, initVectorByte)
        cryptedData = cryptor.decrypt(dataByte)

        padLength = ord(cryptedData.decode('utf-8')[-1])
        decryptedData = cryptedData.decode('utf-8')[:-padLength]
        return decryptedData

    def decryptData(self, filename):
        fileInput = open(filename, 'r')
        fileData = fileInput.read()
        fileInput.close()
        jsonEncrypted = json.loads(fileData)
        key = "Biotec.ORT1450"
        initVector = "CB+I_OrtURU"
        data = self.decryptAES256(jsonEncrypted['info'], key, initVector)
        print("DECRYPTED: ", data)
        return data #decode("utf-8")

    def loadParticularDataFromFile(self, whereToLoad, fileEncrypted):
        print("VERIFICO EXISTENCIA DE: ", self.rootDirectory+fileEncrypted)
        if(self.doesFileExist(self.rootDirectory+fileEncrypted)):
            particularDecrypted = self.decryptData(self.rootDirectory+fileEncrypted)
            particularDataJSON = json.loads(particularDecrypted)
            print("ADMIN DATA: ", particularDataJSON)
            whereToLoad.loadJSONData(particularDataJSON)

    def loadListsDataFromFile(self, whereToLoad, fileEncrypted):
        if(self.doesFileExist(self.rootDirectory+fileEncrypted)):
            usersDecrypted = self.decryptData(self.rootDirectory+fileEncrypted)
            usersDataJSON = json.loads(usersDecrypted)
            print("USERS DATA: ", usersDataJSON)
            for eachUser in usersDataJSON:
                whereToLoad.loadJSONData(eachUser)

    def loadStatusDataFromFile(self):
        if(self.doesFileExist(self.rootDirectory+'StatusDataServer.json')):
            with open(self.rootDirectory+'StatusDataServer.json', 'r') as fileInput:
                statusDataFile = fileInput.read()
                statusDataJSON = json.loads(statusDataFile)
                print("STATUS DATA JSON: ", statusDataJSON)
                self.systemCurrentStatus.loadJSONData(statusDataJSON)

    def saveStatusDataToFile(self):
        statusFileJSON = open(self.rootDirectory+'StatusDataServer.json', 'w')
        statusData = self.systemCurrentStatus.getJSONData()
        statusDataJSON = json.dumps(statusData)
        statusFileJSON.write(statusDataJSON)
        statusFileJSON.close()
        print("STATUS DATA JSON: ", statusDataJSON)

    def saveParticularDataToFile(self, informationToSave, filenames):
        particularFileJSON = open(self.rootDirectory+filenames[1], "w")
        particularData = informationToSave.getJSONData()
        particularDataJSON = json.dumps(particularData)
        particularFileJSON.write(particularDataJSON)
        particularFileJSON.close()
        self.encryptData(filenames)
        os.remove(self.rootDirectory+filenames[1])

    def saveListDataToFile(self, informationToSave, filenames):
        print("LARGO LISTA: ", len(informationToSave))
        print("EXISTENCIA: ", self.rootDirectory+filenames[0])
        if(len(informationToSave)!=0 and self.doesFileExist(self.rootDirectory+filenames[0])):
            os.remove(self.rootDirectory+filenames[0])
            print("ENCONTRO Y REMOVIO ARCHIVO: ", self.rootDirectory+filenames[0])
        if(len(informationToSave)>0):
            usersFileJSON = open(self.rootDirectory+filenames[1], "w")
            usersInformation = []
            print("LARGO LISTA ADENTRO IF: ", len(informationToSave))

            for eachUser in informationToSave:
                userData = eachUser.getJSONData()
                usersInformation.append(userData)

            usersDataJSON = json.dumps(usersInformation)
            usersFileJSON.write(usersDataJSON)
            usersFileJSON.close()
            self.encryptData(filenames)
            os.remove(self.rootDirectory+filenames[1])
            print("DATOS DE USUARIOS SALVADOS")

    def saveParticularVersionListDataToFile(self, particularVersionList, filenames):
        if(len(particularVersionList)!=0 and self.doesFileExist(self.rootDirectory+filenames[0])):
            os.remove(self.rootDirectory+filenames[0])
            print("REMOVIO VERSION")
        if(len(particularVersionList)!=0):
            versionsFileJSON = open(self.rootDirectory+filenames[1], "w")
            versionsInformation = []
            for eachVersion in particularVersionList:
                versionData = eachVersion.getJSONData()
                versionsInformation.append(versionData)
            versionsDataJSON = json.dumps(versionsInformation)
            versionsFileJSON.write(versionsDataJSON)
            versionsFileJSON.close()
            self.encryptData(filenames)
            os.remove(self.rootDirectory+filenames[1])

    def saveVersionsListDataToFile(self, directoryName):
        self.saveParticularVersionListDataToFile(self.versionsHistory.velocityVersions, [directoryName+'VersionsVelocity.json', directoryName+'VersionsVelocityData.bin'])
        self.saveParticularVersionListDataToFile(self.versionsHistory.temperatureVersions, [directoryName+'VersionsTemperature.json', directoryName+'VersionsTemperatureData.bin'])
        self.saveParticularVersionListDataToFile(self.versionsHistory.potentialVersions, [directoryName+'VersionsPotential.json', directoryName+'VersionsPotentialData.bin'])

    def configureInformationDataFromFile(self):
        if(len(self.systemData.informations)<6):
            self.systemData.informations = []
            self.systemData.initializeInformationData()

    def loadVersionsDataFromFile(self):
        self.loadListsDataFromFile(self.versionsHistory.velocityVersions, 'VersionsVelocityData.json')
        self.loadListsDataFromFile(self.versionsHistory.temperatureVersions, 'VersionsTemperatureData.json')
        self.loadListsDataFromFile(self.versionsHistory.potentialVersions, 'VersionsPotentialData.json')

    def loadSmartData(self):
        print("CARGO DATOS")
        self.loadParticularDataFromFile(self.admin, 'AdministratorData.json')
        self.loadListsDataFromFile(self.listProfessors, 'ProfessorsData.json')
        self.loadListsDataFromFile(self.listStudents, 'StudentsData.json')
        self.loadParticularDataFromFile(self.systemCurrentStatus, 'StatusData.json')
        self.loadListsDataFromFile(self.listFermentations, 'FermentationsData.json')
        self.loadListsDataFromFile(self.listReservations, 'ReservationsData.json')
        self.loadListsDataFromFile(self.systemData, 'SystemInformationData.json')
        self.configureInformationDataFromFile()
        self.loadParticularDataFromFile(self.systemCurrentStatus, 'StatusData.json')
        self.loadVersionsDataFromFile()
        self.loadParticularDataFromFile(self.gamesEntertainment, 'EntertainmentData.json') #NUEVO
        self.loadStatusDataFromFile()

    def logFermentationsOnFile(self):
        if(len(self.listFermentations.fermentations)>0):
            filenameFermentation = self.controlDirectory+"FermentationLOG.txt"
            self.eraseDataFile(filenameFermentation)
            for eachFermentation in self.listFermentations.fermentations:
                if(len(eachFermentation.dataFilenames)>0):
                    with open(filenameFermentation, 'a') as logFermentationData:
                        logFermentationData.write(eachFermentation.logFilenamesInformation())
                        logFermentationData.close()

    def saveSmartData(self, directoryName):
        self.logFermentationsOnFile()
        self.saveStatusDataToFile()
        self.saveParticularDataToFile(self.admin, [directoryName+'AdministratorData.json', directoryName+'Administrator.json'])
        self.saveListDataToFile(self.listProfessors.professors, [directoryName+'ProfessorsData.json', directoryName+'Professors.json'])
        self.saveListDataToFile(self.listStudents.students, [directoryName+'StudentsData.json', directoryName+'Students.json'])
        self.saveParticularDataToFile(self.systemCurrentStatus, [directoryName+'StatusData.json', directoryName+'Status.json'])
        self.saveListDataToFile(self.listFermentations.fermentations, [directoryName+'FermentationsData.json', directoryName+'Fermentations.json'])
        self.saveListDataToFile(self.listReservations.reservations, [directoryName+'ReservationsData.json', directoryName+'Reservations.json'])
        self.saveListDataToFile(self.systemData.informations, [directoryName+'SystemInformationData.json', directoryName+'SystemInformations.json'])
        self.saveVersionsListDataToFile(directoryName)
        self.saveParticularDataToFile(self.gamesEntertainment, [directoryName+'EntertainmentData.json', directoryName+'Entertainment.json'])

    def clearAllVersions(self):
        if(len(self.versionsHistory.velocityVersions)>0):
            self.versionsHistory.removeAllVersionsOfMagnitude(self.versionsHistory.velocityVersions)
        if(len(self.versionsHistory.temperatureVersions)>0):
            self.versionsHistory.removeAllVersionsOfMagnitude(self.versionsHistory.temperatureVersions)
        if(len(self.versionsHistory.potentialVersions)>0):
            self.versionsHistory.removeAllVersionsOfMagnitude(self.versionsHistory.potentialVersions)
