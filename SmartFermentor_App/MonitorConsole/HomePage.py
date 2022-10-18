import sys, threading, itertools, time, gi
gi.require_version('Wnck', '3.0')
from gi.repository import Wnck
from datetime import datetime, date, timedelta
from tkinter import *
from tkinter import ttk, messagebox
import tkinter.font
from PIL import Image, ImageTk
from MonitorConsole.AdminPage import AdminPage
from MonitorConsole.StudentPage import StudentPage
from MonitorConsole.Picture import Picture
from MonitorConsole.ListPictures import ListPictures
from MonitorConsole.OriginalLanguage import OriginalLanguage
from MonitorConsole.SpanishLanguage import SpanishLanguage
from MonitorConsole.PortugueseLanguage import PortugueseLanguage
from MonitorConsole.GermanLanguage import GermanLanguage
from Domain.Administrator import Administrator
from Domain.Student import Student
from Domain.Professor import Professor
from Domain.User import User

class HomePage(Frame):

    def setFonts(self):
        self.textFont = tkinter.font.Font(family = 'Times New Roman', size = 18, weight = 'bold')
        self.bigTitleFont = tkinter.font.Font(family = 'Helvetica', size = 32, weight = 'bold')
        self.titleFont = tkinter.font.Font(family = 'Helvetica', size = 20, weight = 'bold')
        self.statusFont = tkinter.font.Font(family = 'Helvetica', size = 12, weight = 'bold')
        self.subtitleFont = tkinter.font.Font(family = 'Comic Sans', size = 16, weight = 'bold') #"-family {Comic Sans} -size 16 -weight bold -slant roman -underline 0 -overstrike 0"
        self.groupMessageFont = tkinter.font.Font(family = 'Times New Roman', size = 14, weight = 'normal') # "-family Times -size 14 -weight normal -slant roman -underline 0 -overstrike 0"
        self.bodyMessageFont = tkinter.font.Font(family = 'Times New Roman', size = 12, weight = 'normal') #"-family Times -size 12 -weight normal -slant roman -underline 0 -overstrike 0"
        self.versionFont = tkinter.font.Font(family = 'Times New Roman', size = 8, weight = 'normal')
        self.buttonFont = tkinter.font.Font(family = 'Helvetica', size = 24, weight = 'bold')
        self.passwordFont = tkinter.font.Font(family = 'Times New Roman', size = 14, weight = 'bold')
        self.colorORT = "#085454"

    def setVariables(self):
        self.animatedPictures = ListPictures()
        self.animationLabels = []
        self.timesEntryTried = 0
        self.interval = 0
        self.rotation = [1,0,0]
        self.doneLoading = False
        self.helpDisplayed = False
        self.extensionX = 466
        self.extensionY = 268
        self.showPassword = IntVar()
        self.animationUpExtensionY = 150
        self.animationDownExtensionY = 200
        self.colorSelected = 0
        self.startLetterToShow = 0
        self.startLetterPosition = [[910,185],[945,185],[978,185],[1013,185],[1050,185]]
        self.colorList = ['red', 'orange', 'gold4', 'brown', 'blue', 'purple', 'green', 'white']
        self.userData = []
        self.startTitle = []
        self.movementAnimation = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]

    def displayPictures(self):
        labelsToDisplay = 0
        while(labelsToDisplay<len(self.animationLabels)):
            labelsDisplayed = self.animationLabels[labelsToDisplay]
            pictureDisplayed = self.animatedPictures.pictures[labelsToDisplay]
            labelsDisplayed.place(x=pictureDisplayed.location[0],y=pictureDisplayed.location[1])
            labelsToDisplay = labelsToDisplay + 1

    def changeAnimationLocation(self, moveSpace):
        picturesChanged = 0
        while(picturesChanged<len(self.animatedPictures.pictures)):
            currentPicture = self.animatedPictures.pictures[picturesChanged]
            currentPicture.setLocation(currentPicture.location[0]+moveSpace[picturesChanged][0], currentPicture.location[1]+moveSpace[picturesChanged][1])
            picturesChanged = picturesChanged + 1

    def animateMovementEven(self):
        movementEven = [[-4,0], [-3,0], [2.5,0], [1,0], [3,0], [-4,0], [-4,0], [-4,0], [0,0], [0,0]]
        if(self.interval<=36):
            movementEven = [[2,0], [3,0], [-0.1,0], [-1,0], [-3,0], [2,0], [4,0], [2,0], [0,0], [0,0]]
        return movementEven

    def animateMovementOdd(self):
        movementOdd = [[1.8,0], [3,0], [-1.5,0], [-1,0], [-2.8,0], [1.8,0], [3.5,0], [1.8,0], [0,0], [0,0]]
        if(self.interval<=36):
            movementOdd = [[-3.5,0], [-2.8,0], [3,0], [1,0], [3,0], [-3.5,0], [-3,0], [-3.5,0], [0,0], [0,0]]
        return movementOdd

    def reinitializeAnimationLocation(self, locations):
        picturesReinitialized = 0
        while(picturesReinitialized<len(self.animatedPictures.pictures)):
            currentPicture = self.animatedPictures.pictures[picturesReinitialized]
            currentPicture.setLocation(locations[picturesReinitialized][0], locations[picturesReinitialized][1])
            picturesReinitialized = picturesReinitialized + 1

    def rotateAnimation(self):
        smElement = Picture(['SmElement','png',95,95,774,28],90*self.rotation[0]*self.rotation[2])
        smElement.purpose = 'Animations'
        feElement = Picture(['FeElement','png',95,95,999,28],90*(-1)*self.rotation[0]*self.rotation[2])
        feElement.purpose = 'Animations'
        self.rotation[2] = self.rotation[2] + 1
        if(self.rotation[2]==4):
            self.rotation[2]=0
        self.rotation[1] = 0
        smPic = self.generateLabel(smElement)
        fePic = self.generateLabel(feElement)
        self.animationLabels[8] = smPic
        self.animationLabels[9] = fePic

    def decideVerticalStep(self):
        verticalStep = [5, -5]
        self.rotation[0] = -1
        if (self.interval<=56):
            verticalStep[0] = -5
            verticalStep[1] = 5
            self.rotation[0] = 1
        return verticalStep

    def animateWords(self):
        self.version = ""
        self.version = self.versionInfo['text'][(len(self.versionInfo['text'])-1):len(self.versionInfo['text'])]
        for position in range(0,len(self.versionInfo['text'])-1):
            self.version = self.version + self.versionInfo['text'][position:position+1]
        self.versionInfo['text'] = self.version

    def animate(self):
        self.animateWords()
        if(self.interval==112):
            self.reinitializeAnimationLocation([[1270,100+self.animationUpExtensionY],[725,340+self.animationDownExtensionY],[1270,160+self.animationUpExtensionY],[720,388+self.animationDownExtensionY],[735,405+self.animationDownExtensionY],[1260,195+self.animationUpExtensionY],[720,290+self.animationDownExtensionY],[1275,240+self.animationUpExtensionY],[774,28],[999,28]])
            self.interval=0
        self.rotation[1] = self.rotation[1] + 1
        if(self.rotation[1]==4):
            if(self.startLetterToShow==5):
                self.startLetterToShow = 0
                self.startTitle[0].place(x=1500, y=185)
                self.startTitle[1].place(x=1500, y=185)
                self.startTitle[2].place(x=1500, y=185)
                self.startTitle[3].place(x=1500, y=185)
                self.startTitle[4].place(x=1500, y=185)
            self.rotateAnimation()
            self.startTitle[self.startLetterToShow].place(x=self.startLetterPosition[self.startLetterToShow][0], y=self.startLetterPosition[self.startLetterToShow][1])
            self.startLetterToShow = self.startLetterToShow + 1
            self.welcomeInformation['fg'] = self.colorList[self.colorSelected]
            self.colorSelected = self.colorSelected + 1
        if(self.colorSelected==8):
            self.colorSelected=0
        self.displayPictures()
        self.changeAnimationLocation([[1,0],[0,0],[-1,0],[0,0],[0,0],[1,0],[-0.2,0],[1,0],[0,0],[0,0]]) #Por desvio observado
        if(self.interval%2==0 and self.interval!=0):
            self.movementAnimation = self.animateMovementEven()
        if(self.interval%2!=0):
            self.movementAnimation = self.animateMovementOdd()
        self.changeAnimationLocation(self.movementAnimation)
        step = self.decideVerticalStep()
        self.changeAnimationLocation([[0,step[1]],[0,step[0]],[0,step[1]],[0,step[0]],[0,step[0]],[0,step[1]],[0,step[0]],[0,step[1]],[0,0],[0,0]])
        self.interval = self.interval+1
        self.after(100,lambda:self.animate())

    def generateLabel(self, onePicture):
        oneImage = Image.open(onePicture.getCompleteFilename()).resize((onePicture.dimensions[0],onePicture.dimensions[1]), Image.ANTIALIAS)
        oneImageRendered = ImageTk.PhotoImage(oneImage.rotate(onePicture.orientation))
        imagePic = Label(self, image=oneImageRendered, borderwidth=0, highlightthickness=0)
        imagePic.image = oneImageRendered
        return imagePic

    def getAnimationsLabels(self):
        animatedPicturesQuantity = 0
        animatedLabels = []
        while(animatedPicturesQuantity<len(self.animatedPictures.pictures)):
            animatedLabels.append(self.generateLabel(self.animatedPictures.pictures[animatedPicturesQuantity]))
            animatedPicturesQuantity = animatedPicturesQuantity + 1
        return animatedLabels

    def setTextBox(self, specialCharacter, location, controller):

        def limitSizeInput(*args):
            value = currentInput.get()
            if len(value) > 12:
                currentInput.set(value[:12])

        def checkShowPassword():
            if(self.showPassword.get()==1):
                textInput['show']=''
            else:
                textInput['show']=specialCharacter

        currentInput = StringVar()
        currentInput.trace('w', limitSizeInput)
        textInput = Entry(self, show=specialCharacter, font=self.textFont, width=20, justify='center', textvariable=currentInput)
        textInput.place(x=location[0], y=location[1])
        if(specialCharacter=='*'):
            self.showPasswordOption = Checkbutton(self, text=controller.currentLanguage.homePageContent[12], font=self.passwordFont, fg='dark grey', bg=self.colorORT, variable=self.showPassword, command=checkShowPassword)
            self.showPasswordOption.place(x=location[0]+40, y=location[1]+40)
        return textInput

    def areFieldsNotEmpty(self):
        fieldsNotEmpty = 0
        if(len(self.userData[0].get())!=1 and len(self.userData[1].get())!=1):
            fieldsNotEmpty = 1
        return fieldsNotEmpty

    def deleteUserFields(self, fields):
        self.userData[1].delete(0,'end')
        if(fields==2):
            self.userData[0].delete(0,'end')

    def isUserInputCorrect(self, controller):
        possibleUser = User(["", "", "", "", "", "", "", "", ""])
        possibleUser.usernumber = self.userData[0].get()
        possibleUser.password = self.userData[1].get()
        userInputCorrect = controller.application.isUserDataRight(possibleUser)
        if(userInputCorrect==2):
            controller.application.listStudents.students[controller.application.systemCurrentStatus.userLogged].updateLastEntry()
        if(userInputCorrect==4):
            controller.application.listProfessors.professors[controller.application.systemCurrentStatus.userLogged].updateLastEntry()
        return userInputCorrect

    def isAdminInputCorrect(self, controller):
        adminInputCorrect = 0
        possibleAdmin = Administrator()
        possibleAdmin.usernumber = self.userData[0].get()
        possibleAdmin.password = self.userData[1].get()
        if(possibleAdmin.isAdminDataRight([controller.application.admin.usernumber, controller.application.admin.password])==1):
            controller.application.admin.updateLastEntry()
            adminInputCorrect=1
        return adminInputCorrect

    def setStatusInformation(self, status, fields, controller):
        self.showStatusLogIn(status, controller)
        self.deleteUserFields(fields)

    def showIncorrectPassword(self, userType, controller):
        messagebox.showwarning(title=userType, message=controller.currentLanguage.homePageContent[11])
        self.setStatusInformation("Incorrect Password", 1, controller)

    def isUserEntryCorrect(self, controller):
        isUserLogging = self.isUserInputCorrect(controller)
        if(isUserLogging==1):
            self.showIncorrectPassword('STUDENT', controller)
        elif(isUserLogging==2): # USER
            #self.loadingTitle.place(x=1024/2, y=800/2)
            #self.doneLoading = False
            #loadingScreen = threading.Thread(target=lambda:self.animateLoading())
            #loadingScreen.start()
            student = Student(["", "", "", "", "", "", "", "", ""])
            student.initiateSession(controller)
            self.setStatusInformation("", 2, controller)
            self.doneLoading = True
        elif(isUserLogging==3):
            self.showIncorrectPassword('PROFESSOR', controller)
        elif(isUserLogging==4):
            #self.loadingTitle.place(x=1024/2, y=800/2)
            #self.doneLoading = False
            #loadingScreen = threading.Thread(target=lambda:self.animateLoading())
            #loadingScreen.start()
            professor = Professor(["", "", "", "", "", "", "", "", ""])
            self.timesEntryTried = 0
            #time.sleep(5)
            professor.initiateSession(controller)
            self.setStatusInformation("", 2, controller)
            self.doneLoading = True
        return isUserLogging

    def animateLoading(self):
        self.loadingTitle.place(x=1024/2, y=800/2)
        print("ENTRO ANIMATE LOADING")
        for c in itertools.cycle(['|', '/', '-', '\\']):
            if self.doneLoading:
                break
            self.loadingTitle['text']=(c + ' LOADING ' + c)
            time.sleep(0.1)
        self.loadingTitle['text']=('DONE!')
        #time.sleep(0.2)
        self.loadingTitle.place(x=2000,y=2000)

        #for c in itertools.cycle(['|', '/', '-', '\\']):
        #    if done:
        #        break
        #    sys.stdout.write('\rloading ' + c)
        #    sys.stdout.flush()
        #    time.sleep(0.1)
        #sys.stdout.write('\rDone!     ')

    def isAdminEntryCorrect(self, userEntryCorrect, controller):
        isAdminLogging = self.isAdminInputCorrect(controller)
        adminCondition = not userEntryCorrect==2 or not userEntryCorrect==4
        if(isAdminLogging==1 and adminCondition): # ADMIN
            #self.loadingTitle.place(x=1024/2, y=800/2)
            #self.doneLoading = False
            #loadingScreen = threading.Thread(target=lambda:self.animateLoading())
            #loadingScreen.start()
            #long process here
            #time.sleep(10)
            admin = Administrator()
            admin.initiateSession(controller)
            self.timesEntryTried = 0
            self.setStatusInformation("", 2, controller)
            #time.sleep(5)
            self.doneLoading = True
        return isAdminLogging==1 and adminCondition

    def checkEntryCorrect(self, controller):
        userEntry = self.isUserEntryCorrect(controller)
        adminEntryCorrect = self.isAdminEntryCorrect(userEntry, controller)
        if(userEntry==0 and not adminEntryCorrect):
            self.setStatusInformation("User Not Registered", 2, controller)
            self.timesEntryTried = self.timesEntryTried + 1
            print("TIMESENTRYTRIED: ", self.timesEntryTried)
            if(self.timesEntryTried==5):
                controller.application.systemCurrentStatus.blockedEntryTime = datetime.today()
                messagebox.showwarning(title=controller.currentLanguage.homePageContent[24], message=controller.currentLanguage.homePageContent[21])
            else:
                messagebox.showerror(title='ERROR', message=controller.currentLanguage.homePageContent[10])

    def checkLogIn(self, controller):
        print("BLOCKED ENTRY TIME: ", controller.application.systemCurrentStatus.blockedEntryTime)
        if(not controller.application.systemCurrentStatus.isUserEntryBlocked()):
            if(self.areFieldsNotEmpty()==1):
                self.checkEntryCorrect(controller)
            else:
                messagebox.showwarning(title=controller.currentLanguage.homePageContent[24], message=controller.currentLanguage.homePageContent[9])
        else:
            timeRemaining = controller.application.systemCurrentStatus.getTimeEntryBlockRemaining().seconds/60
            messagebox.showwarning(title=controller.currentLanguage.homePageContent[24], message=controller.currentLanguage.homePageContent[22]+str(int(timeRemaining))+controller.currentLanguage.homePageContent[23])

    def setLogInButton(self, controller):
        self.userData.append(self.setTextBox('',[977,330], controller))#[607,215])) #USERNAME
        self.userData.append(self.setTextBox('*',[977,460], controller)) #PASSWORD
        self.logInOption = Button(self, text=controller.currentLanguage.homePageContent[20], command=lambda:self.checkLogIn(controller), fg='dark green', bg = 'white', font=self.buttonFont, borderwidth=5, compound=CENTER, highlightthickness = 5, highlightbackground = 'green', highlightcolor = 'green', height=2, width=18)
        self.logInOption.place(x=850, y=580)

    def getAnimationsSmartFermentorElements(self):
        smElement = Picture(['SmElement','png',95,95,774,28],0)
        smElement.purpose = 'Animations'
        feElement = Picture(['FeElement','png',95,95,999,28],0)
        feElement.purpose = 'Animations'
        return [smElement, feElement]

    def loadAnimations(self):
        bubble1Pic = Picture(['Bubble1Smart','png',60,60,1270,100+self.animationUpExtensionY],0)
        bubble1Pic.purpose = 'Animations'
        bubble2Pic = Picture(['Bubble2Smart','png',50,50,725,340+self.animationDownExtensionY],0)
        bubble2Pic.purpose = 'Animations'
        bubble3Pic = Picture(['Bubble1Smart','png',25,25,1270,160+self.animationUpExtensionY],90)
        bubble3Pic.purpose = 'Animations'
        bubble4Pic = Picture(['Bubble1Smart','png',20,20,720,388+self.animationDownExtensionY],0)
        bubble4Pic.purpose = 'Animations'
        eColiADNPic = Picture(['ecoliADNPic','png',44,66,735,405+self.animationDownExtensionY],0)
        eColiADNPic.purpose = 'Animations'
        eColiFungusPic = Picture(['eColiFungusPic','png',70,45,1260,195+self.animationUpExtensionY],0)
        eColiFungusPic.purpose = 'Animations'
        cell1Pic = Picture(['celulaPic','png',45,45,720,290+self.animationDownExtensionY],0)
        cell1Pic.purpose = 'Animations'
        cell2Pic = Picture(['celulaPic','png',35,35,1275,240+self.animationUpExtensionY],90)
        cell2Pic.purpose = 'Animations'
        smartElements = self.getAnimationsSmartFermentorElements()
        animations = [bubble1Pic, bubble2Pic, bubble3Pic, bubble4Pic, eColiADNPic, eColiFungusPic, cell1Pic, cell2Pic, smartElements[0], smartElements[1]]
        self.animatedPictures.addPictures(animations, len(animations))
        self.animationLabels = self.getAnimationsLabels()

    def configureStartLetters(self):
        self.startTitle.append(Label(self, text = "S", fg = 'white', bg = self.colorORT, font = self.bigTitleFont))
        self.startTitle.append(Label(self, text = "T", fg = 'white', bg = self.colorORT, font = self.bigTitleFont))
        self.startTitle.append(Label(self, text = "A", fg = 'white', bg = self.colorORT, font = self.bigTitleFont))
        self.startTitle.append(Label(self, text = "R", fg = 'white', bg = self.colorORT, font = self.bigTitleFont))
        self.startTitle.append(Label(self, text = "T", fg = 'white', bg = self.colorORT, font = self.bigTitleFont))
        self.startTitle[0].place(x=1500, y=185)
        self.startTitle[1].place(x=1500, y=185)
        self.startTitle[2].place(x=1500, y=185)
        self.startTitle[3].place(x=1500, y=185)
        self.startTitle[4].place(x=1500, y=185)

    def fillHomePageTitles(self, controller):
        self.usernameTitle = Label(self, text = controller.currentLanguage.homePageContent[6], fg = 'white', bg = self.colorORT, font = self.titleFont)
        self.usernameTitle.place(x=800, y=325)
        self.passwordTitle = Label(self, text = controller.currentLanguage.homePageContent[7], fg = 'white', bg = self.colorORT, font = self.titleFont)
        self.passwordTitle.place(x=800, y=455)
        self.welcomeInformation = Label(self, text=controller.currentLanguage.homePageContent[8], font=self.titleFont, fg='white', bg=self.colorORT)
        self.welcomeInformation.place(x=820,y=260)
        self.statusInformation = Label(self, font=self.statusFont, fg='red', bg=self.colorORT)
        self.statusInformation.place(x=830,y=400)

    def loadStaticPictures(self, controller):
        institutionORT = Picture(['SmartBackground2','png',905+self.extensionX,500+self.extensionY,-2,0],0)
        institutionPic = self.generateLabel(institutionORT)
        institutionPic.place(x=institutionORT.location[0],y=institutionORT.location[1])

        backgroundForAnimations = Picture(['TabsBackground','png',905+self.extensionX,600,-2,150],0)
        backgroundForAnimationsPic = self.generateLabel(backgroundForAnimations)
        backgroundForAnimationsPic.place(x=backgroundForAnimations.location[0],y=backgroundForAnimations.location[1])

        systemSmart = Picture(['SmartSystem','png',695,585,0,155],0)
        systemPic = self.generateLabel(systemSmart)
        systemPic.place(x=systemSmart.location[0],y=systemSmart.location[1])

        self.versionInfo = Label(self, text = controller.currentLanguage.homePageContent[5], fg = 'dark green', bg = 'white', font = self.groupMessageFont, height = 1, width = 82, justify='center') #anchor = NE)
        self.versionInfo.place(x=142+47+47+47+47, y=470+self.extensionY)
        self.configureStartLetters()

    def configureCanvas(self, controller):
        self.ortMessageTitle = Label(self.canvas, text=controller.currentLanguage.homePageContent[0], font=self.subtitleFont, fg=self.colorORT, bg='white')
        self.ortMessageTitle.place(x=20,y=20)
        self.groupMessageBody = Label(self.canvas, text=controller.currentLanguage.homePageContent[1], font=self.groupMessageFont, fg=self.colorORT, bg='white')
        self.groupMessageBody.place(x=80,y=80)
        self.smartMessageBody = Label(self.canvas, text=controller.currentLanguage.homePageContent[2], font=self.bodyMessageFont, fg=self.colorORT, bg='white', justify=LEFT)
        self.smartMessageBody.place(x=20,y=160)
        self.smartNoticeBody = Label(self.canvas, text=controller.currentLanguage.homePageContent[3], font=self.bodyMessageFont, fg=self.colorORT, bg='white', justify=LEFT)
        self.smartNoticeBody.place(x=20,y=270)
        self.ortMessageBody = Label(self.canvas, text=controller.currentLanguage.homePageContent[4], font=self.bodyMessageFont, fg=self.colorORT, bg='white', justify=LEFT)
        self.ortMessageBody.place(x=20,y=390)

    def refreshTextContent(self, controller):
        self.ortMessageTitle['text'] = controller.currentLanguage.homePageContent[0]
        self.groupMessageBody['text'] = controller.currentLanguage.homePageContent[1]
        self.smartMessageBody['text'] = controller.currentLanguage.homePageContent[2]
        self.smartNoticeBody['text'] = controller.currentLanguage.homePageContent[3]
        self.ortMessageBody['text'] = controller.currentLanguage.homePageContent[4]
        self.versionInfo['text'] = controller.currentLanguage.homePageContent[5]
        self.usernameTitle['text'] = controller.currentLanguage.homePageContent[6]
        self.passwordTitle['text'] = controller.currentLanguage.homePageContent[7]
        self.welcomeInformation['text'] = controller.currentLanguage.homePageContent[8]
        self.showPasswordOption['text'] = controller.currentLanguage.homePageContent[12]
        self.minimizeSystem['text'] = controller.currentLanguage.homePageContent[17]
        self.closeSystem['text'] = controller.currentLanguage.homePageContent[18]
        self.aboutSystem['text'] = controller.currentLanguage.homePageContent[19]
        self.logInOption['text'] = controller.currentLanguage.homePageContent[20]

    def changeLanguage(self, language, controller):
        if(language=='GERMAN'):
            controller.currentLanguage = GermanLanguage()
            self.welcomeInformation.place(x=800,y=260)
            self.minimizeSystem.place(x=1150, y=470+self.extensionY)
        if(language=='PORTUGUESE'):
            controller.currentLanguage = PortugueseLanguage()
            self.welcomeInformation.place(x=820,y=260)
            self.minimizeSystem.place(x=1155, y=470+self.extensionY)
        if(language=='SPANISH'):
            controller.currentLanguage = SpanishLanguage()
            self.welcomeInformation.place(x=820,y=260)
            self.minimizeSystem.place(x=1155, y=470+self.extensionY)
        if(language=='ENGLISH'):
            controller.currentLanguage = OriginalLanguage()
            self.welcomeInformation.place(x=820,y=260)
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
        ortLogo = Picture(['ORTLogo','png',240,100,100+self.extensionX,200+self.extensionY],0)
        ortLogo.purpose = 'Logos'
        oneImage = Image.open(ortLogo.getCompleteFilename()).resize((ortLogo.dimensions[0],ortLogo.dimensions[1]), Image.ANTIALIAS)
        oneImageRendered = ImageTk.PhotoImage(oneImage.rotate(ortLogo.orientation))
        ortLogoPic = Label(self.canvas, image=oneImageRendered, borderwidth=0, highlightthickness=0)
        ortLogoPic.image = oneImageRendered
        ortLogoPic.place(x=ortLogo.location[0],y=ortLogo.location[1])
        self.configureCanvas(controller)
        self.setLanguages(controller)

    def showAbout(self):
        if(self.helpDisplayed == False):
            self.canvas.place(x=0, y=150)
            self.helpDisplayed = True
        else:
            self.canvas.place(x=1000, y=1000)
            self.helpDisplayed = False

    def setAboutButton(self, controller):
        self.aboutSystem = Button(self, text=controller.currentLanguage.homePageContent[19], command=lambda:self.showAbout(), relief = RAISED, fg='white', bg = 'dark green', font=self.bodyMessageFont, compound=CENTER, height = 1, width = 15)
        self.aboutSystem.place(x=0, y=470+self.extensionY)
        self.canvas = Canvas(self, background="white", width= 890+self.extensionX, height= 315+self.extensionY, highlightthickness=5, highlightbackground=self.colorORT)
        self.canvasConfiguration(controller)

    def showStatusLogIn(self, status, controller):
        if(status=="User Not Registered"):
            self.statusInformation['text']=controller.currentLanguage.homePageContent[13]
        elif(status=="Incorrect Password"):
            self.statusInformation['text']=controller.currentLanguage.homePageContent[14]
        elif(status==""):
            self.statusInformation['text']=''

    def minimizeWindow(self):
        print("MINIMIZE")
        screen = Wnck.Screen.get_default()
        screen.force_update()
        windows = screen.get_windows()
        for w in windows:
            if ('SMARTFERMENTOR' in w.get_name()):
                w.minimize()
                print("VENTANA: ", w.get_name())

    def fillHomePageButtons(self, controller):
        self.minimizeSystem = Button(self, text=controller.currentLanguage.homePageContent[17], command=lambda:self.minimizeWindow(), relief = RAISED, fg='white', bg = 'blue', font=self.bodyMessageFont, compound=CENTER, height = 1, width = 10)
        self.minimizeSystem.place(x=1155, y=470+self.extensionY)
        #self.minimizeSystem = Button(self, text=controller.currentLanguage.homePageContent[17], relief = RAISED, fg='white', bg = 'blue', font=self.bodyMessageFont, compound=CENTER, height = 1, width = 10)
        #self.minimizeSystem.place(x=1155, y=470+self.extensionY)
        self.closeSystem = Button(self, text=controller.currentLanguage.homePageContent[18], command=lambda:self.onClosing(controller), relief = RAISED, fg='white', bg = 'red', font=self.bodyMessageFont, compound=CENTER, height = 1, width = 12)
        self.closeSystem.place(x=1252, y=470+self.extensionY)
        self.setLogInButton(controller)
        self.setAboutButton(controller)

    def fadeAway(self, controller):
        alpha = controller.attributes("-alpha")
        if alpha > 0:
            alpha = alpha - 0.1
            controller.attributes("-alpha", alpha)
            self.after(50, lambda:self.fadeAway(controller))
        else:
            controller.destroy()

    def onClosing(self, controller):
        if messagebox.askokcancel(controller.currentLanguage.homePageContent[16], controller.currentLanguage.homePageContent[15]):
            controller.application.saveSmartData("")
            self.fadeAway(controller)

    def __init__(self, parent, controller):

        Frame.__init__(self, parent)
        controller.protocol("WM_DELETE_WINDOW", lambda:self.onClosing(controller))
        controller.settingScreensControl[2] = 1
        controller.settingScreensControl[1] = 1
        self.setFonts()
        self.setVariables()
        self.loadStaticPictures(controller)
        self.loadAnimations()
        self.fillHomePageTitles(controller)
        self.animate()
        self.fillHomePageButtons(controller)
        controller.setPersonalStyle()
        self.loadingTitle = Label(self, text = "... LOADING ...", fg = 'white', relief='groove', bg = self.colorORT, font = self.bigTitleFont, width=12, height=2)
