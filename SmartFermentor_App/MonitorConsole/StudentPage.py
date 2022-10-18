import sys, tkinter.font, gi
gi.require_version('Wnck', '3.0')
from gi.repository import Wnck
import datetime, threading, itertools, time
from datetime import date, datetime, timedelta, time
from tkinter import *
from tkinter import ttk, messagebox
from MonitorConsole.Picture import Picture
from Domain.User import User
from Domain.Fermentation import Fermentation
from Domain.Reservation import Reservation
from Domain.Version import Version
from PIL import Image, ImageTk
from pathlib import Path
import webbrowser
from googlesearch import search
import xlwt, xlrd
from xlwt import *
import tzlocal, pytz
from MonitorConsole.OriginalLanguage import OriginalLanguage
from MonitorConsole.SpanishLanguage import SpanishLanguage
from MonitorConsole.PortugueseLanguage import PortugueseLanguage
from MonitorConsole.GermanLanguage import GermanLanguage

class StudentPage(Frame):

    def setFonts(self):
        self.colorORT = "#085454"
        self.buttonFont = tkinter.font.Font(family = 'Helvetica', size = 14, weight = 'bold')
        self.bigTitleFont = tkinter.font.Font(family = 'Helvetica', size = 32, weight = 'bold')
        self.titleFont = tkinter.font.Font(family = 'Helvetica', size = 20, weight = 'bold')
        self.subtitleFont = tkinter.font.Font(family = 'Comic Sans', size = 16, weight = 'bold')
        self.reservationFont = tkinter.font.Font(family = 'Comic Sans MS', size = 10, weight = 'bold')
        self.gameFont = tkinter.font.Font(family = 'Comic Sans MS', size = 16, weight = 'bold')
        self.userInfoFont = tkinter.font.Font(family = 'Arial', size = 26, weight = 'bold')
        self.statusFont = tkinter.font.Font(family = 'Arial', size = 16, weight = 'bold')
        self.inputFont = tkinter.font.Font(family = 'Times', size = 16)
        self.destinataryFont = tkinter.font.Font(family = 'Times', size = 20)
        self.searchFont = tkinter.font.Font(family = 'Arial', size = 20)
        self.infoFont = tkinter.font.Font(family = 'Times', size = 12)
        self.listElementFont = tkinter.font.Font(family = 'Times', size = 10)
        self.bodyMessageFont = tkinter.font.Font(family = 'Times New Roman', size = 12, weight = 'bold')
        self.groupMessageFont = tkinter.font.Font(family = 'Times New Roman', size = 14, weight = 'bold')

    def setVariables(self):
        self.logOutImage = PhotoImage(file="Images/Logos/logOutLogo.gif")
        self.notifyEraseReservation = IntVar()
        self.isSendFileSelected = IntVar()
        self.helpDisplayed = False
        self.hasCheckedConnection = False
        self.hasCalibratedSensorLow = False
        self.hasCalibratedSensorMiddle = False
        self.hasCalibratedSensorHigh = False
        self.hasExpulsedLiquidAcid = False
        self.hasExpulsedLiquidBase = False
        self.doneLoading = False
        self.extensionX = 466
        self.extensionY = 268
        self.pageOfListFermentations = 0
        self.gameIdentifier = 0

    def setLists(self):
        self.monthsName = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        self.fermentationInput = []
        self.blockFirstWeek = []
        self.blockSecondWeek = []
        self.blockThirdWeek = []
        self.blockFourthWeek = []
        self.blockFifthWeek = []
        self.reservationCheck = []
        self.reservationErase = []
        self.platformInformation = []
        self.passwordInput = []
        self.mailInformation = []
        self.passwordTitle = []
        self.pageNumberOfFermentationList = []
        self.expulsionOption = []
        self.temperatureTesting = []
        self.potentialTesting = []
        self.columnPlaceLeaderboards = []
        self.columnPlayerLeaderboards = []
        self.columnPointsLeaderboards = []

    def placeStaticPictures(self, controller):
        controller.setHeaderSmart(self, 'SmartStudent', self.logOutImage)
        self.studentInformation = Label(self, text=controller.application.listStudents.students[controller.application.systemCurrentStatus.userLogged].showUserRegistry(), font=self.infoFont, fg = 'white', bg = self.colorORT)
        self.studentInformation.place(x=845, y=120)

    def showHelp(self):
        if(self.helpDisplayed == False):
            self.canvas.place(x=0, y=140)
            self.helpDisplayed = True
        else:
            self.canvas.place(x=1000, y=1000)
            self.helpDisplayed = False

    def minimizeWindow(self):
        print("MINIMIZE")
        screen = Wnck.Screen.get_default()
        screen.force_update()
        windows = screen.get_windows()
        for w in windows:
            if ('SMARTFERMENTOR' in w.get_name()):
                w.minimize()
                print("VENTANA: ", w.get_name())

    def setHelpBar(self, controller):
        self.versionInfo = Label(self, text = controller.currentLanguage.adminPageContent[11], fg = 'dark green', bg = 'white', font = self.groupMessageFont, height = 1, width = 82, justify='center') #anchor = NE)
        self.versionInfo.place(x=142+47+47+47+47, y=470+self.extensionY)
        self.minimizeSystem = Button(self, text=controller.currentLanguage.adminPageContent[21], command=lambda:self.minimizeWindow(), relief = RAISED, fg='white', bg = 'blue', font=self.bodyMessageFont, compound=CENTER, height = 1, width = 10)
        self.minimizeSystem.place(x=1155, y=470+self.extensionY)
        #self.minimizeSystem = Button(self, text=controller.currentLanguage.adminPageContent[21], command=lambda:self.onClosing(controller), relief = RAISED, fg='white', bg = 'blue', font=self.bodyMessageFont, compound=CENTER, height = 1, width = 10)
        #self.minimizeSystem.place(x=1155, y=470+self.extensionY)
        self.closeSystem = Button(self, text=controller.currentLanguage.adminPageContent[22], command=lambda:self.onClosing(controller), relief = RAISED, fg='white', bg = 'red', font=self.bodyMessageFont, compound=CENTER, height = 1, width = 12)
        self.closeSystem.place(x=1252, y=470+self.extensionY)
        self.helpSystem = Button(self, text=controller.currentLanguage.adminPageContent[23], command=lambda:self.showHelp(), relief = RAISED, fg='white', bg = 'dark green', font=self.bodyMessageFont, compound=CENTER, height = 1, width = 15)
        self.helpSystem.place(x=0, y=470+self.extensionY)
        self.canvas = Canvas(self, background="white", width= 890+self.extensionX, height= 315+self.extensionY, highlightthickness=5, highlightbackground=self.colorORT)
        self.canvasConfiguration(controller)

    def configureCanvas(self, controller):
        self.helpBarTitle = Label(self.canvas, text=controller.currentLanguage.userPageContent[152]+controller.application.listStudents.students[controller.application.systemCurrentStatus.userLogged].surname, font=self.subtitleFont, fg=self.colorORT, bg='white')
        self.helpBarTitle.place(x=20,y=20)
        self.helpBarBody = Label(self.canvas, text=controller.currentLanguage.userPageContent[153], font=self.groupMessageFont, fg=self.colorORT, bg='white', justify=LEFT)
        self.helpBarBody.place(x=80,y=60)

    def refreshTabTitleInformation(self, controller):
        self.nb.tab(self.pageBeginFermentation, text = controller.currentLanguage.userPageContent[4])
        self.nb.tab(self.pagePreparation, text=controller.currentLanguage.userPageContent[139])
        self.nb.tab(self.pageReserves, text = controller.currentLanguage.userPageContent[5])
        self.nb.tab(self.pagePlatform, text = controller.currentLanguage.userPageContent[7])
        self.nb.tab(self.pageProfile, text = controller.currentLanguage.userPageContent[8])
        self.nb.tab(self.pageContact, text = controller.currentLanguage.userPageContent[9])
        self.nb.tab(self.pageLeaderboards, text=controller.currentLanguage.userPageContent[193])

    def refreshPageBeginFermentationContent(self, controller):
        self.sustanceTitle['text'] = controller.currentLanguage.userPageContent[10]
        self.objectiveTitle['text'] = controller.currentLanguage.userPageContent[11]
        self.motiveTitle['text'] = controller.currentLanguage.userPageContent[12]
        self.descriptionTitle['text'] = controller.currentLanguage.userPageContent[13]
        self.speedTitle['text'] = controller.currentLanguage.userPageContent[14]
        self.temperatureTitle['text'] = controller.currentLanguage.userPageContent[15]
        self.circulatorTitle['text'] = controller.currentLanguage.userPageContent[16]
        self.phSensorTitle['text'] = controller.currentLanguage.userPageContent[17]
        self.phControllerTitle['text'] = controller.currentLanguage.userPageContent[18]
        self.connectionCheckOption['text'] = controller.currentLanguage.userPageContent[21]
        self.calibratePHMiddleOption['text'] = controller.currentLanguage.userPageContent[22]
        self.calibratePHLowOption['text'] = controller.currentLanguage.userPageContent[23]
        self.calibratePHHighOption['text'] = controller.currentLanguage.userPageContent[24]
        self.expulseLiquidAcidValve['text'] = controller.currentLanguage.userPageContent[25]
        self.expulseLiquidBaseValve['text'] = controller.currentLanguage.userPageContent[26]
        self.beginFermentationOption['text'] = controller.currentLanguage.userPageContent[27]
        self.dropsExpulsionInfo1['text'] = controller.currentLanguage.userPageContent[123]
        self.dropsExpulsionInfo2['text'] = controller.currentLanguage.userPageContent[124]
        self.dropsExpulsionInfo3['text'] = controller.currentLanguage.userPageContent[125]
        self.temperatureTestingOption['text'] = controller.currentLanguage.userPageContent[142]
        self.potentialTestingOption['text'] = controller.currentLanguage.userPageContent[142]

    def refreshPagePreparationContent(self, controller):
        self.temperatureTestingTitle['text'] = controller.currentLanguage.userPageContent[140]
        self.potentialTestingTitle['text'] = controller.currentLanguage.userPageContent[141]
        self.temperatureTestingOption['text'] = controller.currentLanguage.userPageContent[142]
        self.potentialTestingOption['text'] = controller.currentLanguage.userPageContent[142]
        self.velocityVersionTitle['text'] = controller.currentLanguage.userPageContent[143]
        self.temperatureVersionTitle['text'] = controller.currentLanguage.userPageContent[144]
        self.potentialVersionTitle['text'] = controller.currentLanguage.userPageContent[145]
        self.velocityVersionOption['text'] = controller.currentLanguage.userPageContent[146]
        self.temperatureVersionOption['text'] = controller.currentLanguage.userPageContent[146]
        self.potentialVersionOption['text'] = controller.currentLanguage.userPageContent[146]
        self.velocityVersion['text'] = controller.currentLanguage.userPageContent[147]
        self.temperatureVersion['text'] = controller.currentLanguage.userPageContent[147]
        self.potentialVersion['text'] = controller.currentLanguage.userPageContent[147]
        self.velocityVersionCommentary['text'] = controller.currentLanguage.userPageContent[148]
        self.temperatureVersionCommentary['text'] = controller.currentLanguage.userPageContent[148]
        self.potentialVersionCommentary['text'] = controller.currentLanguage.userPageContent[148]

    def refreshPageReservationContent(self, controller):
        self.monthNameTitle['text'] = controller.currentLanguage.userPageContent[28][self.reservationMonthShown]
        self.mondayTitle['text'] = controller.currentLanguage.userPageContent[29][0]
        self.tuesdayTitle['text'] = controller.currentLanguage.userPageContent[29][1]
        self.wednesdayTitle['text'] = controller.currentLanguage.userPageContent[29][2]
        self.thursdayTitle['text'] = controller.currentLanguage.userPageContent[29][3]
        self.fridayTitle['text'] = controller.currentLanguage.userPageContent[29][4]
        self.dateCheckTitle['text'] = controller.currentLanguage.userPageContent[30]
        self.eraseMotiveTitle['text'] = controller.currentLanguage.userPageContent[31]
        self.informationReserveTitle['text'] = controller.currentLanguage.userPageContent[32]
        self.previousMonthTitle['text'] = controller.currentLanguage.userPageContent[33]
        self.monthTitlePrevious['text'] = controller.currentLanguage.userPageContent[34]
        self.nextMonthTitle['text'] = controller.currentLanguage.userPageContent[35]
        self.monthTitleNext['text'] = controller.currentLanguage.userPageContent[36]
        self.checkReservationExistanceOption['text'] = controller.currentLanguage.userPageContent[49]
        self.eraseReservationOption['text'] = controller.currentLanguage.userPageContent[50]
        self.reservationCheck[1].config(values=controller.currentLanguage.adminPageContent[44])
        self.reservationCheck[3]['text'] = controller.currentLanguage.userPageContent[51]
        self.reservationErase[1]['text'] = controller.currentLanguage.userPageContent[52]

    def refreshPagePlatformContent(self, controller):
        self.searchTitle['text'] = controller.currentLanguage.userPageContent[76]
        self.descriptionTitle['text'] = controller.currentLanguage.userPageContent[77]
        self.filenameInformationTitle['text'] = controller.currentLanguage.userPageContent[78]
        self.contentExistanceInformation['text'] = controller.currentLanguage.userPageContent[79]
        self.continueFermentationOption['text'] = controller.currentLanguage.userPageContent[86]
        self.fillFermentationsList(controller)
        self.getExcelInformationOption['text'] = controller.currentLanguage.userPageContent[93]
        self.getTXTInformationOption['text'] = controller.currentLanguage.userPageContent[94]
        self.sendFileSelectedOption['text'] = controller.currentLanguage.userPageContent[95]

    def refreshPageContactContent(self, controller):
        self.passwordTitle[0]['text'] = controller.currentLanguage.userPageContent[104]
        self.passwordTitle[1]['text'] = controller.currentLanguage.userPageContent[105]
        self.passwordTitle[2]['text'] = controller.currentLanguage.userPageContent[106]
        self.mailTitle['text'] = controller.currentLanguage.userPageContent[107]
        self.messageTitle['text'] = controller.currentLanguage.userPageContent[108]
        self.updatePasswordOption['text'] = controller.currentLanguage.userPageContent[117]
        self.sendParticularMail['text'] = controller.currentLanguage.userPageContent[118]
        self.sendAdministratorNotesOption['text'] = controller.currentLanguage.userPageContent[119]

    def refreshPageProfileContent(self, controller):
        self.fermentationsQuantityTitle['text'] = controller.currentLanguage.userPageContent[96]+" "+str(controller.application.listStudents.students[controller.application.systemCurrentStatus.userLogged].fermentationsQuantity)
        self.gameRecordsTitle['text'] = controller.currentLanguage.userPageContent[97]
        self.usernumberTitle['text'] = controller.currentLanguage.userPageContent[98]
        self.emailTitle['text'] = controller.currentLanguage.userPageContent[99]
        self.birthdateTitle['text'] = controller.currentLanguage.userPageContent[100]
        self.telephoneTitle['text'] = controller.currentLanguage.userPageContent[101]
        self.addressTitle['text'] = controller.currentLanguage.userPageContent[102]
        self.idNumberTitle['text'] = controller.currentLanguage.userPageContent[103]

    def refreshPageLeaderboardsContent(self, controller):
        self.labelChangeGame['text'] = controller.currentLanguage.userPageContent[163]
        self.labelGame['text'] = controller.currentLanguage.userPageContent[194]
        self.labelDisplayedGame['text'] = controller.currentLanguage.userPageContent[195]
        self.columnPlaceLeaderboards[0]['text'] = controller.currentLanguage.userPageContent[196][0]
        self.columnPlaceLeaderboards[1]['text'] = controller.currentLanguage.userPageContent[196][1]
        self.columnPlaceLeaderboards[2]['text'] = controller.currentLanguage.userPageContent[196][2]
        self.columnPlaceLeaderboards[3]['text'] = controller.currentLanguage.userPageContent[196][3]
        self.columnPlaceLeaderboards[4]['text'] = controller.currentLanguage.userPageContent[196][4]

    def refreshTextContent(self, controller):
        self.refreshTabTitleInformation(controller)
        self.helpBarTitle['text'] = controller.currentLanguage.userPageContent[152]+controller.application.listStudents.students[controller.application.systemCurrentStatus.userLogged].surname
        self.helpBarBody['text'] = controller.currentLanguage.userPageContent[153]
        self.studentInformation['text'] = controller.currentLanguage.userPageContent[2] + controller.application.listStudents.students[controller.application.systemCurrentStatus.userLogged].registrationDate + " :::: "+ controller.currentLanguage.userPageContent[3] + controller.application.listStudents.students[controller.application.systemCurrentStatus.userLogged].lastEntryDate
        self.versionInfo['text'] = controller.currentLanguage.adminPageContent[12]
        self.minimizeSystem['text'] = controller.currentLanguage.adminPageContent[22]
        self.closeSystem['text'] = controller.currentLanguage.adminPageContent[23]
        self.helpSystem['text'] = controller.currentLanguage.adminPageContent[24]

        self.refreshPageBeginFermentationContent(controller)
        self.refreshPagePreparationContent(controller)
        self.refreshPageReservationContent(controller)
        self.refreshPagePlatformContent(controller)
        self.refreshPageContactContent(controller)

        self.refreshPageProfileContent(controller)
        self.refreshPageLeaderboardsContent(controller)


    def changeLanguage(self, language, controller):
        if(language=='GERMAN'):
            controller.currentLanguage = GermanLanguage()
            self.studentInformation.place(x=845, y=120)
            self.minimizeSystem.place(x=1150, y=470+self.extensionY)
        if(language=='PORTUGUESE'):
            controller.currentLanguage = PortugueseLanguage()
            self.studentInformation.place(x=860, y=120)
            self.minimizeSystem.place(x=1155, y=470+self.extensionY)
        if(language=='SPANISH'):
            controller.currentLanguage = SpanishLanguage()
            self.studentInformation.place(x=835, y=120)
            self.minimizeSystem.place(x=1155, y=470+self.extensionY)
        if(language=='ENGLISH'):
            controller.currentLanguage = OriginalLanguage()
            self.studentInformation.place(x=845, y=120)
            self.minimizeSystem.place(x=1155, y=470+self.extensionY)
        self.refreshTextContent(controller)

    def setLanguages(self, controller):
        self.changeLanguage('ENGLISH', controller)
        self.spanishFlagImage = PhotoImage(file="Images/Languages/spainFlag.gif")
        spanishOption = Button(self, image=self.spanishFlagImage, command=lambda:self.changeLanguage('SPANISH', controller), compound=CENTER)
        spanishOption.place(x=142, y=470+self.extensionY)#(x=150, y=500)
        self.englishFlagImage = PhotoImage(file="Images/Languages/britishFlag.gif")
        englishOption = Button(self, image=self.englishFlagImage, command=lambda:self.changeLanguage('ENGLISH', controller), compound=CENTER)
        englishOption.place(x=142+47, y=470+self.extensionY)#(x=200, y=500)
        self.portugueseFlagImage = PhotoImage(file="Images/Languages/brazilFlag.gif")
        portugueseOption = Button(self, image=self.portugueseFlagImage, command=lambda:self.changeLanguage('PORTUGUESE', controller), compound=CENTER)
        portugueseOption.place(x=142+47+47, y=470+self.extensionY)#(x=250, y=500)
        self.germanFlagImage = PhotoImage(file="Images/Languages/germanyFlag.gif")
        germanOption = Button(self, image=self.germanFlagImage, command=lambda:self.changeLanguage('GERMAN', controller), compound=CENTER)
        germanOption.place(x=142+47+47+47, y=470+self.extensionY)#(x=300, y=500)

    def canvasConfiguration(self, controller):
        ortLogo = Picture(['ORTLogo','png',240,100,100+self.extensionX,210+self.extensionY],0)
        ortLogo.purpose = 'Logos'
        oneImage = Image.open(ortLogo.getCompleteFilename()).resize((ortLogo.dimensions[0],ortLogo.dimensions[1]), Image.ANTIALIAS)
        oneImageRendered = ImageTk.PhotoImage(oneImage.rotate(ortLogo.orientation))
        ortLogoPic = Label(self.canvas, image=oneImageRendered, borderwidth=0, highlightthickness=0)
        ortLogoPic.image = oneImageRendered
        ortLogoPic.place(x=ortLogo.location[0],y=ortLogo.location[1])
        self.configureCanvas(controller)
        self.setLanguages(controller)

    def setPicturesOnPageBeginFermentation(self, pageBeginFermentation, controller):
        beginFermentationElement = Picture(['beginFermentationElement','png',130,550,10,10],0)
        beginFermentationElement.purpose = 'Words'
        beginFermentationElementPic = beginFermentationElement.generateLabel(pageBeginFermentation)
        beginFermentationElementPic.place(x=beginFermentationElement.location[0],y=beginFermentationElement.location[1])

        controller.setImagesandSeparators(pageBeginFermentation, 'preparationElement', [115,270,1250,20,115,270,1250,300])

        #connectionCalibrationElement = Picture(['connectionCalibrationElement','png',130,550,1230,10],180)
        #connectionCalibrationElement.purpose = 'Words'
        #connectionCalibrationElementPic = connectionCalibrationElement.generateLabel(pageBeginFermentation)
        #connectionCalibrationElementPic.place(x=connectionCalibrationElement.location[0],y=connectionCalibrationElement.location[1])

        separatorFermentation = Picture(['fermentationSeparator','png',150,580,600,0],0)
        separatorFermentation.purpose = 'Separators'
        separatorFermentationPic = separatorFermentation.generateLabel(pageBeginFermentation)
        separatorFermentationPic.place(x=separatorFermentation.location[0],y=separatorFermentation.location[1])

    def fillPageBeginFermentationTitles(self, pageBeginFermentation, controller):
        self.sustanceTitle = Label(pageBeginFermentation, text=controller.currentLanguage.userPageContent[10], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.sustanceTitle.place(x=150, y=30)
        self.objectiveTitle = Label(pageBeginFermentation, text=controller.currentLanguage.userPageContent[11], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.objectiveTitle.place(x=150, y=110)
        self.motiveTitle = Label(pageBeginFermentation, text=controller.currentLanguage.userPageContent[12], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.motiveTitle.place(x=150, y=190)
        self.descriptionTitle = Label(pageBeginFermentation, text=controller.currentLanguage.userPageContent[13], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.descriptionTitle.place(x=150, y=260)

    def fillPageBeginFermentationEntries(self, pageBeginFermentation):
        self.fermentationInput.append(Entry(pageBeginFermentation, font=self.inputFont, fg = self.colorORT, width=25, justify='center')) # sustanceInput
        self.fermentationInput[0].place(x=315, y=38)
        self.fermentationInput.append(Entry(pageBeginFermentation, font=self.inputFont, fg = self.colorORT, width=24, justify='center')) # objectiveInput
        self.fermentationInput[1].place(x=325, y=118)
        self.fermentationInput.append(Entry(pageBeginFermentation, font=self.inputFont, fg = self.colorORT, width=28, justify='center'))  # motiveInput
        self.fermentationInput[2].place(x=285, y=198)
        self.fermentationInput.append(Text(pageBeginFermentation, font=self.inputFont, fg = self.colorORT, bg='white', height=6, width=40)) # descriptionInput
        self.fermentationInput[3].place(x=150, y=300)

    def setVelocityLogos(self, pageRelevant, positionLogos):
        speedLogo = Picture(['speedSensorLogo','png',70*2,60*2,positionLogos[0],positionLogos[1]],0)
        speedLogo.purpose = 'Logos'
        speedLogoPic = speedLogo.generateLabel(pageRelevant)
        speedLogoPic.place(x=speedLogo.location[0],y=speedLogo.location[1])

        motorLogo = Picture(['motorLogo','png',85*2,60*2,positionLogos[2],positionLogos[3]],0)
        motorLogo.purpose = 'Logos'
        motorLogoPic = motorLogo.generateLabel(pageRelevant)
        motorLogoPic.place(x=motorLogo.location[0],y=motorLogo.location[1])

    def setTemperatureLogos(self, pageRelevant, positionLogos):
        temperatureLogo1 = Picture(['temperatureSensorLogo','png',40*2,60*2,positionLogos[0],positionLogos[1]],0)
        temperatureLogo1.purpose = 'Logos'
        temperatureLogoPic1 = temperatureLogo1.generateLabel(pageRelevant)
        temperatureLogoPic1.place(x=temperatureLogo1.location[0],y=temperatureLogo1.location[1])
        temperatureLogo2 = Picture(['temperatureSensorLogo','png',20*2,30*2,positionLogos[2],positionLogos[3]],0)
        temperatureLogo2.purpose = 'Logos'
        temperatureLogoPic2 = temperatureLogo2.generateLabel(pageRelevant)
        temperatureLogoPic2.place(x=temperatureLogo2.location[0],y=temperatureLogo2.location[1])
        temperatureLogo3 = Picture(['temperatureSensorLogo','png',20*2,30*2,positionLogos[4],positionLogos[5]],0)
        temperatureLogo3.purpose = 'Logos'
        temperatureLogoPic3 = temperatureLogo3.generateLabel(pageRelevant)
        temperatureLogoPic3.place(x=temperatureLogo3.location[0],y=temperatureLogo3.location[1])

        bathLogo = Picture(['bathCirculatorLogo','png',85*2,60*2,positionLogos[6],positionLogos[7]],0)
        bathLogo.purpose = 'Logos'
        bathLogoPic = bathLogo.generateLabel(pageRelevant)
        bathLogoPic.place(x=bathLogo.location[0],y=bathLogo.location[1])

    def setPotHydrogenLogo(self, pageRelevant, positionLogos):
        phSensorLogo = Picture(['pHSensorLogo','png',60*2,60*2,positionLogos[0],positionLogos[1]],0)
        phSensorLogo.purpose = 'Logos'
        phSensorLogoPic = phSensorLogo.generateLabel(pageRelevant)
        phSensorLogoPic.place(x=phSensorLogo.location[0],y=phSensorLogo.location[1])

        phControllerLogo = Picture(['pHControllerLogo','png',60*2,60*2,positionLogos[2],positionLogos[3]],0)
        phControllerLogo.purpose = 'Logos'
        phControllerLogoPic = phControllerLogo.generateLabel(pageRelevant)
        phControllerLogoPic.place(x=phControllerLogo.location[0],y=phControllerLogo.location[1])

    def setPicturesConnectionOnPageBeginFermentation(self, pageBeginFermentation):
        self.setVelocityLogos(pageBeginFermentation, [800, 10, 1010, 10])
        self.setTemperatureLogos(pageBeginFermentation, [825, 160, 805, 195, 885, 195, 1010, 160])
        self.setPotHydrogenLogo(pageBeginFermentation, [805, 310, 1030, 310])

    def fillPageBeginFermentationConnection(self, pageBeginFermentation, foregroundColors, controller):
        self.speedTitle = Label(pageBeginFermentation, text=controller.currentLanguage.userPageContent[14], font=self.statusFont, fg = foregroundColors[0], bg = self.colorORT)
        self.speedTitle.place(x=800, y=120)
        self.motorTitle = Label(pageBeginFermentation, text="Motor MS 801-6", font=self.statusFont, fg = foregroundColors[1], bg = self.colorORT)
        self.motorTitle.place(x=1020, y=120)
        self.temperatureTitle = Label(pageBeginFermentation, text=controller.currentLanguage.userPageContent[15], font=self.statusFont, fg = foregroundColors[2], bg = self.colorORT)
        self.temperatureTitle.place(x=760, y=270)
        self.circulatorTitle = Label(pageBeginFermentation, text=controller.currentLanguage.userPageContent[16], font=self.statusFont, fg = foregroundColors[3], bg = self.colorORT)
        self.circulatorTitle.place(x=1025, y=270)
        self.phSensorTitle = Label(pageBeginFermentation, text=controller.currentLanguage.userPageContent[17], font=self.statusFont, fg = foregroundColors[5], bg = self.colorORT)
        self.phSensorTitle.place(x=820, y=420)
        self.phControllerTitle = Label(pageBeginFermentation, text=controller.currentLanguage.userPageContent[18], font=self.statusFont, fg = foregroundColors[4], bg = self.colorORT)
        self.phControllerTitle.place(x=1035, y=420)

    def checkVelocityModulesConnection(self, controller):
        controller.settingVelocityControl[0] = 2
        while(controller.settingVelocityControl[0] == 2):
            var = 1 + 1
            #print("CONNECTION BEING CHECKED")
        if(controller.settingVelocityControl[0] == 100):
            self.speedTitle['fg']='red'
            self.motorTitle['fg']='red'
        if(controller.settingVelocityControl[0] == 110):
            self.speedTitle['fg']='green'
            self.motorTitle['fg']='red'
        if(controller.settingVelocityControl[0] == 101):
            self.speedTitle['fg']='red'
            self.motorTitle['fg']='green'
        if(controller.settingVelocityControl[0] == 111):
            self.speedTitle['fg']='green'
            self.motorTitle['fg']='green'
        print("VEL CONNECTION CHECKED")

    def checkTemperatureModulesConnection(self, controller):
        controller.settingTemperatureControl[0] = 2
        while(controller.settingTemperatureControl[0] == 2):
            var = 1 + 1
        if(controller.settingTemperatureControl[0] == 100):
            self.temperatureTitle['fg']='red'
            self.circulatorTitle['fg']='red'
        if(controller.settingTemperatureControl[0] == 110):
            self.temperatureTitle['fg']='green'
            self.circulatorTitle['fg']='red'
        if(controller.settingTemperatureControl[0] == 101):
            self.temperatureTitle['fg']='red'
            self.circulatorTitle['fg']='green'
        if(controller.settingTemperatureControl[0] == 111):
            self.temperatureTitle['fg']='green'
            self.circulatorTitle['fg']='green'
        print("TEMP CONNECTION CHECKED")

    def checkPotentialModulesConnection(self, controller):
        controller.settingPotentialHydrogenControl[0] = 2
        while(controller.settingPotentialHydrogenControl[0] == 2):
            var = 1 + 1
        if(controller.settingPotentialHydrogenControl[0] == 100):
            self.phSensorTitle['fg']='red'
            self.phControllerTitle['fg']='red'
        if(controller.settingPotentialHydrogenControl[0] == 110):
            self.phSensorTitle['fg']='green'
            self.phControllerTitle['fg']='red'
        if(controller.settingPotentialHydrogenControl[0] == 101):
            self.phSensorTitle['fg']='red'
            self.phControllerTitle['fg']='green'
        if(controller.settingPotentialHydrogenControl[0] == 111):
            self.phSensorTitle['fg']='green'
            self.phControllerTitle['fg']='green'
        print("POTENTIAL CONNECTION CHECKED")

    def checkConnection(self, controller):
        self.checkVelocityModulesConnection(controller)
        self.checkTemperatureModulesConnection(controller)
        self.checkPotentialModulesConnection(controller)
        self.hasCheckedConnection = True

    def beginFermentationAction(self, controller):
        currentUser = controller.application.listStudents.students[controller.application.systemCurrentStatus.userLogged]
        dataAdded = [self.fermentationInput[0].get(), self.fermentationInput[1].get(), self.fermentationInput[2].get(), self.fermentationInput[3].get(1.0,END)]
        newFermentation = Fermentation(currentUser, dataAdded)
        if(newFermentation.isDataCorrect()):
            newFermentation.isConnectionChecked = self.hasCheckedConnection
            newFermentation.isCalibrated = self.hasCalibratedSensorMiddle and self.hasCalibratedSensorLow and self.hasCalibratedSensorHigh
            newFermentation.isLiquidExpulsed = self.hasExpulsedLiquidAcid or self.hasExpulsedLiquidBase
            controller.application.listFermentations.addFermentation(newFermentation)
            controller.application.systemCurrentStatus.fermentationActual = len(controller.application.listFermentations.fermentations)-1 #CUIDADO
            self.fillFermentationsList(controller)
            self.fermentationInput[0].delete(0,END)
            self.fermentationInput[1].delete(0,END)
            self.fermentationInput[2].delete(0,END)
            self.fermentationInput[3].delete(1.0,END)
            controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].isConnectionChecked = self.hasCheckedConnection
            controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].isCalibrated = self.hasCalibratedSensorLow and self.hasCalibratedSensorMiddle and self.hasCalibratedSensorHigh
            controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].isLiquidExpulsed = self.hasExpulsedLiquidAcid and self.hasExpulsedLiquidBase
            controller.application.systemData.informations[4].addFermentationInitiated()
            messagebox.showinfo(controller.currentLanguage.userPageContent[4], controller.currentLanguage.userPageContent[151])
            #self.doneLoading = False
            #loadingScreen = threading.Thread(target=lambda:self.animateLoading())
            #loadingScreen.start()
            #newFermentation.initiateFermentation(controller)
            #self.doneLoading = True
        else:
            messagebox.showwarning(controller.currentLanguage.userPageContent[19], controller.currentLanguage.userPageContent[20])

    def fillPageBeginFermentationButtons(self, pageBeginFermentation, controller):
        self.connectionCheckOption = Button(pageBeginFermentation, text=controller.currentLanguage.userPageContent[21], command = lambda:self.checkConnection(controller), relief = SUNKEN, fg='white', bg = 'DarkGoldenRod4', font=self.buttonFont, compound=CENTER, height = 3, width = 30)
        self.connectionCheckOption.place(x=810, y=450)
        self.beginFermentationOption = Button(pageBeginFermentation, text=controller.currentLanguage.userPageContent[27], command = lambda:self.beginFermentationAction(controller), relief = SUNKEN, fg='white', bg = 'black', font=self.buttonFont, compound=CENTER, height = 3, width = 30)
        self.beginFermentationOption.place(x=180, y=450)

    def fillPageBeginFermentation(self, pageBeginFermentation, controller):
        self.setPicturesOnPageBeginFermentation(pageBeginFermentation, controller)
        self.fillPageBeginFermentationTitles(pageBeginFermentation, controller)
        self.fillPageBeginFermentationEntries(pageBeginFermentation)
        self.fillPageBeginFermentationButtons(pageBeginFermentation, controller)
        self.setPicturesConnectionOnPageBeginFermentation(pageBeginFermentation)
        self.fillPageBeginFermentationConnection(pageBeginFermentation, ['white', 'white', 'white', 'white', 'white', 'white'], controller)

    def setPicturesOnPagePreparation(self, pagePreparation,controller):
        testingCalibrationElement = Picture(['calibrationTestingElement','png',100,530,10,10],0)
        testingCalibrationElement.purpose = 'Words'
        testingCalibrationElementPic = testingCalibrationElement.generateLabel(pagePreparation)
        testingCalibrationElementPic.place(x=testingCalibrationElement.location[0],y=testingCalibrationElement.location[1])

        controller.setImagesandSeparators(pagePreparation, 'versionElement', [115,270,1250,10,115,270,1250,290])

    def fillPagePreparationTitles(self, pagePreparation, controller):
        temperatureTestingBorder = Label(pagePreparation, bg = self.colorORT, height=10, width=85, borderwidth=2, relief='solid', highlightbackground='orange')
        temperatureTestingBorder.place(x=150, y=5)
        self.temperatureTestingTitle = Label(pagePreparation, text=controller.currentLanguage.userPageContent[140], font=self.buttonFont, fg = 'orange', bg = self.colorORT)
        self.temperatureTestingTitle.place(x=155, y=10)

        potentialTestingBorder = Label(pagePreparation, bg = self.colorORT, height=10, width=85, borderwidth=2, relief='solid', highlightbackground='lime green')
        potentialTestingBorder.place(x=150, y=190)
        self.potentialTestingTitle = Label(pagePreparation, text=controller.currentLanguage.userPageContent[141], font=self.buttonFont, fg = 'lime green', bg = self.colorORT)
        self.potentialTestingTitle.place(x=155, y=195)

        velocityVersionBorder = Label(pagePreparation, bg = self.colorORT, height=10, width=67, borderwidth=2, relief='solid', highlightbackground='blue')
        velocityVersionBorder.place(x=780, y=5)
        self.velocityVersionTitle = Label(pagePreparation, text=controller.currentLanguage.userPageContent[143], font=self.buttonFont, fg = 'blue', bg = self.colorORT)
        self.velocityVersionTitle.place(x=785, y=10)

        temperatureVersionBorder = Label(pagePreparation, bg = self.colorORT, height=10, width=67, borderwidth=2, relief='solid', highlightbackground='orange')
        temperatureVersionBorder.place(x=780, y=190)
        self.temperatureVersionTitle = Label(pagePreparation, text=controller.currentLanguage.userPageContent[144], font=self.buttonFont, fg = 'orange', bg = self.colorORT)
        self.temperatureVersionTitle.place(x=785, y=195)

        potentialVersionBorder = Label(pagePreparation, bg = self.colorORT, height=10, width=67, borderwidth=2, relief='solid', highlightbackground='lime green')
        potentialVersionBorder.place(x=780, y=375)
        self.potentialVersionTitle = Label(pagePreparation, text=controller.currentLanguage.userPageContent[145], font=self.buttonFont, fg = 'lime green', bg = self.colorORT)
        self.potentialVersionTitle.place(x=785, y=380)

    def fillTestingEntries(self, pagePreparation):
        self.temperatureTesting.append(Label(pagePreparation, text="00.00 ℃", bg=self.colorORT, fg = 'orange', font=self.groupMessageFont, compound=CENTER))
        self.temperatureTesting[0].place(x=170, y=80)
        self.temperatureTesting.append(Label(pagePreparation, text="00.00 ℃", bg=self.colorORT, fg = 'orange', font=self.groupMessageFont, compound=CENTER))
        self.temperatureTesting[1].place(x=250, y=80)
        self.temperatureTesting.append(Label(pagePreparation, text="00.00 ℃", bg=self.colorORT, fg = 'orange', font=self.groupMessageFont, compound=CENTER))
        self.temperatureTesting[2].place(x=330, y=80)
        self.temperatureTesting.append(Label(pagePreparation, text="00.00 ℃", bg=self.colorORT, fg = 'orange', font=self.groupMessageFont, compound=CENTER))
        self.temperatureTesting[3].place(x=410, y=80)
        self.temperatureTesting.append(Label(pagePreparation, text="00.00 ℃", bg=self.colorORT, fg = 'orange', font=self.groupMessageFont, compound=CENTER))
        self.temperatureTesting[4].place(x=490, y=80)

        self.potentialTesting.append(Label(pagePreparation, text="00.000", bg=self.colorORT, fg = 'lime green', font=self.groupMessageFont, compound=CENTER))
        self.potentialTesting[0].place(x=170, y=265)
        self.potentialTesting.append(Label(pagePreparation, text="00.000", bg=self.colorORT, fg = 'lime green', font=self.groupMessageFont, compound=CENTER))
        self.potentialTesting[1].place(x=250, y=265)
        self.potentialTesting.append(Label(pagePreparation, text="00.000", bg=self.colorORT, fg = 'lime green', font=self.groupMessageFont, compound=CENTER))
        self.potentialTesting[2].place(x=330, y=265)
        self.potentialTesting.append(Label(pagePreparation, text="00.000", bg=self.colorORT, fg = 'lime green', font=self.groupMessageFont, compound=CENTER))
        self.potentialTesting[3].place(x=410, y=265)
        self.potentialTesting.append(Label(pagePreparation, text="00.000", bg=self.colorORT, fg = 'lime green', font=self.groupMessageFont, compound=CENTER))
        self.potentialTesting[4].place(x=490, y=265)

    def fillVersionEntries(self, pagePreparation, controller):
        self.velocityVersion = Label(pagePreparation, text=controller.currentLanguage.userPageContent[147], bg=self.colorORT, fg = 'blue', font=self.groupMessageFont, compound=CENTER)
        self.velocityVersion.place(x=900, y=60)
        self.temperatureVersion = Label(pagePreparation, text=controller.currentLanguage.userPageContent[147], bg=self.colorORT, fg = 'orange', font=self.groupMessageFont, compound=CENTER)
        self.temperatureVersion.place(x=900, y=240)
        self.potentialVersion = Label(pagePreparation, text=controller.currentLanguage.userPageContent[147], bg=self.colorORT, fg = 'lime green', font=self.groupMessageFont, compound=CENTER)
        self.potentialVersion.place(x=900, y=430)

        self.velocityVersionCommentary = Label(pagePreparation, text=controller.currentLanguage.userPageContent[148], bg=self.colorORT, fg = 'blue', font=self.groupMessageFont, compound=CENTER)
        self.velocityVersionCommentary.place(x=850, y=110)
        self.temperatureVersionCommentary = Label(pagePreparation, text=controller.currentLanguage.userPageContent[148], bg=self.colorORT, fg = 'orange', font=self.groupMessageFont, compound=CENTER)
        self.temperatureVersionCommentary.place(x=850, y=290)
        self.potentialVersionCommentary = Label(pagePreparation, text=controller.currentLanguage.userPageContent[148], bg=self.colorORT, fg = 'lime green', font=self.groupMessageFont, compound=CENTER)
        self.potentialVersionCommentary.place(x=850, y=480)

    def fillPagePreparationEntries(self, pagePreparation, controller):
        self.expulsionOption.append(Spinbox(pagePreparation, from_=1, to=4, font=self.inputFont, fg = self.colorORT, width=3, justify='center'))
        self.expulsionOption[0].place(x=370, y=470)
        self.expulsionOption.append(Spinbox(pagePreparation, from_=1, to=50, font=self.inputFont, fg = self.colorORT, width=3, justify='center'))
        self.expulsionOption[1].place(x=410, y=500)

        self.fillTestingEntries(pagePreparation)
        self.fillVersionEntries(pagePreparation, controller)

    def calibrateMiddle(self, controller):
        print("PH CALIBRATED MIDDLE")
        controller.settingPotentialHydrogenControl[0] = 3
        while(controller.settingPotentialHydrogenControl[0] == 3):
            var = 1 + 1
        if(controller.settingPotentialHydrogenControl[0] == 31):
            messagebox.showinfo(controller.currentLanguage.userPageContent[126]+" 7.0", controller.currentLanguage.userPageContent[127])
        else:
            messagebox.showerror(controller.currentLanguage.userPageContent[126]+" 7.0", controller.currentLanguage.userPageContent[128])
        self.hasCalibratedSensorMiddle = True

    def calibrateLow(self, controller):
        print("PH CALIBRATED LOW")
        controller.settingPotentialHydrogenControl[0] = 4
        while(controller.settingPotentialHydrogenControl[0] == 4):
            var = 1 + 1
        if(controller.settingPotentialHydrogenControl[0] == 41):
            messagebox.showinfo(controller.currentLanguage.userPageContent[126]+" 4.0", controller.currentLanguage.userPageContent[129])
        else:
            messagebox.showerror(controller.currentLanguage.userPageContent[126]+" 4.0", controller.currentLanguage.userPageContent[130])
        self.hasCalibratedSensorLow = True

    def calibrateHigh(self, controller):
        print("PH CALIBRATED HIGH")
        controller.settingPotentialHydrogenControl[0] = 5
        while(controller.settingPotentialHydrogenControl[0] == 5):
            var = 1 + 1
        if(controller.settingPotentialHydrogenControl[0] == 51):
            messagebox.showinfo(controller.currentLanguage.userPageContent[126]+" 10.0", controller.currentLanguage.userPageContent[131])
        else:
            messagebox.showerror(controller.currentLanguage.userPageContent[126]+" 10.0", controller.currentLanguage.userPageContent[132])
        self.hasCalibratedSensorHigh = True

    def areExpulsionOptionsCorrect(self):
        dropsOptionCorrect = self.expulsionOption[0].get().isdigit() and int(self.expulsionOption[0].get())<=4 and int(self.expulsionOption[0].get())>=1
        burstsOptionCorrect = self.expulsionOption[1].get().isdigit() and int(self.expulsionOption[1].get())<=50 and int(self.expulsionOption[1].get())>=1
        return dropsOptionCorrect and burstsOptionCorrect

    def expulseAcid(self, controller):
        print("ACID EXPULSION")
        if(self.areExpulsionOptionsCorrect()):
            controller.settingPotentialHydrogenControl[8] = int(self.expulsionOption[0].get())+int(self.expulsionOption[1].get())*100
            controller.settingPotentialHydrogenControl[0] = 6
            while(controller.settingPotentialHydrogenControl[0] == 6):
                var = 1 + 1
            if(controller.settingPotentialHydrogenControl[0] == 61):
                messagebox.showinfo(controller.currentLanguage.userPageContent[133], controller.currentLanguage.userPageContent[134])
            else:
                messagebox.showerror(controller.currentLanguage.userPageContent[133], controller.currentLanguage.userPageContent[135])
            self.hasExpulsedLiquidAcid = True
        else:
            messagebox.showwarning(controller.currentLanguage.userPageContent[121], controller.currentLanguage.userPageContent[122])

    def expulseBase(self, controller):
        print("BASE EXPULSION")
        if(self.areExpulsionOptionsCorrect()):
            controller.settingPotentialHydrogenControl[8] = int(self.expulsionOption[0].get())+int(self.expulsionOption[1].get())*100
            controller.settingPotentialHydrogenControl[0] = 7
            while(controller.settingPotentialHydrogenControl[0] == 7):
                var = 1 + 1
            if(controller.settingPotentialHydrogenControl[0] == 71):
                messagebox.showinfo(controller.currentLanguage.userPageContent[136], controller.currentLanguage.userPageContent[137])
            else:
                messagebox.showerror(controller.currentLanguage.userPageContent[136], controller.currentLanguage.userPageContent[138])
            self.hasExpulsedLiquidBase = True
        else:
            messagebox.showwarning(controller.currentLanguage.userPageContent[121], controller.currentLanguage.userPageContent[122])

    def makeTemperatureTesting(self, controller):
        print("TEMPERATURE TESTING")
        controller.settingTemperatureControl[0] = 12
        while(controller.settingTemperatureControl[0] == 12):
            var = 1 + 1
        if(controller.settingTemperatureControl[11] > 10):
            self.temperatureTesting[0]['text'] = str(float(controller.settingTemperatureControl[11]/100))+" ℃"
        else:
            self.temperatureTesting[0]['text'] = controller.currentLanguage.userPageContent[149]
        if(controller.settingTemperatureControl[12] > 10):
            self.temperatureTesting[1]['text'] = str(float(controller.settingTemperatureControl[12]/100))+" ℃"
        else:
            self.temperatureTesting[1]['text'] = controller.currentLanguage.userPageContent[149]
        if(controller.settingTemperatureControl[13] > 10):
            self.temperatureTesting[2]['text'] = str(float(controller.settingTemperatureControl[13]/100))+" ℃"
        else:
            self.temperatureTesting[2]['text'] = controller.currentLanguage.userPageContent[149]
        if(controller.settingTemperatureControl[14] > 10):
            self.temperatureTesting[3]['text'] = str(float(controller.settingTemperatureControl[14]/100))+" ℃"
        else:
            self.temperatureTesting[3]['text'] = controller.currentLanguage.userPageContent[149]
        if(controller.settingTemperatureControl[15] > 10):
            self.temperatureTesting[4]['text'] = str(float(controller.settingTemperatureControl[15]/100))+" ℃"
        else:
            self.temperatureTesting[4]['text'] = controller.currentLanguage.userPageContent[149]

    def makePotentialTesting(self, controller):
        print("POTENTIAL TESTING")
        controller.settingPotentialHydrogenControl[0] = 12
        while(controller.settingPotentialHydrogenControl[0] == 12):
            var = 1 + 1
        if(controller.settingPotentialHydrogenControl[11] > 2):
            self.potentialTesting[0]['text'] = str(float(controller.settingPotentialHydrogenControl[11]/1000))
        else:
            self.potentialTesting[0]['text'] = controller.currentLanguage.userPageContent[150]
        if(controller.settingPotentialHydrogenControl[12] > 10):
            self.potentialTesting[1]['text'] = str(float(controller.settingPotentialHydrogenControl[12]/1000))
        else:
            self.potentialTesting[1]['text'] = controller.currentLanguage.userPageContent[150]
        if(controller.settingPotentialHydrogenControl[13] > 2):
            self.potentialTesting[2]['text'] = str(float(controller.settingPotentialHydrogenControl[13]/1000))
        else:
            self.potentialTesting[2]['text'] = controller.currentLanguage.userPageContent[150]
        if(controller.settingPotentialHydrogenControl[14] > 2):
            self.potentialTesting[3]['text'] = str(float(controller.settingPotentialHydrogenControl[14]/1000))
        else:
            self.potentialTesting[3]['text'] = controller.currentLanguage.userPageContent[150]
        if(controller.settingPotentialHydrogenControl[15] > 2):
            self.potentialTesting[4]['text'] = str(float(controller.settingPotentialHydrogenControl[15]/1000))
        else:
            self.potentialTesting[4]['text'] = controller.currentLanguage.userPageContent[150]

    def checkVelocityVersion(self, controller):
        print("VELOCITY VERSION")
        controller.settingVelocityControl[0] = 13
        while(controller.settingVelocityControl[0] == 13):
            var = 1 + 1
        if(controller.settingVelocityControl[16] > 0):
            self.velocityVersion['text'] = "Version "+ str(float(controller.settingVelocityControl[16]/100))
            possibleNewVersion = Version(float(controller.settingVelocityControl[16]/100), "")
            controller.application.versionsHistory.addMagnitudeVersion(controller.application.versionsHistory.velocityVersions, possibleNewVersion)
            self.velocityVersionCommentary['text'] = controller.application.versionsHistory.getCommentaryOfMagnitudeVersion(controller.application.versionsHistory.velocityVersions, possibleNewVersion, controller.currentLanguage.adminPageContent[122])
        else:
            self.velocityVersion['text'] = "ERROR"

    def checkTemperatureVersion(self, controller):
        print("TEMPERATURE VERSION")
        controller.settingTemperatureControl[0] = 13
        while(controller.settingTemperatureControl[0] == 13):
            var = 1 + 1
        if(controller.settingTemperatureControl[16] > 0):
            self.temperatureVersion['text'] = "Version "+ str(float(controller.settingTemperatureControl[16]/100))
            possibleNewVersion = Version(float(controller.settingTemperatureControl[16]/100), "")
            controller.application.versionsHistory.addMagnitudeVersion(controller.application.versionsHistory.temperatureVersions, possibleNewVersion)
            self.temperatureVersionCommentary['text'] = controller.application.versionsHistory.getCommentaryOfMagnitudeVersion(controller.application.versionsHistory.temperatureVersions, possibleNewVersion, controller.currentLanguage.adminPageContent[122])
        else:
            self.temperatureVersion['text'] = "ERROR"

    def checkPotentialVersion(self, controller):
        print("POTENTIAL VERSION")
        controller.settingPotentialHydrogenControl[0] = 13
        while(controller.settingPotentialHydrogenControl[0] == 13):
            var = 1 + 1
        if(controller.settingPotentialHydrogenControl[16] > 0):
            self.potentialVersion['text'] = "Version "+ str(float(controller.settingPotentialHydrogenControl[16]/100))
            possibleNewVersion = Version(float(controller.settingPotentialHydrogenControl[16]/100), "")
            controller.application.versionsHistory.addMagnitudeVersion(controller.application.versionsHistory.potentialVersions, possibleNewVersion)
            self.potentialVersionCommentary['text'] = controller.application.versionsHistory.getCommentaryOfMagnitudeVersion(controller.application.versionsHistory.potentialVersions, possibleNewVersion, controller.currentLanguage.adminPageContent[122])
        else:
            self.potentialVersion['text'] = "ERROR"

    def fillPagePreparationButtons(self, pagePreparation, controller):
        self.temperatureTestingOption = Button(pagePreparation, text=controller.currentLanguage.userPageContent[142], command = lambda:self.makeTemperatureTesting(controller), relief = SUNKEN, fg='white', bg = 'orange', font=self.buttonFont, compound=CENTER, height = 6, width = 8)
        self.temperatureTestingOption.place(x=640, y=8)
        self.potentialTestingOption = Button(pagePreparation, text=controller.currentLanguage.userPageContent[142], command = lambda:self.makePotentialTesting(controller), relief = SUNKEN, fg='white', bg = 'lime green', font=self.buttonFont, compound=CENTER, height = 6, width = 8)
        self.potentialTestingOption.place(x=640, y=190)
        self.calibratePHMiddleOption = Button(pagePreparation, text=controller.currentLanguage.userPageContent[22], command = lambda:self.calibrateMiddle(controller), relief = SUNKEN, fg='white', bg = 'green4', font=self.buttonFont, compound=CENTER, height = 3, width = 10)
        self.calibratePHMiddleOption.place(x=370, y=370)
        self.calibratePHLowOption = Button(pagePreparation, text=controller.currentLanguage.userPageContent[23], command = lambda:self.calibrateLow(controller), relief = SUNKEN, fg='white', bg = 'dark red', font=self.buttonFont, compound=CENTER, height = 3, width = 10)
        self.calibratePHLowOption.place(x=210, y=370)
        self.calibratePHHighOption = Button(pagePreparation, text=controller.currentLanguage.userPageContent[24], command = lambda:self.calibrateHigh(controller), relief = SUNKEN, fg='white', bg = 'purple4', font=self.buttonFont, compound=CENTER, height = 3, width = 10)
        self.calibratePHHighOption.place(x=530, y=370)
        self.expulseLiquidAcidValve = Button(pagePreparation, text=controller.currentLanguage.userPageContent[25], command = lambda:self.expulseAcid(controller), relief = SUNKEN, fg='white', bg = 'dark red', font=self.buttonFont, compound=CENTER, height = 2, width = 15)
        self.expulseLiquidAcidValve.place(x=170, y=470)
        self.expulseLiquidBaseValve = Button(pagePreparation, text=controller.currentLanguage.userPageContent[26], command = lambda:self.expulseBase(controller), relief = SUNKEN, fg='white', bg = 'purple4', font=self.buttonFont, compound=CENTER, height = 2, width = 15)
        self.expulseLiquidBaseValve.place(x=530, y=470)
        self.dropsExpulsionInfo1 = Label(pagePreparation, text=controller.currentLanguage.userPageContent[123], font=self.bodyMessageFont, fg = 'white', bg = self.colorORT)
        self.dropsExpulsionInfo1.place(x=430, y=470)
        self.dropsExpulsionInfo2 = Label(pagePreparation, text=controller.currentLanguage.userPageContent[124], font=self.bodyMessageFont, fg = 'white', bg = self.colorORT)
        self.dropsExpulsionInfo2.place(x=370, y=500)
        self.dropsExpulsionInfo3 = Label(pagePreparation, text=controller.currentLanguage.userPageContent[125], font=self.bodyMessageFont, fg = 'white', bg = self.colorORT)
        self.dropsExpulsionInfo3.place(x=470, y=500)
        self.velocityVersionOption = Button(pagePreparation, text=controller.currentLanguage.userPageContent[146], command = lambda:self.checkVelocityVersion(controller), relief = SUNKEN, fg='white', bg = 'blue', font=self.buttonFont, compound=CENTER, height = 6, width = 10)
        self.velocityVersionOption.place(x=1120, y=6)
        self.temperatureVersionOption = Button(pagePreparation, text=controller.currentLanguage.userPageContent[146], command = lambda:self.checkTemperatureVersion(controller), relief = SUNKEN, fg='white', bg = 'orange', font=self.buttonFont, compound=CENTER, height = 6, width = 10)
        self.temperatureVersionOption.place(x=1120, y=192)
        self.potentialVersionOption = Button(pagePreparation, text=controller.currentLanguage.userPageContent[146], command = lambda:self.checkPotentialVersion(controller), relief = SUNKEN, fg='white', bg = 'lime green', font=self.buttonFont, compound=CENTER, height = 6, width = 10)
        self.potentialVersionOption.place(x=1120, y=378)

    def fillPagePreparation(self, pagePreparation, controller):
        self.setPicturesOnPagePreparation(pagePreparation, controller)
        self.fillPagePreparationTitles(pagePreparation, controller)
        self.fillPagePreparationEntries(pagePreparation, controller)
        self.fillPagePreparationButtons(pagePreparation, controller)

    def fillPageReservesPictures(self, pageReserves):
        reservesElementLeft = Picture(['reservationsElement','png',130,450,10,100],0)
        reservesElementLeft.purpose = 'Words'
        reservesElementLeftPic = reservesElementLeft.generateLabel(pageReserves)
        reservesElementLeftPic.place(x=reservesElementLeft.location[0],y=reservesElementLeft.location[1])
        reservesElementRight = Picture(['reservationsElement','png',130,450,1230,10],180)
        reservesElementRight.purpose = 'Words'
        reservesElementRightPic = reservesElementRight.generateLabel(pageReserves)
        reservesElementRightPic.place(x=reservesElementRight.location[0],y=reservesElementRight.location[1])

        monthElement = Picture(['monthElement','png',140,70,600,0],0)
        monthElement.purpose = 'Words'
        monthElementPic = monthElement.generateLabel(pageReserves)
        monthElementPic.place(x=monthElement.location[0],y=monthElement.location[1])
        weekElement = Picture(['weeksElement','png',110,55,610,70],0)
        weekElement.purpose = 'Words'
        weekElementPic = weekElement.generateLabel(pageReserves)
        weekElementPic.place(x=weekElement.location[0],y=weekElement.location[1])

    def initializeBlocks(self):
        for eachDay in self.blockFirstWeek:
            eachDay['bg'] = 'white'
            eachDay['text'] = ''
        for eachDay in self.blockSecondWeek:
            eachDay['bg'] = 'white'
            eachDay['text'] = ''
        for eachDay in self.blockThirdWeek:
            eachDay['bg'] = 'white'
            eachDay['text'] = ''
        for eachDay in self.blockFourthWeek:
            eachDay['bg'] = 'white'
            eachDay['text'] = ''
        for eachDay in self.blockFifthWeek:
            eachDay['bg'] = 'white'
            eachDay['text'] = ''

    def displayReservation(self, blockOfWeek, blockPosition, reservationInformation):
        blockText = reservationInformation.userToReserve.usernumber+"\nPR: "+reservationInformation.professorResponsible.usernumber
        if(blockPosition[0]==1):
            blockOfWeek[0]['text'] = blockText
            blockOfWeek[0]['bg'] = 'yellow'
        if(blockPosition[1]==1):
            blockOfWeek[1]['text'] = blockText
            blockOfWeek[1]['bg'] = 'yellow'
        if(blockPosition[2]==1):
            blockOfWeek[2]['text'] = blockText
            blockOfWeek[2]['bg'] = 'yellow'
        if(blockPosition[3]==1):
            blockOfWeek[3]['text'] = blockText
            blockOfWeek[3]['bg'] = 'yellow'
        if(blockPosition[4]==1):
            blockOfWeek[4]['text'] = blockText
            blockOfWeek[4]['bg'] = 'yellow'

    def updateReservationDisplay(self, pageReserves, controller):
        monthNameTitle = Label(pageReserves, text=self.monthsName[self.reservationMonthShown], font=self.titleFont, justify='center', fg='white', bg=self.colorORT, height=2, width=15)
        monthNameTitle.place(x=230, y=0)
        self.initializeBlocks()
        for eachReservation in controller.application.listReservations.reservations:
            numberOfWeek = 1
            while(numberOfWeek<6):
                blockPosition = eachReservation.getWeekAndDayOfDate(numberOfWeek, self.reservationMonthShown+1)
                if(numberOfWeek==1):
                    self.displayReservation(self.blockFirstWeek, blockPosition, eachReservation)
                if(numberOfWeek==2):
                    self.displayReservation(self.blockSecondWeek, blockPosition, eachReservation)
                if(numberOfWeek==3):
                    self.displayReservation(self.blockThirdWeek, blockPosition, eachReservation)
                if(numberOfWeek==4):
                    self.displayReservation(self.blockFourthWeek, blockPosition, eachReservation)
                if(numberOfWeek==5):
                    self.displayReservation(self.blockFifthWeek, blockPosition, eachReservation)
                numberOfWeek = numberOfWeek + 1

    def configureRowOfDay(self, pageReserves, blockOfWeek, position):
        blockOfWeek.append(Label(pageReserves, fg=self.colorORT, bg='white', font=self.reservationFont, height=4, width=10, borderwidth=2, relief='groove')) #height=4,width=10
        blockOfWeek[position[1]].place(x=position[2], y=position[3]-10)

    def configureMonthMatrix(self, pageReserves, position):
        for row in range(140,140+90*5,90):
            for column in range(130,130+85*5,85):
                if(position[0]==0):
                    self.configureRowOfDay(pageReserves, self.blockFirstWeek, [position[0], position[1], row, column])
                if(position[0]==1):
                    self.configureRowOfDay(pageReserves, self.blockSecondWeek, [position[0], position[1], row, column])
                if(position[0]==2):
                    self.configureRowOfDay(pageReserves, self.blockThirdWeek, [position[0], position[1], row, column])
                if(position[0]==3):
                    self.configureRowOfDay(pageReserves, self.blockFourthWeek, [position[0], position[1], row, column])
                if(position[0]==4):
                    self.configureRowOfDay(pageReserves, self.blockFifthWeek, [position[0], position[1], row, column])
                position[1] = position[1] + 1
            position[0] = position[0] + 1
            position[1] = 0

    def setReservesOfMonth(self, pageReserves, controller):
        position = [0, 0]
        self.monthNameTitle = Label(pageReserves, text=controller.currentLanguage.userPageContent[28][date.today().month-1], font=self.titleFont, justify='center', fg='white', bg=self.colorORT, height=2, width=15)
        self.monthNameTitle.place(x=230, y=0)

        for week in range(1,6,1):
            numberOfWeek = Label(pageReserves, text=str(week), font=self.statusFont, justify='center', fg='white', bg=self.colorORT, height=2, width=6, borderwidth=2, relief='groove')
            numberOfWeek.place(x=140+2+90*(week-1), y=75)
        self.configureMonthMatrix(pageReserves, position)

    def fillPageReservesWeekdaysTitles(self, pageReserves, controller):
        self.mondayTitle = Label(pageReserves, text=controller.currentLanguage.userPageContent[29][0], font=self.inputFont, justify='center', fg='white', bg=self.colorORT, height=2, width=8)
        self.mondayTitle.place(x=620, y=145)
        self.tuesdayTitle = Label(pageReserves, text=controller.currentLanguage.userPageContent[29][1], font=self.inputFont, justify='center', fg='white', bg=self.colorORT, height=2, width=8)
        self.tuesdayTitle.place(x=620, y=225)
        self.wednesdayTitle = Label(pageReserves, text=controller.currentLanguage.userPageContent[29][2], font=self.inputFont, justify='center', fg='white', bg=self.colorORT, height=2, width=8)
        self.wednesdayTitle.place(x=620, y=310)
        self.thursdayTitle = Label(pageReserves, text=controller.currentLanguage.userPageContent[29][3], font=self.inputFont, justify='center', fg='white', bg=self.colorORT, height=2, width=8)
        self.thursdayTitle.place(x=620, y=390)
        self.fridayTitle = Label(pageReserves, text=controller.currentLanguage.userPageContent[29][4], font=self.inputFont, justify='center', fg='white', bg=self.colorORT, height=2, width=8)
        self.fridayTitle.place(x=620, y=475)

    def fillPageReservesTitles(self, pageReserves, controller):
        self.fillPageReservesWeekdaysTitles(pageReserves, controller)
        self.dateCheckTitle = Label(pageReserves, text=controller.currentLanguage.userPageContent[30], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.dateCheckTitle.place(x=770, y=20)
        self.eraseMotiveTitle = Label(pageReserves, text=controller.currentLanguage.userPageContent[31], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.eraseMotiveTitle.place(x=770, y=155)
        self.informationReserveTitle = Label(pageReserves, text=controller.currentLanguage.userPageContent[32], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.informationReserveTitle.place(x=770, y=270)
        self.previousMonthTitle = Label(pageReserves, text=controller.currentLanguage.userPageContent[33], font=self.buttonFont, fg = 'dark red', bg = self.colorORT)
        self.previousMonthTitle.place(x=900, y=460)
        self.monthTitlePrevious = Label(pageReserves, text=controller.currentLanguage.userPageContent[34], font=self.buttonFont, fg = 'dark blue', bg = self.colorORT)
        self.monthTitlePrevious.place(x=920, y=500)
        self.nextMonthTitle = Label(pageReserves, text=controller.currentLanguage.userPageContent[35], font=self.buttonFont, fg = 'dark blue', bg = self.colorORT)
        self.nextMonthTitle.place(x=1020, y=460)
        self.monthTitleNext = Label(pageReserves, text=controller.currentLanguage.userPageContent[36], font=self.buttonFont, fg = 'dark red', bg = self.colorORT)
        self.monthTitleNext.place(x=1020, y=500)

    def fillPageReservesWithReserves(self, pageReserves, controller):
        self.reservationMonthShown = date.today().month-1
        self.setReservesOfMonth(pageReserves, controller)
        self.updateReservationDisplay(pageReserves, controller)
        #self.setReservesOfMonth(pageReserves, "September", [840, 770])

    def showPreviousMonth(self, pageReserves, controller):
        if(self.reservationMonthShown>1):
            self.reservationMonthShown = self.reservationMonthShown - 1
        print("RESERVATION MONTH: ", self.reservationMonthShown)
        self.updateReservationDisplay(pageReserves, controller)

    def showNextMonth(self, pageReserves, controller):
        if(self.reservationMonthShown<12):
            self.reservationMonthShown = self.reservationMonthShown + 1
        print("RESERVATION MONTH: ", self.reservationMonthShown)
        self.updateReservationDisplay(pageReserves, controller)

    def showReservationSelected(self, controller, reservationToCheck):
        self.reservationCheck[3]['text'] = controller.currentLanguage.userPageContent[37]
        self.reservationCheck[3]['fg'] = "blue"
        reservationInfo = controller.application.listReservations.getInformationOfDate(reservationToCheck.datesOfReservation[0])
        if(not reservationInfo[0].areEqual(reservationInfo[1])):
            userReservationInformation = controller.currentLanguage.userPageContent[38]+reservationInfo[0].surname.upper()+", "+reservationInfo[0].name+controller.currentLanguage.userPageContent[39]+reservationInfo[1].surname.upper()+", "+reservationInfo[1].name+controller.currentLanguage.userPageContent[40]
        else:
            userReservationInformation = controller.currentLanguage.userPageContent[41]+reservationInfo[0].surname.upper()+", "+reservationInfo[0].name+controller.currentLanguage.userPageContent[40]
        if(len(reservationInfo[2])<2):
            self.reservationCheck[4]['text'] = userReservationInformation+controller.currentLanguage.userPageContent[42]
        else:
            self.reservationCheck[4]['text'] = userReservationInformation+reservationInfo[2]

    def checkRegistrationSelected(self, controller, reservationToCheck):
        if (controller.application.listReservations.isReservationPeriodAvailable(reservationToCheck)):
            self.reservationCheck[3]['text'] = controller.currentLanguage.userPageContent[43]
            self.reservationCheck[3]['fg'] = "red"
        else:
            self.showReservationSelected(controller, reservationToCheck)

    def checkReservationExistance(self, controller):
        currentUser = controller.application.listStudents.students[controller.application.systemCurrentStatus.userLogged]
        if(self.isRegistrationInputCorrect(currentUser, self.reservationCheck)):
            dateToCheck = date(int(self.reservationCheck[2].get()), self.getNumberOfMonth(self.reservationCheck[1].get()), int(self.reservationCheck[0].get()))
            reservationToCheck = Reservation([currentUser, currentUser],[dateToCheck, dateToCheck])
            self.checkRegistrationSelected(controller, reservationToCheck)
        else:
            messagebox.showerror(controller.currentLanguage.userPageContent[44], controller.currentLanguage.userPageContent[45])

    def checkReservationToErase(self, controller, reservationToCheck):
        if (controller.application.listReservations.isReservationPeriodAvailable(reservationToCheck)):
            messagebox.showwarning(controller.currentLanguage.userPageContent[46], controller.currentLanguage.userPageContent[47])
        else:
            reservationRemoved = controller.application.listReservations.removeReservationByDate(reservationToCheck.datesOfReservation[0])
            beginningRemoved = reservationRemoved.datesOfReservation[0].strftime("%d/%B/%Y")
            endingRemoved = reservationRemoved.datesOfReservation[len(reservationRemoved.datesOfReservation)-1].strftime("%d/%B/%Y")
            self.updateReservationDisplay(pageReserves, controller)
            messageReservationToDisplay = controller.currentLanguage.userPageContent[48][0]+beginningRemoved+controller.currentLanguage.userPageContent[48][1]+endingRemoved+controller.currentLanguage.userPageContent[48][2]
            if(self.notifyEraseReservation.get()==1):
                reservationRmovedBodyMail = "\n\n"+controller.currentLanguage.userPageContent[164]+reservationRemoved.professorResponsible.getCompleteNameSurname()+controller.currentLanguage.userPageContent[165]+reservationRemoved.userToReserve.getCompleteNameSurname()+",\n\n    Professor "+controller.application.listProfessors.professors[controller.application.systemCurrentStatus.userLogged].getCompleteNameSurname()+controller.currentLanguage.userPageContent[166]+beginningRemoved+" to "+endingRemoved+controller.currentLanguage.userPageContent[167]
                controller.application.sendEmail([reservationRemoved.professorResponsible.email, reservationRemoved.userToReserve.email], [controller.currentLanguage.userPageContent[170], 'Images/MailContent/reservationErasedMail.png', reservationRmovedBodyMail, "IMAGE"])
                messageReservationToDisplay = messageReservationToDisplay + controller.currentLanguage.userPageContent[168]
            messagebox.showinfo(controller.currentLanguage.userPageContent[169], messageReservationToDisplay)
            #messagebox.showinfo("RESERVATION ERASED","Reservation from "+beginningRemoved+"\nto "+endingRemoved+" was SUCCESFULLY Erased")
            #print("LISTA DE RESERVATIONS: ", len(controller.application.listReservations.reservations))

    def eraseReservation(self, pageReserves, controller):
        currentUser = controller.application.listStudents.students[controller.application.systemCurrentStatus.userLogged]
        if(self.isRegistrationInputCorrect(currentUser, self.reservationCheck)):
            dateToCheck = date(int(self.reservationCheck[2].get()), self.getNumberOfMonth(self.reservationCheck[1].get()), int(self.reservationCheck[0].get()))
            reservationToCheck = Reservation([currentUser, currentUser],[dateToCheck, dateToCheck])
            self.checkReservationToErase(controller, reservationToCheck)
        else:
            messagebox.showerror(controller.currentLanguage.userPageContent[44], controller.currentLanguage.userPageContent[45])

    def fillPageReservesButtons(self, pageReserves, controller):
        self.arrowLeftImageMonths = PhotoImage(file="Images/Logos/arrowLeft.gif")
        previousMonthOption = Button(pageReserves, image=self.arrowLeftImageMonths, relief = SUNKEN, compound=CENTER, command=lambda:self.showPreviousMonth(pageReserves, controller))
        previousMonthOption.place(x=790, y=455)
        self.arrowRightImageMonths = PhotoImage(file="Images/Logos/arrowRight.gif")
        nextMonthOption = Button(pageReserves, image=self.arrowRightImageMonths, relief = SUNKEN, compound=CENTER, command=lambda:self.showNextMonth(pageReserves, controller))
        nextMonthOption.place(x=1100, y=455)

        self.checkReservationExistanceOption = Button(pageReserves, text=controller.currentLanguage.userPageContent[49], font=self.buttonFont, fg=self.colorORT, bg='white', relief = SUNKEN, compound=CENTER, command=lambda:self.checkReservationExistance(controller))
        self.checkReservationExistanceOption.place(x=990, y=100)
        self.eraseReservationOption = Button(pageReserves, text=controller.currentLanguage.userPageContent[50], font=self.buttonFont, fg=self.colorORT, bg='white', relief = SUNKEN, compound=CENTER, command=lambda:self.eraseReservation(pageReserves, controller))
        self.eraseReservationOption.place(x=990, y=210)

    def fillPageReservesEntries(self, pageReserves, controller):
        self.reservationCheck.append(Spinbox(pageReserves, from_=1, to=31, font=self.inputFont, width=3, justify='center'))
        self.reservationCheck[0].place(x=940, y=20)
        self.reservationCheck.append(Spinbox(pageReserves, values=controller.currentLanguage.adminPageContent[44], font=self.inputFont, width=8, justify='center'))
        self.reservationCheck[1].place(x=995, y=20)
        self.reservationCheck.append(Spinbox(pageReserves, from_=2018, to=2040,  font=self.inputFont, width=5, justify='center'))
        self.reservationCheck[2].place(x=1105, y=20)
        self.reservationCheck.append(Label(pageReserves, text=controller.currentLanguage.userPageContent[51], font="Times 12 bold", fg = 'white', bg = self.colorORT))
        self.reservationCheck[3].place(x=780, y=100)
        self.reservationCheck.append(Label(pageReserves, font=self.inputFont, fg = self.colorORT, bg='white', height=5, width=38))
        self.reservationCheck[4].place(x=770, y=320)

        self.reservationErase.append(Entry(pageReserves,font=self.inputFont, width=25, justify='center'))
        self.reservationErase[0].place(x=945, y=160)
        self.reservationErase.append(Checkbutton(pageReserves, text=controller.currentLanguage.userPageContent[52], font="Times 12 bold", fg='dark grey', bg=self.colorORT, variable=self.notifyEraseReservation))
        self.reservationErase[1].place(x=770, y=210)

    def fillPageReservesIndicators(self, pageReserves):
        reservationDayCheckIndicator = Label(pageReserves, text="DD  /", font="Times 14 bold", fg = 'white', bg = self.colorORT)
        reservationDayCheckIndicator.place(x=950, y=50)
        reservationMonthCheckIndicator = Label(pageReserves, text="MM  /", font="Times 14 bold", fg = 'white', bg = self.colorORT)
        reservationMonthCheckIndicator.place(x=1030, y=50)
        reservationYearCheckIndicator = Label(pageReserves, text="YY", font="Times 14 bold", fg = 'white', bg = self.colorORT)
        reservationYearCheckIndicator.place(x=1140, y=50)

    def fillPageReserves(self, pageReserves, controller):
        self.fillPageReservesTitles(pageReserves, controller)
        self.fillPageReservesPictures(pageReserves)
        self.fillPageReservesWithReserves(pageReserves, controller)
        self.fillPageReservesButtons(pageReserves, controller)
        self.fillPageReservesEntries(pageReserves, controller)
        self.fillPageReservesIndicators(pageReserves)

    def fillPagePlatformPictures(self, pagePlatform):
        fermentHistoryElement = Picture(['fermentationsHistoryElement','png',130,550,10,10],0)
        fermentHistoryElement.purpose = 'Words'
        fermentHistoryElementPic = fermentHistoryElement.generateLabel(pagePlatform)
        fermentHistoryElementPic.place(x=fermentHistoryElement.location[0],y=fermentHistoryElement.location[1])

    def fillPagePlatformTitles(self, pagePlatform, controller):
        self.searchTitle = Label(pagePlatform, text=controller.currentLanguage.userPageContent[76], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.searchTitle.place(x=690, y=10)
        self.descriptionTitle = Label(pagePlatform, text=controller.currentLanguage.userPageContent[77], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.descriptionTitle.place(x=690, y=100)
        self.filenameInformationTitle = Label(pagePlatform, text=controller.currentLanguage.userPageContent[78], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.filenameInformationTitle.place(x=690, y=380)
        self.contentExistanceInformation = Label(pagePlatform, text=controller.currentLanguage.userPageContent[79], font=self.inputFont, bg = self.colorORT)
        self.contentExistanceInformation.place(x=920, y=390)

    def fillPagePlatformEntries(self, pagePlatform):
        self.platformInformation.append(Entry(pagePlatform, font=self.searchFont, fg = self.colorORT, bg='white', width=39))
        self.platformInformation[0].place(x=690, y=50)
        self.platformInformation.append(Entry(pagePlatform, font=self.searchFont, fg = self.colorORT, bg='white', width=39))
        self.platformInformation[1].place(x=690, y=420)
        self.platformInformation.append(Label(pagePlatform, text="", font=self.inputFont, fg = self.colorORT, bg='white', height=10, width=51))
        self.platformInformation[2].place(x=690, y=140)

    def searchOnline(self, stringToSearch):
        directionWiki = ''
        firstPageFound = ''
        isFirstURL = False
        for urlFound in search(stringToSearch, stop=10):#tld='en', lang='en', stop=20):
            if(not isFirstURL):
                firstPageFound = urlFound
                isFirstURL = True
            if(urlFound.find('wikipedia')==11):
                directionWiki = urlFound
                break
        if(directionWiki==''):
            directionWiki = firstPageFound
        webbrowser.open(directionWiki)

    def searchContent(self):
        inputToSearch = self.platformInformation[0].get()
        if(inputToSearch!=''):
            self.searchOnline(inputToSearch)
            self.platformInformation[0].delete(0,END)

    def verifyContentExistance(self, controller):
        doesContentExist = False
        if(len(self.fermentationsList.curselection())>0):
            dataOfFermentationSelected = controller.application.listFermentations.fermentations[int(self.fermentationsList.curselection()[0])+self.pageOfListFermentations*30].dataFilenames
            for eachDataFile in dataOfFermentationSelected:
                velocityFile = "ControlData/Velocity/DATA_Log/"+eachDataFile+"_VEL.txt"
                temperatureFile = "ControlData/Temperature/DATA_Log/"+eachDataFile+"_TEM.txt"
                potentialHydrogenFile = "ControlData/PotentialHydrogen/DATA_Log/"+eachDataFile+"_POT.txt"
                if(Path(velocityFile).exists() or Path(temperatureFile).exists() or Path(potentialHydrogenFile).exists()):
                    doesContentExist = True
                    break
            if(doesContentExist):
                self.contentExistanceInformation.config(text=controller.currentLanguage.userPageContent[80], fg='green4')
            else:
                self.contentExistanceInformation.config(text=controller.currentLanguage.userPageContent[81], fg='red')
        else:
            self.contentExistanceInformation.config(text=controller.currentLanguage.userPageContent[79], fg='blue')
            messagebox.showwarning(controller.currentLanguage.userPageContent[82], controller.currentLanguage.userPageContent[83])

    def fillFermentationsList(self, controller):
        if(len(controller.application.listFermentations.fermentations)>0):
            self.fermentationsList.delete(0,END)
            positionGraphicList = 1
            positionGlobalList = 0
            for aFermentation in controller.application.listFermentations.fermentations:
                if(positionGlobalList>=self.pageOfListFermentations*30 and positionGlobalList<(self.pageOfListFermentations+1)*30):
                    self.fermentationsList.insert(positionGraphicList, aFermentation.showInformation())
                    positionGraphicList = positionGraphicList + 1
                positionGlobalList = positionGlobalList + 1
        else:
            self.fermentationsList.delete(0,END)
            self.fermentationsList.insert(1, controller.currentLanguage.adminPageContent[74])

    def configureFermentationList(self, pagePlatform, controller):

        def onselectFermentation(evt):
            try:
                listOfFermentations = evt.widget
                self.platformInformation[2]['text'] = controller.application.listFermentations.fermentations[int(listOfFermentations.curselection()[0])+self.pageOfListFermentations*30].getDescriptiveInformation()
            except IndexError:
                self.fermentationsList.activate(0)
                self.platformInformation[2]['text'] = ""
            except AttributeError:
                self.platformInformation[2]['text'] = controller.currentLanguage.userPageContent[84]

        self.fermentationsList = Listbox(pagePlatform, width=83, height=30, font=self.listElementFont)
        self.fermentationsList.place(x=140,y=10)
        self.fillFermentationsList(controller)
        self.fermentationsList.bind('<<ListboxSelect>>', onselectFermentation)

    def animateLoading(self):
        self.loadingTitle.place(x=1024/2, y=800/2)
        for c in itertools.cycle(['|', '/', '-', '\\']):
            if self.doneLoading:
                break
            self.loadingTitle['text']=(c + ' LOADING ' + c)
            time.sleep(0.1)
        self.loadingTitle['text']=('DONE!')
        #time.sleep(0.2)
        self.loadingTitle.place(x=2000,y=2000)

    def continueFermentation(self, controller):
        if(len(self.fermentationsList.curselection())>0):
            controller.application.systemCurrentStatus.fermentationActual = int(self.fermentationsList.curselection()[0])+self.pageOfListFermentations*30
            currentUser = controller.application.listStudents.students[controller.application.systemCurrentStatus.userLogged]
            dataAdded = [self.fermentationInput[0].get(), self.fermentationInput[1].get(), self.fermentationInput[2].get(), self.fermentationInput[3].get(1.0,END)]
            controller.application.systemData.informations[4].addFermentationContinued()
            controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].isFermentationContinuing = True
            messagebox.showinfo(controller.currentLanguage.userPageContent[4], controller.currentLanguage.userPageContent[151])
            #self.doneLoading = False
            #loadingScreen = threading.Thread(target=lambda:self.animateLoading())
            #loadingScreen.start()
            #newFermentation = Fermentation(currentUser, dataAdded)
            #newFermentation.initiateFermentation(controller)
            #self.doneLoading = True
        else:
            messagebox.showwarning(controller.currentLanguage.userPageContent[85], controller.currentLanguage.userPageContent[83])

    def showPageOfListFermentations(self, controller, numberOfPage):
        for eachButton in self.pageNumberOfFermentationList:
            eachButton['bg']='white'
        self.pageOfListFermentations = numberOfPage-1
        self.pageNumberOfFermentationList[self.pageOfListFermentations]['bg'] = 'yellow'
        self.fillFermentationsList(controller)

    def configureHistoryListButtons(self, pagePlatform, controller):
        self.continueFermentationOption = Button(pagePlatform, text=controller.currentLanguage.userPageContent[86], relief = SUNKEN, fg='white', bg = 'IndianRed4', font=self.buttonFont, compound=CENTER, height = 2, width = 16, command=lambda:self.continueFermentation(controller))
        self.continueFermentationOption.place(x=140, y=490)
        self.pageNumberOfFermentationList.append(Button(pagePlatform, text="1", relief = SUNKEN, fg=self.colorORT, bg = 'yellow', font=self.buttonFont, compound=CENTER, height = 2, width = 4, command=lambda:self.showPageOfListFermentations(controller, 1)))
        self.pageNumberOfFermentationList[0].place(x=340, y=490)
        self.pageNumberOfFermentationList.append(Button(pagePlatform, text="2", relief = SUNKEN, fg=self.colorORT, bg = 'white', font=self.buttonFont, compound=CENTER, height = 2, width = 4, command=lambda:self.showPageOfListFermentations(controller, 2)))
        self.pageNumberOfFermentationList[1].place(x=400, y=490)
        self.pageNumberOfFermentationList.append(Button(pagePlatform, text="3", relief = SUNKEN, fg=self.colorORT, bg = 'white', font=self.buttonFont, compound=CENTER, height = 2, width = 4, command=lambda:self.showPageOfListFermentations(controller, 3)))
        self.pageNumberOfFermentationList[2].place(x=460, y=490)
        self.pageNumberOfFermentationList.append(Button(pagePlatform, text="4", relief = SUNKEN, fg=self.colorORT, bg = 'white', font=self.buttonFont, compound=CENTER, height = 2, width = 4, command=lambda:self.showPageOfListFermentations(controller, 4)))
        self.pageNumberOfFermentationList[3].place(x=520, y=490)
        self.pageNumberOfFermentationList.append(Button(pagePlatform, text="5", relief = SUNKEN, fg=self.colorORT, bg = 'white', font=self.buttonFont, compound=CENTER, height = 2, width = 4, command=lambda:self.showPageOfListFermentations(controller, 5)))
        self.pageNumberOfFermentationList[4].place(x=580, y=490)

    def getMagnitudeContentTitle(self, nameOfFile):
        excelTitle = ""
        if('Velocity' in nameOfFile):
            excelTitle = 'Date,Time,TZ,Speed Current[rpm],Speed Objective[rpm],System Temperature[°C],Frequency[Hz]'
        if('Temperature' in nameOfFile):
            excelTitle = 'Date,Time,TZ,FERM Temp Current[°C],FERM Temp Objective[°C],BATH Temp[°C],BATH Temp Objective[°C],Pump Step'
        if('PotentialHydrogen' in nameOfFile):
            excelTitle = 'Date,Time,TZ,FERM pH Current[no dim.],Ferm pH Objective[no dim.],ACID Volume[mL],BASE Volume[mL]'
        self.magnitudeRowList.append(excelTitle.split(','))

    def getMagnitudeData(self, currentFile, timeInformation):
        fileContent = open(currentFile, 'r+')
        for row in fileContent:
            magnitudeRow = row.split(',')
            if('Velocity' in currentFile or 'PotentialHydrogen' in currentFile):
                timeDelta = timeInformation[0] + timedelta(seconds=int(magnitudeRow[4]), microseconds=int(magnitudeRow[5]))
                finalString = timeDelta.strftime("%Y-%m-%d")+","+timeDelta.strftime("%I:%M:%S:%f")+","+timeInformation[1]+","+str(magnitudeRow[0])+","+str(magnitudeRow[1])+","+str(round(float(magnitudeRow[2]),5))+","+str(round(float(magnitudeRow[3]),5))
            if('Temperature' in currentFile):
                timeDelta = timeInformation[0] + timedelta(seconds=int(magnitudeRow[5]), microseconds=int(magnitudeRow[6]))
                finalString = timeDelta.strftime("%Y-%m-%d")+","+timeDelta.strftime("%I:%M:%S:%f")+","+timeInformation[1]+","+str(magnitudeRow[0])+","+str(magnitudeRow[1])+","+str(magnitudeRow[2])+","+str(magnitudeRow[3])+","+str(magnitudeRow[4])
            finalRow = finalString.split(',')
            self.magnitudeRowList.append(finalRow)
            self.lastMeasurementOfMagnitude = timeDelta
            if(self.firstPosition):
                self.firstMeasureOfMagnitude = timeDelta
                self.firstPosition = False
        fileContent.close()

    def getDataForFile(self, magnitudeName, storageFile):
        magnitudeFile = "ControlData/"+str(magnitudeName)+"/DATA_Log/"
        self.magnitudeRowList = []
        self.firstMeasureOfMagnitude = None
        self.lastMeasurementOfMagnitude = None
        self.firstPosition = True
        firstPositionForTitle = True
        utcInformation = str(datetime.now(tz=pytz.UTC).astimezone(pytz.timezone(str(tzlocal.get_localzone()))))[26:32]
        for eachFile in storageFile:
            currentFile = str(magnitudeFile)+str(eachFile)
            if(Path(currentFile).exists()):
                nowDate = date(int(eachFile[0:4]), int(eachFile[4:6]), int(eachFile[6:8]))
                nowTime = time(int(eachFile[9:11]),int(eachFile[11:13]),int(eachFile[13:15]))
                fileTime = datetime.combine(nowDate, nowTime)
                if(firstPositionForTitle):
                    self.getMagnitudeContentTitle(magnitudeFile)
                    firstPositionForTitle = False
                self.getMagnitudeData(currentFile, [fileTime, utcInformation])

    def getStyleOfExcelTitle(self):
        fontTitleVelocity = Font()
        fontTitleVelocity.name = 'Times New Roman'
        fontTitleVelocity.bold = True
        fontTitleVelocity.height = 15*20
        fontTitleVelocity.colour_index = 4
        bordersTitle = Borders()
        bordersTitle.left = 2
        bordersTitle.right = 2
        bordersTitle.top = 2
        bordersTitle.bottom = 2
        styleTitleVelocity = XFStyle()
        styleTitleVelocity.font = fontTitleVelocity
        styleTitleVelocity.alignment.horz = xlwt.Alignment.HORZ_CENTER
        styleTitleVelocity.borders = bordersTitle

        fontTitleTemperature = Font()
        fontTitleTemperature.name = 'Times New Roman'
        fontTitleTemperature.bold = True
        fontTitleTemperature.height = 15*20
        fontTitleTemperature.colour_index = 2
        styleTitleTemperature = XFStyle()
        styleTitleTemperature.font = fontTitleTemperature
        styleTitleTemperature.alignment.horz = xlwt.Alignment.HORZ_CENTER
        styleTitleTemperature.borders = bordersTitle

        fontTitlePotHydrogen = Font()
        fontTitlePotHydrogen.name = 'Times New Roman'
        fontTitlePotHydrogen.bold = True
        fontTitlePotHydrogen.height = 15*20
        fontTitlePotHydrogen.colour_index = 3
        styleTitlePotHydrogen = XFStyle()
        styleTitlePotHydrogen.font = fontTitlePotHydrogen
        styleTitlePotHydrogen.alignment.horz = xlwt.Alignment.HORZ_CENTER
        styleTitlePotHydrogen.borders = bordersTitle
        return [styleTitleVelocity, styleTitleTemperature, styleTitlePotHydrogen]

    def getStyleOfExcelData(self):
        fontData = Font()
        fontData.height = 10*20
        bordersData = Borders()
        bordersData.left = 1
        bordersData.right = 1
        bordersData.top = 1
        bordersData.bottom = 1
        styleData = XFStyle()
        styleData.font = fontData
        styleData.alignment.horz = xlwt.Alignment.HORZ_CENTER
        styleData.borders = bordersData
        return styleData

    def configureExcelVelocity(self, eachFileName, styleTitle, worksheet):
        velocityCustomization = self.fermentationSelected.magnitudesToControl.getVelocityCustomizationData()
        worksheet.write_merge(2,2,8,10,eachFileName+" Control Unit: ", styleTitle[self.magnitudePosition])
        worksheet.write_merge(2,2,11,14,velocityCustomization[0], styleTitle[self.magnitudePosition])
        worksheet.write_merge(3,3,8,10,eachFileName+" Control Precision: ", styleTitle[self.magnitudePosition])
        worksheet.write_merge(3,3,11,14,velocityCustomization[1], styleTitle[self.magnitudePosition])
        worksheet.write_merge(4,4,8,10,eachFileName+" Control Slope: ", styleTitle[self.magnitudePosition])
        worksheet.write_merge(4,4,11,14,velocityCustomization[2], styleTitle[self.magnitudePosition])
        worksheet.write_merge(5,5,8,10,eachFileName+" Spin Orientation: ", styleTitle[self.magnitudePosition])
        worksheet.write_merge(5,5,11,14,velocityCustomization[3], styleTitle[self.magnitudePosition])
        worksheet.write_merge(6,6,8,10,eachFileName+" Control Data Interval: ", styleTitle[self.magnitudePosition])
        worksheet.write_merge(6,6,11,14,velocityCustomization[4], styleTitle[self.magnitudePosition])
        return worksheet

    def configureExcelTemperature(self, eachFileName, styleTitle, worksheet):
        temperatureCustomization = self.fermentationSelected.magnitudesToControl.getTemperatureCustomizationData()
        worksheet.write_merge(2,2,8,10,eachFileName+" Control Unit: ", styleTitle[self.magnitudePosition])
        worksheet.write_merge(2,2,11,14,temperatureCustomization[0], styleTitle[self.magnitudePosition])
        worksheet.write_merge(3,3,8,10,eachFileName+" Control Precision: ", styleTitle[self.magnitudePosition])
        worksheet.write_merge(3,3,11,14,temperatureCustomization[1], styleTitle[self.magnitudePosition])
        worksheet.write_merge(4,4,8,10,eachFileName+" Pump Step: ", styleTitle[self.magnitudePosition])
        worksheet.write_merge(4,4,11,14,temperatureCustomization[2], styleTitle[self.magnitudePosition])
        worksheet.write_merge(5,5,8,10,eachFileName+" Control Slope: ", styleTitle[self.magnitudePosition])
        worksheet.write_merge(5,5,11,14,temperatureCustomization[3], styleTitle[self.magnitudePosition])
        worksheet.write_merge(6,6,8,10,eachFileName+" Control Data Interval: ", styleTitle[self.magnitudePosition])
        worksheet.write_merge(6,6,11,14,temperatureCustomization[4], styleTitle[self.magnitudePosition])
        return worksheet

    def configureExcelPotentialHydrogen(self, eachFileName, styleTitle, worksheet):
        potentialCustomization = self.fermentationSelected.magnitudesToControl.getPotentialCustomizationData()
        worksheet.write_merge(2,2,8,10,eachFileName+" Control Unit: ", styleTitle[self.magnitudePosition])
        worksheet.write_merge(2,2,11,14,potentialCustomization[0], styleTitle[self.magnitudePosition])
        worksheet.write_merge(3,3,8,10,eachFileName+" Control Precision: ", styleTitle[self.magnitudePosition])
        worksheet.write_merge(3,3,11,14,potentialCustomization[1], styleTitle[self.magnitudePosition])
        worksheet.write_merge(4,4,8,10,eachFileName+" Burst Mode: ", styleTitle[self.magnitudePosition])
        worksheet.write_merge(4,4,11,14,potentialCustomization[2], styleTitle[self.magnitudePosition])
        worksheet.write_merge(5,5,8,10,eachFileName+" Time Between Drops: ", styleTitle[self.magnitudePosition])
        worksheet.write_merge(5,5,11,14,potentialCustomization[3], styleTitle[self.magnitudePosition])
        worksheet.write_merge(6,6,8,10,eachFileName+" Control Data Interval: ", styleTitle[self.magnitudePosition])
        worksheet.write_merge(6,6,11,14,potentialCustomization[4], styleTitle[self.magnitudePosition])
        return worksheet

    def configureEachExcelMagnitude(self, eachFileName, styleTitle, worksheet):
        worksheet.write_merge(0,0,8,10,eachFileName+" Data Quantity: ", styleTitle[self.magnitudePosition])
        worksheet.write(0,11,len(self.magnitudeRowList), styleTitle[self.magnitudePosition])
        worksheet.write_merge(1,1,8,10,eachFileName+" Control Duration: ", styleTitle[self.magnitudePosition])
        duration = self.lastMeasurementOfMagnitude-self.firstMeasureOfMagnitude
        worksheet.write_merge(1,1,11,14,str(duration.days)+" Days, "+str(duration.seconds)+" Seconds", styleTitle[self.magnitudePosition])
        if(eachFileName=="Velocity"):
            worksheet = self.configureExcelVelocity(eachFileName, styleTitle, worksheet)
        if(eachFileName=="Temperature"):
            worksheet = self.configureExcelTemperature(eachFileName, styleTitle, worksheet)
        if(eachFileName=="PotentialHydrogen"):
            worksheet = self.configureExcelPotentialHydrogen(eachFileName, styleTitle, worksheet)
        return worksheet

    def configureExcelFile(self, controller):
        nameOfFileToSave = "FermentationData/"+str(self.platformInformation[1].get())+".xls"
        self.fermentationSelected = controller.application.listFermentations.fermentations[int(self.fermentationsList.curselection()[0])+self.pageOfListFermentations*30]
        nameOfFile = self.fermentationSelected.dataFilenames #["20180903_153022.txt", "20180903_153544.txt", "20180913_125339.txt"]
        workbook = xlwt.Workbook()
        styleTitle = self.getStyleOfExcelTitle()
        styleData = self.getStyleOfExcelData()
        self.magnitudePosition = 0
        filesName = ["Velocity", "Temperature", "PotentialHydrogen"]
        for eachFileName in filesName:
            self.getDataForFile(eachFileName, nameOfFile)
            worksheet = workbook.add_sheet(eachFileName)
            position = 0
            if(len(self.magnitudeRowList)>1):
                magnitudeColumnContent = zip(*self.magnitudeRowList)
                for column in magnitudeColumnContent:
                    for item in range(len(column)):
                        if(item==0):
                            worksheet.write(0, position, column[item], styleTitle[self.magnitudePosition])
                        else:
                            worksheet.write(item, position, column[item], styleData)
                        worksheet.col(position).width = 0x0d00 + 80*20
                    workbook.save(nameOfFileToSave)
                    position = position + 1

                worksheet = self.configureEachExcelMagnitude(eachFileName, styleTitle, worksheet)
                workbook.save(nameOfFileToSave)
                self.magnitudePosition = self.magnitudePosition + 1

    def getExcelDataOfFermentation(self, controller):
        if(self.platformInformation[1].get()!="" and len(self.fermentationsList.curselection())>0):
            self.configureExcelFile()
            if(self.isSendFileSelected.get()==1):
                fermentationDataFileBodyMail = "\n\n"+controller.currentLanguage.userPageContent[171]+controller.application.listStudents.students[controller.application.systemCurrentStatus.userLogged].getCompleteNameSurname()+":\n"+controller.currentLanguage.userPageContent[182]+controller.application.listFermentations.fermentations[int(listOfFermentations.curselection()[0])+self.pageOfListFermentations*30].getDescriptiveInformation()+"\n\n\n"+controller.currentLanguage.userPageContent[178]
                controller.application.sendEmail([controller.application.listStudents.students[controller.application.systemCurrentStatus.userLogged].email], [controller.currentLanguage.userPageContent[180], "FermentationData/"+str(self.platformInformation[1].get())+".xls", fermentationDataFileBodyMail, "FILE"])
                messageExcelToDisplay = messageExcelToDisplay + controller.currentLanguage.userPageContent[88]
            messagebox.showinfo(controller.currentLanguage.userPageContent[89], messageExcelToDisplay)
            self.platformInformation[1].delete(0,END)
        else:
            messagebox.showwarning(controller.currentLanguage.userPageContent[90], controller.currentLanguage.userPageContent[91])

    def configureTXTFile(self, controller):
        nameOfFileToSave = "FermentationData/"+str(self.platformInformation[1].get())+".txt"
        nameOfFile = controller.application.listFermentations.fermentations[int(self.fermentationsList.curselection()[0])+self.pageOfListFermentations*30].dataFilenames #["20180903_153022.txt", "20180903_153544.txt", "20180913_125339.txt"]
        filesName = ["Velocity", "Temperature", "PotentialHydrogen"]
        self.getDataForFile('Velocity', nameOfFile)
        velData = self.magnitudeRowList
        self.getDataForFile('Temperature', nameOfFile)
        temperatureData = self.magnitudeRowList
        self.getDataForFile('PotentialHydrogen', nameOfFile)
        potentialData = self.magnitudeRowList
        position = 0
        while(position<len(velData) or position<=len(temperatureData) or position<=len(potentialData)):
            if(position<len(velData)):
                velInfo = ';'.join(velData[position])
            else:
                velInfo="0000-00-00;00:00:00:0000;-00:00;000.00;000.00;00.00000;00.00000"
            if(position<len(temperatureData)):
                temperatureInfo = ';'.join(temperatureData[position])
            else:
                temperatureInfo="0000-00-00;00:00:00:0000;-00:00;00.00;00.00;00.00;00.00;0"
            if(position<len(potentialData)):
                potentialInfo = ';'.join(potentialData[position])
            else:
                potentialInfo ="0000-00-00;00:00:00:0000;-00:00;00.00;00.00;00.00000;00.00000"
            with open(nameOfFileToSave, 'a') as txtData:
                txtData.write(velInfo+";"+temperatureInfo+";"+potentialInfo+'\n')
                txtData.close()
            position = position+1

    def getTXTDataOfFermentation(self, controller):
        if(self.platformInformation[1].get()!="" and len(self.fermentationsList.curselection())>0):
            self.configureTXTFile()
            messageTXTToDisplay = "TXT "+controller.currentLanguage.userPageContent[87]+" FermentationData/"+str(self.platformInformation[1].get())+".txt"
            if(self.isSendFileSelected.get()==1):
                fermentationDataFileBodyMail = "\n\n"+controller.currentLanguage.userPageContent[171]+controller.application.listStudents.students[controller.application.systemCurrentStatus.userLogged].getCompleteNameSurname()+":\n"+controller.currentLanguage.userPageContent[181]+controller.application.listFermentations.fermentations[int(listOfFermentations.curselection()[0])+self.pageOfListFermentations*30].getDescriptiveInformation()+"\n\n\n"+controller.currentLanguage.userPageContent[178]
                controller.application.sendEmail([controller.application.listStudents.students[controller.application.systemCurrentStatus.userLogged].email], [controller.currentLanguage.userPageContent[180], "FermentationData/"+str(self.platformInformation[1].get())+".txt", fermentationDataFileBodyMail, "FILE"])
                messageTXTToDisplay = messageTXTToDisplay + controller.currentLanguage.userPageContent[88]
            messagebox.showinfo(controller.currentLanguage.userPageContent[89], messageTXTToDisplay)
            self.platformInformation[1].delete(0,END)
        else:
            messagebox.showwarning(controller.currentLanguage.userPageContent[92], controller.currentLanguage.userPageContent[91])

    def fillPagePlatformButtons(self, pagePlatform, controller):
        self.searchImage = PhotoImage(file="Images/Logos/lupaLogo.gif")
        searchOption = Button(pagePlatform, image=self.searchImage, command=lambda:self.searchContent(), relief = SUNKEN, compound=CENTER)
        searchOption.place(x=1270, y=50)
        self.verifyImage = PhotoImage(file="Images/Logos/verifyLogo.gif")
        verifyOption = Button(pagePlatform, image=self.verifyImage, command=lambda:self.verifyContentExistance(controller), relief = SUNKEN, compound=CENTER)
        verifyOption.place(x=1270, y=420)
        self.getExcelInformationOption = Button(pagePlatform, text=controller.currentLanguage.userPageContent[93], relief = SUNKEN, fg='white', bg = 'green', font=self.buttonFont, compound=CENTER, height = 3, width = 17, command=lambda:self.getExcelDataOfFermentation(controller))
        self.getExcelInformationOption.place(x=690, y=470)
        self.getTXTInformationOption = Button(pagePlatform, text=controller.currentLanguage.userPageContent[94], relief = SUNKEN, fg='white', bg = 'snow4', font=self.buttonFont, compound=CENTER, height = 3, width = 17, command=lambda:self.getTXTDataOfFermentation(controller))
        self.getTXTInformationOption.place(x=950, y=470)
        self.sendFileSelectedOption = Checkbutton(pagePlatform, text=controller.currentLanguage.userPageContent[95], font=self.infoFont, fg='dark grey', bg=self.colorORT, variable=self.isSendFileSelected)
        self.sendFileSelectedOption.place(x=1180, y=470)
        self.configureHistoryListButtons(pagePlatform, controller)

    def fillPagePlatform(self, pagePlatform, controller):
        self.fillPagePlatformPictures(pagePlatform)
        self.configureFermentationList(pagePlatform, controller)
        self.fillPagePlatformTitles(pagePlatform, controller)
        self.fillPagePlatformEntries(pagePlatform)
        self.fillPagePlatformButtons(pagePlatform, controller)

    def doesFileExist(self, filename):
        file = "Images/Elements/"+filename
        filePath = Path(file)
        return filePath.exists()

    def getUserAdaptableElementPictures(self, pageToFill, userData):
        fileToLookName1Letter = userData[0][0:1]+'Element'
        fileToLookSurname1Letter = userData[1][0:1]+'Element'
        fileToLookName2Letters = userData[0][0:2]+'Element'
        fileToLookSurname2Letters = userData[1][0:2]+'Element'
        if(self.doesFileExist(fileToLookName2Letters+'.png')):
            userNameElement = Picture([fileToLookName2Letters,'png',60,60,285,20],0)
            userNameElement.purpose = 'Elements'
            userNameElementPic = userNameElement.generateLabel(pageToFill)
            userNameElementPic.place(x=userNameElement.location[0],y=userNameElement.location[1])
        elif(self.doesFileExist(fileToLookName1Letter+'.png')):
            userNameElement = Picture([fileToLookName1Letter,'png',60,60,265,20],0)
            userNameElement.purpose = 'Elements'
            userNameElementPic = userNameElement.generateLabel(pageToFill)
            userNameElementPic.place(x=userNameElement.location[0],y=userNameElement.location[1])
        if(self.doesFileExist(fileToLookSurname2Letters+'.png')):
            userSurnameElement = Picture([fileToLookSurname2Letters,'png',60,60,338,110],0)
            userSurnameElement.purpose = 'Elements'
            userSurnameElementPic = userSurnameElement.generateLabel(pageToFill)
            userSurnameElementPic.place(x=userSurnameElement.location[0],y=userSurnameElement.location[1])
        elif(self.doesFileExist(fileToLookSurname1Letter+'.png')):
            userSurnameElement = Picture([fileToLookSurname1Letter,'png',60,60,318,110],0)
            userSurnameElement.purpose = 'Elements'
            userSurnameElementPic = userSurnameElement.generateLabel(pageToFill)
            userSurnameElementPic.place(x=userSurnameElement.location[0],y=userSurnameElement.location[1])

    def fillPageNameSurname(self, pageToFill, controller):
        userName = controller.application.listStudents.students[controller.application.systemCurrentStatus.userLogged].name
        userSurname = controller.application.listStudents.students[controller.application.systemCurrentStatus.userLogged].surname
        studentName = Label(pageToFill, text=userName, font=self.userInfoFont, fg = 'white', bg = self.colorORT)
        studentName.place(x=300, y=30)
        studentSurname = Label(pageToFill, text=userSurname, font=self.userInfoFont, fg = 'white', bg = self.colorORT)
        studentSurname.place(x=350, y=120)
        self.getUserAdaptableElementPictures(pageToFill, [userName, userSurname])

    def fillPageProfileUserStatisticsTitles(self, pageProfile, controller):
        self.fermentationsQuantityTitle = Label(pageProfile, text=controller.currentLanguage.userPageContent[96]+" "+str(controller.application.listStudents.students[controller.application.systemCurrentStatus.userLogged].fermentationsQuantity), font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.fermentationsQuantityTitle.place(x=180, y=210)
        self.gameRecordsTitle = Label(pageProfile, text=controller.currentLanguage.userPageContent[97], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.gameRecordsTitle.place(x=180, y=300)
        self.scrambledTitle = Label(pageProfile, text="SCRAMBLED:  "+str(controller.application.listStudents.students[controller.application.systemCurrentStatus.userLogged].gamesScore[0])+controller.currentLanguage.userPageContent[183], font=self.gameFont, fg = 'DodgerBlue3', bg = self.colorORT)
        self.scrambledTitle.place(x=200, y=350)
        self.hangmanTitle = Label(pageProfile, text="HANGMAN:  "+str(controller.application.listStudents.students[controller.application.systemCurrentStatus.userLogged].gamesScore[1])+controller.currentLanguage.userPageContent[183], font=self.gameFont, fg = 'lime green', bg = self.colorORT)
        self.hangmanTitle.place(x=250, y=400)
        self.triviaTitle = Label(pageProfile, text="KNOW IT ALL:  "+str(controller.application.listStudents.students[controller.application.systemCurrentStatus.userLogged].gamesScore[2])+controller.currentLanguage.userPageContent[183], font=self.gameFont, fg = 'chocolate3', bg = self.colorORT)
        self.triviaTitle.place(x=300, y=450)

    def fillPageProfileUserInformationTitles(self, pageProfile, controller):
        self.usernumberTitle = Label(pageProfile, text=controller.currentLanguage.userPageContent[98], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.usernumberTitle.place(x=790, y=30)
        self.emailTitle = Label(pageProfile, text=controller.currentLanguage.userPageContent[99], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.emailTitle.place(x=790, y=120)
        self.birthdateTitle = Label(pageProfile, text=controller.currentLanguage.userPageContent[100], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.birthdateTitle.place(x=790, y=210)
        self.telephoneTitle = Label(pageProfile, text=controller.currentLanguage.userPageContent[101], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.telephoneTitle.place(x=790, y=300)
        self.addressTitle = Label(pageProfile, text=controller.currentLanguage.userPageContent[102], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.addressTitle.place(x=790, y=390)
        self.idNumberTitle = Label(pageProfile, text=controller.currentLanguage.userPageContent[103], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.idNumberTitle.place(x=790, y=480)

    def fillPageProfileTitles(self, pageProfile, controller):
        self.fillPageProfileUserStatisticsTitles(pageProfile, controller)
        self.fillPageProfileUserInformationTitles(pageProfile, controller)

    def fillPageProfileInformation(self, pageProfile, controller):
        usernumberInfo = Label(pageProfile, text=controller.application.listStudents.students[controller.application.systemCurrentStatus.userLogged].usernumber, font=self.inputFont, fg = 'white', bg = self.colorORT)
        usernumberInfo.place(x=1000, y=38)
        emailInfo = Label(pageProfile, text=controller.application.listStudents.students[controller.application.systemCurrentStatus.userLogged].email, font=self.inputFont, fg = 'white', bg = self.colorORT)
        emailInfo.place(x=930, y=128)
        birthdateInfo = Label(pageProfile, text=controller.application.listStudents.students[controller.application.systemCurrentStatus.userLogged].birthDate, font=self.inputFont, fg = 'white', bg = self.colorORT)
        birthdateInfo.place(x=1000, y=218)
        telephoneInfo = Label(pageProfile, text="0"+controller.application.listStudents.students[controller.application.systemCurrentStatus.userLogged].telephone, font=self.inputFont, fg = 'white', bg = self.colorORT)
        telephoneInfo.place(x=990, y=308)
        addressInfo = Label(pageProfile, text=controller.application.listStudents.students[controller.application.systemCurrentStatus.userLogged].address, font=self.inputFont, fg = 'white', bg = self.colorORT)
        addressInfo.place(x=970, y=398)
        idNumberInfo = Label(pageProfile, text=controller.application.listStudents.students[controller.application.systemCurrentStatus.userLogged].idNumber, font=self.inputFont, fg = 'white', bg = self.colorORT)
        idNumberInfo.place(x=990, y=488)

    def fillPageProfile(self, pageProfile, controller):
        controller.setImagesandSeparators(pageProfile, 'profileElement', [115,250,10,30,115,250,10,290])
        controller.setImagesandSeparators(pageProfile, 'informationElement', [115,260,1250,20,115,260,1250,300])
        separatorProfile = Picture(['profileInformationSeparator','png',150,580,600,0],0)
        separatorProfile.purpose = 'Separators'
        separatorProfilePic = separatorProfile.generateLabel(pageProfile)
        separatorProfilePic.place(x=separatorProfile.location[0],y=separatorProfile.location[1])
        self.fillPageNameSurname(pageProfile, controller)
        self.fillPageProfileTitles(pageProfile, controller)
        self.fillPageProfileInformation(pageProfile,controller)

    def fillPageContactTitles(self, pageContact, controller):
        self.passwordTitle.append(Label(pageContact, text=controller.currentLanguage.userPageContent[104], font=self.titleFont, fg = 'white', bg = self.colorORT))
        self.passwordTitle[0].place(x=150, y=210)
        self.passwordTitle.append(Label(pageContact, text=controller.currentLanguage.userPageContent[105], font=self.titleFont, fg = 'white', bg = self.colorORT))
        self.passwordTitle[1].place(x=150, y=300)
        self.passwordTitle.append(Label(pageContact, text=controller.currentLanguage.userPageContent[106], font=self.titleFont, fg = 'white', bg = self.colorORT))
        self.passwordTitle[2].place(x=150, y=390)

        self.mailTitle = Label(pageContact, text=controller.currentLanguage.userPageContent[107], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.mailTitle.place(x=720, y=20)
        self.messageTitle = Label(pageContact, text=controller.currentLanguage.userPageContent[108], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.messageTitle.place(x=720, y=120)

    def fillPageContactEntries(self, pageContact):
        self.passwordInput.append(Entry(pageContact, font=self.inputFont, width=20, justify='center')) # currentPasswordInput
        self.passwordInput[0].place(x=430, y=218)
        self.passwordInput.append(Entry(pageContact, font=self.inputFont, width=20, justify='center')) # passwordInput
        self.passwordInput[1].place(x=430, y=308)
        self.passwordInput.append(Entry(pageContact, font=self.inputFont, width=20, justify='center')) # confirmPasswordInput
        self.passwordInput[2].place(x=430, y=398)

        self.mailInformation.append(Entry(pageContact, font=self.destinataryFont, width=22, justify='center')) # mailInput
        self.mailInformation[0].place(x=720, y=70)
        self.mailInformation.append(Text(pageContact, font=self.inputFont, fg = self.colorORT, bg='white', height=12, width=46))
        self.mailInformation[1].place(x=720, y=160)

    def arePasswordConditionsRight(self, controller):
        self.cleanPasswordTitles()
        currentPasswordCorrect = self.passwordInput[0].get() != "" and self.passwordInput[0].get() == controller.application.listStudents.students[controller.application.systemCurrentStatus.userLogged].password
        anUser = User(["","","","","","","","",""])
        anUser.password = self.passwordInput[1].get()
        newPasswordCorrect = self.passwordInput[1].get() != "" and anUser.isPasswordRight()
        confirmPasswordCorrect = self.passwordInput[2].get() != "" and self.passwordInput[1].get() == self.passwordInput[2].get()
        if(not currentPasswordCorrect):
            self.passwordTitle[0]['fg'] = 'red'
        if(not newPasswordCorrect):
            self.passwordTitle[1]['fg'] = 'red'
        if(not confirmPasswordCorrect):
            self.passwordTitle[2]['fg'] = 'red'
        return currentPasswordCorrect and newPasswordCorrect and confirmPasswordCorrect

    def cleanPasswordTitles(self):
        for passwordTitle in self.passwordTitle:
            passwordTitle['fg'] = 'white'

    def deletePasswordFields(self):
        for passwordField in self.passwordInput:
            passwordField.delete(0,END)

    def checkPassword(self, controller):
        if(self.arePasswordConditionsRight(controller)):
            controller.application.listStudents.students[controller.application.systemCurrentStatus.userLogged].password = self.passwordInput[1].get()
            passwordBodyMail = "\n\n"+controller.currentLanguage.userPageContent[171]+controller.application.listStudents.students[controller.application.systemCurrentStatus.userLogged].getCompleteNameSurname()+",\n    "+controller.currentLanguage.userPageContent[184]
            controller.sendEmail([controller.application.listStudents.students[controller.application.systemCurrentStatus.userLogged].email], [controller.currentLanguage.userPageContent[185], 'Images/MailContent/passwordMail.png', passwordBodyMail, "IMAGE"])
            messagebox.showinfo(controller.currentLanguage.userPageContent[109], controller.currentLanguage.userPageContent[110])
            self.cleanPasswordTitles()
            self.deletePasswordFields()
        else:
            messagebox.showinfo(controller.currentLanguage.userPageContent[109], controller.currentLanguage.userPageContent[111])

    def sendParticularMailOption(self, controller):
        userSample = User(["","","","",self.mailInformation[0].get(),"","","",""])
        if(userSample.isEmailRight()==1):
            if(controller.isMessageRight(self.mailInformation[1])):
                controller.application.sendEmail([self.mailInformation[0].get()], [controller.currentLanguage.userPageContent[188], 'Images/MailContent/messageFromStudentMail.png', "\n\n"+controller.currentLanguage.userPageContent[189]+controller.application.listStudents.students[controller.application.systemCurrentStatus.userLogged].getCompleteNameSurname()+": "+self.mailInformation[1].get(1.0, END), "IMAGE"])
                messagebox.showinfo(controller.currentLanguage.userPageContent[89], controller.currentLanguage.userPageContent[112])
            else:
                messagebox.showerror(controller.currentLanguage.userPageContent[44], controller.currentLanguage.userPageContent[113])
        else:
            messagebox.showerror(controller.currentLanguage.userPageContent[44], controller.currentLanguage.userPageContent[114]+" @gmail.com, @ort.edu.uy, @yahoo.com, @vera.com, @adinet.com")

    def sendAdministratorOption(self, controller):
        if(controller.isMessageRight(self.mailInformation[1])):
            controller.application.sendEmail([controller.application.admin.email], [controller.currentLanguage.userPageContent[188], 'Images/MailContent/messageFromStudentMail.png', "\n\n"+controller.currentLanguage.userPageContent[189]+controller.application.listStudents.students[controller.application.systemCurrentStatus.userLogged].getCompleteNameSurname()+": "+self.mailInformation[1].get(1.0, END), "IMAGE"])
            messagebox.showinfo(controller.currentLanguage.userPageContent[89], controller.currentLanguage.userPageContent[115])
        else:
            messagebox.showerror(controller.currentLanguage.userPageContent[44], controller.currentLanguage.userPageContent[113])

    def sendProfessorsOption(self, controller):
        if(len(controller.application.listProfessors.professors)>0):
            if(controller.isMessageRight(self.mailInformation[1])):
                allProfessorsEmails = controller.application.listProfessors.getAllMailFromList()
                controller.application.sendEmail([allProfessorsEmails], [controller.currentLanguage.userPageContent[188], 'Images/MailContent/messageFromStudentMail.png', "\n\n"+controller.currentLanguage.userPageContent[189]+controller.application.listStudents.students[controller.application.systemCurrentStatus.userLogged].getCompleteNameSurname()+": "+self.mailInformation[1].get(1.0, END), "IMAGE"])
                messagebox.showinfo(controller.currentLanguage.userPageContent[89], controller.currentLanguage.userPageContent[190])
            else:
                messagebox.showerror(controller.currentLanguage.userPageContent[44], controller.currentLanguage.userPageContent[113])
        else:
            messagebox.showwarning(controller.currentLanguage.userPageContent[19], controller.currentLanguage.userPageContent[191])

    def fillPageContactButtons(self, pageContact, controller):
        self.updatePasswordOption = Button(pageContact, text=controller.currentLanguage.userPageContent[117], command=lambda:self.checkPassword(controller), relief = SUNKEN, fg='white', bg = 'PaleGreen3', font=self.buttonFont, compound=CENTER, height = 3, width = 30)
        self.updatePasswordOption.place(x=220, y=455)
        self.sendParticularMail = Button(pageContact, text=controller.currentLanguage.userPageContent[118], command=lambda:self.sendParticularMailOption(controller), relief = SUNKEN, fg='white', bg = 'IndianRed4', font=self.buttonFont, compound=CENTER, height = 3, width = 13)
        self.sendParticularMail.place(x=1050, y=20)
        self.sendAdministratorNotesOption = Button(pageContact, text=controller.currentLanguage.userPageContent[119], command=lambda:self.sendAdministratorOption(controller), relief = SUNKEN, fg='white', bg = 'AntiqueWhite4', font=self.buttonFont, compound=CENTER, height = 3, width = 22)
        self.sendAdministratorNotesOption.place(x=700, y=455)
        self.sendProfessorsNotesOption = Button(pageContact, text=controller.currentLanguage.userPageContent[192], command=lambda:self.sendProfessorsOption(controller), relief = SUNKEN, fg='white', bg = 'dark blue', font=self.buttonFont, compound=CENTER, height = 3, width = 22)
        self.sendProfessorsNotesOption.place(x=980, y=455)

    def fillPageContact(self, pageContact, controller):
        controller.setImagesandSeparators(pageContact, 'passwordElement', [115,250,10,30,115,250,10,290])
        controller.setImagesandSeparators(pageContact, 'contactElement', [115,250,1250,30,115,250,1250,290])
        self.fillPageNameSurname(pageContact, controller)
        self.fillPageContactTitles(pageContact, controller)
        self.fillPageContactEntries(pageContact)
        self.fillPageContactButtons(pageContact, controller)

    def showPreviousGame(self, pageLeaderboards, controller):
        if(self.gameIdentifier>0):
            self.gameIdentifier = self.gameIdentifier - 1
            self.setLeaderboardsContent(pageLeaderboards, controller)

    def showNextGame(self, pageLeaderboards, controller):
        if(self.gameIdentifier<2):
            self.gameIdentifier = self.gameIdentifier + 1
            self.setLeaderboardsContent(pageLeaderboards, controller)

    def fillPageLeaderboardsButtons(self, pageLeaderboards, controller):
        self.arrowLeftImageLeaderboards = PhotoImage(file="Images/Logos/arrowLeft.gif")
        previousGameOption = Button(pageLeaderboards, image=self.arrowLeftImageLeaderboards, command=lambda:self.showPreviousGame(pageLeaderboards, controller), relief = SUNKEN, compound=CENTER)
        previousGameOption.place(x=1195, y=50)
        self.arrowRightImageLeaderboards = PhotoImage(file="Images/Logos/arrowRight.gif")
        nextGameOption = Button(pageLeaderboards, image=self.arrowRightImageLeaderboards, command=lambda:self.showNextGame(pageLeaderboards, controller), relief = SUNKEN, compound=CENTER)
        nextGameOption.place(x=1195, y=400)
        self.labelChangeGame = Label(pageLeaderboards, text=controller.currentLanguage.userPageContent[163], bg=self.colorORT, fg = 'red', font=self.titleFont, compound=CENTER)
        self.labelChangeGame.place(x=1180, y=180)
        self.labelGame = Label(pageLeaderboards, text=controller.currentLanguage.userPageContent[194], bg=self.colorORT, fg = 'blue', font=self.titleFont, compound=CENTER)
        self.labelGame.place(x=1150, y=250)
        self.labelDisplayedGame = Label(pageLeaderboards, text=controller.currentLanguage.userPageContent[195], bg=self.colorORT, fg = 'red', font=self.titleFont, compound=CENTER)
        self.labelDisplayedGame.place(x=1160, y=320)

    def fillPageLeaderboardsSeparators(self, pageLeaderboards):
        placeAndPlayerSeparator = Label(pageLeaderboards, text="|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n", bg=self.colorORT, fg = 'white', font=self.inputFont, compound=CENTER)
        placeAndPlayerSeparator.place(x=370, y=10)
        playerAndPointsSeparator = Label(pageLeaderboards, text="|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n", bg=self.colorORT, fg = 'white', font=self.inputFont, compound=CENTER)
        playerAndPointsSeparator.place(x=870, y=10)
        horizontalSeparator = Label(pageLeaderboards, text="- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -", bg=self.colorORT, fg = 'white', font=self.inputFont, compound=CENTER)
        horizontalSeparator.place(x=10, y=105)

    def fillLeaderboardsColumnPlace(self, pageLeaderboards, controller):
        print("PLACE")
        placeElement = Picture(['placeElement','png',212,90,130,10],0)
        placeElement.purpose = 'Words'
        placeElementPic = placeElement.generateLabel(pageLeaderboards)
        placeElementPic.place(x=placeElement.location[0],y=placeElement.location[1])
        self.columnPlaceLeaderboards.append(Label(pageLeaderboards, text=controller.currentLanguage.userPageContent[196][0], bg=self.colorORT, fg = 'white', font=self.titleFont, compound=CENTER))
        self.columnPlaceLeaderboards[0].place(x=150, y=150)
        self.columnPlaceLeaderboards.append(Label(pageLeaderboards, text=controller.currentLanguage.userPageContent[196][1], bg=self.colorORT, fg = 'white', font=self.titleFont, compound=CENTER))
        self.columnPlaceLeaderboards[1].place(x=150, y=220)
        self.columnPlaceLeaderboards.append(Label(pageLeaderboards, text=controller.currentLanguage.userPageContent[196][2], bg=self.colorORT, fg = 'white', font=self.titleFont, compound=CENTER))
        self.columnPlaceLeaderboards[2].place(x=150, y=290)
        self.columnPlaceLeaderboards.append(Label(pageLeaderboards, text=controller.currentLanguage.userPageContent[196][3], bg=self.colorORT, fg = 'white', font=self.titleFont, compound=CENTER))
        self.columnPlaceLeaderboards[3].place(x=150, y=360)
        self.columnPlaceLeaderboards.append(Label(pageLeaderboards, text=controller.currentLanguage.userPageContent[196][4], bg=self.colorORT, fg = 'white', font=self.titleFont, compound=CENTER))
        self.columnPlaceLeaderboards[4].place(x=150, y=430)

    def fillLeaderboardsColumnNameSurname(self, pageLeaderboards, controller):
        print("PERSON")
        nameSurnameElement = Picture(['nameSurnameElement','png',450,90,400,10],0)
        nameSurnameElement.purpose = 'Words'
        nameSurnameElementPic = nameSurnameElement.generateLabel(pageLeaderboards)
        nameSurnameElementPic.place(x=nameSurnameElement.location[0],y=nameSurnameElement.location[1])
        self.columnPlayerLeaderboards.append(Label(pageLeaderboards, text="NO PLAYER", bg=self.colorORT, fg = 'white', font=self.groupMessageFont, compound=CENTER))
        self.columnPlayerLeaderboards[0].place(x=500, y=160)
        self.columnPlayerLeaderboards.append(Label(pageLeaderboards, text="NO PLAYER", bg=self.colorORT, fg = 'white', font=self.groupMessageFont, compound=CENTER))
        self.columnPlayerLeaderboards[1].place(x=500, y=230)
        self.columnPlayerLeaderboards.append(Label(pageLeaderboards, text="NO PLAYER", bg=self.colorORT, fg = 'white', font=self.groupMessageFont, compound=CENTER))
        self.columnPlayerLeaderboards[2].place(x=500, y=300)
        self.columnPlayerLeaderboards.append(Label(pageLeaderboards, text="NO PLAYER", bg=self.colorORT, fg = 'white', font=self.groupMessageFont, compound=CENTER))
        self.columnPlayerLeaderboards[3].place(x=500, y=370)
        self.columnPlayerLeaderboards.append(Label(pageLeaderboards, text="NO PLAYER", bg=self.colorORT, fg = 'white', font=self.groupMessageFont, compound=CENTER))
        self.columnPlayerLeaderboards[4].place(x=500, y=440)

    def fillLeaderboardsColumnPoints(self, pageLeaderboards, controller):
        print("POINTS")
        pointsElement = Picture(['pointsElement','png',212,90,900,10],0)
        pointsElement.purpose = 'Words'
        pointsElementPic = pointsElement.generateLabel(pageLeaderboards)
        pointsElementPic.place(x=pointsElement.location[0],y=pointsElement.location[1])
        self.columnPointsLeaderboards.append(Label(pageLeaderboards, text="0", bg=self.colorORT, fg = 'white', font=self.titleFont, compound=CENTER))
        self.columnPointsLeaderboards[0].place(x=960, y=150)
        self.columnPointsLeaderboards.append(Label(pageLeaderboards, text="0", bg=self.colorORT, fg = 'white', font=self.titleFont, compound=CENTER))
        self.columnPointsLeaderboards[1].place(x=960, y=220)
        self.columnPointsLeaderboards.append(Label(pageLeaderboards, text="0", bg=self.colorORT, fg = 'white', font=self.titleFont, compound=CENTER))
        self.columnPointsLeaderboards[2].place(x=960, y=290)
        self.columnPointsLeaderboards.append(Label(pageLeaderboards, text="0", bg=self.colorORT, fg = 'white', font=self.titleFont, compound=CENTER))
        self.columnPointsLeaderboards[3].place(x=960, y=360)
        self.columnPointsLeaderboards.append(Label(pageLeaderboards, text="0", bg=self.colorORT, fg = 'white', font=self.titleFont, compound=CENTER))
        self.columnPointsLeaderboards[4].place(x=960, y=430)

    def setLeaderboardsContent(self, pageLeaderboards, controller):
        playersQuantity = 0
        if(self.gameIdentifier==0):
            controller.setImagesandSeparators(pageLeaderboards, 'scrambledElement', [100,250,10,10,100,250,10,310])
            while(playersQuantity<5):
                self.columnPlayerLeaderboards[playersQuantity].config(text=controller.application.gamesEntertainment.scrambledData.recordsUsersNames[playersQuantity])
                self.columnPointsLeaderboards[playersQuantity].config(text=controller.application.gamesEntertainment.scrambledData.currentRecord[playersQuantity])
                playersQuantity = playersQuantity + 1
        elif(self.gameIdentifier==1):
            controller.setImagesandSeparators(pageLeaderboards, 'hangmanElement', [100,250,10,10,100,250,10,310])
            while(playersQuantity<5):
                self.columnPlayerLeaderboards[playersQuantity].config(text=controller.application.gamesEntertainment.hangmanData.recordsUsersNames[playersQuantity])
                self.columnPointsLeaderboards[playersQuantity].config(text=controller.application.gamesEntertainment.hangmanData.currentRecord[playersQuantity])
                playersQuantity = playersQuantity + 1
        elif(self.gameIdentifier==2):
            triviaElement = Picture(['knowItAllElement','png',120,530,10,10],0)
            triviaElement.purpose = 'Words'
            triviaElementPic = triviaElement.generateLabel(pageLeaderboards)
            triviaElementPic.place(x=triviaElement.location[0],y=triviaElement.location[1])
            while(playersQuantity<5):
                self.columnPlayerLeaderboards[playersQuantity].config(text=controller.application.gamesEntertainment.triviaData.recordsUsersNames[playersQuantity])
                self.columnPointsLeaderboards[playersQuantity].config(text=controller.application.gamesEntertainment.triviaData.currentRecord[playersQuantity])
                playersQuantity = playersQuantity + 1

    def fillPageLeaderboards(self, pageLeaderboards, controller):
        self.fillPageLeaderboardsButtons(pageLeaderboards, controller)
        self.fillPageLeaderboardsSeparators(pageLeaderboards)
        self.fillLeaderboardsColumnPlace(pageLeaderboards, controller)
        self.fillLeaderboardsColumnNameSurname(pageLeaderboards, controller)
        self.fillLeaderboardsColumnPoints(pageLeaderboards, controller)
        self.setLeaderboardsContent(pageLeaderboards, controller)

    def fadeAway(self, controller):
        alpha = controller.attributes("-alpha")
        if alpha > 0:
            alpha = alpha - 0.1
            controller.attributes("-alpha", alpha)
            self.after(50, lambda:self.fadeAway(controller))
        else:
            controller.destroy()

    def onClosing(self, controller):
        if messagebox.askokcancel(controller.currentLanguage.adminPageContent[21], controller.currentLanguage.adminPageContent[20]):
            controller.application.systemData.informations[4].updateInformationTimesVerificationsDone([self.hasCheckedConnection, self.hasCalibratedSensorLow and self.hasCalibratedSensorHigh and self.hasCalibratedSensorMiddle])
            #controller.application.updateFermentationVerificationsData()
            controller.application.saveSmartData("")
            self.fadeAway(controller)

    def animateWords(self):
        self.version = ""
        self.version = self.versionInfo['text'][(len(self.versionInfo['text'])-1):len(self.versionInfo['text'])]
        for position in range(0,len(self.versionInfo['text'])-1):
            self.version = self.version + self.versionInfo['text'][position:position+1]
        self.versionInfo['text'] = self.version
        self.after(100,lambda:self.animateWords())

    def setTabs(self, controller):
        self.pageBeginFermentation = Frame(self.nb)
        self.nb.add(self.pageBeginFermentation, text=controller.currentLanguage.userPageContent[4])
        controller.setBackgroundOfTab(self.pageBeginFermentation)
        self.fillPageBeginFermentation(self.pageBeginFermentation, controller)
        self.pagePreparation= Frame(self.nb)
        self.nb.add(self.pagePreparation, text=controller.currentLanguage.userPageContent[139])
        controller.setBackgroundOfTab(self.pagePreparation)
        self.fillPagePreparation(self.pagePreparation, controller)
        self.pageReserves = Frame(self.nb)
        self.nb.add(self.pageReserves, text=controller.currentLanguage.userPageContent[5])
        controller.setBackgroundOfTab(self.pageReserves)
        self.fillPageReserves(self.pageReserves, controller)
        self.pagePlatform = Frame(self.nb)
        self.nb.add(self.pagePlatform, text=controller.currentLanguage.userPageContent[7])
        controller.setBackgroundOfTab(self.pagePlatform)
        self.fillPagePlatform(self.pagePlatform, controller)
        self.pageProfile = Frame(self.nb)
        self.nb.add(self.pageProfile, text=controller.currentLanguage.userPageContent[8])
        controller.setBackgroundOfTab(self.pageProfile)
        self.fillPageProfile(self.pageProfile, controller)
        self.pageContact = Frame(self.nb)
        self.nb.add(self.pageContact, text=controller.currentLanguage.userPageContent[9])
        controller.setBackgroundOfTab(self.pageContact)
        self.fillPageContact(self.pageContact, controller)
        self.pageLeaderboards = Frame(self.nb)
        self.nb.add(self.pageLeaderboards, text=controller.currentLanguage.userPageContent[193])
        controller.setBackgroundOfTab(self.pageLeaderboards)
        self.fillPageLeaderboards(self.pageLeaderboards, controller)

    def __init__(self, parent, controller):

        Frame.__init__(self, parent)
        self.setFonts()
        self.setVariables()
        self.setLists()
        self.placeStaticPictures(controller)

        rows = 0
        while rows < 50:
            self.rowconfigure(rows, weight=1)
            self.columnconfigure(rows, weight=1)
            rows = rows + 1

        self.nb = ttk.Notebook(self)
        self.nb.grid(row=10, column=0, columnspan=500, rowspan=490, sticky='NESW')

        self.setTabs(controller)
        self.setHelpBar(controller)
        self.loadingTitle = Label(self, text = "... LOADING ...", fg = 'white', relief='groove', bg = self.colorORT, font = self.bigTitleFont, width=12, height=2)
        #self.animateWords()
