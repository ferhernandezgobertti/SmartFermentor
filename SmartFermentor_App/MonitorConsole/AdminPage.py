import sys, time, gi
gi.require_version('Wnck', '3.0')
from gi.repository import Wnck
from tkinter import *
from tkinter import ttk, messagebox
import pickle, tkinter.font
from PIL import Image, ImageTk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import matplotlib.ticker as ticker
from MonitorConsole.Picture import Picture
from Domain.Student import Student
from Domain.Professor import Professor
from Domain.User import User
from Domain.Version import Version
from MonitorConsole.OriginalLanguage import OriginalLanguage
from MonitorConsole.SpanishLanguage import SpanishLanguage
from MonitorConsole.PortugueseLanguage import PortugueseLanguage
from MonitorConsole.GermanLanguage import GermanLanguage

class AdminPage(Frame):

    def setFonts(self):
        self.colorORT = "#085454"
        self.buttonFontSmaller = tkinter.font.Font(family = 'Helvetica', size = 12, weight = 'bold')
        self.buttonFont = tkinter.font.Font(family = 'Helvetica', size = 14, weight = 'bold')
        self.titleFont = tkinter.font.Font(family = 'Helvetica', size = 20, weight = 'bold')
        self.inputFont = tkinter.font.Font(family = 'Times', size = 16)
        self.infoFont = tkinter.font.Font(family = 'Times', size = 12)
        self.groupMessageFont = tkinter.font.Font(family = 'Times New Roman', size = 14, weight = 'bold')
        self.listElementFont = tkinter.font.Font(family = 'Times', size = 10)
        self.bodyMessageFont = tkinter.font.Font(family = 'Times New Roman', size = 12, weight = 'bold')
        self.subtitleFont = tkinter.font.Font(family = 'Comic Sans', size = 16, weight = 'bold')

    def setVariables(self):
        self.logOutImage = PhotoImage(file="Images/Logos/logOutLogo.gif")
        self.previousAdminUsernumber = ""
        self.previousAdminPassword = ""
        self.pageOfListProfessors = 0
        self.pageOfListStudents = 0
        self.pageOfListFermentations = 0
        self.pageOfListProfessorsToEdit = 0
        self.pageOfListStudentsToEdit = 0
        self.pageOfListVersions = 0
        self.userIndex = 0
        self.lastIndexSelectedListProfessor = 0
        self.lastIndexSelectedListStudent = 0
        self.usersPerPage = 28
        self.helpDisplayed = False
        self.extensionX = 466
        self.extensionY = 268

    def setLists(self):
        self.userInput = []
        self.professorEditionTitles = []
        self.studentEditionTitles = []
        self.userInputEditProfessor = []
        self.userInputEditStudent = []
        self.userProfession = [] # [ Professor, Student ]
        self.userProfession.append(IntVar())
        self.userProfession.append(IntVar())
        self.userBirthDate = []
        self.professorData = []
        self.professorDataEdition = []
        self.studentData = []
        self.studentDataEdition = []
        self.professorEdit = []
        self.studentEdit = []
        self.adminDataEdition = []
        self.userInfo = []
        self.professorInfo = []
        self.studentInfo = []
        self.pageNumberOfFermentationList = []
        self.pageNumberOfProfessorsList = []
        self.pageNumberOfStudentsList = []
        self.pageNumberOfProfessorsToEditList = []
        self.pageNumberOfStudentsToEditList = []
        self.pageNumberOfVersionsList = []

    def setInformationGraphics(self):
        self.systemUsersInformationFigure = Figure(figsize=(6.7,5.5), dpi=100, facecolor=self.colorORT, edgecolor='white')
        self.systemUsersInformationGraphic = self.systemUsersInformationFigure.add_subplot(111)
        self.systemFermentationsInformationFigure = Figure(figsize=(6.7,5.5), dpi=100, facecolor=self.colorORT, edgecolor='white')
        self.systemFermentationsInformationGraphic = self.systemFermentationsInformationFigure.add_subplot(111)
        self.systemControlsInformationFigure = Figure(figsize=(4.5,4.5), dpi=100, facecolor=self.colorORT, edgecolor='white')
        self.systemControlsInformationGraphic = self.systemControlsInformationFigure.add_subplot(111)
        self.systemVerificationInformationFigure = Figure(figsize=(4.5,4.5), dpi=100, facecolor=self.colorORT, edgecolor='white')
        self.systemVerificationInformationGraphic = self.systemVerificationInformationFigure.add_subplot(111)
        self.systemGamesInformationFigure = Figure(figsize=(4.5,4.5), dpi=100, facecolor=self.colorORT, edgecolor='white')
        self.systemGamesInformationGraphic = self.systemGamesInformationFigure.add_subplot(111)

    def placeStaticPictures(self, controller):
        controller.setHeaderSmart(self, 'SmartAdministrator', self.logOutImage)
        self.adminInformation = Label(self, text=controller.currentLanguage.adminPageContent[2] + controller.application.admin.registrationDate + " :::: "+ controller.currentLanguage.adminPageContent[3] + controller.application.admin.lastEntryDate, font=self.infoFont, fg = 'white', bg = self.colorORT)
        self.adminInformation.place(x=845, y=120)

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
        #self.minimizeSystem = Button(self, text=controller.currentLanguage.homePageContent[17], relief = RAISED, fg='white', bg = 'blue', font=self.bodyMessageFont, compound=CENTER, height = 1, width = 10)
        #self.minimizeSystem.place(x=1155, y=470+self.extensionY)
        self.closeSystem = Button(self, text=controller.currentLanguage.adminPageContent[22], command=lambda:self.onClosing(controller), relief = RAISED, fg='white', bg = 'red', font=self.bodyMessageFont, compound=CENTER, height = 1, width = 12)
        self.closeSystem.place(x=1252, y=470+self.extensionY)
        self.helpSystem = Button(self, text=controller.currentLanguage.adminPageContent[23], command=lambda:self.showHelp(), relief = RAISED, fg='white', bg = 'dark green', font=self.bodyMessageFont, compound=CENTER, height = 1, width = 15)
        self.helpSystem.place(x=0, y=470+self.extensionY)
        self.canvas = Canvas(self, background="white", width= 890+self.extensionX, height= 315+2+self.extensionY, highlightthickness=5, highlightbackground=self.colorORT)
        self.canvasConfiguration(controller)

    def configureCanvas(self, controller):
        self.helpBarTitle = Label(self.canvas, text=controller.currentLanguage.adminPageContent[0], font=self.subtitleFont, fg=self.colorORT, bg='white')
        self.helpBarTitle.place(x=20,y=20)
        self.helpBarBody = Label(self.canvas, text=controller.currentLanguage.adminPageContent[1], font=self.groupMessageFont, fg=self.colorORT, bg='white', justify=LEFT)
        self.helpBarBody.place(x=80,y=60)

    def refreshTabTitleInformation(self, controller):
        self.nb.tab(self.pageUsers, text = controller.currentLanguage.adminPageContent[4])
        self.nb.tab(self.pageNewUser, text = controller.currentLanguage.adminPageContent[5])
        self.nb.tab(self.pageEditProfessor, text = controller.currentLanguage.adminPageContent[6])
        self.nb.tab(self.pageEditStudent, text = controller.currentLanguage.adminPageContent[7])
        self.nb.tab(self.pageUserInfo, text = controller.currentLanguage.adminPageContent[8])
        self.nb.tab(self.pagePlatformInfo, text = controller.currentLanguage.adminPageContent[9])
        self.nb.tab(self.pageStatus, text=controller.currentLanguage.adminPageContent[115])
        self.nb.tab(self.pageStatistics, text = controller.currentLanguage.adminPageContent[10])
        self.nb.tab(self.pageSettings, text = controller.currentLanguage.adminPageContent[11])
        self.nb.tab(self.pageVersion, text=controller.currentLanguage.adminPageContent[119])

    def refreshPageUsersContent(self, controller):
        controller.fillProfessorsList(self.professorsList, self.pageOfListProfessors)
        controller.fillStudentsList(self.studentsList, self.pageOfListStudents)
        self.removeProfessorOption['text'] = controller.currentLanguage.adminPageContent[16]
        self.removeStudentOption['text'] = controller.currentLanguage.adminPageContent[17]
        self.orderProfessorOption['text'] = controller.currentLanguage.adminPageContent[163]
        self.orderStudentOption['text'] = controller.currentLanguage.adminPageContent[163]
        
    def refreshPageNewUserContent(self, controller):
        self.usernumberTitle['text'] = controller.currentLanguage.adminPageContent[25]
        self.passwordTitle['text'] = controller.currentLanguage.adminPageContent[26]
        self.nameTitle['text'] = controller.currentLanguage.adminPageContent[27]
        self.surnameTitle['text'] = controller.currentLanguage.adminPageContent[28]
        self.emailTitle['text'] = controller.currentLanguage.adminPageContent[29]
        self.birthdateTitle['text'] = controller.currentLanguage.adminPageContent[30]
        self.telephoneTitle['text'] = controller.currentLanguage.adminPageContent[31]
        self.addressTitle['text'] = controller.currentLanguage.adminPageContent[32]
        self.idNumberTitle['text'] = controller.currentLanguage.adminPageContent[33]
        self.usernumberCondition['text'] = controller.currentLanguage.adminPageContent[35]
        self.passwordCondition1['text'] = controller.currentLanguage.adminPageContent[36]
        self.passwordCondition2['text'] = controller.currentLanguage.adminPageContent[37]
        self.nameCondition1['text'] = controller.currentLanguage.adminPageContent[38]
        self.nameCondition2['text'] = controller.currentLanguage.adminPageContent[39]
        self.surnameCondition1['text'] = controller.currentLanguage.adminPageContent[40]
        self.surnameCondition2['text'] = controller.currentLanguage.adminPageContent[41]
        self.addressCondition['text'] = controller.currentLanguage.adminPageContent[42]
        self.telephoneCondition['text'] = controller.currentLanguage.adminPageContent[43]
        self.streetIndicator['text'] = controller.currentLanguage.adminPageContent[34]
        self.userBirthDate[1].config(values=controller.currentLanguage.adminPageContent[44])
        self.professorData[0].config(values=controller.currentLanguage.adminPageContent[45])
        self.professorData[1].config(values=controller.currentLanguage.adminPageContent[46])
        self.studentData[0].config(values=controller.currentLanguage.adminPageContent[47])
        self.addProfessorOption['text'] = controller.currentLanguage.adminPageContent[55]
        self.addStudentOption['text'] = controller.currentLanguage.adminPageContent[56]

    def refreshPageEditProfessorContent(self, controller):
        controller.fillProfessorsList(self.professorsListEdition, self.pageOfListProfessorsToEdit)
        self.professorEditionTitles[0]['text'] = controller.currentLanguage.adminPageContent[26]
        self.professorEditionTitles[1]['text'] = controller.currentLanguage.adminPageContent[29]
        self.professorEditionTitles[2]['text'] = controller.currentLanguage.adminPageContent[31]
        self.professorEditionTitles[3]['text'] = controller.currentLanguage.adminPageContent[32]
        self.professorEditionTitles[4]['text'] = controller.currentLanguage.adminPageContent[57]
        self.professorDataEdition[0].config(values=controller.currentLanguage.adminPageContent[45])
        self.professorDataEdition[1].config(values=controller.currentLanguage.adminPageContent[46])
        self.modifyProfessorOption['text'] = controller.currentLanguage.adminPageContent[58]
        self.streetIndicatorEdition['text'] = controller.currentLanguage.adminPageContent[34]
        self.orderProfessorEditionOption['text'] = controller.currentLanguage.adminPageContent[163]

    def refreshPageEditStudentContent(self, controller):
        controller.fillStudentsList(self.studentsListEdition, self.pageOfListStudentsToEdit)
        self.studentEditionTitles[0]['text'] = controller.currentLanguage.adminPageContent[26]
        self.studentEditionTitles[1]['text'] = controller.currentLanguage.adminPageContent[29]
        self.studentEditionTitles[2]['text'] = controller.currentLanguage.adminPageContent[31]
        self.studentEditionTitles[3]['text'] = controller.currentLanguage.adminPageContent[32]
        self.studentEditionTitles[4]['text'] = controller.currentLanguage.adminPageContent[57]
        self.modifyStudentOption['text'] = controller.currentLanguage.adminPageContent[62]
        self.orderStudentEditionOption['text'] = controller.currentLanguage.adminPageContent[163]

    def refreshPageInformationContent(self, controller):
        self.userTitle['text'] = controller.currentLanguage.adminPageContent[63]
        self.previousUserTitle['text'] = controller.currentLanguage.adminPageContent[64]
        self.nextUserTitle['text'] = controller.currentLanguage.adminPageContent[65]
        self.userTitlePrevious['text'] = controller.currentLanguage.adminPageContent[66]
        self.userTitleNext['text'] = controller.currentLanguage.adminPageContent[66]
        if(len(controller.application.listProfessors.professors)>0):
            self.updateWithProfessorInformation(self.pageUserInfo, controller.application.listProfessors.professors[self.userIndex], controller)
        if(len(controller.application.listStudents.students)>0):
            self.updateWithStudentInformation(self.pageUserInfo, controller.application.listStudents.students[self.userIndex-len(controller.application.listProfessors.professors)], controller)

    def refreshPagePlatformContent(self, controller):
        self.fillFermentationsList(controller)
        self.descriptionTitle['text'] = controller.currentLanguage.adminPageContent[76]
        self.notificationTitle['text'] = controller.currentLanguage.adminPageContent[77]
        self.sendProfessorNotesOption['text'] = controller.currentLanguage.adminPageContent[87]
        self.sendStudentNotesOption['text'] = controller.currentLanguage.adminPageContent[88]

    def refreshPageSettingsContent(self, controller):
        self.removeFermentationOption['text'] = controller.currentLanguage.adminPageContent[89]
        self.updateAdminInfoOption['text'] = controller.currentLanguage.adminPageContent[102]
        self.eraseProfessorsOption['text'] = controller.currentLanguage.adminPageContent[103]
        self.eraseStudentsOption['text'] = controller.currentLanguage.adminPageContent[104]
        self.eraseFermentationsOption['text'] = controller.currentLanguage.adminPageContent[105]
        self.currentIdTitle['text'] = controller.currentLanguage.adminPageContent[106]
        self.newIdTitle['text'] = controller.currentLanguage.adminPageContent[107]
        self.currentPasswordTitle['text'] = controller.currentLanguage.adminPageContent[108]
        self.newPasswordTitle['text'] = controller.currentLanguage.adminPageContent[109]
        self.confirmPasswordTitle['text'] = controller.currentLanguage.adminPageContent[110]
        self.platformEmailTitle['text'] = controller.currentLanguage.adminPageContent[111]
        self.platformEmailPasswordTitle['text'] = controller.currentLanguage.adminPageContent[112]
        self.usersAddedTitle['text'] = controller.currentLanguage.adminPageContent[113]
        self.usersDeletedTitle['text'] = controller.currentLanguage.adminPageContent[114]

    def refreshPageStatisticsContent(self, controller):
        self.systemUsersInformationGraphic.set_xlabel(controller.currentLanguage.adminPageContent[143], color='white')
        self.systemUsersInformationGraphic.set_ylabel(controller.currentLanguage.adminPageContent[144], color='white')
        self.systemUsersInformationGraphic.set_title(controller.currentLanguage.adminPageContent[145], color='white')
        self.systemFermentationsInformationGraphic.set_xlabel(controller.currentLanguage.adminPageContent[143], color='white')
        self.systemFermentationsInformationGraphic.set_ylabel(controller.currentLanguage.adminPageContent[146], color='white')
        self.systemFermentationsInformationGraphic.set_xticklabels(controller.currentLanguage.adminPageContent[147], color='white')
        self.systemFermentationsInformationGraphic.set_title(controller.currentLanguage.adminPageContent[148], color='white')

    def refreshPageVersionContent(self, controller):
        self.velocityVersionTitle['text'] = controller.currentLanguage.userPageContent[143]
        self.temperatureVersionTitle['text'] = controller.currentLanguage.userPageContent[144]
        self.potentialVersionTitle['text'] = controller.currentLanguage.userPageContent[145]
        self.velocityVersion['text'] = controller.currentLanguage.userPageContent[147]
        self.temperatureVersion['text'] = controller.currentLanguage.userPageContent[147]
        self.potentialVersion['text'] = controller.currentLanguage.userPageContent[147]
        self.velocityVersionOption['text'] = controller.currentLanguage.userPageContent[146]
        self.temperatureVersionOption['text'] = controller.currentLanguage.userPageContent[146]
        self.potentialVersionOption['text'] = controller.currentLanguage.userPageContent[146]
        self.velocityVersionCommentaryOption['text'] = controller.currentLanguage.adminPageContent[116]
        self.temperatureVersionCommentaryOption['text'] = controller.currentLanguage.adminPageContent[116]
        self.potentialVersionCommentaryOption['text'] = controller.currentLanguage.adminPageContent[116]
        self.clearVersionsOption['text'] = controller.currentLanguage.adminPageContent[120]

    def refreshTextContent(self, controller):
        self.refreshTabTitleInformation(controller)
        self.helpBarTitle['text'] = controller.currentLanguage.adminPageContent[0]
        self.helpBarBody['text'] = controller.currentLanguage.adminPageContent[1]
        self.adminInformation['text'] = controller.currentLanguage.adminPageContent[2] + controller.application.admin.registrationDate + " :::: "+ controller.currentLanguage.adminPageContent[3] + controller.application.admin.lastEntryDate
        self.versionInfo['text'] = controller.currentLanguage.adminPageContent[12]
        self.minimizeSystem['text'] = controller.currentLanguage.adminPageContent[22]
        self.closeSystem['text'] = controller.currentLanguage.adminPageContent[23]
        self.helpSystem['text'] = controller.currentLanguage.adminPageContent[24]

        self.refreshPageUsersContent(controller)
        self.refreshPageNewUserContent(controller)
        self.refreshPageEditProfessorContent(controller)
        self.refreshPageEditStudentContent(controller)
        self.refreshPageInformationContent(controller)
        self.refreshPagePlatformContent(controller)
        self.refreshPageSettingsContent(controller)
        self.refreshPageStatisticsContent(controller)
        self.refreshPageVersionContent(controller)

    def changeLanguage(self, language, controller):
        if(language=='GERMAN'):
            controller.currentLanguage = GermanLanguage()
            self.adminInformation.place(x=845, y=120)
        if(language=='PORTUGUESE'):
            controller.currentLanguage = PortugueseLanguage()
            self.adminInformation.place(x=860, y=120)
        if(language=='SPANISH'):
            controller.currentLanguage = SpanishLanguage()
            self.adminInformation.place(x=835, y=120)
        if(language=='ENGLISH'):
            controller.currentLanguage = OriginalLanguage()
            self.adminInformation.place(x=845, y=120)
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
        ortLogo = Picture(['ORTLogo','png',240,100,100+self.extensionX,220+self.extensionY],0)
        ortLogo.purpose = 'Logos'
        oneImage = Image.open(ortLogo.getCompleteFilename()).resize((ortLogo.dimensions[0],ortLogo.dimensions[1]), Image.ANTIALIAS)
        oneImageRendered = ImageTk.PhotoImage(oneImage.rotate(ortLogo.orientation))
        ortLogoPic = Label(self.canvas, image=oneImageRendered, borderwidth=0, highlightthickness=0)
        ortLogoPic.image = oneImageRendered
        ortLogoPic.place(x=ortLogo.location[0],y=ortLogo.location[1])
        self.configureCanvas(controller)
        self.setLanguages(controller)

    def removeProfessor(self, controller):
        if(len(self.professorsList.curselection())>0):
            removeProfessorBodyMail = "\n\n"+controller.application.getDayTimeMomentMessage(controller.currentLanguage.adminPageContent[162])+", "+controller.currentLanguage.adminPageContent[133]+controller.application.listProfessors.professors[int(self.professorsList.curselection()[0])+self.pageOfListProfessor*self.usersPerPage].getCompleteNameSurname()+":\n\n    "+controller.currentLanguage.adminPageContent[131]
            controller.application.sendEmail([controller.application.listProfessors.professors[int(self.professorsList.curselection()[0])+self.pageOfListProfessor*self.usersPerPage].email], [controller.currentLanguage.adminPageContent[132], 'Images/MailContent/erasedFromSystemMail.png', removeProfessorBodyMail, "IMAGE"])
            controller.application.listProfessors.removeProfessor(int(self.professorsList.curselection()[0])+self.pageOfListProfessor*self.usersPerPage)
            self.professorsList.delete(int(self.professorsList.curselection()[0])+self.pageOfListProfessor*self.usersPerPage)
        else:
            messagebox.showwarning(controller.currentLanguage.adminPageContent[15], controller.currentLanguage.adminPageContent[13])

    def removeStudent(self, controller):
        if(len(self.studentsList.curselection())>0):
            removeStudentBodyMail = "\n\n"+controller.currentLanguage.adminPageContent[134]+controller.application.listStudents.students[int(self.studentsList.curselection()[0])+self.pageOfListStudent*self.usersPerPage].getCompleteNameSurname()+",\n\n    "+controller.currentLanguage.adminPageContent[131]
            controller.application.sendEmail([controller.application.listStudents.students[int(self.studentsList.curselection()[0])+self.pageOfListStudent*self.usersPerPage].email], [controller.currentLanguage.adminPageContent[132], 'Images/MailContent/erasedFromSystemMail.png', removeStudentBodyMail, "IMAGE"])
            controller.application.listStudents.removeStudent(int(self.studentsList.curselection()[0])+self.pageOfListStudent*self.usersPerPage)
            self.studentsList.delete(int(self.studentsList.curselection()[0])+self.pageOfListStudent*self.usersPerPage)
        else:
            messagebox.showwarning(controller.currentLanguage.adminPageContent[15], controller.currentLanguage.adminPageContent[14])

    def showPageOfListProfessors(self, controller, numberOfPage):
        for eachButton in self.pageNumberOfProfessorsList:
            eachButton['bg']='white'
        self.pageOfListProfessors = numberOfPage-1
        self.pageNumberOfProfessorsList[self.pageOfListProfessors]['bg'] = 'yellow'
        controller.fillProfessorsList(self.professorsList, self.pageOfListProfessors)

    def showPageOfListStudents(self, controller, numberOfPage):
        for eachButton in self.pageNumberOfStudentsList:
            eachButton['bg']='white'
        self.pageOfListStudents = numberOfPage-1
        self.pageNumberOfStudentsList[self.pageOfListStudents]['bg'] = 'yellow'
        controller.fillStudentsList(self.studentsList, self.pageOfListStudents)

    def orderProfessors(self, controller):
        if(len(controller.application.listProfessors.professors)>0):
            controller.application.listProfessors.orderList()
            controller.fillProfessorsList(self.professorsList, self.pageOfListProfessors)
            self.configureListProfessorsToEdit(self.pageEditProfessor, controller)

    def orderStudents(self, controller):
        if(len(controller.application.listStudents.students)>0):
            controller.application.listStudents.orderList()
            controller.fillStudentsList(self.studentsList, self.pageOfListStudents)
            self.configurePageEditStudentsList(self.pageEditStudent, controller)

    def configurePageUsersButton(self, pageUsers, controller):
        self.removeProfessorOption = Button(pageUsers, text=controller.currentLanguage.adminPageContent[16], command = lambda:self.removeProfessor(controller), relief = SUNKEN, fg='white', bg = 'dark blue', font=self.buttonFont, compound=CENTER, height = 2, width = 17)
        self.removeProfessorOption.place(x=120, y=475)
        self.orderProfessorOption = Button(pageUsers, text=controller.currentLanguage.adminPageContent[163], command = lambda:self.orderProfessors(controller), relief = SUNKEN, fg='white', bg = 'red', font=self.buttonFont, compound=CENTER, height = 2, width = 7)
        self.orderProfessorOption.place(x=340, y=475)
        self.removeStudentOption = Button(pageUsers, text=controller.currentLanguage.adminPageContent[17], command = lambda:self.removeStudent(controller), relief = SUNKEN, fg='white', bg = 'dark green', font=self.buttonFont, compound=CENTER, height = 2, width = 17)
        self.removeStudentOption.place(x=750, y=475)
        self.orderStudentOption = Button(pageUsers, text=controller.currentLanguage.adminPageContent[163], command = lambda:self.orderStudents(controller), relief = SUNKEN, fg='white', bg = 'red', font=self.buttonFont, compound=CENTER, height = 2, width = 7)
        self.orderStudentOption.place(x=970, y=475)

        self.pageNumberOfProfessorsList.append(Button(pageUsers, text="1", relief = SUNKEN, fg=self.colorORT, bg = 'yellow', font=self.buttonFont, compound=CENTER, height = 2, width = 4, command=lambda:self.showPageOfListProfessors(controller, 1)))
        self.pageNumberOfProfessorsList[0].place(x=440, y=475)
        self.pageNumberOfProfessorsList.append(Button(pageUsers, text="2", relief = SUNKEN, fg=self.colorORT, bg = 'white', font=self.buttonFont, compound=CENTER, height = 2, width = 4, command=lambda:self.showPageOfListProfessors(controller, 2)))
        self.pageNumberOfProfessorsList[1].place(x=500, y=475)
        self.pageNumberOfProfessorsList.append(Button(pageUsers, text="3", relief = SUNKEN, fg=self.colorORT, bg = 'white', font=self.buttonFont, compound=CENTER, height = 2, width = 4, command=lambda:self.showPageOfListProfessors(controller, 3)))
        self.pageNumberOfProfessorsList[2].place(x=560, y=475)
        self.pageNumberOfStudentsList.append(Button(pageUsers, text="1", relief = SUNKEN, fg=self.colorORT, bg = 'yellow', font=self.buttonFont, compound=CENTER, height = 2, width = 4, command=lambda:self.showPageOfListStudents(controller, 1)))
        self.pageNumberOfStudentsList[0].place(x=1070, y=475)
        self.pageNumberOfStudentsList.append(Button(pageUsers, text="2", relief = SUNKEN, fg=self.colorORT, bg = 'white', font=self.buttonFont, compound=CENTER, height = 2, width = 4, command=lambda:self.showPageOfListStudents(controller, 2)))
        self.pageNumberOfStudentsList[1].place(x=1130, y=475)
        self.pageNumberOfStudentsList.append(Button(pageUsers, text="3", relief = SUNKEN, fg=self.colorORT, bg = 'white', font=self.buttonFont, compound=CENTER, height = 2, width = 4, command=lambda:self.showPageOfListStudents(controller, 3)))
        self.pageNumberOfStudentsList[2].place(x=1190, y=475)

    def configurePageUsersLists(self, pageUsers, controller):
        separatorLists = Picture(['listsSeparator','png',100,540,640,5],0)
        separatorLists.purpose = 'Separators'
        separatorListsPic = separatorLists.generateLabel(pageUsers)
        separatorListsPic.place(x=separatorLists.location[0],y=separatorLists.location[1])

        self.professorsList = Listbox(pageUsers, width=83, height=28, font=self.listElementFont)
        self.professorsList.place(x=120,y=10)
        controller.fillProfessorsList(self.professorsList, self.pageOfListProfessors)
        self.studentsList = Listbox(pageUsers, width=83, height=28, font=self.listElementFont)#, xscrollcommand=self.xScroll.set,yscrollcommand=self.yScroll.set)#, sticky=N+S+E+W)
        self.studentsList.place(x=750,y=10)
        controller.fillStudentsList(self.studentsList, self.pageOfListStudents)

    def fillPageUsers(self, pageUsers, controller):
        controller.setImagesandSeparators(pageUsers, 'professorsElement', [115,280,10,0,115,280,10,290])
        controller.setImagesandSeparators(pageUsers, 'studentsElement', [115,280,1260,0,115,280,1260,290])
        self.configurePageUsersLists(pageUsers, controller)
        self.configurePageUsersButton(pageUsers, controller)

    def fillPageNewUserTitles(self, pageNewUser, controller):
        self.usernumberTitle = Label(pageNewUser, text=controller.currentLanguage.adminPageContent[25], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.usernumberTitle.place(x=20, y=30)
        self.passwordTitle = Label(pageNewUser, text=controller.currentLanguage.adminPageContent[26], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.passwordTitle.place(x=20, y=120)
        self.nameTitle = Label(pageNewUser, text=controller.currentLanguage.adminPageContent[27], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.nameTitle.place(x=20, y=230)
        self.surnameTitle = Label(pageNewUser, text=controller.currentLanguage.adminPageContent[28], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.surnameTitle.place(x=20, y=340)
        self.emailTitle = Label(pageNewUser, text=controller.currentLanguage.adminPageContent[29], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.emailTitle.place(x=20, y=450)
        self.birthdateTitle = Label(pageNewUser, text=controller.currentLanguage.adminPageContent[30], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.birthdateTitle.place(x=800, y=30)
        self.telephoneTitle = Label(pageNewUser, text=controller.currentLanguage.adminPageContent[31], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.telephoneTitle.place(x=800, y=120)
        self.addressTitle = Label(pageNewUser, text=controller.currentLanguage.adminPageContent[32], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.addressTitle.place(x=800, y=230)
        self.idNumberTitle = Label(pageNewUser, text=controller.currentLanguage.adminPageContent[33], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.idNumberTitle.place(x=800, y=340)

    def fillPageNewUserIndicators(self, pageNewUser, controller):
        self.streetIndicator = Label(pageNewUser, text=controller.currentLanguage.adminPageContent[34], font=self.bodyMessageFont, fg = 'white', bg = self.colorORT)
        self.streetIndicator.place(x=1060, y=262)
        doorNumberIndicator = Label(pageNewUser, text="Num", font=self.bodyMessageFont, fg = 'white', bg = self.colorORT)
        doorNumberIndicator.place(x=1170, y=262)
        telephoneInput = Label(pageNewUser, text="+598", font=self.groupMessageFont, width=5, fg='grey', bg='white')
        telephoneInput.place(x=995, y=128)
        birthDayIndicator = Label(pageNewUser, text="DD  /", font=self.groupMessageFont, fg = 'white', bg = self.colorORT)
        birthDayIndicator.place(x=1000, y=50)
        birthMonthIndicator = Label(pageNewUser, text="MM  /", font=self.groupMessageFont, fg = 'white', bg = self.colorORT)
        birthMonthIndicator.place(x=1080, y=50)
        birthYearIndicator = Label(pageNewUser, text="YY", font=self.groupMessageFont, fg = 'white', bg = self.colorORT)
        birthYearIndicator.place(x=1170, y=50)

    def fillPageNewUserEntries(self, pageNewUser):
        self.userInput.append(Entry(pageNewUser, font=self.inputFont, width=16, justify='center')) # usernumberInput
        self.userInput[0].place(x=225, y=38)
        self.userInput.append(Entry(pageNewUser, font=self.inputFont, width=20, justify='center')) # passwordInput
        self.userInput[1].place(x=182, y=128)
        self.userInput.append(Entry(pageNewUser, font=self.inputFont, width=20, justify='center'))  # nameInput
        self.userInput[2].place(x=182, y=238)
        self.userInput.append(Entry(pageNewUser, font=self.inputFont, width=20, justify='center')) # surnameInput
        self.userInput[3].place(x=182, y=348)
        self.userInput.append(Entry(pageNewUser, font=self.inputFont, width=20, justify='center')) # emailInput
        self.userInput[4].place(x=182, y=458)
        self.userInput.append(Entry(pageNewUser, font=self.inputFont, width=15, justify='center')) # telephoneInput
        self.userInput[5].place(x=1060, y=128)
        self.userInput.append(Entry(pageNewUser, font=self.inputFont, width=15, justify='center')) # streetInput
        self.userInput[6].place(x=1002, y=233)
        self.userInput.append(Entry(pageNewUser, font=self.inputFont, width=7, justify='center')) # doorNumberInput
        self.userInput[7].place(x=1147, y=233)
        self.userInput.append(Entry(pageNewUser, font=self.inputFont, width=20, justify='center')) # IdNumberInput
        self.userInput[8].place(x=1005, y=348)

    def fillPageNewUserHelpers(self, pageNewUser, controller):
        self.fillPageNewUserExamples(pageNewUser)
        self.fillPageNewUserConditions(pageNewUser, controller)

    def fillPageNewUserExamples(self, pageNewUser):
        usernumberExample = Label(pageNewUser, text="( i.e. 173631 )", font=self.infoFont, fg = 'white', bg = self.colorORT)
        usernumberExample.place(x=265, y=70)
        passwordExample = Label(pageNewUser, text="( i.e. Ferment.18 )", font=self.infoFont, fg = 'white', bg = self.colorORT)
        passwordExample.place(x=190, y=160)
        nameExample = Label(pageNewUser, text="( i.e. Carlos )", font=self.infoFont, fg = 'white', bg = self.colorORT)
        nameExample.place(x=225, y=270)
        surnameExample = Label(pageNewUser, text="( i.e. Sanguinetti )", font=self.infoFont, fg = 'white', bg = self.colorORT)
        surnameExample.place(x=225, y=380)
        emailExample = Label(pageNewUser, text="( i.e. ortUniversity@ort.edu.uy )", font=self.infoFont, fg = 'white', bg = self.colorORT)
        emailExample.place(x=175, y=490)
        addressExample = Label(pageNewUser, text="( i.e. Cuareim 1450 )", font=self.infoFont, fg = 'white', bg = self.colorORT)
        addressExample.place(x=1075, y=290)
        telephoneExample = Label(pageNewUser, text="( i.e. 98742547 )", font=self.infoFont, fg = 'white', bg = self.colorORT)
        telephoneExample.place(x=1075, y=160)
        idNumberExample = Label(pageNewUser, text="( i.e. 232.898-5 || 8.999.832-2 )", font=self.infoFont, fg = 'white', bg = self.colorORT)
        idNumberExample.place(x=1015, y=380)

    def fillPageNewUserConditions(self, pageNewUser, controller):
        self.usernumberCondition = Label(pageNewUser, text=controller.currentLanguage.adminPageContent[35], font=self.infoFont, fg = 'white', bg = self.colorORT)
        self.usernumberCondition.place(x=180, y=90)
        self.passwordCondition1 = Label(pageNewUser, text=controller.currentLanguage.adminPageContent[36], font=self.infoFont, fg = 'white', bg = self.colorORT)
        self.passwordCondition1.place(x=120, y=180)
        self.passwordCondition2 = Label(pageNewUser, text=controller.currentLanguage.adminPageContent[37], font=self.infoFont, fg = 'white', bg = self.colorORT)
        self.passwordCondition2.place(x=90, y=200)
        self.nameCondition1 = Label(pageNewUser, text=controller.currentLanguage.adminPageContent[38], font=self.infoFont, fg = 'white', bg = self.colorORT)
        self.nameCondition1.place(x=175, y=290)
        self.nameCondition2 = Label(pageNewUser, text=controller.currentLanguage.adminPageContent[39], font=self.infoFont, fg = 'white', bg = self.colorORT)
        self.nameCondition2.place(x=135, y=310)
        self.surnameCondition1 = Label(pageNewUser, text=controller.currentLanguage.adminPageContent[40], font=self.infoFont, fg = 'white', bg = self.colorORT)
        self.surnameCondition1.place(x=185, y=400)
        self.surnameCondition2 = Label(pageNewUser, text=controller.currentLanguage.adminPageContent[41], font=self.infoFont, fg = 'white', bg = self.colorORT)
        self.surnameCondition2.place(x=135, y=420)
        self.emailCondition = Label(pageNewUser, text="( @gmail.com, @ort.edu.uy, @vera.com, @yahoo.com )", font=self.infoFont, fg = 'white', bg = self.colorORT)
        self.emailCondition.place(x=85, y=510)
        self.addressCondition = Label(pageNewUser, text=controller.currentLanguage.adminPageContent[42], font=self.infoFont, fg = 'white', bg = self.colorORT)
        self.addressCondition.place(x=1055, y=310)
        self.telephoneCondition = Label(pageNewUser, text=controller.currentLanguage.adminPageContent[43], font=self.infoFont, fg = 'white', bg = self.colorORT)
        self.telephoneCondition.place(x=1015, y=180)

    def setSpinboxsPageNewUser(self, pageNewUser, controller):
        self.userBirthDate.append(Spinbox(pageNewUser, from_=1, to=31, font=self.inputFont, width=3, justify='center'))
        self.userBirthDate[0].place(x=1000, y=25)
        self.userBirthDate.append(Spinbox(pageNewUser, values=controller.currentLanguage.adminPageContent[44], font=self.inputFont, width=8, justify='center'))
        self.userBirthDate[1].place(x=1050, y=25)
        self.userBirthDate.append(Spinbox(pageNewUser, from_=1950, to=2019,  font=self.inputFont, width=5, justify='center'))
        self.userBirthDate[2].place(x=1160, y=25)
        self.professorData.append(Spinbox(pageNewUser, values=controller.currentLanguage.adminPageContent[45],  font=self.inputFont, width=10, justify='center'))
        self.professorData[0].place(x=765, y=420)
        self.professorData.append(Spinbox(pageNewUser, values=controller.currentLanguage.adminPageContent[46],  font=self.inputFont, width=7, justify='center'))
        self.professorData[1].place(x=900, y=420)
        self.studentData.append(Spinbox(pageNewUser, values=controller.currentLanguage.adminPageContent[47], font=self.inputFont, width=17, justify='center'))
        self.studentData[0].place(x=1040, y=420)
        self.studentData.append(Spinbox(pageNewUser, values=("Sem. 1", "Sem. 2", "Sem. 3", "Sem. 4", "Sem. 5", "Sem. 6", "Sem. 7", "Sem. 8", "Sem. 9", "Sem. 10"),  font=self.inputFont, width=7, justify='center'))
        self.studentData[1].place(x=1250, y=420)

    def clearEntriesNewUser(self):
        self.usernumberTitle['fg']='white'
        self.passwordTitle['fg']='white'
        self.nameTitle['fg']='white'
        self.surnameTitle['fg']='white'
        self.emailTitle['fg']='white'
        self.birthdateTitle['fg']='white'
        self.telephoneTitle['fg']='white'
        self.addressTitle['fg']='white'
        self.idNumberTitle['fg']='white'
        for position in range(0,9):
            self.userInput[position].delete(0,END)

    def showMistakesNewUser(self, userMistakes):
        if(userMistakes[0:1]=='0'):
            self.usernumberTitle['fg']='red'
        if(userMistakes[1:2]=='0'):
            self.passwordTitle['fg']='red'
        if(userMistakes[2:3]=='0'):
            self.nameTitle['fg']='red'
            self.surnameTitle['fg']='red'
        if(userMistakes[3:4]=='0'):
            self.emailTitle['fg']='red'
        if(userMistakes[4:5]=='0'):
            self.addressTitle['fg']='red'
        if(userMistakes[5:6]=='0'):
            self.telephoneTitle['fg']='red'
        if(userMistakes[6:7]=='0'):
            self.idNumberTitle['fg']='red'
        if(userMistakes=='0000000'):
            self.birthdateTitle['fg']='red'

    def checkProfessorAlreadyRegistered(self, controller, professorBeingChecked):
        if(professorBeingChecked.isUserWellRegistered()):
            controller.application.listProfessors.addProfessor(professorBeingChecked)
            registrationBodyMail = "\n\n"+controller.application.getDayTimeMomentMessage(controller.currentLanguage.adminPageContent[162])+", "+controller.currentLanguage.adminPageContent[133]+controller.application.listProfessors.professors[len(controller.application.listProfessors.professors)-1].getCompleteNameSurname()+":\n    "+controller.currentLanguage.adminPageContent[135]+controller.application.listProfessors.professors[len(controller.application.listProfessors.professors)-1].showInitialData()+"\n\n"+controller.currentLanguage.adminPageContent[136]
            controller.application.sendEmail([controller.application.listProfessors.professors[len(controller.application.listProfessors.professors)-1].email], [controller.currentLanguage.adminPageContent[137], 'Images/MailContent/registrationMessage.jpg', registrationBodyMail, "IMAGE"])
            messagebox.showinfo(controller.currentLanguage.adminPageContent[48], controller.currentLanguage.adminPageContent[49])
            self.clearEntriesNewUser()
            controller.application.systemData.informations[5].addProfessorRegistered()
            controller.fillProfessorsList(self.professorsList, self.pageOfListProfessors)
            controller.fillProfessorsList(self.professorsListEdition, self.pageOfListProfessorsToEdit)
        else:
            messagebox.showerror(controller.currentLanguage.adminPageContent[50], controller.currentLanguage.adminPageContent[51])
            self.showMistakesNewUser(professorBeingChecked.checkUserData())

    def checkAddProfessor(self, controller):
        professorData = [self.userInput[0].get(), self.userInput[1].get(), self.userInput[2].get(), self.userInput[3].get(), self.userInput[4].get(), self.userInput[5].get(), self.userInput[6].get()+' '+self.userInput[7].get(),
        self.userInput[8].get(), self.userBirthDate[0].get()+'/'+self.monthsName[self.userBirthDate[1].index(self.userBirthDate[1].get())]+'/'+self.userBirthDate[2].get()]
        professorToCheck = Professor(professorData)
        professorToCheck.configureTitle(self.professorData[0].index(self.professorData[0].get()))
        professorToCheck.grade = self.professorData[1].get()[6:7]
        if(controller.application.listProfessors.isProfessorRegistered(professorToCheck)[1]==-1):
            self.checkProfessorAlreadyRegistered(controller, professorToCheck)
        else:
            messagebox.showwarning(controller.currentLanguage.adminPageContent[15], controller.currentLanguage.adminPageContent[52])

    def checkStudentAlreadyRegistered(self, controller, studentBeingChecked):
        if(studentBeingChecked.isUserWellRegistered()):
            controller.application.listStudents.addStudent(studentBeingChecked)
            registrationBodyMail = "\n\n"+controller.currentLanguage.adminPageContent[134]+controller.application.listStudents.students[len(controller.application.listStudents.students)-1].getCompleteNameSurname()+",\n    "+controller.currentLanguage.adminPageContent[135]+controller.application.listStudents.students[len(controller.application.listStudents.students)-1].showInitialData()+"\n\n"+controller.currentLanguage.adminPageContent[136]
            controller.application.sendEmail([controller.application.listStudents.students[len(controller.application.listStudents.students)-1].email], [controller.currentLanguage.adminPageContent[137], 'Images/MailContent/registrationMessage.png', registrationBodyMail, "IMAGE"])
            messagebox.showinfo(controller.currentLanguage.adminPageContent[48], controller.currentLanguage.adminPageContent[53])
            self.clearEntriesNewUser()
            controller.application.systemData.informations[5].addStudentsRegistered()
            controller.fillStudentsList(self.studentsList, self.pageOfListStudents)
            controller.fillStudentsList(self.studentsListEdition, self.pageOfListStudentsToEdit)
        else:
            messagebox.showerror(controller.currentLanguage.adminPageContent[50], controller.currentLanguage.adminPageContent[51])
            self.showMistakes(studentBeingChecked.checkUserData())

    def checkAddStudent(self, controller):
        studentData = [self.userInput[0].get(), self.userInput[1].get(), self.userInput[2].get(), self.userInput[3].get(), self.userInput[4].get(), self.userInput[5].get(), self.userInput[6].get()+' '+self.userInput[7].get(),
         self.userInput[8].get(), self.userBirthDate[0].get()+'/'+self.userBirthDate[1].get()+'/'+self.userBirthDate[2].get()]
        studentToCheck = Student(studentData)
        studentToCheck.configureCareer(self.studentData[0].index(self.studentData[0].get()))
        studentToCheck.semester = int(self.studentData[1].get()[5:7])
        if(controller.application.listStudents.isStudentRegistered(studentToCheck)[1]==-1):
            self.checkStudentAlreadyRegistered(controller, studentToCheck)
        else:
            messagebox.showwarning(controller.currentLanguage.adminPageContent[15], controller.currentLanguage.adminPageContent[54])

    def fillPageNewUser(self, controller, pageNewUser):
        self.fillPageNewUserTitles(pageNewUser, controller)
        self.fillPageNewUserEntries(pageNewUser)
        self.fillPageNewUserIndicators(pageNewUser, controller)
        self.fillPageNewUserHelpers(pageNewUser, controller)

        informationElement = Picture(['basicUserInformation','png',300,550,440,20],0)
        informationElement.purpose = 'Words'
        informationElementPic = informationElement.generateLabel(pageNewUser)
        informationElementPic.place(x=informationElement.location[0],y=informationElement.location[1])

        self.setSpinboxsPageNewUser(pageNewUser, controller)
        self.addProfessorOption = Button(pageNewUser, text=controller.currentLanguage.adminPageContent[55], command=lambda:self.checkAddProfessor(controller), relief = SUNKEN, fg='white', bg = 'dark blue', font="Times 22 bold", compound=CENTER, height = 2, width = 15)
        self.addProfessorOption.place(x=750, y=450)
        self.addStudentOption = Button(pageNewUser, text=controller.currentLanguage.adminPageContent[56], command=lambda:self.checkAddStudent(controller), relief = SUNKEN, fg='white', bg = 'green', font="Times 22 bold", compound=CENTER, height = 2, width = 15)
        self.addStudentOption.place(x=1050, y=450)

    def fillPageEditionTitles(self, pageEdition, editionTitles, controller):
        editionTitles.append(Label(pageEdition, text=controller.currentLanguage.adminPageContent[26], font=self.titleFont, fg = 'white', bg = self.colorORT))
        editionTitles[0].place(x=800, y=30)
        editionTitles.append(Label(pageEdition, text=controller.currentLanguage.adminPageContent[29], font=self.titleFont, fg = 'white', bg = self.colorORT))
        editionTitles[1].place(x=800, y=130)
        editionTitles.append(Label(pageEdition, text=controller.currentLanguage.adminPageContent[31], font=self.titleFont, fg = 'white', bg = self.colorORT))
        editionTitles[2].place(x=800, y=240)
        editionTitles.append(Label(pageEdition, text=controller.currentLanguage.adminPageContent[32], font=self.titleFont, fg = 'white', bg = self.colorORT))
        editionTitles[3].place(x=800, y=350)
        editionTitles.append(Label(pageEdition, text=controller.currentLanguage.adminPageContent[57], font=self.titleFont, fg = 'white', bg = self.colorORT))
        editionTitles[4].place(x=800, y=450)

        self.streetIndicatorEdition = Label(pageEdition, text=controller.currentLanguage.adminPageContent[34], font="Times 12 bold", fg = 'white', bg = self.colorORT)
        self.streetIndicatorEdition.place(x=1060, y=372)
        doorNumberIndicator = Label(pageEdition, text="Num", font="Times 12 bold", fg = 'white', bg = self.colorORT)
        doorNumberIndicator.place(x=1170, y=372)
        telephoneInput = Label(pageEdition, text="+598", font="Times 14 bold", width=5, fg='grey', bg='white')
        telephoneInput.place(x=1008, y=248)

        return editionTitles

    def fillPageEditionEntries(self, pageEdition, userInputEdition):
        userInputEdition.append(Entry(pageEdition, font=self.inputFont, width=20, justify='center')) # passwordInput
        userInputEdition[0].place(x=1008, y=38)
        userInputEdition.append(Entry(pageEdition, font=self.inputFont, width=20, justify='center')) # emailInput
        userInputEdition[1].place(x=1008, y=138)
        userInputEdition.append(Entry(pageEdition, font=self.inputFont, width=15, justify='center')) # telephoneInput
        userInputEdition[2].place(x=1068, y=248)
        userInputEdition.append(Entry(pageEdition, font=self.inputFont, width=15, justify='center')) # streetInput
        userInputEdition[3].place(x=1008, y=338)
        userInputEdition.append(Entry(pageEdition, font=self.inputFont, width=7, justify='center')) # doorNumberInput
        userInputEdition[4].place(x=1150, y=338)

    def updateEditionEntries(self, entriesOfUsersToEdit, userToEdit):
        for position in range(0,5):
            entriesOfUsersToEdit[position].delete(0,END)
        entriesOfUsersToEdit[0].insert(0, userToEdit.password)
        entriesOfUsersToEdit[1].insert(0, userToEdit.email)
        entriesOfUsersToEdit[2].insert(0, userToEdit.telephone)
        entriesOfUsersToEdit[3].insert(0, userToEdit.address[0:len(userToEdit.address)-4])
        entriesOfUsersToEdit[4].insert(0, userToEdit.address[len(userToEdit.address)-4:len(userToEdit.address)])

    def showMistakesEditUser(self, editionTitles, userMistakes):
        if(userMistakes[0:1]=='0'):
            editionTitles[0]['fg']='red'
        if(userMistakes[1:2]=='0'):
            editionTitles[1]['fg']='red'
        if(userMistakes[2:3]=='0'):
            editionTitles[2]['fg']='red'
        if(userMistakes[3:4]=='0'):
            editionTitles[3]['fg']='red'

    def getProfessorModifiedData(self, controller):
        professorEdited = controller.application.listProfessors.professors[self.lastIndexSelectedListProfessor]
        professorEdited.password = self.userInputEditProfessor[0].get()
        professorEdited.email = self.userInputEditProfessor[1].get()
        professorEdited.telephone = self.userInputEditProfessor[2].get()
        professorEdited.address = self.userInputEditProfessor[3].get()+' '+self.userInputEditProfessor[4].get()
        professorEdited.title = self.professorDataEdition[0].get()
        professorEdited.grade = self.professorDataEdition[1].get()[6:7]
        return professorEdited

    def updateReservationsInformation(self, controller, userEdited):
        for eachReservation in controller.application.listReservations.reservations:
            if(eachReservation.professorResponsible.areEqual(userEdited)):
                eachReservation.professorResponsible.email = userEdited.email
            if(eachReservation.userToReserve.areEqual(userEdited)):
                eachReservation.userToReserve.email = userEdited.email

    def checkModifyProfessor(self, controller):
        professorEdited = self.getProfessorModifiedData(controller)
        if(professorEdited.isDataToEditRight()):
            controller.application.listProfessors.professors[self.lastIndexSelectedListProfessor] = professorEdited
            self.updateReservationsInformation(controller, professorEdited)
            dataProfessorChangedBodyMail = "\n\n"+controller.application.getDayTimeMomentMessage(controller.currentLanguage.adminPageContent[162])+", "+controller.currentLanguage.adminPageContent[133]+controller.application.listProfessors.professors[self.lastIndexSelectedListProfessor].getCompleteNameSurname()+":\n   "+controller.currentLanguage.adminPageContent[138]+controller.application.listProfessors.professors[self.lastIndexSelectedListProfessor].showInitialData()+"\n\n"+controller.currentLanguage.adminPageContent[139]
            controller.application.sendEmail([controller.application.listProfessors.professors[self.lastIndexSelectedListProfessor].email], [controller.currentLanguage.adminPageContent[140], 'Images/MailContent/userDataChangedMail.png', dataProfessorChangedBodyMail, "IMAGE"])
            messagebox.showinfo(controller.currentLanguage.adminPageContent[59], controller.currentLanguage.adminPageContent[61])
            self.clearEntriesEdition(self.professorEditionTitles)
            controller.fillProfessorsList(self.professorsList, self.pageOfListProfessors)
            controller.fillProfessorsList(self.professorsListEdition, self.pageOfListProfessorsToEdit)
        else:
            messagebox.showerror(controller.currentLanguage.adminPageContent[50], controller.currentLanguage.adminPageContent[51])
            self.showMistakesEditUser(self.professorEditionTitles, professorToCheck.checkEditionData())

    def clearEntriesEdition(self, editionTitles):
        editionTitles[0]['fg']='white'
        editionTitles[1]['fg']='white'
        editionTitles[2]['fg']='white'
        editionTitles[3]['fg']='white'

    def fillPageEditProfessorSpinbox(self, pageEditProfessor, controller):
        self.professorDataEdition.append(Spinbox(pageEditProfessor, values=controller.currentLanguage.adminPageContent[45],  font=self.inputFont, width=10, justify='center'))
        self.professorDataEdition[0].place(x=1005, y=458)
        self.professorDataEdition.append(Spinbox(pageEditProfessor, values=controller.currentLanguage.adminPageContent[46],  font=self.inputFont, width=7, justify='center'))
        self.professorDataEdition[1].place(x=1140, y=458)

    def fillPageEditProfessorPictures(self, pageEditProfessor, controller):
        controller.setImagesandSeparators(pageEditProfessor, 'professorsElement', [115,280,10,0,115,280,10,290])
        controller.setImagesandSeparators(pageEditProfessor, 'professorsElement', [115,280,1260,0,115,280,1260,290])
        self.fillPageEditionTitles(pageEditProfessor, self.professorEditionTitles, controller)
        self.fillPageEditionEntries(pageEditProfessor, self.userInputEditProfessor)
        self.fillPageEditProfessorSpinbox(pageEditProfessor, controller)
        editionSeparatorLists = Picture(['editionProfessorSeparator','png',160,550,640,0],0)
        editionSeparatorLists.purpose = 'Separators'
        editionSeparatorListsPic = editionSeparatorLists.generateLabel(pageEditProfessor)
        editionSeparatorListsPic.place(x=editionSeparatorLists.location[0],y=editionSeparatorLists.location[1])

    def configureListProfessorsToEdit(self, pageEditProfessor, controller):
        def onselectProfessor(evt):
            try:
                listOfProfessors = evt.widget
                self.lastIndexSelectedListProfessor = int(listOfProfessors.curselection()[0])+self.pageOfListProfessorsToEdit*self.usersPerPage
                value = listOfProfessors.get(self.lastIndexSelectedListProfessor)
                self.updateEditionEntries(self.userInputEditProfessor, controller.application.listProfessors.professors[self.lastIndexSelectedListProfessor])
            except IndexError:
                self.professorsListEdition.activate(self.lastIndexSelectedListProfessor)

        self.professorsListEdition = Listbox(pageEditProfessor, width=83, height=28, font=self.listElementFont)
        self.professorsListEdition.place(x=140,y=10)
        controller.fillProfessorsList(self.professorsListEdition, self.pageOfListProfessorsToEdit)
        self.professorsListEdition.bind('<<ListboxSelect>>', onselectProfessor)

    def showPageOfListProfessorsToEdit(self, controller, numberOfPage):
        for eachButton in self.pageNumberOfProfessorsToEditList:
            eachButton['bg']='white'
        self.pageOfListProfessorsToEdit = numberOfPage-1
        self.pageNumberOfProfessorsToEditList[self.pageOfListProfessorsToEdit]['bg'] = 'yellow'
        controller.fillProfessorsList(self.professorsListEdition, self.pageOfListProfessorsToEdit)

    def fillPageEditProfessorButtons(self, pageEditProfessor, controller):
        self.modifyProfessorOption = Button(pageEditProfessor, text=controller.currentLanguage.adminPageContent[58], command=lambda:self.checkModifyProfessor(controller), relief = SUNKEN, fg='white', bg = 'dark blue', font=self.buttonFont, compound=CENTER, height = 2, width = 17)
        self.modifyProfessorOption.place(x=140, y=475)
        self.orderProfessorEditionOption = Button(pageEditProfessor, text=controller.currentLanguage.adminPageContent[163], command = lambda:self.orderProfessors(controller), relief = SUNKEN, fg='white', bg = 'red', font=self.buttonFont, compound=CENTER, height = 2, width = 7)
        self.orderProfessorEditionOption.place(x=355, y=475)
        self.pageNumberOfProfessorsToEditList.append(Button(pageEditProfessor, text="1", relief = SUNKEN, fg=self.colorORT, bg = 'yellow', font=self.buttonFont, compound=CENTER, height = 2, width = 4, command=lambda:self.showPageOfListProfessorsToEdit(controller, 1)))
        self.pageNumberOfProfessorsToEditList[0].place(x=455, y=475)
        self.pageNumberOfProfessorsToEditList.append(Button(pageEditProfessor, text="2", relief = SUNKEN, fg=self.colorORT, bg = 'white', font=self.buttonFont, compound=CENTER, height = 2, width = 4, command=lambda:self.showPageOfListProfessorsToEdit(controller, 2)))
        self.pageNumberOfProfessorsToEditList[1].place(x=515, y=475)
        self.pageNumberOfProfessorsToEditList.append(Button(pageEditProfessor, text="3", relief = SUNKEN, fg=self.colorORT, bg = 'white', font=self.buttonFont, compound=CENTER, height = 2, width = 4, command=lambda:self.showPageOfListProfessorsToEdit(controller, 3)))
        self.pageNumberOfProfessorsToEditList[2].place(x=575, y=475)

    def fillPageEditProfessor(self, pageEditProfessor, controller):
        self.configureListProfessorsToEdit(pageEditProfessor, controller)
        self.fillPageEditProfessorPictures(pageEditProfessor, controller)
        self.fillPageEditProfessorButtons(pageEditProfessor, controller)

    def getStudentModifiedData(self, controller):
        studentEdited = controller.application.listStudents.students[self.lastIndexSelectedListStudent]
        studentEdited.password = self.userInputEditStudent[0].get()
        studentEdited.email = self.userInputEditStudent[1].get()
        studentEdited.telephone = self.userInputEditStudent[2].get()
        studentEdited.address = self.userInputEditStudent[3].get()+' '+self.userInputEditStudent[4].get()
        studentEdited.career = self.studentDataEdition[0].get()
        studentEdited.semester = int(self.studentDataEdition[1].get()[5:7])
        return studentEdited

    def checkModifyStudent(self, controller):
        studentEdited = self.getStudentModifiedData(controller)
        if(studentEdited.isDataToEditRight()):
            controller.application.listStudents.students[self.lastIndexSelectedListStudent] = studentEdited
            self.updateReservationsInformation(controller, studentEdited)
            dataStudentChangedBodyMail = "\n\n"+controller.currentLanguage.adminPageContent[134]+controller.application.listStudents.students[self.lastIndexSelectedListStudent].getCompleteNameSurname()+":\n   "+controller.currentLanguage.adminPageContent[138]+controller.application.listStudents.students[self.lastIndexSelectedListStudent].showInitialData()+"\n\n"+controller.currentLanguage.adminPageContent[139]
            controller.application.sendEmail([controller.application.listStudents.students[self.lastIndexSelectedListStudent].email], [controller.currentLanguage.adminPageContent[140], 'Images/MailContent/userDataChangedMail.png', dataStudentChangedBodyMail, "IMAGE"])
            messagebox.showinfo(controller.currentLanguage.adminPageContent[59], controller.currentLanguage.adminPageContent[60])
            self.clearEntriesEdition(self.studentEditionTitles)
            controller.fillStudentsList(self.studentsList, self.pageOfListStudents)
            controller.fillStudentsList(self.studentsListEdition, self.pageOfListStudentsToEdit)
        else:
            messagebox.showerror(controller.currentLanguage.adminPageContent[50], controller.currentLanguage.adminPageContent[51])
            self.showMistakesEditUser(self.studentEditionTitles, studentEdited.checkEditionData())

    def fillPageEditStudentSpinbox(self, pageEditStudent, controller):
        self.studentDataEdition.append(Spinbox(pageEditStudent, values=controller.currentLanguage.adminPageContent[47], font=self.inputFont, width=17, justify='center'))
        self.studentDataEdition[0].place(x=965, y=458)
        self.studentDataEdition.append(Spinbox(pageEditStudent, values=("Sem. 1", "Sem. 2", "Sem. 3", "Sem. 4", "Sem. 5", "Sem. 6", "Sem. 7", "Sem. 8", "Sem. 9", "Sem. 10"),  font=self.inputFont, width=7, justify='center'))
        self.studentDataEdition[1].place(x=1175, y=458)

    def fillPageEditStudentPictures(self, pageEditStudent, controller):
        controller.setImagesandSeparators(pageEditStudent, 'studentsElement', [115,280,10,0,115,280,10,290])
        controller.setImagesandSeparators(pageEditStudent, 'studentsElement', [115,280,1260,0,115,280,1260,290])
        editionSeparatorLists = Picture(['editionStudentSeparator','png',160,550,640,0],0)
        editionSeparatorLists.purpose = 'Separators'
        editionSeparatorListsPic = editionSeparatorLists.generateLabel(pageEditStudent)
        editionSeparatorListsPic.place(x=editionSeparatorLists.location[0],y=editionSeparatorLists.location[1])

    def configurePageEditStudentsList(self, pageEditStudent, controller):
        def onselectStudent(evt):
            try:
                listOfStudents = evt.widget
                self.lastIndexSelectedListStudent = int(listOfStudents.curselection()[0])+self.pageOfListStudentsToEdit*self.usersPerPage
                value = listOfStudents.get(self.lastIndexSelectedListStudent)
                self.updateEditionEntries(self.userInputEditStudent, controller.application.listStudents.students[self.lastIndexSelectedListStudent])
            except IndexError:
                self.studentsListEdition.activate(self.lastIndexSelectedListStudent)

        self.studentsListEdition = Listbox(pageEditStudent, width=83, height=28, font=self.listElementFont)
        self.studentsListEdition.place(x=140,y=10)
        controller.fillStudentsList(self.studentsListEdition, self.pageOfListStudentsToEdit)
        self.studentsListEdition.bind('<<ListboxSelect>>', onselectStudent)

    def showPageOfListStudentsToEdit(self, controller, numberOfPage):
        for eachButton in self.pageNumberOfStudentsToEditList:
            eachButton['bg']='white'
        self.pageOfListStudentsToEdit = numberOfPage-1
        self.pageNumberOfStudentsToEditList[self.pageOfListStudentsToEdit]['bg'] = 'yellow'
        controller.fillStudentsList(self.studentsListEdition, self.pageOfListStudentsToEdit)

    def fillPageEditStudentsButtons(self, pageEditStudent, controller):
        self.modifyStudentOption = Button(pageEditStudent, text=controller.currentLanguage.adminPageContent[62], command=lambda:self.checkModifyStudent(controller), relief = SUNKEN, fg='white', bg = 'green', font=self.buttonFont, compound=CENTER, height = 2, width = 17)
        self.modifyStudentOption.place(x=140, y=475)
        self.orderStudentEditionOption = Button(pageEditStudent, text=controller.currentLanguage.adminPageContent[163], command = lambda:self.orderStudents(controller), relief = SUNKEN, fg='white', bg = 'red', font=self.buttonFont, compound=CENTER, height = 2, width = 7)
        self.orderStudentEditionOption.place(x=355, y=475)
        self.pageNumberOfStudentsToEditList.append(Button(pageEditStudent, text="1", relief = SUNKEN, fg=self.colorORT, bg = 'yellow', font=self.buttonFont, compound=CENTER, height = 2, width = 4, command=lambda:self.showPageOfListStudentsToEdit(controller, 1)))
        self.pageNumberOfStudentsToEditList[0].place(x=455, y=475)
        self.pageNumberOfStudentsToEditList.append(Button(pageEditStudent, text="2", relief = SUNKEN, fg=self.colorORT, bg = 'white', font=self.buttonFont, compound=CENTER, height = 2, width = 4, command=lambda:self.showPageOfListStudentsToEdit(controller, 2)))
        self.pageNumberOfStudentsToEditList[1].place(x=515, y=475)
        self.pageNumberOfStudentsToEditList.append(Button(pageEditStudent, text="3", relief = SUNKEN, fg=self.colorORT, bg = 'white', font=self.buttonFont, compound=CENTER, height = 2, width = 4, command=lambda:self.showPageOfListStudentsToEdit(controller, 3)))
        self.pageNumberOfStudentsToEditList[2].place(x=575, y=475)

    def fillPageEditStudent(self, pageEditStudent, controller):

        self.fillPageEditStudentPictures(pageEditStudent, controller)
        self.fillPageEditionTitles(pageEditStudent, self.studentEditionTitles, controller)
        self.fillPageEditionEntries(pageEditStudent, self.userInputEditStudent)
        self.fillPageEditStudentSpinbox(pageEditStudent, controller)
        self.configurePageEditStudentsList(pageEditStudent, controller)
        self.fillPageEditStudentsButtons(pageEditStudent, controller)

    #def createListUsers(self, controller):
    #    del self.listUsers[:]
    #    for eachProfessor in controller.application.listProfessors.professors:
    #        self.listUsers.append(eachProfessor)
    #    for eachStudent in controller.application.listStudents.students:
    #        self.listUsers.append(eachStudent)

    def fillPageUserInfoTitles(self, pageUserInfo, controller):
        self.usernumberTitle = Label(pageUserInfo, text=controller.currentLanguage.adminPageContent[25], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.usernumberTitle.place(x=200, y=30)
        self.passwordTitle = Label(pageUserInfo, text=controller.currentLanguage.adminPageContent[26], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.passwordTitle.place(x=200, y=100)
        self.nameTitle = Label(pageUserInfo, text=controller.currentLanguage.adminPageContent[27], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.nameTitle.place(x=200, y=190)
        self.surnameTitle = Label(pageUserInfo, text=controller.currentLanguage.adminPageContent[28], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.surnameTitle.place(x=200, y=280)
        self.emailTitle = Label(pageUserInfo, text=controller.currentLanguage.adminPageContent[29], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.emailTitle.place(x=200, y=370)
        self.userTitle = Label(pageUserInfo, text=controller.currentLanguage.adminPageContent[63], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.userTitle.place(x=200, y=460)
        self.birthdateTitle = Label(pageUserInfo, text=controller.currentLanguage.adminPageContent[30], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.birthdateTitle.place(x=800, y=30)
        self.telephoneTitle = Label(pageUserInfo, text=controller.currentLanguage.adminPageContent[31], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.telephoneTitle.place(x=800, y=100)
        self.addressTitle = Label(pageUserInfo, text=controller.currentLanguage.adminPageContent[32], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.addressTitle.place(x=800, y=190)
        self.idNumberTitle = Label(pageUserInfo, text=controller.currentLanguage.adminPageContent[33], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.idNumberTitle.place(x=800, y=280)
        self.lastLoginTitle = Label(pageUserInfo, text=controller.currentLanguage.adminPageContent[3], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.lastLoginTitle.place(x=800, y=370)
        self.previousUserTitle = Label(pageUserInfo, text=controller.currentLanguage.adminPageContent[64], font=self.buttonFont, fg = 'dark red', bg = self.colorORT)
        self.previousUserTitle.place(x=900, y=450)
        self.userTitlePrevious = Label(pageUserInfo, text=controller.currentLanguage.adminPageContent[66], font=self.buttonFont, fg = 'dark blue', bg = self.colorORT)
        self.userTitlePrevious.place(x=910, y=490)
        self.nextUserTitle = Label(pageUserInfo, text=controller.currentLanguage.adminPageContent[65], font=self.buttonFont, fg = 'dark blue', bg = self.colorORT)
        self.nextUserTitle.place(x=1040, y=450)
        self.userTitleNext = Label(pageUserInfo, text=controller.currentLanguage.adminPageContent[66], font=self.buttonFont, fg = 'dark red', bg = self.colorORT)
        self.userTitleNext.place(x=1040, y=490)

    def fillWithUserInformation(self, pageUserInfo, userToShow):
        self.userInfo.append(Label(pageUserInfo, text=userToShow.usernumber, font=self.inputFont, fg = 'white', bg = self.colorORT))
        self.userInfo[0].place(x=420, y=38)
        self.userInfo.append(Label(pageUserInfo, text=userToShow.password, font=self.inputFont, fg = 'white', bg = self.colorORT))
        self.userInfo[1].place(x=410, y=108)
        self.userInfo.append(Label(pageUserInfo, text=userToShow.name, font=self.inputFont, fg = 'white', bg = self.colorORT))
        self.userInfo[2].place(x=430, y=198)
        self.userInfo.append(Label(pageUserInfo, text=userToShow.surname, font=self.inputFont, fg = 'white', bg = self.colorORT))
        self.userInfo[3].place(x=420, y=288)
        self.userInfo.append(Label(pageUserInfo, text=userToShow.email, font=self.inputFont, fg = 'white', bg = self.colorORT))
        self.userInfo[4].place(x=400, y=378)
        self.userInfo.append(Label(pageUserInfo, text=userToShow.birthDate, font=self.inputFont, fg = 'white', bg = self.colorORT))
        self.userInfo[5].place(x=1050, y=38)
        self.userInfo.append(Label(pageUserInfo, text="0"+userToShow.telephone, font=self.inputFont, fg = 'white', bg = self.colorORT))
        self.userInfo[6].place(x=1050, y=108)
        self.userInfo.append(Label(pageUserInfo, text=userToShow.address, font=self.inputFont, fg = 'white', bg = self.colorORT))
        self.userInfo[7].place(x=1050, y=198)
        self.userInfo.append(Label(pageUserInfo, text=userToShow.idNumber, font=self.inputFont, fg = 'white', bg = self.colorORT))
        self.userInfo[8].place(x=1050, y=288)
        self.userInfo.append(Label(pageUserInfo, text=userToShow.lastEntryDate, font=self.inputFont, fg = 'white', bg = self.colorORT))
        self.userInfo[9].place(x=1050, y=378)
        self.professorInfo.append(Label(pageUserInfo, text="", font=self.inputFont, fg = 'white', bg = self.colorORT))
        self.professorInfo[0].place(x=340, y=458)
        self.professorInfo.append(Label(pageUserInfo, text="", font=self.inputFont, fg = 'white', bg = self.colorORT))
        self.professorInfo[1].place(x=340, y=488)
        self.studentInfo.append(Label(pageUserInfo, text="", font=self.inputFont, fg = 'white', bg = self.colorORT))
        self.studentInfo[0].place(x=340, y=458)
        self.studentInfo.append(Label(pageUserInfo, text="", font=self.inputFont, fg = 'white', bg = self.colorORT))
        self.studentInfo[1].place(x=340, y=488)

    def updateWithProfessorInformation(self, pageUserInfo, professorToShow, controller):
        self.professorInfo[0]['text'] = controller.currentLanguage.adminPageContent[67] + professorToShow.title + controller.currentLanguage.adminPageContent[68]
        self.professorInfo[1]['text'] =  controller.currentLanguage.adminPageContent[69] + professorToShow.grade
        self.studentInfo[0]['text'] = ""
        self.studentInfo[1]['text'] = ""

    def updateWithStudentInformation(self, pageUserInfo, studentToShow, controller):
        self.professorInfo[0]['text'] = ""
        self.professorInfo[1]['text'] = ""
        self.studentInfo[0]['text'] =  controller.currentLanguage.adminPageContent[70] + studentToShow.career
        self.studentInfo[1]['text'] =  controller.currentLanguage.adminPageContent[71] + str(studentToShow.semester)

    def setUserInfoContent(self, pageUserInfo, controller):
        if(self.userIndex < len(controller.application.listProfessors.professors)):
            controller.setImagesandSeparators(pageUserInfo, 'professorsElement', [115,280,10,0,115,280,10,290])
            controller.setImagesandSeparators(pageUserInfo, 'professorsElement', [115,280,1260,0,115,280,1260,290])
            self.updateWithProfessorInformation(pageUserInfo, controller.application.listProfessors.professors[self.userIndex], controller)
        elif(self.userIndex < len(controller.application.listProfessors.professors) + len(controller.application.listStudents.students)):
            controller.setImagesandSeparators(pageUserInfo, 'studentsElement', [115,280,10,0,115,280,10,290])
            controller.setImagesandSeparators(pageUserInfo, 'studentsElement', [115,280,1260,0,115,280,1260,290])
            self.updateWithStudentInformation(pageUserInfo, controller.application.listStudents.students[self.userIndex-len(controller.application.listProfessors.professors)], controller)

    def configureUserDataShown(self, pageUserInfo, controller):
        if(self.userIndex < len(controller.application.listProfessors.professors)):
            self.fillWithUserInformation(pageUserInfo, controller.application.listProfessors.professors[self.userIndex])
        elif(self.userIndex < len(controller.application.listProfessors.professors) + len(controller.application.listStudents.students)):
            self.fillWithUserInformation(pageUserInfo, controller.application.listStudents.students[self.userIndex-len(controller.application.listProfessors.professors)])
        self.setUserInfoContent(pageUserInfo, controller)

    def updateWithUserInformation(self, userToShow):
        self.userInfo[0]['text'] = userToShow.usernumber
        self.userInfo[1]['text'] = userToShow.password
        self.userInfo[2]['text'] = userToShow.name
        self.userInfo[3]['text'] = userToShow.surname
        self.userInfo[4]['text'] = userToShow.email
        self.userInfo[5]['text'] = userToShow.birthDate
        self.userInfo[6]['text'] = "0"+userToShow.telephone
        self.userInfo[7]['text'] = userToShow.address
        self.userInfo[8]['text'] = userToShow.idNumber
        self.userInfo[9]['text'] = userToShow.lastEntryDate

    def updateUserDataShown(self, pageUserInfo, controller):
        if(self.userIndex < len(controller.application.listProfessors.professors)):
            self.updateWithUserInformation(controller.application.listProfessors.professors[self.userIndex])
        elif(self.userIndex < len(controller.application.listProfessors.professors) + len(controller.application.listStudents.students)):
            self.updateWithUserInformation(controller.application.listStudents.students[self.userIndex-len(controller.application.listProfessors.professors)])
        self.setUserInfoContent(pageUserInfo, controller)

    def showPreviousUser(self, pageUserInfo, controller):
        if(self.userIndex>0):
            self.userIndex=self.userIndex-1
            self.updateUserDataShown(pageUserInfo, controller)
        else:
            messagebox.showwarning(controller.currentLanguage.adminPageContent[15], controller.currentLanguage.adminPageContent[72])

    def showNextUser(self, pageUserInfo, controller):
        if(self.userIndex<len(controller.application.listProfessors.professors)+len(controller.application.listStudents.students)):
            self.userIndex=self.userIndex+1
            self.updateUserDataShown(pageUserInfo, controller)
        else:
            messagebox.showwarning(controller.currentLanguage.adminPageContent[15], controller.currentLanguage.adminPageContent[73])

    def setButtonsAndSeparatorsOnPageUserInfo(self, pageUserInfo, controller):
        separatorUserInfo = Picture(['userInfoSeparator','png',140,550,640,0],0)
        separatorUserInfo.purpose = 'Separators'
        separatorUserInfoPic = separatorUserInfo.generateLabel(pageUserInfo)
        separatorUserInfoPic.place(x=separatorUserInfo.location[0],y=separatorUserInfo.location[1])

        self.arrowLeftImage = PhotoImage(file="Images/Logos/arrowLeft.gif")
        previousUserOption = Button(pageUserInfo, image=self.arrowLeftImage, command=lambda:self.showPreviousUser(pageUserInfo, controller), relief = SUNKEN, compound=CENTER)
        previousUserOption.place(x=790, y=430)
        self.arrowRightImage = PhotoImage(file="Images/Logos/arrowRight.gif")
        nextUserOption = Button(pageUserInfo, image=self.arrowRightImage, command=lambda:self.showNextUser(pageUserInfo, controller), relief = SUNKEN, compound=CENTER)
        nextUserOption.place(x=1145, y=430)

    def fillPageUserInfo(self, pageUserInfo, controller):
        self.fillPageUserInfoTitles(pageUserInfo, controller)
        self.configureUserDataShown(pageUserInfo, controller)
        self.setButtonsAndSeparatorsOnPageUserInfo(pageUserInfo, controller)

    def fillPagePlatformInfoPictures(self, pagePlatformInfo):
        fermentHistoryElement = Picture(['fermentationsHistoryElement','png',130,550,10,10],0)
        fermentHistoryElement.purpose = 'Words'
        fermentHistoryElementPic = fermentHistoryElement.generateLabel(pagePlatformInfo)
        fermentHistoryElementPic.place(x=fermentHistoryElement.location[0],y=fermentHistoryElement.location[1])

    def fillFermentationsList(self, controller):
        if(len(controller.application.listFermentations.fermentations)>0):
            self.fermentationsList.delete(0,END)
            positionGraphicList = 1
            positionGlobalList = 0
            for aFermentation in controller.application.listFermentations.fermentations:
                if(positionGlobalList>=self.pageOfListFermentations*self.usersPerPage and positionGlobalList<(self.pageOfListFermentations+1)*self.usersPerPage):
                    self.fermentationsList.insert(positionGraphicList, aFermentation.showInformation())
                    positionGraphicList = positionGraphicList + 1
                positionGlobalList = positionGlobalList + 1
        else:
            self.fermentationsList.delete(0,END)
            self.fermentationsList.insert(1, controller.currentLanguage.adminPageContent[74])

    def configureFermentationList(self, pagePlatformInfo, controller):

        def onselectFermentation(evt):
            try:
                listOfFermentations = evt.widget
                self.descriptionInformation['text'] = controller.application.listFermentations.fermentations[int(listOfFermentations.curselection()[0])+self.pageOfListFermentations*self.usersPerPage].getDescriptiveInformationForAdmin()
            except IndexError:
                self.fermentationsList.activate(0)
                self.descriptionInformation['text'] = ""
            except AttributeError:
                self.descriptionInformation['text'] = controller.currentLanguage.adminPageContent[75]

        self.fermentationsList = Listbox(pagePlatformInfo, width=83, height=28, font=self.listElementFont)
        self.fermentationsList.place(x=140,y=10)
        self.fillFermentationsList(controller)
        self.fermentationsList.bind('<<ListboxSelect>>', onselectFermentation)

    def fillPagePlatformInfoTitles(self, pagePlatformInfo, controller):
        self.descriptionTitle = Label(pagePlatformInfo, text=controller.currentLanguage.adminPageContent[76], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.descriptionTitle.place(x=690, y=10)
        self.notificationTitle = Label(pagePlatformInfo, text=controller.currentLanguage.adminPageContent[77], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.notificationTitle.place(x=690, y=210)

    def fillPagePlatformInfoEntries(self, pagePlatformInfo):
        self.notificationMessage = Text(pagePlatformInfo, font=self.inputFont, fg = self.colorORT, bg='white', height=9, width=56)
        self.notificationMessage.place(x=690, y=250)
        self.descriptionInformation = Label(pagePlatformInfo, text="", font=self.inputFont, fg = self.colorORT, bg='white', height=6, width=51)
        self.descriptionInformation.place(x=690, y=50)

    def removeFermentationAction(self, controller):
        if(len(self.fermentationsList.curselection())>0):
            controller.application.fermentations.removeFermentation(int(self.fermentationsList.curselection()[0])+self.pageOfListFermentations*self.usersPerPage)
        else:
            messagebox.showwarning(controller.currentLanguage.adminPageContent[78], controller.currentLanguage.adminPageContent[79])

    def showPageOfListFermentations(self, controller, numberOfPage):
        for eachButton in self.pageNumberOfFermentationList:
            eachButton['bg']='white'
        self.pageOfListFermentations = numberOfPage-1
        self.pageNumberOfFermentationList[self.pageOfListFermentations]['bg'] = 'yellow'
        self.fillFermentationsList(controller)

    def sendProfessorsOption(self, controller):
        if(len(controller.application.listProfessors.professors)>0):
            if(controller.isMessageRight(self.notificationMessage)):
                allProfessorsEmails = controller.application.listProfessors.getAllMailFromList()
                controller.application.sendEmail([allProfessorsEmails], [controller.currentLanguage.adminPageContent[141], 'Images/MailContent/messageFromAdministratorMail.png', "\n\n"+controller.currentLanguage.adminPageContent[142]+self.notificationMessage.get(1.0, END), "IMAGE"])
                messagebox.showinfo(controller.currentLanguage.adminPageContent[80], controller.currentLanguage.adminPageContent[81])
            else:
                messagebox.showerror(controller.currentLanguage.adminPageContent[50], controller.currentLanguage.adminPageContent[82])
        else:
            messagebox.showwarning(controller.currentLanguage.adminPageContent[15], controller.currentLanguage.adminPageContent[83])

    def sendStudentsOption(self, controller):
        if(len(controller.application.listStudents.students)>0):
            if(controller.isMessageRight(self.notificationMessage)):
                allStudentsEmails = controller.application.listStudents.getAllMailFromList()
                controller.application.sendEmail([allStudentsEmails], [controller.currentLanguage.adminPageContent[141], 'Images/MailContent/messageFromAdministratorMail.png', "\n\n"+controller.currentLanguage.adminPageContent[142]+self.notificationMessage.get(1.0, END), "IMAGE"])
                messagebox.showinfo(controller.currentLanguage.adminPageContent[80], controller.currentLanguage.adminPageContent[84])
            else:
                messagebox.showerror(controller.currentLanguage.adminPageContent[50], controller.currentLanguage.adminPageContent[85])
        else:
            messagebox.showwarning(controller.currentLanguage.adminPageContent[15], controller.currentLanguage.adminPageContent[86])

    def fillPagePlatformInfoButtons(self, pagePlatformInfo, controller):
        self.sendProfessorNotesOption = Button(pagePlatformInfo, text=controller.currentLanguage.adminPageContent[87], relief = SUNKEN, fg='white', bg = 'dark blue', font=self.buttonFont, compound=CENTER, height = 2, width = 25, command=lambda:self.sendProfessorsOption(controller))
        self.sendProfessorNotesOption.place(x=690, y=465)
        self.sendStudentNotesOption = Button(pagePlatformInfo, text=controller.currentLanguage.adminPageContent[88], relief = SUNKEN, fg='white', bg = 'green', font=self.buttonFont, compound=CENTER, height = 2, width = 25, command=lambda:self.sendStudentsOption(controller))
        self.sendStudentNotesOption.place(x=1010, y=465)
        self.removeFermentationOption = Button(pagePlatformInfo, text=controller.currentLanguage.adminPageContent[89], relief = SUNKEN, fg='white', bg = 'DodgerBlue3', font=self.buttonFont, compound=CENTER, height = 2, width = 16, command=lambda:self.removeFermentationAction(controller))
        self.removeFermentationOption.place(x=140, y=475)
        self.pageNumberOfFermentationList.append(Button(pagePlatformInfo, text="1", relief = SUNKEN, fg=self.colorORT, bg = 'yellow', font=self.buttonFont, compound=CENTER, height = 2, width = 4, command=lambda:self.showPageOfListFermentations(controller, 1)))
        self.pageNumberOfFermentationList[0].place(x=340, y=475)
        self.pageNumberOfFermentationList.append(Button(pagePlatformInfo, text="2", relief = SUNKEN, fg=self.colorORT, bg = 'white', font=self.buttonFont, compound=CENTER, height = 2, width = 4, command=lambda:self.showPageOfListFermentations(controller, 2)))
        self.pageNumberOfFermentationList[1].place(x=400, y=475)
        self.pageNumberOfFermentationList.append(Button(pagePlatformInfo, text="3", relief = SUNKEN, fg=self.colorORT, bg = 'white', font=self.buttonFont, compound=CENTER, height = 2, width = 4, command=lambda:self.showPageOfListFermentations(controller, 3)))
        self.pageNumberOfFermentationList[2].place(x=460, y=475)
        self.pageNumberOfFermentationList.append(Button(pagePlatformInfo, text="4", relief = SUNKEN, fg=self.colorORT, bg = 'white', font=self.buttonFont, compound=CENTER, height = 2, width = 4, command=lambda:self.showPageOfListFermentations(controller, 4)))
        self.pageNumberOfFermentationList[3].place(x=520, y=475)
        self.pageNumberOfFermentationList.append(Button(pagePlatformInfo, text="5", relief = SUNKEN, fg=self.colorORT, bg = 'white', font=self.buttonFont, compound=CENTER, height = 2, width = 4, command=lambda:self.showPageOfListFermentations(controller, 5)))
        self.pageNumberOfFermentationList[4].place(x=580, y=475)

    def fillPagePlatformInfo(self, pagePlatformInfo, controller):
        self.fillPagePlatformInfoPictures(pagePlatformInfo)
        self.configureFermentationList(pagePlatformInfo, controller)
        self.fillPagePlatformInfoTitles(pagePlatformInfo, controller)
        self.fillPagePlatformInfoEntries(pagePlatformInfo)
        self.fillPagePlatformInfoButtons(pagePlatformInfo, controller)

    def configureUsersInformationGraphics(self, pageStatistics, controller, monthsHistoryConsidered):
        self.systemUsersInformationCanvas = FigureCanvasTkAgg(self.systemUsersInformationFigure, pageStatistics)
        monthsQuantity = len(monthsHistoryConsidered)
        professorsRegisteredQuantity = controller.application.systemData.getProfessorsQuantityHistory() #(90, 55, 40, 65, 30, 32}
        studentsRegisteredQuantity = controller.application.systemData.getStudentsQuantityHistory() #(85, 62, 54, 20, 40, 44)
        self.systemUsersInformationGraphic.bar(np.arange(monthsQuantity), professorsRegisteredQuantity, 0.2, alpha=0.8, color='blue', label='Professors')
        self.systemUsersInformationGraphic.bar(np.arange(monthsQuantity) + 0.2, studentsRegisteredQuantity, 0.2, alpha=0.8, color='green', label='Students')
        self.systemUsersInformationGraphic.set_xlabel(controller.currentLanguage.adminPageContent[143], color='white')
        self.systemUsersInformationGraphic.set_ylabel(controller.currentLanguage.adminPageContent[144], color='white')
        self.systemUsersInformationGraphic.set_xticks([0, 1, 2, 3, 4, 5])
        self.systemUsersInformationGraphic.set_xticklabels(monthsHistoryConsidered, color='white')  #['March 2019','April 2019','May 2019', 'June 2019', 'July 2019', 'August 2019'], color='white')
        #self.systemUsersInformationGraphic.set_yticks(color='white')
        self.systemUsersInformationGraphic.set_title(controller.currentLanguage.adminPageContent[145], color='white')
        self.systemUsersInformationFigure.legend(shadow=True, loc='upper right') #, bbox_to_anchor=(0.5, 0.5))
        self.systemUsersInformationGraphic.grid(axis='y', color='black', linestyle='--', linewidth=1)
        #self.systemUsersInformationGraphic.rc_context({'axes.edgecolor':'orange', 'ytick.color':'black', 'figure.facecolor':'white'})
        self.systemUsersInformationFigure.tight_layout()
        self.systemUsersInformationCanvas.draw()
        self.systemUsersInformationCanvas.get_tk_widget().place(x=0, y=0)

    def configureFermentationsInformationGraphics(self, pageStatistics, controller, monthsHistoryConsidered):
        self.systemFermentationsInformationCanvas = FigureCanvasTkAgg(self.systemFermentationsInformationFigure, pageStatistics)
        monthsQuantity = len(monthsHistoryConsidered)
        fermentationsInitiatedQuantity = controller.application.systemData.getFermentationsInitiatedQuantityHistory()  #(90, 55, 40, 65, 30, 32)
        fermentationsContinuedQuantity = controller.application.systemData.getFermentationsContinuedQuantityHistory() #(85, 62, 54, 20, 40, 44)
        self.systemFermentationsInformationGraphic.bar(np.arange(monthsQuantity), fermentationsInitiatedQuantity, 0.2, alpha=0.8, color='black', label='Initiated')
        self.systemFermentationsInformationGraphic.bar(np.arange(monthsQuantity) + 0.2, fermentationsContinuedQuantity, 0.2, alpha=0.8, color='red', label='Continued')
        self.systemFermentationsInformationGraphic.set_xlabel(controller.currentLanguage.adminPageContent[143], color='white')
        self.systemFermentationsInformationGraphic.set_ylabel(controller.currentLanguage.adminPageContent[146], color='white')
        self.systemFermentationsInformationGraphic.set_xticks([0, 1, 2, 3, 4, 5])
        self.systemFermentationsInformationGraphic.set_xticklabels(controller.currentLanguage.adminPageContent[147], color='white')
        #self.systemUsersInformationGraphic.set_yticklabels(color='white')
        self.systemFermentationsInformationGraphic.set_title(controller.currentLanguage.adminPageContent[148], color='white')
        self.systemFermentationsInformationFigure.legend(shadow=True, loc='upper right')
        self.systemFermentationsInformationGraphic.grid(axis='y', color='green', linestyle='--', linewidth=1)
        self.systemFermentationsInformationFigure.tight_layout()
        self.systemFermentationsInformationCanvas.draw()
        self.systemFermentationsInformationCanvas.get_tk_widget().place(x=680, y=0)

    def fillPageStatistics(self, pageStatistics, controller):
        monthsHistoryConsidered = controller.application.systemData.getDatesConsidered()
        self.configureUsersInformationGraphics(pageStatistics, controller, monthsHistoryConsidered)
        self.configureFermentationsInformationGraphics(pageStatistics, controller, monthsHistoryConsidered)

    def setImagesOnPageStatus(self, pageStatus):
        controlsElement = Picture(['controlsElement','png',260,120,130,440],0)
        controlsElement.purpose = 'Words'
        controlsElementPic = controlsElement.generateLabel(pageStatus)
        controlsElementPic.place(x=controlsElement.location[0],y=controlsElement.location[1])

        verificationElement = Picture(['verificationsElement','png',400,120,470,0],0)
        verificationElement.purpose = 'Words'
        verificationElementPic = verificationElement.generateLabel(pageStatus)
        verificationElementPic.place(x=verificationElement.location[0],y=verificationElement.location[1])

        gamesHorizontalElement = Picture(['gamesElementHorizontal','png',260,120,1040,440],0)
        gamesHorizontalElement.purpose = 'Words'
        gamesHorizontalElementPic = gamesHorizontalElement.generateLabel(pageStatus)
        gamesHorizontalElementPic.place(x=gamesHorizontalElement.location[0],y=gamesHorizontalElement.location[1])

    def configureControlsGraphic(self, pageStatus, controller):
        self.systemControlsInformationCanvas = FigureCanvasTkAgg(self.systemControlsInformationFigure, pageStatus)
        sizes = controller.application.systemData.getCurrentMonthControlsInformation() #[28.4, 35, 20.7, 10.3, 5.3, 4.7, 5.6] # APPROPIATE WITH INFORMATION
        labels = ['VEL', 'TEMP', 'POT', 'VEL\n + \nTEMP', 'VEL\n+\nPOT', 'TEMP\n+\nPOT', 'VEL+\nTEMP+\n POT']
        colors = ['blue', 'red', 'green', 'purple', 'cyan', 'orange', 'black' ]
        _, texts, autotexts = self.systemControlsInformationGraphic.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
        for text in texts:
            text.set_color('white')
        for autotext in autotexts:
            autotext.set_color('white')
        #self.systemControlsInformationFigure.axis('equal')
        self.systemControlsInformationFigure.tight_layout()
        self.systemControlsInformationCanvas.draw()
        self.systemControlsInformationCanvas.get_tk_widget().place(x=0, y=0)

    def configureVerificationGraphic(self, pageStatus, controller):
        self.systemVerificationInformationCanvas = FigureCanvasTkAgg(self.systemVerificationInformationFigure, pageStatus)
        sizes = controller.application.systemData.getCurrentMonthVerificationsInformation() #[38.4, 40.6, 20.7, 10.3]
        labels = controller.currentLanguage.adminPageContent[149]
        colors = ['red', 'orange', 'blue', 'green']
        _, texts, autotexts = self.systemVerificationInformationGraphic.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=45)
        for text in texts:
            text.set_color('white')
        for autotext in autotexts:
            autotext.set_color('white')
        #self.systemControlsInformationFigure.axis('equal')
        self.systemVerificationInformationFigure.tight_layout()
        self.systemVerificationInformationCanvas.draw()
        self.systemVerificationInformationCanvas.get_tk_widget().place(x=455, y=100)

    def configureGamesGraphic(self, pageStatus, controller):
        self.systemGamesInformationCanvas = FigureCanvasTkAgg(self.systemGamesInformationFigure, pageStatus)
        labels = controller.currentLanguage.adminPageContent[150]
        sizes = [38.4, 40.6, 31] #controller.application.systemData.getCurrentMonthGamesInformation()
        colors = ['blue', 'red', 'green']
        _, texts, autotexts = self.systemGamesInformationGraphic.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=45)
        for text in texts:
            text.set_color('white')
        for autotext in autotexts:
            autotext.set_color('white')
        #self.systemControlsInformationFigure.axis('equal')
        self.systemGamesInformationFigure.tight_layout()
        self.systemGamesInformationCanvas.draw()
        self.systemGamesInformationCanvas.get_tk_widget().place(x=910, y=0)

    def setPageStatusGraphics(self, pageStatus, controller):
        self.configureControlsGraphic(pageStatus, controller)
        self.configureVerificationGraphic(pageStatus, controller)
        self.configureGamesGraphic(pageStatus, controller)

    def fillPageStatus(self, pageStatus, controller):
        self.setImagesOnPageStatus(pageStatus)
        self.setPageStatusGraphics(pageStatus, controller)

    def fillPageVersionPictures(self, pageVersion, controller):
        controller.setImagesandSeparators(pageVersion, 'versionElement', [115,270,1250,10,115,270,1250,290])
        versionsHistoryElement = Picture(['versionsHistoryElement','png',130,550,10,10],0)
        versionsHistoryElement.purpose = 'Words'
        versionsHistoryElementPic = versionsHistoryElement.generateLabel(pageVersion)
        versionsHistoryElementPic.place(x=versionsHistoryElement.location[0],y=versionsHistoryElement.location[1])
        separatorVersion = Picture(['userInfoSeparator','png',140,550,640,0],0)
        separatorVersion.purpose = 'Separators'
        separatorVersionPic = separatorVersion.generateLabel(pageVersion)
        separatorVersionPic.place(x=separatorVersion.location[0],y=separatorVersion.location[1])

    def fillPageVersionTitles(self, pageVersion, controller):
        velocityVersionBorder = Label(pageVersion, bg = self.colorORT, height=10, width=67, borderwidth=2, relief='solid', highlightbackground='blue')
        velocityVersionBorder.place(x=780, y=5)
        self.velocityVersionTitle = Label(pageVersion, text=controller.currentLanguage.userPageContent[143], font=self.buttonFont, fg = 'blue', bg = self.colorORT)
        self.velocityVersionTitle.place(x=785, y=10)

        temperatureVersionBorder = Label(pageVersion, bg = self.colorORT, height=10, width=67, borderwidth=2, relief='solid', highlightbackground='orange')
        temperatureVersionBorder.place(x=780, y=190)
        self.temperatureVersionTitle = Label(pageVersion, text=controller.currentLanguage.userPageContent[144], font=self.buttonFont, fg = 'orange', bg = self.colorORT)
        self.temperatureVersionTitle.place(x=785, y=195)

        potentialVersionBorder = Label(pageVersion, bg = self.colorORT, height=10, width=67, borderwidth=2, relief='solid', highlightbackground='lime green')
        potentialVersionBorder.place(x=780, y=375)
        self.potentialVersionTitle = Label(pageVersion, text=controller.currentLanguage.userPageContent[145], font=self.buttonFont, fg = 'lime green', bg = self.colorORT)
        self.potentialVersionTitle.place(x=785, y=380)

    def fillPageVersionEntries(self, pageVersion, controller):
        self.velocityVersion = Label(pageVersion, text=controller.currentLanguage.userPageContent[147], bg=self.colorORT, fg = 'blue', font=self.groupMessageFont, compound=CENTER)
        self.velocityVersion.place(x=900, y=60)
        self.temperatureVersion = Label(pageVersion, text=controller.currentLanguage.userPageContent[147], bg=self.colorORT, fg = 'orange', font=self.groupMessageFont, compound=CENTER)
        self.temperatureVersion.place(x=900, y=240)
        self.potentialVersion = Label(pageVersion, text=controller.currentLanguage.userPageContent[147], bg=self.colorORT, fg = 'lime green', font=self.groupMessageFont, compound=CENTER)
        self.potentialVersion.place(x=900, y=430)

        self.velocityVersionCommentary = Entry(pageVersion, fg = 'blue', bg='white', width = 20, font=self.groupMessageFont)
        self.velocityVersionCommentary.place(x=850, y=110)
        self.temperatureVersionCommentary = Entry(pageVersion,  fg = 'orange', bg='white', width = 20, font=self.groupMessageFont)
        self.temperatureVersionCommentary.place(x=850, y=290)
        self.potentialVersionCommentary = Entry(pageVersion, fg = 'lime green', bg='white', width = 20, font=self.groupMessageFont)
        self.potentialVersionCommentary.place(x=850, y=480)

    def fillVersionsList(self, controller):
        allListsVersions = []
        for eachVersion in controller.application.versionsHistory.velocityVersions:
            allListsVersions.append(eachVersion)
        for eachVersion in controller.application.versionsHistory.temperatureVersions:
            allListsVersions.append(eachVersion)
        for eachVersion in controller.application.versionsHistory.potentialVersions:
            allListsVersions.append(eachVersion)
        if(len(allListsVersions)>0):
            self.versionsList.delete(0,END)
            positionGraphicList = 1
            positionGlobalList = 0
            for aVersion in versionsLists:
                if(positionGlobalList>=self.pageOfListVersions*self.usersPerPage and positionGlobalList<(self.pageOfListVersions+1)*self.usersPerPage):
                    self.versionsList.insert(positionGraphicList, aVersion.showInformation())
                    positionGraphicList = positionGraphicList + 1
                positionGlobalList = positionGlobalList + 1
        else:
            self.versionsList.delete(0,END)
            self.versionsList.insert(1, controller.currentLanguage.adminPageContent[121])

    def fillPageVersionList(self, pageVersion, controller):
        self.versionsList = Listbox(pageVersion, width=83, height=28, font=self.listElementFont)
        self.versionsList.place(x=140,y=10)
        self.fillVersionsList(controller)

    def checkVelocityVersion(self, controller):
        print("VELOCITY VERSION")
        controller.settingVelocityControl[0] = 13
        while(controller.settingVelocityControl[0] == 13):
            var = 1 + 1
        if(controller.settingVelocityControl[16] > 0):
            #controller.application.versionNumber[0] = float(controller.settingVelocityControl[16]/100)
            self.velocityVersion['text'] = "Version "+ str(float(controller.settingVelocityControl[16]/100))
            possibleNewVersion = Version(float(controller.settingVelocityControl[16]/100), "")
            controller.application.versionsHistory.addMagnitudeVersion(controller.application.versionsHistory.velocityVersions, possibleNewVersion)
            self.fillVersionsList(controller)
        else:
            self.velocityVersion['text'] = "ERROR"

    def checkTemperatureVersion(self, controller):
        print("TEMPERATURE VERSION")
        controller.settingTemperatureControl[0] = 13
        while(controller.settingTemperatureControl[0] == 13):
            var = 1 + 1
        if(controller.settingTemperatureControl[16] > 0):
            #controller.application.versionNumber[1] = float(controller.settingTemperatureControl[16]/100)
            self.temperatureVersion['text'] = "Version "+ str(float(controller.settingTemperatureControl[16]/100))
            possibleNewVersion = Version(float(controller.settingTemperatureControl[16]/100), "")
            controller.application.versionsHistory.addMagnitudeVersion(controller.application.versionsHistory.temperatureVersions, possibleNewVersion)
            self.fillVersionsList(controller)
        else:
            self.temperatureVersion['text'] = "ERROR"

    def checkPotentialVersion(self, controller):
        print("POTENTIAL VERSION")
        controller.settingPotentialControl[0] = 13
        while(controller.settingPotentialControl[0] == 13):
            var = 1 + 1
        if(controller.settingPotentialControl[16] > 0):
            #controller.application.versionNumber[2] = float(controller.settingPotentialControl[16]/100)
            self.potentialVersion['text'] = "Version "+ str(float(controller.settingPotentialControl[16]/100))
            possibleNewVersion = Version(float(controller.settingPotentialControl[16]/100), "")
            controller.application.versionsHistory.addMagnitudeVersion(controller.application.versionsHistory.potentialVersions, possibleNewVersion)
            self.fillVersionsList(controller)
        else:
            self.potentialVersion['text'] = "ERROR"

    def setVelocityCommentary(self, controller):
        #controller.application.versionCommentary[0] = str(self.velocityVersionCommentary.get())
        currentVersion = Version(float(controller.settingVelocityControl[16]/100), "")
        controller.application.versionsHistory.setCommentaryOfMagnitudeVersion(controller.application.versionsHistory.velocityVersions, currentVersion, "VEL: "+str(self.velocityVersionCommentary.get()))
        self.fillVersionsList(controller)
        messagebox.showinfo(controller.currentLanguage.adminPageContent[117], controller.currentLanguage.adminPageContent[118])

    def setTemperatureCommentary(self, controller):
        #controller.application.versionCommentary[1] = str(self.temperatureVersionCommentary.get())
        currentVersion = Version(float(controller.settingTemperatureControl[16]/100), "")
        controller.application.versionsHistory.setCommentaryOfMagnitudeVersion(controller.application.versionsHistory.temperatureVersions, currentVersion, "TEMP: "+str(self.temperatureVersionCommentary.get()))
        self.fillVersionsList(controller)
        messagebox.showinfo(controller.currentLanguage.adminPageContent[117], controller.currentLanguage.adminPageContent[118])

    def setPotentialCommentary(self, controller):
        #controller.application.versionCommentary[2] = str(self.potentialVersionCommentary.get())
        currentVersion = Version(float(controller.settingPotentialControl[16]/100), "")
        controller.application.versionsHistory.setCommentaryOfMagnitudeVersion(controller.application.versionsHistory.potentialVersions, currentVersion, "PH: "+str(self.potentialVersionCommentary.get()))
        self.fillVersionsList(controller)
        messagebox.showinfo(controller.currentLanguage.adminPageContent[117], controller.currentLanguage.adminPageContent[118])

    def clearAllVersions(self, controller):
        if(len(controller.application.versionsHistory.velocityVersions)>0):
            controller.application.versionsHistory.removeAllVersionsOfMagnitude(controller.application.versionsHistory.velocityVersions)
        if(len(controller.application.versionsHistory.temperatureVersions)>0):
            controller.application.versionsHistory.removeAllVersionsOfMagnitude(controller.application.versionsHistory.temperatureVersions)
        if(len(controller.application.versionsHistory.potentialVersions)>0):
            controller.application.versionsHistory.removeAllVersionsOfMagnitude(controller.application.versionsHistory.potentialVersions)

    def showPageOfListVersions(self, controller, numberOfPage):
        for eachButton in self.pageNumberOfVersionsList:
            eachButton['bg']='white'
        self.pageOfListVersions = numberOfPage-1
        self.pageNumberOfVersionsList[self.pageOfListVersions]['bg'] = 'yellow'
        self.fillVersionsList(controller)

    def fillPageVersionButtons(self, pageVersion, controller):
        self.velocityVersionOption = Button(pageVersion, text=controller.currentLanguage.userPageContent[146], command = lambda:self.checkVelocityVersion(controller), relief = SUNKEN, fg='white', bg = 'blue', font=self.buttonFont, compound=CENTER, height = 3, width = 10)
        self.velocityVersionOption.place(x=1120, y=6)
        self.temperatureVersionOption = Button(pageVersion, text=controller.currentLanguage.userPageContent[146], command = lambda:self.checkTemperatureVersion(controller), relief = SUNKEN, fg='white', bg = 'orange', font=self.buttonFont, compound=CENTER, height = 3, width = 10)
        self.temperatureVersionOption.place(x=1120, y=192)
        self.potentialVersionOption = Button(pageVersion, text=controller.currentLanguage.userPageContent[146], command = lambda:self.checkPotentialVersion(controller), relief = SUNKEN, fg='white', bg = 'lime green', font=self.buttonFont, compound=CENTER, height = 3, width = 10)
        self.potentialVersionOption.place(x=1120, y=378)
        self.velocityVersionCommentaryOption = Button(pageVersion, text=controller.currentLanguage.adminPageContent[116], command = lambda:self.setVelocityCommentary(controller), relief = SUNKEN, fg='white', bg = 'black', font=self.buttonFontSmaller, compound=CENTER, height = 4, width = 12)
        self.velocityVersionCommentaryOption.place(x=1120, y=75)
        self.temperatureVersionCommentaryOption = Button(pageVersion, text=controller.currentLanguage.adminPageContent[116], command = lambda:self.setTemperatureCommentary(controller), relief = SUNKEN, fg='white', bg = 'black', font=self.buttonFontSmaller, compound=CENTER, height = 4, width = 12)
        self.temperatureVersionCommentaryOption.place(x=1120, y=260)
        self.potentialVersionCommentaryOption = Button(pageVersion, text=controller.currentLanguage.adminPageContent[116], command = lambda:self.setPotentialCommentary(controller), relief = SUNKEN, fg='white', bg = 'black', font=self.buttonFontSmaller, compound=CENTER, height = 4, width = 12)
        self.potentialVersionCommentaryOption.place(x=1120, y=445)
        self.clearVersionsOption = Button(pageVersion, text=controller.currentLanguage.adminPageContent[120], relief = SUNKEN, fg='white', bg = 'black', font=self.buttonFont, compound=CENTER, height = 3, width = 16, command=lambda:self.clearAllVersions(controller))
        self.clearVersionsOption.place(x=140, y=465)
        self.pageNumberOfVersionsList.append(Button(pageVersion, text="1", relief = SUNKEN, fg=self.colorORT, bg = 'yellow', font=self.buttonFont, compound=CENTER, height = 2, width = 4, command=lambda:self.showPageOfListVersions(controller, 1)))
        self.pageNumberOfVersionsList[0].place(x=340, y=475)
        self.pageNumberOfVersionsList.append(Button(pageVersion, text="2", relief = SUNKEN, fg=self.colorORT, bg = 'white', font=self.buttonFont, compound=CENTER, height = 2, width = 4, command=lambda:self.showPageOfListVersions(controller, 2)))
        self.pageNumberOfVersionsList[1].place(x=400, y=475)
        self.pageNumberOfVersionsList.append(Button(pageVersion, text="3", relief = SUNKEN, fg=self.colorORT, bg = 'white', font=self.buttonFont, compound=CENTER, height = 2, width = 4, command=lambda:self.showPageOfListVersions(controller, 3)))
        self.pageNumberOfVersionsList[2].place(x=460, y=475)
        self.pageNumberOfVersionsList.append(Button(pageVersion, text="4", relief = SUNKEN, fg=self.colorORT, bg = 'white', font=self.buttonFont, compound=CENTER, height = 2, width = 4, command=lambda:self.showPageOfListVersions(controller, 4)))
        self.pageNumberOfVersionsList[3].place(x=520, y=475)
        self.pageNumberOfVersionsList.append(Button(pageVersion, text="5", relief = SUNKEN, fg=self.colorORT, bg = 'white', font=self.buttonFont, compound=CENTER, height = 2, width = 4, command=lambda:self.showPageOfListVersions(controller, 5)))
        self.pageNumberOfVersionsList[4].place(x=580, y=475)

    def fillPageVersion(self, pageVersion, controller):
        self.fillPageVersionPictures(pageVersion, controller)
        self.fillPageVersionTitles(pageVersion, controller)
        self.fillPageVersionEntries(pageVersion, controller)
        self.fillPageVersionList(pageVersion, controller)
        self.fillPageVersionButtons(pageVersion, controller)

    def fillPageSettingsDynamicInformation(self, pageSettings, controller):
        currentId = Label(pageSettings, text=controller.application.admin.usernumber, font=self.inputFont, fg = 'white', bg = self.colorORT)
        currentId.place(x=393, y=48)
        currentPassword = Label(pageSettings, text=controller.application.admin.password, font=self.inputFont, fg = 'white', bg = self.colorORT)
        currentPassword.place(x=448, y=208)
        usersAdded = Label(pageSettings, text=str(controller.application.admin.usersAdded)+controller.currentLanguage.adminPageContent[151]+str(controller.application.admin.registrationDate), font=self.inputFont, fg = 'white', bg = self.colorORT)
        usersAdded.place(x=988, y=208)
        usersDeleted = Label(pageSettings, text=str(controller.application.admin.usersDeleted)+controller.currentLanguage.adminPageContent[151]+str(controller.application.admin.registrationDate), font=self.inputFont, fg = 'white', bg = self.colorORT)
        usersDeleted.place(x=988, y=298)

    def fillPageSettingsTitles(self, pageSettings, controller):
        self.currentIdTitle = Label(pageSettings, text=controller.currentLanguage.adminPageContent[106], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.currentIdTitle.place(x=130, y=40)
        self.newIdTitle = Label(pageSettings, text=controller.currentLanguage.adminPageContent[107], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.newIdTitle.place(x=130, y=110)
        self.currentPasswordTitle = Label(pageSettings, text=controller.currentLanguage.adminPageContent[108], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.currentPasswordTitle.place(x=130, y=200)
        self.newPasswordTitle = Label(pageSettings, text=controller.currentLanguage.adminPageContent[109], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.newPasswordTitle.place(x=130, y=290)
        self.confirmPasswordTitle = Label(pageSettings, text=controller.currentLanguage.adminPageContent[110], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.confirmPasswordTitle.place(x=130, y=380)
        self.platformEmailTitle = Label(pageSettings, text=controller.currentLanguage.adminPageContent[111], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.platformEmailTitle.place(x=710, y=40)
        self.platformEmail = Label(pageSettings, text="smartFermentor@gmail.com", font=self.inputFont, fg = 'white', bg = self.colorORT)
        self.platformEmail.place(x=980, y=48)
        self.platformEmailPasswordTitle = Label(pageSettings, text=controller.currentLanguage.adminPageContent[112], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.platformEmailPasswordTitle.place(x=710, y=110)
        self.platformEmailPassword = Label(pageSettings, text="Smart.1450", font=self.inputFont, fg = 'white', bg = self.colorORT)
        self.platformEmailPassword.place(x=1020, y=118)
        self.usersAddedTitle = Label(pageSettings, text=controller.currentLanguage.adminPageContent[113], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.usersAddedTitle.place(x=710, y=200)
        self.usersDeletedTitle = Label(pageSettings, text=controller.currentLanguage.adminPageContent[114], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.usersDeletedTitle.place(x=710, y=290)

    def fillPageSettingsEntries(self, pageSettings):
        self.adminDataEdition.append(Entry(pageSettings, font=self.inputFont, width=20, justify='center')) # usernameInput
        self.adminDataEdition[0].place(x=368, y=118)
        self.adminDataEdition.append(Entry(pageSettings, font=self.inputFont, width=20, justify='center')) # passwordInput
        self.adminDataEdition[1].place(x=398, y=298)
        self.adminDataEdition.append(Entry(pageSettings, font=self.inputFont, width=20, justify='center')) # confirmPasswordInput
        self.adminDataEdition[2].place(x=398, y=388)

    def fillPageSettingsPictures(self, pageSettings, controller):
        controller.setImagesandSeparators(pageSettings, 'settingsElement', [115,280,10,0,115,280,10,290])
        controller.setImagesandSeparators(pageSettings, 'settingsElement', [115,280,1260,0,115,280,1260,290])
        separatorSettings = Picture(['settingsSeparator','png',130,550,580,0],0)
        separatorSettings.purpose = 'Separators'
        separatorSettingsPic = separatorSettings.generateLabel(pageSettings)
        separatorSettingsPic.place(x=separatorSettings.location[0],y=separatorSettings.location[1])

    def checkAdminPassword(self, controller):
        anAdmin = User(["","","","","","","","",""])
        anAdmin.password = self.adminDataEdition[1].get()
        adminPasswordSaved = 2
        if(anAdmin.isPasswordRight() or self.adminDataEdition[1].get()==self.adminDataEdition[2].get()):
            self.previousAdminPassword = controller.application.admin.password
            controller.application.admin.password = self.adminDataEdition[1].get()
            adminPasswordSaved = adminPasswordSaved + 2
            self.adminDataEdition[1].delete(0,END)
            self.adminDataEdition[2].delete(0,END)
        return adminPasswordSaved

    def checkAdminData(self, controller):
        adminDataSaved = 0
        if(self.adminDataEdition[0].get()!=""):
            self.previousAdminUsernumber = controller.application.admin.usernumber
            controller.application.admin.usernumber = self.adminDataEdition[0].get()
            adminDataSaved = 1
            self.adminDataEdition[0].delete(0,END)
        if(self.adminDataEdition[1].get()!="" or self.adminDataEdition[2].get()!=""):
            adminDataSaved = adminDataSaved + self.checkAdminPassword(controller)
        return adminDataSaved

    def saveAdminData(self, pageSettings, controller):
        adminDataStatus = self.checkAdminData(controller)
        if(adminDataStatus==0):
            messagebox.showwarning(controller.currentLanguage.adminPageContent[15], controller.currentLanguage.adminPageContent[90])
        elif(adminDataStatus==1):
            messagebox.showinfo(controller.currentLanguage.adminPageContent[91], controller.currentLanguage.adminPageContent[92])
        elif(adminDataStatus==2):
            messagebox.showerror(controller.currentLanguage.adminPageContent[50], controller.currentLanguage.adminPageContent[93])
        elif(adminDataStatus==3):
            administratorUsernumberChangedBodyMail = "\n\n"+controller.application.getDayTimeMomentMessage(controller.currentLanguage.adminPageContent[162])+", "+controller.currentLanguage.adminPageContent[152]+self.previousAdminUsernumber+controller.currentLanguage.adminPageContent[156]+controller.application.admin.usernumber+"  .\n\n"+controller.currentLanguage.adminPageContent[155]
            controller.application.sendEmail(['smartFermentor@gmail.com'], [controller.currentLanguage.adminPageContent[157], 'Images/MailContent/userDataChangedMail.png', administratorUsernumberChangedBodyMail, "IMAGE"])
            messagebox.showinfo(controller.currentLanguage.adminPageContent[91], controller.currentLanguage.adminPageContent[94])
        elif(adminDataStatus==4):
            administratorPasswordChangedBodyMail = "\n\n"+controller.application.getDayTimeMomentMessage(controller.currentLanguage.adminPageContent[162])+", "+controller.currentLanguage.adminPageContent[153]+self.previousAdminPassword+controller.currentLanguage.adminPageContent[156]+controller.application.admin.password+"  .\n\n"+controller.currentLanguage.adminPageContent[155]
            controller.application.sendEmail(['smartFermentor@gmail.com'], [controller.currentLanguage.adminPageContent[157], 'Images/MailContent/passwordModificationMail.png', administratorPasswordChangedBodyMail, "IMAGE"])
            messagebox.showinfo(controller.currentLanguage.adminPageContent[95], controller.currentLanguage.adminPageContent[96])
        elif(adminDataStatus==5):
            administratorDataChangedBodyMail = "\n\n"+controller.application.getDayTimeMomentMessage(controller.currentLanguage.adminPageContent[162])+", "+controller.currentLanguage.adminPageContent[154]+self.previousAdminUsernumber+", "+self.previousAdminPassword+controller.currentLanguage.adminPageContent[156]+controller.application.admin.showParticularInitialData()+"  .\n\n"+controller.currentLanguage.adminPageContent[155]
            controller.application.sendEmail(['smartFermentor@gmail.com'], [controller.currentLanguage.adminPageContent[157], 'Images/MailContent/userDataChangedMail.png', administratorDataChangedBodyMail, "IMAGE"])
            messagebox.showinfo(controller.currentLanguage.adminPageContent[97], controller.currentLanguage.adminPageContent[98])
        self.fillPageSettingsDynamicInformation(pageSettings, controller)

    def clearAllProfessors(self, controller):
        if (messagebox.askquestion(controller.currentLanguage.adminPageContent[123], controller.currentLanguage.adminPageContent[124], icon='warning')=='yes'):
            if(len(controller.application.listProfessors.professors)>0):
                allProfessorsEmails = controller.application.listProfessors.getAllMailFromList()
                removeAllProfessorsBodyMail = "\n\n"+controller.application.getDayTimeMomentMessage(controller.currentLanguage.adminPageContent[162])+", "+controller.currentLanguage.adminPageContent[133]+",\n\n    "+controller.currentLanguage.adminPageContent[158]
                controller.application.sendEmail([allProfessorsEmails], [controller.currentLanguage.adminPageContent[132], 'Images/MailContent/erasedFromSystemMail.png', removeAllProfessorsBodyMail, "IMAGE"])
                controller.application.listProfessors.clearProfessorsList()
                controller.fillProfessorsList(self.professorsList, self.pageOfListProfessors)
                controller.fillProfessorsList(self.professorsListEdition, self.pageOfListProfessorsToEdit)
                messagebox.showinfo(controller.currentLanguage.adminPageContent[80], controller.currentLanguage.adminPageContent[99])
            else:
                messagebox.showwarning(controller.currentLanguage.adminPageContent[15], controller.currentLanguage.adminPageContent[83])

    def clearAllStudents(self, controller):
        if (messagebox.askquestion(controller.currentLanguage.adminPageContent[125],controller.currentLanguage.adminPageContent[126], icon='warning')=='yes'):
            if(len(controller.application.listStudents.students)>0):
                allStudentsEmails = controller.application.listStudents.getAllMailFromList()
                removeAllStudentsBodyMail = "\n\n"+controller.currentLanguage.adminPageContent[134]+"\n\n    "+controller.currentLanguage.adminPageContent[159]
                controller.application.sendEmail([allStudentsEmails], [controller.currentLanguage.adminPageContent[132], 'Images/MailContent/erasedFromSystemMail.png', removeAllStudentsBodyMail, "IMAGE"])
                controller.application.listStudents.clearStudentsList()
                controller.fillStudentsList(self.studentsList, self.pageOfListStudents)
                controller.fillStudentsList(self.studentsListEdition, self.pageOfListStudentsToEdit)
                messagebox.showinfo(controller.currentLanguage.adminPageContent[80], controller.currentLanguage.adminPageContent[100])
            else:
                messagebox.showwarning(controller.currentLanguage.adminPageContent[15], controller.currentLanguage.adminPageContent[86])

    def clearAllFermentations(self, controller):
        if (messagebox.askquestion(controller.currentLanguage.adminPageContent[127], controller.currentLanguage.adminPageContent[128], icon='warning')=='yes'):
            if(len(controller.application.listFermentations.fermentations)>0):
                allProfessorsEmails = controller.application.listProfessors.getAllMailFromList()
                removeFermentationHistoryBodyMailProfessors = "\n\n"+controller.application.getDayTimeMomentMessage(controller.currentLanguage.adminPageContent[162])+", "+controller.currentLanguage.adminPageContent[133]+",\n\n    "+controller.currentLanguage.adminPageContent[160]
                controller.application.sendEmail([allProfessorsEmails], [controller.currentLanguage.adminPageContent[161], 'Images/MailContent/erasedFromSystemMail.png', removeFermentationHistoryBodyMailProfessors, "IMAGE"])
                allStudentsEmails = controller.application.listStudents.getAllMailFromList()
                removeFermentationHistoryBodyMailStudents = "\n\n"+controller.currentLanguage.adminPageContent[134]+":\n\n    "+controller.currentLanguage.adminPageContent[160]
                controller.application.sendEmail([allStudentsEmails], [controller.currentLanguage.adminPageContent[161], 'Images/MailContent/erasedFromSystemMail.png', removeFermentationHistoryBodyMailStudents, "IMAGE"])
                controller.application.listStudents.clearStudentsList()
                self.fillFermentationsList(controller)
                messagebox.showinfo(controller.currentLanguage.adminPageContent[80], controller.currentLanguage.adminPageContent[101])
            else:
                messagebox.showwarning(controller.currentLanguage.adminPageContent[15], controller.currentLanguage.adminPageContent[74])

    def getTitleForBlockUsersEntry(self, controller):
        titleForBlockUserEntry = ""
        if(controller.application.systemCurrentStatus.isUserEntryBlocked()):
            titleForBlockUserEntry = controller.currentLanguage.adminPageContent[129]
        else:
            titleForBlockUserEntry = controller.currentLanguage.adminPageContent[130]
        return titleForBlockUserEntry

    def blockUserEntryAction(self, controller):
        if(controller.application.systemCurrentStatus.isUserEntryBlocked()):
            controller.application.systemCurrentStatus.blockedEntryTime = datetime(2010, 9, 12, 11, 19, 54)
            self.blockUserEntryOption['text'] = controller.currentLanguage.adminPageContent[130]
        else:
            controller.application.systemCurrentStatus.blockUserEntry()
            self.blockUserEntryOption['text'] = controller.currentLanguage.adminPageContent[129]

    def fillPageSettingsButtons(self, pageSettings, controller):
        self.blockUserEntryOption = Button(pageSettings, text=self.getTitleForBlockUsersEntry(controller), command=lambda: self.blockUserEntryAction(controller), relief = SUNKEN, fg='white', bg = 'DarkGoldenRod4', font=self.buttonFont, compound=CENTER, height = 3, width = 15)
        self.blockUserEntryOption.place(x=140, y=455)
        self.updateAdminInfoOption = Button(pageSettings, text=controller.currentLanguage.adminPageContent[102], command=lambda: self.saveAdminData(pageSettings, controller), relief = SUNKEN, fg='white', bg = 'dark red', font=self.buttonFont, compound=CENTER, height = 3, width = 18)
        self.updateAdminInfoOption.place(x=350, y=455)
        self.eraseProfessorsOption = Button(pageSettings, text=controller.currentLanguage.adminPageContent[103], command=lambda: self.clearAllProfessors(controller), relief = SUNKEN, fg='white', bg = 'dark blue', font=self.buttonFont, compound=CENTER, height = 2, width = 25)
        self.eraseProfessorsOption.place(x=830, y=335)
        self.eraseStudentsOption = Button(pageSettings, text=controller.currentLanguage.adminPageContent[104], command=lambda: self.clearAllStudents(controller), relief = SUNKEN, fg='white', bg = 'green', font=self.buttonFont, compound=CENTER, height = 2, width = 25)
        self.eraseStudentsOption.place(x=830, y=405)
        self.eraseFermentationsOption = Button(pageSettings, text=controller.currentLanguage.adminPageContent[105], command=lambda: self.clearAllFermentations(controller), relief = SUNKEN, fg='white', bg = 'black', font=self.buttonFont, compound=CENTER, height = 2, width = 34)
        self.eraseFermentationsOption.place(x=780, y=475)

    def fillPageSettings(self, pageSettings, controller):
        self.fillPageSettingsTitles(pageSettings, controller)
        self.fillPageSettingsDynamicInformation(pageSettings, controller)
        self.fillPageSettingsEntries(pageSettings)
        self.fillPageSettingsPictures(pageSettings, controller)
        self.fillPageSettingsButtons(pageSettings, controller)

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
        self.pageUsers = Frame(self.nb)
        self.nb.add(self.pageUsers, text=controller.currentLanguage.adminPageContent[4])
        controller.setBackgroundOfTab(self.pageUsers)
        self.fillPageUsers(self.pageUsers, controller)
        self.pageNewUser = Frame(self.nb)
        self.nb.add(self.pageNewUser, text=controller.currentLanguage.adminPageContent[5])
        controller.setBackgroundOfTab(self.pageNewUser)
        self.fillPageNewUser(controller, self.pageNewUser)
        self.pageEditProfessor = Frame(self.nb)
        self.nb.add(self.pageEditProfessor, text=controller.currentLanguage.adminPageContent[6])
        controller.setBackgroundOfTab(self.pageEditProfessor)
        self.fillPageEditProfessor(self.pageEditProfessor, controller)
        self.pageEditStudent = Frame(self.nb)
        self.nb.add(self.pageEditStudent, text=controller.currentLanguage.adminPageContent[7])
        controller.setBackgroundOfTab(self.pageEditStudent)
        self.fillPageEditStudent(self.pageEditStudent, controller)
        self.pageUserInfo = Frame(self.nb)
        self.nb.add(self.pageUserInfo, text=controller.currentLanguage.adminPageContent[8])
        controller.setBackgroundOfTab(self.pageUserInfo)
        self.fillPageUserInfo(self.pageUserInfo, controller)
        self.pagePlatformInfo = Frame(self.nb)
        self.nb.add(self.pagePlatformInfo, text=controller.currentLanguage.adminPageContent[9])
        controller.setBackgroundOfTab(self.pagePlatformInfo)
        self.fillPagePlatformInfo(self.pagePlatformInfo, controller)
        self.pageStatistics = Frame(self.nb)
        self.nb.add(self.pageStatistics, text=controller.currentLanguage.adminPageContent[10])
        controller.setBackgroundOfTab(self.pageStatistics)
        self.fillPageStatistics(self.pageStatistics, controller)
        self.pageStatus = Frame(self.nb)
        self.nb.add(self.pageStatus, text=controller.currentLanguage.adminPageContent[115])
        controller.setBackgroundOfTab(self.pageStatus)
        self.fillPageStatus(self.pageStatus, controller)
        self.pageVersion = Frame(self.nb)
        self.nb.add(self.pageVersion, text=controller.currentLanguage.adminPageContent[119])
        controller.setBackgroundOfTab(self.pageVersion)
        self.fillPageVersion(self.pageVersion, controller)
        #self.fillPagePlatformInfo(pagePlatformInfo)
        #self.settingsImage = PhotoImage(file="Images/Logos/settingsLogo.gif")
        self.pageSettings = Frame(self.nb)
        self.nb.add(self.pageSettings, text=controller.currentLanguage.adminPageContent[11]) #image=self.settingsImage)
        controller.setBackgroundOfTab(self.pageSettings)
        self.fillPageSettings(self.pageSettings, controller)

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.setFonts()
        self.setVariables()
        self.setLists()
        self.placeStaticPictures(controller)
        self.setInformationGraphics()

        rows = 0
        while rows < 50:
            self.rowconfigure(rows, weight=1)
            self.columnconfigure(rows, weight=1)
            rows = rows + 1

        controller.settingScreensControl[2] = 2
        controller.settingScreensControl[1] = 1
        print("INICIA ADMINISTRADOR")
        self.nb = ttk.Notebook(self)
        self.nb.grid(row=10, column=0, columnspan=500, rowspan=490, sticky='NESW')
        self.setTabs(controller)
        self.setHelpBar(controller)
        self.animateWords()
