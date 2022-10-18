import sys
import time
from tkinter import *
from tkinter import ttk, messagebox
import tkinter.font
from PIL import Image, ImageTk
from MonitorConsole.HomePage import HomePage
from MonitorConsole.AdminPage import AdminPage
from MonitorConsole.StudentPage import StudentPage
from MonitorConsole.ProfessorPage import ProfessorPage
from MonitorConsole.FermentationPage import FermentationPage
from MonitorConsole.Picture import Picture
from Domain.SmartFermentorApp import SmartFermentorApp
from MonitorConsole.OriginalLanguage import OriginalLanguage
from multiprocessing import Process, Array
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

class SmartManagementInterface(Tk):

    application = SmartFermentorApp()
    settingVelocityControl = Array('i', [0] * 23) # 6
    valuesVelocityControl = Array('i', [0] * 20)
    durationVelocityControl = Array('i', [0] * 20)

    settingTemperatureControl = Array('i', [0] * 25) # 6
    valuesTemperatureControl = Array('i', [0] * 20)
    durationTemperatureControl = Array('i', [0] * 20)

    settingPotentialHydrogenControl = Array('i', [0] * 24) # 6
    valuesPotentialHydrogenControl = Array('i', [0] * 20)
    durationPotentialHydrogenControl = Array('i', [0] * 20)

    settingScreensControl = Array('i', [0] * 23)

    currentLanguage = OriginalLanguage()

    gamesManager = Array('i', [0] * 5)

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.settingVelocityControl[0] = 1
        self.settingTemperatureControl[0] = 1
        self.settingPotentialHydrogenControl[0] = 1
        self.settingScreensControl[0] = 1

        self.container = Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)



        self.extension = [466, 268]
        self.frames = {}

        #for F in (HomePage):
        #    frame = F(self.container, self)
        #    self.frames[F] = frame
        #    frame.grid(row=0, column=0, sticky="nsew")
        frame = HomePage(self.container, self)
        self.frames[HomePage] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(HomePage)

    def show_frame(self, context):
        frame = self.frames[context]
        frame.tkraise()

    def show_frameAdministrator(self):
        try:
            frame = AdminPage(self.container, self)
            self.frames[AdminPage] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            self.show_frame(AdminPage)
        except TclError:
            self.show_frame(AdminPage)

    def show_frameStudent(self):
        frame = StudentPage(self.container, self)
        self.frames[StudentPage] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StudentPage)

    def show_frameProfessor(self):
        frame = ProfessorPage(self.container, self)
        self.frames[ProfessorPage] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(ProfessorPage)

    def show_frameFermentation(self):
        frame = FermentationPage(self.container, self)
        self.frames[FermentationPage] = frame
        del self.frames[HomePage]
        del self.frames[ProfessorPage]
        frame.grid(row=0, column=0, sticky="nsew")
        print("FRAMES LOADED: ", self.frames)
        self.show_frame(FermentationPage)

    def returnToSession(self):
        if(self.application.isStudentLogged):
            self.show_frameStudent()
        else:
            self.show_frameProfessor()

    def returnHome(self):
        self.show_frame(HomePage)

    def setPersonalStyle(self):
        white = '#ffffff'
        colorORT = "#085454"
        fontNormal = "-family {DejaVu Sans} -size 13 -weight normal -slant roman -underline 0 -overstrike 0"
        fontSelected = "-family {DejaVu Sans} -size 13 -weight bold -slant roman -underline 0 -overstrike 0"

        style = ttk.Style()
        style.theme_create( "MyStyle", parent="alt", settings={
                "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0], "background": colorORT } },
                "TNotebook.Tab": {"configure": {"padding": [20, 10], "background": colorORT, "foreground": white, "font": fontNormal },
                "map":       {"background": [("selected", white)], "foreground": [("selected", colorORT)], "font": [("selected", fontSelected)]},}})
        style.theme_use("MyStyle")

    def setBackgroundOfTab(self, interestedTab):
        tabsBack = Picture(['TabsBackground','png',900+self.extension[0],500+self.extension[1],0,-120],0)
        tabsBackPic = tabsBack.generateLabel(interestedTab)
        tabsBackPic.place(x=tabsBack.location[0],y=tabsBack.location[1])

    def setHeaderSmart(self, interestedPage, imageNameSmart, logOutImage):
        elementSmart = Picture([imageNameSmart,'png',900+self.extension[0],500+self.extension[1],0,0],0)
        elementSmartPic = elementSmart.generateLabel(interestedPage)
        elementSmartPic.place(x=elementSmart.location[0],y=elementSmart.location[1])

        logOutOption = Button(interestedPage, image=logOutImage, command=lambda:self.returnHome(), relief = SUNKEN, compound=CENTER)
        logOutOption.place(x=1250, y=15)

    def setImagesandSeparators(self, pageRelevant, imageName, imageProperties):
        userElement = Picture([imageName,'png',imageProperties[0],imageProperties[1],imageProperties[2],imageProperties[3]],0) # 10 o 1260
        userElement.purpose = 'Words'
        userElementPic = userElement.generateLabel(pageRelevant)
        userElementPic.place(x=userElement.location[0],y=userElement.location[1])

        userElement2 = Picture([imageName,'png',imageProperties[4],imageProperties[5],imageProperties[6],imageProperties[7]],180)
        userElement2.purpose = 'Words'
        userElement2Pic = userElement2.generateLabel(pageRelevant)
        userElement2Pic.place(x=userElement2.location[0],y=userElement2.location[1]-20)

        separatorUsers = Label(pageRelevant, text='----------', font=tkinter.font.Font(family = 'Helvetica', size = 20, weight = 'bold'), bg = "#085454", fg = 'white', borderwidth=0, highlightthickness=0)
        separatorUsers.place(x=imageProperties[2]+15, y=260)

    def isMessageRight(self, messageText):
        return len(messageText.get(1.0,END))>0 and len(messageText.get(1.0,END))<=200

    def fillStudentsList(self, listOfStudents, pageOfListStudent):
        if(len(self.application.listStudents.students)>0):
            listOfStudents.delete(0,END)
            positionGraphicList = 1
            positionGlobalList = 0
            for aStudent in self.application.listStudents.students:
                if(positionGlobalList>=pageOfListStudent*27 and positionGlobalList<(pageOfListStudent+1)*27):
                    listOfStudents.insert(positionGraphicList, aStudent.showUserInfo())
                    positionGraphicList = positionGraphicList + 1
                positionGlobalList = positionGlobalList + 1
        else:
            listOfStudents.delete(0,END)
            listOfStudents.insert(1, self.currentLanguage.adminPageContent[19])

    def fillProfessorsList(self, listOfProfessors, pageOfListProfessor):
        if(len(self.application.listProfessors.professors)>0):
            listOfProfessors.delete(0,END)
            positionGraphicList = 1
            positionGlobalList = 0
            for aProfessor in self.application.listProfessors.professors:
                if(positionGlobalList>=pageOfListProfessor*27 and positionGlobalList<(pageOfListProfessor+1)*27):
                    listOfProfessors.insert(positionGraphicList, aProfessor.showUserInfo())
                    positionGraphicList = positionGraphicList + 1
                positionGlobalList = positionGlobalList + 1
        else:
            listOfProfessors.delete(0,END)
            listOfProfessors.insert(1, self.currentLanguage.adminPageContent[18])
