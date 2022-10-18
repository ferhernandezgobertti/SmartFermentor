import sys, time, matplotlib
from datetime import datetime, date, timedelta
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import style
import matplotlib.animation as animation
import matplotlib.ticker as ticker
from pathlib import Path
from tkinter import *
from tkinter import ttk, messagebox
import tkinter.font
from PIL import Image, ImageTk
from Domain.Fermentation import Fermentation
from Domain.Velocity import Velocity
from Domain.Temperature import Temperature
from Domain.PotentialHydrogen import PotentialHydrogen
from MonitorConsole.Picture import Picture
from MonitorConsole.OriginalLanguage import OriginalLanguage
from MonitorConsole.SpanishLanguage import SpanishLanguage
from MonitorConsole.PortugueseLanguage import PortugueseLanguage
from MonitorConsole.GermanLanguage import GermanLanguage
from MonitorConsole.EntertainmentDisplay import EntertainmentDisplay

class FermentationPage(Frame):

    def setFonts(self):
        self.colorORT = "#085454"
        self.buttonFont = tkinter.font.Font(family = 'Helvetica', size = 14, weight = 'bold')
        self.titleFont = tkinter.font.Font(family = 'Helvetica', size = 20, weight = 'bold')
        self.subtitleFont = tkinter.font.Font(family = 'Comic Sans', size = 16, weight = 'bold')
        self.statusFont = tkinter.font.Font(family = 'Arial', size = 16, weight = 'bold')
        self.inputFont = tkinter.font.Font(family = 'Times', size = 16)
        self.infoFont = tkinter.font.Font(family = 'Times', size = 12)
        self.listElementFont = tkinter.font.Font(family = 'Times', size = 12)
        self.gameFont = tkinter.font.Font(family = 'Comic Sans MS', size = 16, weight = 'bold')
        self.gameTitleFont = tkinter.font.Font(family = 'Comic Sans MS', size = 20, weight = 'bold')
        self.magnitudeExtraFont = tkinter.font.Font(family = 'Arial', size = 12, weight = 'bold')
        self.bodyMessageFont = tkinter.font.Font(family = 'Times New Roman', size = 12, weight = 'bold')
        self.groupMessageFont = tkinter.font.Font(family = 'Times New Roman', size = 14, weight = 'bold')

    def setVariables(self):
        self.freeWheelSelection = [IntVar(), IntVar(), IntVar()]
        self.stopMagniudeWhenVelocity = [IntVar(), IntVar()]
        self.stopMagnitudeWhenTemperature = [IntVar(), IntVar()]
        self.stopMagnitudeWhenPotential = [IntVar(), IntVar()]
        self.triviaOptionSelection = [IntVar(), IntVar(), IntVar(), IntVar()]
        self.isControlInitialized = [False, False, False]
        self.isErrorFound = [False, False, False] # NEED TO BE CHECKED WHEN ERROR OCCURS !!!
        self.isMagnitudeListEditable = [True, True, True]

        self.extensions = [466, 268]
        self.helpDisplayed = False
        self.currentMagnitudeControlStep = ["", "", ""]
        self.traslation = 110
        self.countUntilSave = 0

    def setFileNames(self, currentFermentation):
        fileTime = datetime.today()
        self.velocityStatusFileTimeStr = "ControlData/Velocity/STATUS_Log/"+str(currentFermentation.sustance)+"_"+str(fileTime.strftime("%Y%m%d"))+"_VEL.txt"
        self.velocityDataFileTimeStr = "ControlData/Velocity/DATA_Log/"+str(fileTime.strftime("%Y%m%d_%I%M%S"))+"_VEL.txt"
        self.velocityErrorFileTimeStr = "ControlData/Velocity/ERROR_Log/"+str(currentFermentation.sustance)+"_"+str(fileTime.strftime("%Y%m%d"))+"_VEL.txt"
        self.temperatureStatusFileTimeStr = "ControlData/Temperature/STATUS_Log/"+str(currentFermentation.sustance)+"_"+str(fileTime.strftime("%Y%m%d"))+"_TEM.txt"
        self.temperatureDataFileTimeStr = "ControlData/Temperature/DATA_Log/"+str(fileTime.strftime("%Y%m%d_%I%M%S"))+"_TEM.txt"
        self.temperatureErrorFileTimeStr = "ControlData/Temperature/ERROR_Log/"+str(currentFermentation.sustance)+"_"+str(fileTime.strftime("%Y%m%d"))+"_TEM.txt"
        self.potentialHydrogenStatusFileTimeStr = "ControlData/PotentialHydrogen/STATUS_Log/"+str(currentFermentation.sustance)+"_"+str(fileTime.strftime("%Y%m%d"))+"_POT.txt"
        self.potentialHydrogenDataFileTimeStr = "ControlData/PotentialHydrogen/DATA_Log/"+str(fileTime.strftime("%Y%m%d_%I%M%S"))+"_POT.txt"
        self.potentialHydrogenErrorFileTimeStr = "ControlData/PotentialHydrogen/ERROR_Log/"+str(currentFermentation.sustance)+"_"+str(fileTime.strftime("%Y%m%d"))+"_POT.txt"


    def setLists(self):
        self.velocityInput = []
        self.temperatureInput = []
        self.potentialHydrogenInput = []
        self.buttonsSystem = []
        self.buttonsVelocity = []
        self.buttonsTemperature = []
        self.buttonsPotentialHydrogen = []
        self.systemInformation = []
        self.generalInformation = []
        self.freeWheelInformation = []
        self.customizationInformation = []
        self.freeWheelOption = []
        self.velocityInformation = []
        self.temperatureInformation = []
        self.potentialHydrogenInformation = []
        self.errorInformation = []
        self.errorParameters = []
        self.currentGameStatus = []
        self.velList = []
        self.freqList = []
        self.secondsListVelocity=[]
        self.temperatureFermentorList=[]
        self.temperatureBathList=[]
        self.secondsListTemperature=[]
        self.potHydrogenList = []
        self.volumeAcidList = []
        self.volumeBaseList = []
        self.potHydrogenList=[]
        self.acidDropsList=[]
        self.baseDropsList=[]
        self.secondsListPotential=[]
        self.addMagnitudeInfo = []
        self.changeMagnitudeInfo = []
        self.removeMagnitudeInfo = []
        self.beginControlMagnitudeInfo = []
        self.pauseControlMagnitudeInfo = []
        self.stopControlMagnitudeInfo = []
        self.previousStepOfMagnitudeInfo = []
        self.nextStepOfMagnitudeInfo = []
        self.restartControlMagnitudeInfo = []
        self.removeAllListMagnitudeInfo = []


    def setGraphics(self):

        def make_patch_spines_invisible(ax):
            ax.set_frame_on(True)
            ax.patch.set_visible(False)
            for sp in ax.spines.values():
                sp.set_visible(False)

        self.systemMagnitudesFigure = Figure(figsize=(7.5,5.5), dpi=100, facecolor=self.colorORT, edgecolor='white')
        self.systemMagnitudesGraph1 = self.systemMagnitudesFigure.add_subplot(111)
        self.systemMagnitudesGraph2 = self.systemMagnitudesGraph1.twinx()  # instantiate a second axes that shares the same x-axis
        self.systemMagnitudesGraph3 = self.systemMagnitudesGraph1.twinx()  # instantiate a second axes that shares the same x-axis
        self.systemMagnitudesFigure.subplots_adjust(right=0.75)
        self.systemMagnitudesGraph3.spines["right"].set_position(("axes", 1.2))
        make_patch_spines_invisible(self.systemMagnitudesGraph3)
        self.systemMagnitudesGraph3.spines["right"].set_visible(True)

        self.freeWheelFigure = Figure(figsize=(7,5.5), dpi=100, facecolor=self.colorORT, edgecolor='white')
        self.freeWheelVelocityGraph = self.freeWheelFigure.add_subplot(111)
        self.freeWheelTemperatureGraph = self.freeWheelVelocityGraph.twinx()  # instantiate a second axes that shares the same x-axis
        self.freeWheelPotentialGraph = self.freeWheelVelocityGraph.twinx()  # instantiate a second axes that shares the same x-axis
        self.freeWheelFigure.subplots_adjust(right=0.75)
        self.freeWheelPotentialGraph.spines["right"].set_position(("axes", 1.2))
        make_patch_spines_invisible(self.freeWheelPotentialGraph)
        self.freeWheelPotentialGraph.spines["right"].set_visible(True)

        self.frequencyFigure = Figure(figsize=(6.2,5.5), dpi=100, facecolor=self.colorORT, edgecolor='white') #figsize = (3.8,2.9)
        self.frequencyGraph = self.frequencyFigure.add_subplot(111)
        self.frequencyGraph.grid(b=None, which='major', axis='both', linestyle='dashed', linewidth=1)
        #self.bathTemperatureFigure = Figure(figsize=(5,4), dpi=100, facecolor=self.colorORT, edgecolor='white')
        self.bathTemperatureGraph = self.frequencyGraph.twinx()
        self.frequencyFigure.subplots_adjust(right=0.75)
        self.bathTemperatureGraph.grid(b=None, which='major', axis='both', linestyle='dashed', linewidth=1)

        self.dropsFigure = Figure(figsize=(6.2,5.5), dpi=100, facecolor=self.colorORT, edgecolor='white') #figsize = (3.8,2.9)
        self.dropsAcidGraph = self.dropsFigure.add_subplot(111)
        self.dropsAcidGraph.grid(b=None, which='major', axis='both', linestyle='dashed', linewidth=1)
        self.dropsBaseGraph = self.dropsAcidGraph.twinx()
        self.dropsFigure.subplots_adjust(right=0.75)

        self.velocityFigure = Figure(figsize=(5.5,4), dpi=100, facecolor=self.colorORT, edgecolor='white')
        self.velocityGraph = self.velocityFigure.add_subplot(111)
        self.velocityGraph.grid(b=None, which='major', axis='both', linestyle='dashed', linewidth=1)
        self.temperatureFigure = Figure(figsize=(5.5,4), dpi=100, facecolor=self.colorORT, edgecolor='white')
        self.temperatureGraph = self.temperatureFigure.add_subplot(111)
        self.temperatureGraph.grid(b=None, which='major', axis='both', linestyle='dashed', linewidth=1)
        self.potentialHydrogenFigure = Figure(figsize=(5.5,4), dpi=100, facecolor=self.colorORT, edgecolor='white')
        self.potentialHydrogenGraph = self.potentialHydrogenFigure.add_subplot(111)
        self.potentialHydrogenGraph.grid(b=None, which='major', axis='both', linestyle='dashed', linewidth=1)

    def closeFermentation(self, controller):
        #controller.application.updateFermentationControlsData()
        #controller.application.updateFermentationVerificationsData()
        #controller.application.listFermentations.fermentation[controller.application.systemCurrentStatus.fermentationActual].isFermentationContinuing = False
        controller.returnToSession()

    def loadStaticPictures(self, controller):
        imagesLogo = ["Images/Logos/addMagnitudeLogo.gif", "Images/Logos/changeMagnitudeLogo.gif", "Images/Logos/removeMagnitudeLogo.gif", "Images/Logos/beginControlMagnitudeLogo2.gif", "Images/Logos/pauseControlMagnitudeLogo2.gif", "Images/Logos/stopControlMagnitudeLogo2.gif", "Images/Logos/previousStepLogo.gif", "Images/Logos/nextStepLogo.gif", "Images/Logos/restartControlLogo.gif", "Images/Logos/removeAllListMagnitudeLogo.gif"]
        for anImage in imagesLogo:
            self.buttonsSystem.append(PhotoImage(file=anImage))
            self.buttonsVelocity.append(PhotoImage(file=anImage))
            self.buttonsTemperature.append(PhotoImage(file=anImage))
            self.buttonsPotentialHydrogen.append(PhotoImage(file=anImage))

        fermentationSmart = Picture(['SmartFermentation','png',900+self.extensions[0],500+self.extensions[1],0,0],0)
        fermentationSmartPic = fermentationSmart.generateLabel(self)
        fermentationSmartPic.place(x=fermentationSmart.location[0],y=fermentationSmart.location[1])

        self.powerOffImage = PhotoImage(file="Images/Logos/powerOffLogo.gif")
        powerOffOption = Button(self, image=self.powerOffImage, command=lambda:self.closeFermentation(controller), relief = SUNKEN, compound=CENTER)
        powerOffOption.place(x=1260, y=25)

    def showHelp(self):
        if(self.helpDisplayed == False):
            self.canvas.place(x=0, y=140)
            self.helpDisplayed = True
        else:
            self.canvas.place(x=1000, y=1000)
            self.helpDisplayed = False

    def setHelpBar(self, controller):
        self.versionInfo = Label(self, text = controller.currentLanguage.adminPageContent[11], fg = 'dark green', bg = 'white', font = self.groupMessageFont, height = 1, width = 82, justify='center') #anchor = NE)
        self.versionInfo.place(x=142+47+47+47+47, y=470+self.extensions[1])
        self.minimizeSystem = Button(self, text=controller.currentLanguage.adminPageContent[21], command=lambda:self.onClosing(controller), relief = RAISED, fg='white', bg = 'blue', font=self.bodyMessageFont, compound=CENTER, height = 1, width = 10)
        self.minimizeSystem.place(x=1155, y=470+self.extensions[1])
        self.closeSystem = Button(self, text=controller.currentLanguage.adminPageContent[22], command=lambda:self.onClosing(controller), relief = RAISED, fg='white', bg = 'red', font=self.bodyMessageFont, compound=CENTER, height = 1, width = 12)
        self.closeSystem.place(x=1252, y=470+self.extensions[1])
        self.helpSystem = Button(self, text=controller.currentLanguage.adminPageContent[23], command=lambda:self.showHelp(), relief = RAISED, fg='white', bg = 'dark green', font=self.bodyMessageFont, compound=CENTER, height = 1, width = 15)
        self.helpSystem.place(x=0, y=470+self.extensions[1])
        self.canvas = Canvas(self, background="white", width= 890+self.extensions[0], height= 320+self.extensions[1], highlightthickness=5, highlightbackground=self.colorORT)
        #self.canvasConfiguration(controller)

    def configureCanvas(self, controller):
        self.ortMessageTitle = Label(self.canvas, text=controller.currentLanguage.fermentationPageContent[0], font=self.subtitleFont, fg=self.colorORT, bg='white')
        self.ortMessageTitle.place(x=20,y=10)
        self.groupMessageBody = Label(self.canvas, text=controller.currentLanguage.fermentationPageContent[1], font=self.groupMessageFont, fg=self.colorORT, bg='white', justify=LEFT)
        self.groupMessageBody.place(x=80,y=35)

    def refreshTabsContent(self, controller):
        self.nb.tab(self.pageSystem, text = controller.currentLanguage.fermentationPageContent[3])
        self.nb.tab(self.pageGlobal, text = controller.currentLanguage.fermentationPageContent[4])
        self.nb.tab(self.pageVelocity, text = controller.currentLanguage.fermentationPageContent[5])
        self.nb.tab(self.pageTemperature, text = controller.currentLanguage.fermentationPageContent[6])
        self.nb.tab(self.pagePotentialHydrogen, text = controller.currentLanguage.fermentationPageContent[7])
        self.nb.tab(self.pageCustomization, text = controller.currentLanguage.fermentationPageContent[8])
        self.nb.tab(self.pageEntertainment, text = controller.currentLanguage.fermentationPageContent[9])
        #self.nb.tab(self.pageTrivia, text = controller.currentLanguage.fermentationPageContent[10])

    def refreshPageSystemContent(self, controller):
        self.frequenceTitle['text'] = controller.currentLanguage.fermentationPageContent[11]
        self.acidTitle['text'] = controller.currentLanguage.fermentationPageContent[12]
        self.baseTitle['text'] = controller.currentLanguage.fermentationPageContent[13]
        self.freeWheelTitle['text'] = controller.currentLanguage.fermentationPageContent[14] + ": "
        self.velocityFreeWheelTitle['text'] = controller.currentLanguage.fermentationPageContent[15]
        self.temperatureFreeWheelTitle['text'] = controller.currentLanguage.fermentationPageContent[16]
        self.potentialHydrogenFreeWheelTitle['text'] = controller.currentLanguage.fermentationPageContent[17]
        self.extractionFreeWheelTitle['text'] = controller.currentLanguage.fermentationPageContent[18]
        self.generalInformation[0]['text'] = controller.currentLanguage.fermentationPageContent[19]
        self.generalInformation[1]['text'] = controller.currentLanguage.fermentationPageContent[20]
        self.generalInformation[2]['text'] = controller.currentLanguage.fermentationPageContent[21]
        self.runAllControlInfo['text'] = controller.currentLanguage.fermentationPageContent[22]
        self.restartAllControlInfo['text'] = controller.currentLanguage.fermentationPageContent[23]
        self.pauseAllControlInfo['text'] = controller.currentLanguage.fermentationPageContent[24]
        self.stopAllControlInfo['text'] = controller.currentLanguage.fermentationPageContent[25]
        self.extractionOption['text'] = controller.currentLanguage.fermentationPageContent[41]

    def refreshMagnitudesInformationContent(self, controller):
        for eachAddMagnitud in self.addMagnitudeInfo:
            eachAddMagnitud['text'] = controller.currentLanguage.fermentationPageContent[50]
        for eachChangeMagnitud in self.changeMagnitudeInfo:
            eachChangeMagnitud['text'] = controller.currentLanguage.fermentationPageContent[51]
        for eachRemoveMagnitud in self.removeMagnitudeInfo:
            eachRemoveMagnitud['text'] = controller.currentLanguage.fermentationPageContent[52]
        for eachBeginMagnitud in self.beginControlMagnitudeInfo:
            eachBeginMagnitud['text'] = controller.currentLanguage.fermentationPageContent[53]
        for eachPauseMagnitud in self.pauseControlMagnitudeInfo:
            eachPauseMagnitud['text'] = controller.currentLanguage.fermentationPageContent[54]
        for eachStopMagnitud in self.stopControlMagnitudeInfo:
            eachStopMagnitud['text'] = controller.currentLanguage.fermentationPageContent[55]
        for eachPreviousMagnitud in self.previousStepOfMagnitudeInfo:
            eachPreviousMagnitud['text'] = controller.currentLanguage.fermentationPageContent[56]
        for eachNextMagnitud in self.nextStepOfMagnitudeInfo:
            eachNextMagnitud['text'] = controller.currentLanguage.fermentationPageContent[57]
        for eachRestartMagnitud in self.restartControlMagnitudeInfo:
            eachRestartMagnitud['text'] = controller.currentLanguage.fermentationPageContent[58]
        for eachRemoveMagnitud in self.removeAllListMagnitudeInfo:
            eachRemoveMagnitud['text'] = controller.currentLanguage.fermentationPageContent[59]
        self.temperatureInfo['text'] = controller.currentLanguage.fermentationPageContent[98]
        self.potentialHydrogenInfo['text'] = controller.currentLanguage.fermentationPageContent[126]
        self.potentialHydrogenRangeInfo['text'] = controller.currentLanguage.fermentationPageContent[127]

    def refreshVelocityCustomizationContent(self, controller):
        self.velocityCustomizationTitle['text'] = controller.currentLanguage.fermentationPageContent[134]
        self.velocityUnitTitle['text'] = controller.currentLanguage.fermentationPageContent[135]
        self.velocityPrecisionTitle['text'] = controller.currentLanguage.fermentationPageContent[136]
        self.velocityPrecisionInfo['text'] = controller.currentLanguage.fermentationPageContent[137]
        self.velocitySensibilityTitle['text'] = controller.currentLanguage.fermentationPageContent[138]
        self.velocityOrientationTitle['text'] = controller.currentLanguage.fermentationPageContent[139]
        self.velocityDataIntervalTitle['text'] = controller.currentLanguage.fermentationPageContent[140]
        self.velocityDataIntervalInfo['text'] = controller.currentLanguage.fermentationPageContent[141]

    def refreshTemperatureCustomizationContent(self, controller):
        self.temperatureCustomizationTitle['text'] = controller.currentLanguage.fermentationPageContent[142]
        self.temperatureUnitTitle['text'] = controller.currentLanguage.fermentationPageContent[143]
        self.temperaturePrecisionTitle['text'] = controller.currentLanguage.fermentationPageContent[144]
        self.temperaturePrecisionInfo['text'] = controller.currentLanguage.fermentationPageContent[145]
        self.temperatureSensibilityTitle['text'] = controller.currentLanguage.fermentationPageContent[146]
        self.temperatureDataIntervalTitle['text'] = controller.currentLanguage.fermentationPageContent[147]
        self.temperatureDataIntervalInfo['text'] = controller.currentLanguage.fermentationPageContent[141]
        self.pumpStepTitle['text'] = controller.currentLanguage.fermentationPageContent[158]

    def refreshPotentialHydrogenCustomizationContent(self, controller):
        self.potHydrogenCustomizationTitle['text'] = controller.currentLanguage.fermentationPageContent[148]
        self.potHydrogenUnitTitle['text'] = controller.currentLanguage.fermentationPageContent[149]
        self.potHydrogenPrecisionTitle['text'] = controller.currentLanguage.fermentationPageContent[150]
        self.potHydrogenPrecisionInfo['text'] = controller.currentLanguage.fermentationPageContent[151]
        self.potHydrogenBurstTitle['text'] = controller.currentLanguage.fermentationPageContent[152]
        self.potHydrogenBurstInfo['text'] = controller.currentLanguage.fermentationPageContent[153]
        self.potHydrogenIntervalTitle['text'] = controller.currentLanguage.fermentationPageContent[154]
        self.potHydrogenIntervalInfo['text'] = controller.currentLanguage.fermentationPageContent[155]
        self.potHydrogenDataIntervalTitle['text'] = controller.currentLanguage.fermentationPageContent[156]
        self.potHydrogenDataIntervalInfo['text'] = controller.currentLanguage.fermentationPageContent[141]
        #self.potHydrogenBurstModelTitle['text'] = controller.currentLanguage.fermentationPageContent[159]

    def refreshPageCustomizationContent(self, controller):
        self.refreshVelocityCustomizationContent(controller)
        self.refreshTemperatureCustomizationContent(controller)
        self.refreshPotentialHydrogenCustomizationContent(controller)
        self.configureNewCustomization['text'] = controller.currentLanguage.fermentationPageContent[157]

    def refreshPageErrorsContent(self, controller):
        self.velocityErrorTitle['text'] = controller.currentLanguage.fermentationPageContent[161]
        self.temperatureErrorTitle['text'] = controller.currentLanguage.fermentationPageContent[162]
        self.potentialErrorTitle['text'] = controller.currentLanguage.fermentationPageContent[163]
        self.errorParameters[0]['text'] = controller.currentLanguage.fermentationPageContent[166]
        self.errorParameters[1]['text'] = controller.currentLanguage.fermentationPageContent[167]
        self.errorParameters[2]['text'] = controller.currentLanguage.fermentationPageContent[165]
        self.errorParameters[3]['text'] = controller.currentLanguage.fermentationPageContent[167]
        self.errorParameters[4]['text'] = controller.currentLanguage.fermentationPageContent[165]
        self.errorParameters[5]['text'] = controller.currentLanguage.fermentationPageContent[166]

    def refreshPageEntertainmentContent(self, controller):
        self.informationTitle['text'] = controller.currentLanguage.fermentationPageContent[133]

    def refreshTextContent(self, controller):
        self.refreshTabsContent(controller)
        #self.fermentationInformation['text'] = controller.currentLanguage.fermentationPageContent[2]+controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].dateBeginning
        self.versionInfo['text'] = controller.currentLanguage.adminPageContent[12]
        self.minimizeSystem['text'] = controller.currentLanguage.adminPageContent[22]
        self.closeSystem['text'] = controller.currentLanguage.adminPageContent[23]
        self.helpSystem['text'] = controller.currentLanguage.adminPageContent[24]

        #self.refreshPageSystemContent(controller)
        #self.refreshMagnitudesInformationContent(controller)
        #self.refreshPageEntertainmentContent(controller)
        #self.refreshPageCustomizationContent(controller)
        #self.refreshPageErrorsContent(controller)

    def changeLanguage(self, language, controller):
        if(language=='GERMAN'):
            controller.currentLanguage = GermanLanguage()
            self.fermentationInformation.place(x=1142, y=120)
            self.minimizeSystem.place(x=1150, y=470+self.extensions[1])
        if(language=='PORTUGUESE'):
            controller.currentLanguage = PortugueseLanguage()
            self.fermentationInformation.place(x=1155, y=120)
            self.minimizeSystem.place(x=1155, y=470+self.extensions[1])
        if(language=='SPANISH'):
            controller.currentLanguage = SpanishLanguage()
            self.fermentationInformation.place(x=1135, y=120)
            self.minimizeSystem.place(x=1155, y=470+self.extensions[1])
        if(language=='ENGLISH'):
            controller.currentLanguage = OriginalLanguage()
            self.fermentationInformation.place(x=1120, y=120)
            self.minimizeSystem.place(x=1155, y=470+self.extensions[1])
        #self.refreshTextContent(controller)

    def setLanguages(self, controller):
        self.changeLanguage('ENGLISH', controller)
        self.spanishFlagImage = PhotoImage(file="Images/Languages/spainFlag.gif")
        spanishOption = Button(self, image=self.spanishFlagImage, command=lambda:self.changeLanguage('SPANISH', controller), compound=CENTER)
        spanishOption.place(x=142, y=470+self.extensions[1])#(x=150, y=500)
        self.englishFlagImage = PhotoImage(file="Images/Languages/britishFlag.gif")
        englishOption = Button(self, image=self.englishFlagImage, command=lambda:self.changeLanguage('ENGLISH', controller), compound=CENTER)
        englishOption.place(x=142+47, y=470+self.extensions[1])#(x=200, y=500)
        self.portugueseFlagImage = PhotoImage(file="Images/Languages/brazilFlag.gif")
        portugueseOption = Button(self, image=self.portugueseFlagImage, command=lambda:self.changeLanguage('PORTUGUESE', controller), compound=CENTER)
        portugueseOption.place(x=142+47+47, y=470+self.extensions[1])#(x=250, y=500)
        self.germanFlagImage = PhotoImage(file="Images/Languages/germanyFlag.gif")
        germanOption = Button(self, image=self.germanFlagImage, command=lambda:self.changeLanguage('GERMAN', controller), compound=CENTER)
        germanOption.place(x=142+47+47+47, y=470+self.extensions[1])#(x=300, y=500)

    def canvasConfiguration(self, controller):
        ortLogo = Picture(['ORTLogo','png',240,100,100+self.extensions[0],220+self.extensions[1]],0)
        ortLogo.purpose = 'Logos'
        oneImage = Image.open(ortLogo.getCompleteFilename()).resize((ortLogo.dimensions[0],ortLogo.dimensions[1]), Image.ANTIALIAS)
        oneImageRendered = ImageTk.PhotoImage(oneImage.rotate(ortLogo.orientation))
        ortLogoPic = Label(self.canvas, image=oneImageRendered, borderwidth=0, highlightthickness=0)
        ortLogoPic.image = oneImageRendered
        ortLogoPic.place(x=ortLogo.location[0],y=ortLogo.location[1])
        self.configureCanvas(controller)
        self.setLanguages(controller)

    
    def isTimeCorrect(self, timeToCheck, maximumValue):
        return timeToCheck<=maximumValue and timeToCheck>=0

    def isMagnitudeInputCorrectOnFreeWheel(self, magnitudInput, extremeValues):
        return magnitudInput.get().isdigit() and int(magnitudInput.get())<=extremeValues[1] and int(magnitudInput.get())>=extremeValues[0]

    def isMagnitudeInputCorrect(self, magnitudInput, extremeValues):
        areFieldsNotEmpty =  magnitudInput[0].get().isdigit() and magnitudInput[1].get().isdigit() and magnitudInput[2].get().isdigit() and magnitudInput[3].get().isdigit()
        isMagnitudeValueCorrect = int(magnitudInput[0].get())<=extremeValues[1] and int(magnitudInput[0].get())>=extremeValues[0]
        isMagnitudeDurationCorrect =  self.isTimeCorrect(int(magnitudInput[1].get()), 91) and self.isTimeCorrect(int(magnitudInput[2].get()), 61) and self.isTimeCorrect(int(magnitudInput[3].get()), 61)
        return areFieldsNotEmpty and isMagnitudeValueCorrect and isMagnitudeDurationCorrect

    def configureMagnitudeButtons(self, controller, magnitud, buttonOptions):
        if(magnitud=="VELOCITY"):
            self.configureVelocityButtons(controller, buttonOptions)
        if(magnitud=="TEMPERATURE"):
            self.configureTemperatureButtons(controller, buttonOptions)
        if(magnitud=="POTENTIALHYDROGEN"):
            self.configurePotentialHydrogenButtons(controller, buttonOptions)

    def fillMagnitudeInformation(self, pageReference, controller):
        self.addMagnitudeInfo.append(Label(pageReference, text=controller.currentLanguage.fermentationPageContent[50], font=self.inputFont, fg = 'green', bg = self.colorORT))
        self.addMagnitudeInfo[len(self.addMagnitudeInfo)-1].place(x=740, y=165)
        self.changeMagnitudeInfo.append(Label(pageReference, text=controller.currentLanguage.fermentationPageContent[51], font=self.inputFont, fg = 'blue', bg = self.colorORT))
        self.changeMagnitudeInfo[len(self.changeMagnitudeInfo)-1].place(x=715, y=280)
        self.removeMagnitudeInfo.append(Label(pageReference, text=controller.currentLanguage.fermentationPageContent[52], font=self.inputFont, fg = 'red', bg = self.colorORT))
        self.removeMagnitudeInfo[len(self.removeMagnitudeInfo)-1].place(x=715, y=395)
        self.beginControlMagnitudeInfo.append(Label(pageReference, text=controller.currentLanguage.fermentationPageContent[53], font=self.inputFont, fg = 'green', bg = self.colorORT))
        self.beginControlMagnitudeInfo[len(self.beginControlMagnitudeInfo)-1].place(x=870, y=160)
        self.pauseControlMagnitudeInfo.append(Label(pageReference, text=controller.currentLanguage.fermentationPageContent[54], font=self.inputFont, fg = 'blue', bg = self.colorORT))
        self.pauseControlMagnitudeInfo[len(self.pauseControlMagnitudeInfo)-1].place(x=1010, y=520)
        self.stopControlMagnitudeInfo.append(Label(pageReference, text=controller.currentLanguage.fermentationPageContent[55], font=self.inputFont, fg = 'red', bg = self.colorORT))
        self.stopControlMagnitudeInfo[len(self.stopControlMagnitudeInfo)-1].place(x=1165, y=160)
        self.previousStepOfMagnitudeInfo.append(Label(pageReference, text=controller.currentLanguage.fermentationPageContent[56], font=self.inputFont, fg = 'DarkGoldenrod4', bg = self.colorORT))
        self.previousStepOfMagnitudeInfo[len(self.previousStepOfMagnitudeInfo)-1].place(x=860, y=520)
        self.nextStepOfMagnitudeInfo.append(Label(pageReference, text=controller.currentLanguage.fermentationPageContent[57], font=self.inputFont, fg = 'DarkGoldenrod4', bg = self.colorORT))
        self.nextStepOfMagnitudeInfo[len(self.nextStepOfMagnitudeInfo)-1].place(x=1165, y=520)
        self.restartControlMagnitudeInfo.append(Label(pageReference, text=controller.currentLanguage.fermentationPageContent[58], font=self.inputFont, fg = 'blue', bg = self.colorORT))
        self.restartControlMagnitudeInfo[len(self.restartControlMagnitudeInfo)-1].place(x=995, y=160)
        self.removeAllListMagnitudeInfo.append(Label(pageReference, text=controller.currentLanguage.fermentationPageContent[59], font=self.inputFont, fg = 'maroon4', bg = self.colorORT))
        self.removeAllListMagnitudeInfo[len(self.removeAllListMagnitudeInfo)-1].place(x=700, y=515)

    def setMagnitudeOptions(self, pageReference, controller, magnitud):
        magnitudesOptions = [Button(pageReference, relief = SUNKEN), Button(pageReference,relief = SUNKEN), Button(pageReference, relief = SUNKEN), Button(pageReference, relief = SUNKEN), Button(pageReference,relief = SUNKEN), Button(pageReference, relief = SUNKEN), Button(pageReference, relief = SUNKEN), Button(pageReference, relief = SUNKEN), Button(pageReference, relief = SUNKEN), Button(pageReference, relief = SUNKEN)]
        magnitudesOptions[0].place(x=720, y=85) # ADD
        magnitudesOptions[1].place(x=720, y=200) # CHANGE
        magnitudesOptions[2].place(x=720, y=315) # REMOVE
        magnitudesOptions[3].place(x=850, y=80)#720, y=505) # RUN
        magnitudesOptions[4].place(x=1000, y=440)#x=720, y=325)#880, y=505) # PAUSE
        magnitudesOptions[5].place(x=1150, y=80)#y=445)#1060, y=505) # STOP
        magnitudesOptions[6].place(x=850, y=440) #PREVIOUS STEP
        magnitudesOptions[7].place(x=1150, y=440) #NEXT STEP
        magnitudesOptions[8].place(x=1000, y=80) #RESTART
        magnitudesOptions[9].place(x=720, y=435) # REMOVE ALL
        self.fillMagnitudeInformation(pageReference, controller)
        self.configureMagnitudeButtons(controller, magnitud, magnitudesOptions)

    def setVelocityMagnitudeEntries(self, pageVelocity, controller):
        self.velocityInput.append(Spinbox(pageVelocity, from_=200, to=800, font=self.inputFont, width=7, justify='center'))#(Entry(pageVelocity, font=self.inputFont, width=10, justify='center')) # currentPasswordInput
        self.velocityInput[0].place(x=700, y=20)
        self.velocityInfo = Label(pageVelocity, text=controller.currentLanguage.fermentationPageContent[60], font=self.inputFont, fg = 'white', bg = self.colorORT)
        self.velocityInfo.place(x=805, y=20)
        velocitySecondsInfo = Label(pageVelocity, text="200-800 rpm", font=self.infoFont, fg = 'white', bg = self.colorORT)
        velocitySecondsInfo.place(x=710, y=50)
        self.velocityInput.append(Spinbox(pageVelocity, from_=0, to=90, font=self.inputFont, width=4, justify='center'))#Entry(pageVelocity, font=self.inputFont, width=4, justify='center')) # passwordInput
        self.velocityInput[1].place(x=915, y=20)
        velocityHoursInfo = Label(pageVelocity, text="hs", font=self.inputFont, fg = 'white', bg = self.colorORT)
        velocityHoursInfo.place(x=980, y=20)
        self.velocityInput.append(Spinbox(pageVelocity, from_=0, to=59, font=self.inputFont, width=4, justify='center'))#Entry(pageVelocity, font=self.inputFont, width=4, justify='center')) # confirmPasswordInput
        self.velocityInput[2].place(x=1010, y=20)
        velocityMinutesInfo = Label(pageVelocity, text="min", font=self.inputFont, fg = 'white', bg = self.colorORT)
        velocityMinutesInfo.place(x=1075, y=20)
        self.velocityInput.append(Spinbox(pageVelocity, from_=0, to=59, font=self.inputFont, width=4, justify='center'))#Entry(pageVelocity, font=self.inputFont, width=4, justify='center')) # confirmPasswordInput
        self.velocityInput[3].place(x=1120, y=20)
        velocitySecondsInfo = Label(pageVelocity, text="sec", font=self.inputFont, fg = 'white', bg = self.colorORT)
        velocitySecondsInfo.place(x=1190, y=20)

    def addVelocity(self, controller):
        if(self.isMagnitudeListEditable[0]):
            if(self.isMagnitudeInputCorrect(self.velocityInput, [199,801])):
                newVelocity = Velocity([self.velocityInput[0].get(), self.velocityInput[1].get(), self.velocityInput[2].get(), self.velocityInput[3].get()])
                newVelocity.setCustomization(self.velocityCustomizationInformation)
                controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].magnitudesToControl.addVelocity(newVelocity)
                self.fillVelocityList(controller)
            else:
                messagebox.showerror(controller.currentLanguage.fermentationPageContent[61], controller.currentLanguage.fermentationPageContent[62])
        else:
            messagebox.showwarning(controller.currentLanguage.fermentationPageContent[63], controller.currentLanguage.fermentationPageContent[64])

    def changeVelocity(self, controller):
        try:
            positionSelected = int(self.velocityList.curselection()[0])
            if(self.isMagnitudeListEditable[0] and not controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].isVelocityControlOnFreeWheel):
                if(self.isMagnitudeInputCorrect(self.velocityInput, [199,801])):
                    controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].magnitudesToControl.velocities[positionSelected].valueObjective = self.velocityInput[0].get()
                    controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].magnitudesToControl.velocities[positionSelected].duration = [self.velocityInput[1].get(), self.velocityInput[2].get(), self.velocityInput[3].get()]
                    self.fillVelocityList(controller)
                else:
                    messagebox.showerror(controller.currentLanguage.fermentationPageContent[61], controller.currentLanguage.fermentationPageContent[65])
            else:
                messagebox.showwarning(controller.currentLanguage.fermentationPageContent[63], controller.currentLanguage.fermentationPageContent[64])
        except IndexError:
            messagebox.showwarning(controller.currentLanguage.fermentationPageContent[66], controller.currentLanguage.fermentationPageContent[67])

    def removeVelocity(self, controller):
        try:
            positionSelected = int(self.velocityList.curselection()[0])
            if(self.isMagnitudeListEditable[0]):
                controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].magnitudesToControl.removeVelocity(positionSelected)
                self.fillVelocityList(controller)
            else:
                messagebox.showwarning(controller.currentLanguage.fermentationPageContent[63], controller.currentLanguage.fermentationPageContent[64])
        except IndexError:
            messagebox.showwarning(controller.currentLanguage.fermentationPageContent[66], controller.currentLanguage.fermentationPageContent[68])

    def setVelocityControlValues(self, controller):
        if(controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].isVelocityControlOnFreeWheel):
            controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].magnitudesToControl.clearVelocities()
            freeWheelVelocity = Velocity([self.freeWheelInformation[0].get(), 7*24, 0, 0])
            freeWheelVelocity.setCustomization(self.velocityCustomizationInformation)
            controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].magnitudesToControl.addVelocity(freeWheelVelocity)
            self.fillVelocityList(controller)
        position = 0
        for eachVelocity in controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].magnitudesToControl.velocities:
            controller.valuesVelocityControl[position] = int(eachVelocity.valueObjective)
            controller.durationVelocityControl[position] = int(eachVelocity.getDuration())
            position = position + 1

    def saveMagnitudeControlStatus(self, magnitudeFile, messageStatus):
        with open(magnitudeFile, 'a') as registerMagnitudeStatus:
            registerMagnitudeStatus.write(str(messageStatus)+'\n')
            registerMagnitudeStatus.close()


    def runVelocity(self, controller):
        self.setVelocityControlValues(controller)
        fileTime = datetime.today()
        self.velocityDataFileTimeStr = "ControlData/Velocity/DATA_Log/"+str(fileTime.strftime("%Y%m%d_%I%M%S"))+"_VEL.txt"
        print("VELOCITY FILE IN RUN: ", self.velocityDataFileTimeStr)
        controller.application.systemCurrentStatus.velocityControlData[0]=self.velocityDataFileTimeStr
        controller.settingVelocityControl[4] = int(self.velocityDataFileTimeStr[39:45])
        controller.settingVelocityControl[5] = int(self.velocityDataFileTimeStr[30:38])
        controller.settingVelocityControl[2] = 0
        controller.settingVelocityControl[1] = 1
        controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].dataFilenames.append(str(fileTime.strftime("%Y%m%d_%I%M%S")))
        self.isControlInitialized[0] = True
        currentTime = datetime.today()
        currentTimeStr = currentTime.strftime("%b %d %Y %H:%M:%S.%f")
        self.velocityInformation[0]['text'] = controller.currentLanguage.fermentationPageContent[69] + currentTimeStr
        self.velocityInformation[1]['text'] = controller.currentLanguage.fermentationPageContent[70]
        controller.application.systemCurrentStatus.velocityControlData[2]=self.velocityInformation[0]['text']
        #self.generalInformation[0]['text'] = controller.currentLanguage.fermentationPageContent[71]
        self.isMagnitudeListEditable[0] = False
        controller.application.saveStatusDataToFile()
        self.saveMagnitudeControlStatus(self.velocityStatusFileTimeStr, currentTimeStr+" - Control INITIATED Successfully")

    def runVelocityControl(self, controller):
        if(len(controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].magnitudesToControl.velocities)>0):
            controller.application.systemCurrentStatus.velocityControlData[1]="1"
            self.runVelocity(controller)
        else:
            messagebox.showwarning(controller.currentLanguage.fermentationPageContent[63], controller.currentLanguage.fermentationPageContent[72])

    def configureVelocityPauseState(self, controller):
        currentTime = datetime.today()
        currentTimeStr = currentTime.strftime("%b %d %Y %H:%M:%S.%f")
        if(controller.settingVelocityControl[2] == 0):
            controller.settingVelocityControl[2] = 2
            self.velocityInformation[1]['text'] = controller.currentLanguage.fermentationPageContent[73]
            #self.generalInformation[0]['text'] = controller.currentLanguage.fermentationPageContent[74]
            self.isMagnitudeListEditable[0] = True
            self.saveMagnitudeControlStatus(self.velocityStatusFileTimeStr, currentTimeStr+" - Control PAUSED Successfully")
        else:
            controller.settingVelocityControl[2] = 0
            controller.settingVelocityControl[1] = 1
            self.setVelocityControlValues(controller)
            self.velocityInformation[1]['text'] = controller.currentLanguage.fermentationPageContent[75]
            #self.generalInformation[0]['text'] = controller.currentLanguage.fermentationPageContent[76]
            self.isMagnitudeListEditable[0] = False
            self.saveMagnitudeControlStatus(self.velocityStatusFileTimeStr, currentTimeStr+" - Control RESUMED AFTER PAUSED Successfully")
        controller.application.systemCurrentStatus.velocityControlData[2]=self.velocityInformation[0]['text']
        controller.application.systemCurrentStatus.velocityControlData[3] = self.velocityInformation[2]['text']
        controller.application.saveStatusDataToFile()

    def pauseVelocityControl(self, controller):
        if(controller.settingVelocityControl[1] == 1 or controller.settingVelocityControl[2] == 2):
            controller.application.systemCurrentStatus.velocityControlData[1]="2"
            self.configureVelocityPauseState(controller)
        else:
            messagebox.showwarning(controller.currentLanguage.fermentationPageContent[63], controller.currentLanguage.fermentationPageContent[77])

    def stopVelocity(self, controller):
        controller.settingVelocityControl[1] = 0
        self.isControlInitialized[0] = False
        controller.settingVelocityControl[2] = 1
        currentTime = datetime.today()
        currentTimeStr = currentTime.strftime("%b %d %Y %H:%M:%S.%f")
        self.velocityInformation[0]['text'] =  controller.currentLanguage.fermentationPageContent[78] + currentTimeStr
        self.velocityInformation[1]['text'] = controller.currentLanguage.fermentationPageContent[79]
        #self.generalInformation[0]['text'] =  controller.currentLanguage.fermentationPageContent[80]
        self.isMagnitudeListEditable[0] = True
        controller.application.systemCurrentStatus.velocityControlData[2]=self.velocityInformation[0]['text']
        controller.application.systemCurrentStatus.velocityControlData[3] = self.velocityInformation[2]['text']
        controller.application.saveStatusDataToFile()
        self.saveMagnitudeControlStatus(self.velocityStatusFileTimeStr, currentTimeStr+" - Control STOPPED Successfully")

    def stopVelocityControl(self, controller):
        if(controller.settingVelocityControl[1] == 1):
            controller.application.systemCurrentStatus.velocityControlData[1]="3"
            self.stopVelocity(controller)
        else:
            messagebox.showwarning(controller.currentLanguage.fermentationPageContent[63], controller.currentLanguage.fermentationPageContent[81])

    def restartVelocityControl(self, controller):
        controller.settingVelocityControl[1] = 0
        controller.settingVelocityControl[2] = 1
        currentTime = datetime.today()
        currentTimeStr = currentTime.strftime("%b %d %Y %H:%M:%S.%f")
        self.velocityInformation[0]['text'] = controller.currentLanguage.fermentationPageContent[82] + currentTimeStr
        self.velocityInformation[1]['text'] = controller.currentLanguage.fermentationPageContent[83]
        #self.generalInformation[0]['text'] = controller.currentLanguage.fermentationPageContent[84]
        self.saveMagnitudeControlStatus(self.velocityStatusFileTimeStr, currentTimeStr+" - Control RESTARTED AND INITIATED Successfully")
        time.sleep(1)
        fileTime = datetime.today()
        self.velocityDataFileTimeStr = "ControlData/Velocity/DATA_Log/"+str(fileTime.strftime("%Y%m%d_%I%M%S"))+"_VEL.txt"
        controller.settingVelocityControl[4] = int(self.velocityDataFileTimeStr[39:45])
        controller.settingVelocityControl[5] = int(self.velocityDataFileTimeStr[30:38])
        controller.settingVelocityControl[2] = 0
        controller.settingVelocityControl[1] = 1
        controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].dataFilenames.append(str(fileTime.strftime("%Y%m%d_%I%M%S")))

    def previousStepOnVelocityControl(self, controller):
        currentTime = datetime.today()
        currentTimeStr = currentTime.strftime("%b %d %Y %H:%M:%S.%f")
        controller.settingVelocityControl[2] = 3
        self.saveMagnitudeControlStatus(self.velocityStatusFileTimeStr, currentTimeStr+" - Control WENT BACKWARDS ONE STEP Successfully")
        if(controller.settingVelocityControl[3]<=0):
            self.velocityList.itemconfig(0, {'bg':'cornflower blue'})
        else:
            self.velocityList.itemconfig(controller.settingVelocityControl[3]+1, {'bg':'white'})
            self.velocityList.itemconfig(controller.settingVelocityControl[3], {'bg':'cornflower blue'})

    def nextStepOnVelocityControl(self, controller):
        currentTime = datetime.today()
        currentTimeStr = currentTime.strftime("%b %d %Y %H:%M:%S.%f")
        controller.settingVelocityControl[2] = 4
        self.saveMagnitudeControlStatus(self.velocityStatusFileTimeStr, currentTimeStr+" - Control WENT FORWARDS ONE STEP Successfully")
        if(controller.settingVelocityControl[3]<len(controller.application.listOfFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].magnitudesToControl.velocities)):
            self.velocityList.itemconfig(controller.settingVelocityControl[3]-1, {'bg':'white'})
            self.velocityList.itemconfig(controller.settingVelocityControl[3], {'bg':'cornflower blue'})

    def removeAllListOfVelocityControl(self, controller):
        if(self.isMagnitudeListEditable[0]):
            controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].magnitudesToControl.clearVelocities()
            self.fillVelocityList(controller)
        else:
            messagebox.showwarning(controller.currentLanguage.fermentationPageContent[63], controller.currentLanguage.fermentationPageContent[64])

    def updateVelocityGlobalInformation(self, controller):
        if(len(self.velList)>0):
            self.systemInformation[0]['text'] = str(self.velList[len(self.velList)-1])
        else:
            self.systemInformation[0]['text'] = "0.00"
        if(len(self.freqList)>0):
            self.systemInformation[1]['text'] = str(self.freqList[len(self.freqList)-1])+" Hz"
        else:
            self.systemInformation[1]['text'] = "0.00 Hz"

        if(controller.settingVelocityControl[6]==0):
            self.systemInformation[0]['text'] = self.systemInformation[0]['text'] + " rpm"
        if(controller.settingVelocityControl[6]==1):
            self.systemInformation[0]['text'] = self.systemInformation[0]['text'] + " m/s"
        if(controller.settingVelocityControl[6]==2):
            self.systemInformation[0]['text'] = self.systemInformation[0]['text'] + " rad/s"

    def updateVelocityGraphic(self, controller):
        #fileData = open("ControlData/Velocity/20180903_153022.txt","r")
        filePath = self.velocityDataFileTimeStr
        velocityFile = Path(filePath)
        self.velList=[]
        self.freqList=[]
        self.secondsListVelocity=[]
        if(velocityFile.exists()):
            fileData = open(filePath,"r")
            pulldata = fileData.read()
            dataList = pulldata.split('\n')

            for eachLine in dataList:
                if len(eachLine)>1:
                    try:   
                        vel, velObj, temp, freq, sec, mili = eachLine.split(',')
                        self.velList.append(float(vel))
                        self.freqList.append(round(float(freq),2))
                        self.secondsListVelocity.append(int(sec)+int(mili)*0.000001)
                    except ValueError:
                        print("VALUE ERROR GRAPH VEL")

            fileData.close()
            self.velocityGraph.clear()
            self.velocityGraph.set_xlabel(controller.currentLanguage.fermentationPageContent[42], color='tab:blue')
            if(controller.settingVelocityControl[6]==0):
                self.velocityGraph.set_ylabel(controller.currentLanguage.fermentationPageContent[43]+"[rpm]", color='tab:blue')
            if(controller.settingVelocityControl[6]==1):
                self.velocityGraph.set_ylabel(controller.currentLanguage.fermentationPageContent[43]+"[m/s]", color='tab:blue')
            if(controller.settingVelocityControl[6]==2):
                self.velocityGraph.set_ylabel(controller.currentLanguage.fermentationPageContent[43]+"[rad]/s]", color='tab:blue')
            self.velocityGraph.tick_params(axis='x', labelcolor='tab:blue')
            self.velocityGraph.tick_params(axis='y', labelcolor='tab:blue')
            #self.velocityGraph.yaxis.set_major_locator(ticker.MultipleLocator(50))
            self.velocityGraph.grid(b=None, which='major', axis='both', linestyle='dashed', linewidth=1)
            self.velocityGraph.plot(self.secondsListVelocity, self.velList, color='tab:blue')
            self.velocityCanvas.draw()
            self.velocityCanvas.get_tk_widget().place(x=150, y=10)
        
        if(len(self.velList)==0):
            return 0
        else:
            return self.velList[len(self.velList)-1]
        #self.after(10000,lambda:self.updateVelocityGraphic(controller))

    def checkVelocityError(self, controller):
        if(self.isErrorFound[0] and self.stopMagniudeWhenVelocity[0].get()==1):
            controller.settingTemperatureControl[1] = 0
            self.isControlInitialized[1] = False
            controller.settingTemperatureControl[2] = 1
        if(self.isErrorFound[0] and self.stopMagniudeWhenVelocity[1].get()==1):
            controller.settingPotentialControl[1] = 0
            self.isControlInitialized[2] = False
            controller.settingPotentialControl[2] = 1
        self.isErrorFound[0] = False

    def setVelocityDisplay(self, controller, currentVelocity):
        controller.settingScreensControl[2] = 6 #Page Status
        controller.settingScreensControl[6] = 0 #Error Status - CHANGE WHEN GEMMA
        controller.settingScreensControl[9] = controller.settingVelocityControl[6] #Unit Status
        controller.settingScreensControl[10] = controller.settingVelocityControl[9] #Orientation
        controller.settingScreensControl[13] = controller.settingVelocityControl[8] #Slope
        controller.settingScreensControl[14] = controller.settingScreensControl[14] + 1 #Controls Running
        controller.settingScreensControl[18] = int(currentVelocity*10) #Value
        if(controller.settingScreensControl[1] != 1):
            controller.settingScreensControl[1] = 1

    def checkVelocityStatus(self, controller):
        if(self.isControlInitialized[0]):
            currentVelocity = self.updateVelocityGraphic(controller)
        #self.updateVelocityGlobalInformation(controller)
        self.checkVelocityError(controller)
        currentTime = datetime.today()
        currentTimeStr = currentTime.strftime("%b %d %Y %H:%M:%S.%f")        
        if(controller.settingVelocityControl[1]!=0):
            self.setVelocityDisplay(controller, currentVelocity)
            currentStepInformation = self.velocityList.get(controller.settingVelocityControl[3])
            self.velocityInformation[2]['text'] = controller.currentLanguage.fermentationPageContent[85] + currentStepInformation
            if(controller.settingVelocityControl[3]<=0):
                self.velocityList.itemconfig(0, {'bg':'cornflower blue'})
            else:
                self.velocityList.itemconfig(controller.settingVelocityControl[3]-1, {'bg':'white'})
                self.velocityList.itemconfig(controller.settingVelocityControl[3], {'bg':'cornflower blue'})
            if(self.currentMagnitudeControlStep[0]!=currentStepInformation):
                self.saveMagnitudeControlStatus(self.velocityStatusFileTimeStr, currentTimeStr+" - "+currentStepInformation[3:])
                self.currentMagnitudeControlStep[0] = currentStepInformation
        else:
            self.velocityInformation[2]['text'] = controller.currentLanguage.fermentationPageContent[86]
            self.isMagnitudeListEditable[0] = True
            if(self.isControlInitialized[0]):
                self.velocityInformation[0]['text'] = controller.currentLanguage.fermentationPageContent[87] + currentTimeStr
                self.velocityInformation[1]['text'] = controller.currentLanguage.fermentationPageContent[88]
                #self.generalInformation[0]['text'] = controller.currentLanguage.fermentationPageContent[89]
                self.isControlInitialized[0] = False
                self.velocityList.itemconfig(controller.settingVelocityControl[3], {'bg':'white'})
                self.saveMagnitudeControlStatus(self.velocityStatusFileTimeStr, currentTimeStr+" - Control FINISHED Successfully")
        controller.application.loadStatusDataFromFile()
        controller.application.systemCurrentStatus.velocityControlData[3] = self.velocityInformation[2]['text']
        if(controller.application.systemCurrentStatus.velocityControlData[1]=="0"):
            print("Velocidad Sin Arrancar")
        if(controller.application.systemCurrentStatus.velocityControlData[1]=="1" and not self.isControlInitialized[0]):
            self.runVelocity(controller)
            print("Velocidad EJECUTANDOSE")
        if(controller.application.systemCurrentStatus.velocityControlData[1]=="2" and self.isControlInitialized[0]):
            self.pauseVelocityControl(controller)
            print("Velocidad PAUSADO")
        if(controller.application.systemCurrentStatus.velocityControlData[1]=="3" and self.isControlInitialized[0]):
            self.stopVelocity(controller)
            print("Velocidad DETENIDO")
        controller.application.systemCurrentStatus.velocityControlData[3] = self.velocityInformation[2]['text']
        controller.application.saveStatusDataToFile()
        self.after(10000,lambda:self.checkVelocityStatus(controller))

    def configureVelocityButtons(self, controller, buttonOptions):
        buttonOptions[0].config(image = self.buttonsVelocity[0], command = lambda:self.addVelocity(controller))
        buttonOptions[1].config(image = self.buttonsVelocity[1], command = lambda:self.changeVelocity(controller))
        buttonOptions[2].config(image = self.buttonsVelocity[2], command = lambda:self.removeVelocity(controller))
        buttonOptions[3].config(image = self.buttonsVelocity[3], command = lambda:self.runVelocityControl(controller))
        buttonOptions[4].config(image = self.buttonsVelocity[4], command = lambda:self.pauseVelocityControl(controller))
        buttonOptions[5].config(image = self.buttonsVelocity[5], command = lambda:self.stopVelocityControl(controller))
        buttonOptions[6].config(image = self.buttonsVelocity[6], command = lambda:self.previousStepOnVelocityControl(controller))
        buttonOptions[7].config(image = self.buttonsVelocity[7], command = lambda:self.nextStepOnVelocityControl(controller))
        buttonOptions[8].config(image = self.buttonsVelocity[8], command = lambda:self.restartVelocityControl(controller))
        buttonOptions[9].config(image = self.buttonsVelocity[9], command = lambda:self.removeAllListOfVelocityControl(controller))

    def fillVelocityList(self, controller):
        if(controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].isVelocityControlOnFreeWheel):
            self.velocityList.delete(0,END)
            self.velocityList.insert(1, controller.currentLanguage.fermentationPageContent[90]+self.freeWheelInformation[0].get()+" rpm")
        else:
            velocities = controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].magnitudesToControl.velocities #len(controller.application.listFermentations.fermentations)-1].magnitudesToControl.velocities
            self.velocityList.delete(0,END)
            if(len(velocities)>0):
                position = 1
                for eachVelocity in velocities:
                    evolutionInformation = controller.currentLanguage.fermentationPageContent[91]
                    if(position==1):
                        evolutionInformation = controller.currentLanguage.fermentationPageContent[92]
                    elif(velocities[position-2].valueObjective>eachVelocity.valueObjective):
                        evolutionInformation = controller.currentLanguage.fermentationPageContent[93]
                    self.velocityList.insert(position, str(position)+". "+evolutionInformation+eachVelocity.showInformation())
                    position = position + 1
                    #print("DURATION: ", eachVelocity.getDuration())
                    #print("INFORMATION: ", eachVelocity.showInformation())
            else:
                self.velocityList.insert(1, controller.currentLanguage.fermentationPageContent[94])

    def setVelocityList(self, pageVelocity, controller):
        self.velocityCanvas = FigureCanvasTkAgg(self.velocityFigure, pageVelocity)
        self.velocityCanvas.draw()
        self.velocityCanvas.get_tk_widget().place(x=150, y=10)

        #toolbar = NavigationToolbar2TkAgg(canvas, pageVelocity)
        #toolbar.update()
        #canvas._tkcanvas.place(x=150, y=10)
        #self.velocityGraphic = Label(pageVelocity, borderwidth=2, relief="groove", text='VELOCITY GRAPHIC', fg='white', bg = self.colorORT, height=27, width=75, highlightbackground='white')
        #self.velocityGraphic.place(x=150, y=10)

        self.velocityInformation.append(Label(pageVelocity, text=controller.currentLanguage.fermentationPageContent[95], font=self.infoFont, fg = self.colorORT, bg = 'white', height=2, width=58))
        self.velocityInformation[0].place(x=150, y=420)
        self.velocityInformation.append(Label(pageVelocity, text=controller.currentLanguage.fermentationPageContent[96], font=self.infoFont, fg = self.colorORT, bg = 'white', height=2, width=58))
        self.velocityInformation[1].place(x=150, y=455)
        self.velocityInformation.append(Label(pageVelocity, text=controller.currentLanguage.fermentationPageContent[97], font=self.infoFont, fg = self.colorORT, bg = 'white', height=2, width=58))
        self.velocityInformation[2].place(x=150, y=490)
        self.velocityList = Listbox(pageVelocity, width=50, height=11, font=self.listElementFont)
        self.velocityList.place(x=840,y=200)
        self.fillVelocityList(controller)

    def fillPageVelocity(self, pageVelocity, controller):
        controller.setImagesandSeparators(pageVelocity, 'velocityElement', [115,270,10,10,115,270,10,300])
        controller.setImagesandSeparators(pageVelocity, 'velocityElement', [115,270,1250,10,115,270,1250,300])
        self.setVelocityMagnitudeEntries(pageVelocity, controller)
        self.setMagnitudeOptions(pageVelocity, controller, "VELOCITY")
        self.setVelocityList(pageVelocity, controller)

    def setImagesOnPageTemperature(self, pageTemperature):
        userElement = Picture(['temperatureElement3','png',140,560,10,0],0)
        userElement.purpose = 'Words'
        userElementPic = userElement.generateLabel(pageTemperature)
        userElementPic.place(x=userElement.location[0],y=userElement.location[1])

        userElement2 = Picture(['temperatureElement3','png',140,560,1240,0],180)
        userElement2.purpose = 'Words'
        userElement2Pic = userElement2.generateLabel(pageTemperature)
        userElement2Pic.place(x=userElement2.location[0],y=userElement2.location[1])

    def setTemperatureMagnitudeEntries(self, pageTemperature, controller):
        self.temperatureInput.append(Spinbox(pageTemperature, from_=10, to=95, font=self.inputFont, width=7, justify='center'))#(Entry(pageVelocity, font=self.inputFont, width=10, justify='center')) # currentPasswordInput
        self.temperatureInput[0].place(x=700, y=20)
        self.temperatureInfo = Label(pageTemperature, text=controller.currentLanguage.fermentationPageContent[98], font=self.inputFont, fg = 'white', bg = self.colorORT)
        self.temperatureInfo.place(x=805, y=20)
        temperaturRangeInfo = Label(pageTemperature, text="10-95 ℃", font=self.infoFont, fg = 'white', bg = self.colorORT)
        temperaturRangeInfo.place(x=710, y=50)
        self.temperatureInput.append(Spinbox(pageTemperature, from_=0, to=90, font=self.inputFont, width=4, justify='center'))#Entry(pageVelocity, font=self.inputFont, width=4, justify='center')) # passwordInput
        self.temperatureInput[1].place(x=915, y=20)
        temperatureHoursInfo = Label(pageTemperature, text="hs", font=self.inputFont, fg = 'white', bg = self.colorORT)
        temperatureHoursInfo.place(x=980, y=20)
        self.temperatureInput.append(Spinbox(pageTemperature, from_=0, to=59, font=self.inputFont, width=4, justify='center'))#Entry(pageVelocity, font=self.inputFont, width=4, justify='center')) # confirmPasswordInput
        self.temperatureInput[2].place(x=1010, y=20)
        temperatureMinutesInfo = Label(pageTemperature, text="min", font=self.inputFont, fg = 'white', bg = self.colorORT)
        temperatureMinutesInfo.place(x=1080, y=20)
        self.temperatureInput.append(Spinbox(pageTemperature, from_=0, to=59, font=self.inputFont, width=4, justify='center'))#Entry(pageVelocity, font=self.inputFont, width=4, justify='center')) # confirmPasswordInput
        self.temperatureInput[3].place(x=1120, y=20)
        temperatureSecondsInfo = Label(pageTemperature, text="sec", font=self.inputFont, fg = 'white', bg = self.colorORT)
        temperatureSecondsInfo.place(x=1185, y=20)

    def addTemperature(self, controller):
        if(self.isMagnitudeListEditable[1]):
            if(self.isMagnitudeInputCorrect(self.temperatureInput, [9,98])):
                newTemperature = Temperature([self.temperatureInput[0].get(), self.temperatureInput[1].get(), self.temperatureInput[2].get(), self.temperatureInput[3].get()])
                newTemperature.setCustomization(self.temperatureCustomizationInformation)
                controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].magnitudesToControl.addTemperature(newTemperature)
                #print("LIST TEMPERATURE: ", controller.application.listFermentations.fermentations[len(controller.application.listFermentations.fermentations)-1].temperatureControl.magnitudes)
                self.fillTemperatureList(controller)
            else:
                messagebox.showerror(controller.currentLanguage.fermentationPageContent[61], controller.currentLanguage.fermentationPageContent[62])
        else:
            messagebox.showwarning(controller.currentLanguage.fermentationPageContent[99], controller.currentLanguage.fermentationPageContent[64])

    def changeTemperature(self, controller):
        try:
            positionSelected = int(self.temperatureList.curselection()[0])
            if(self.isMagnitudeListEditable[1] and not controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].isTemperatureControlOnFreeWheel):
                if(self.isMagnitudeInputCorrect(self.temperatureInput, [9,98])):
                    controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].magnitudesToControl.temperatures[positionSelected].valueObjective = self.temperatureInput[0].get()
                    controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].magnitudesToControl.temperatures[positionSelected].duration = [self.temperatureInput[1].get(), self.temperatureInput[2].get(), self.temperatureInput[3].get()]
                    self.fillTemperatureList(controller)
                else:
                    messagebox.showerror(controller.currentLanguage.fermentationPageContent[61], controller.currentLanguage.fermentationPageContent[62])
            else:
                messagebox.showwarning(controller.currentLanguage.fermentationPageContent[99], controller.currentLanguage.fermentationPageContent[64])
        except IndexError:
            messagebox.showwarning(controller.currentLanguage.fermentationPageContent[66], controller.currentLanguage.fermentationPageContent[67])

    def removeTemperature(self, controller):
        try:
            positionSelected = int(self.temperatureList.curselection()[0])
            if(self.isMagnitudeListEditable[1]):
                controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].magnitudesToControl.removeTemperature(positionSelected)
                self.fillTemperatureList(controller)
            else:
                messagebox.showwarning(controller.currentLanguage.fermentationPageContent[99], controller.currentLanguage.fermentationPageContent[64])
        except IndexError:
            messagebox.showwarning(controller.currentLanguage.fermentationPageContent[66], controller.currentLanguage.fermentationPageContent[68])

    def setTemperatureControlValues(self, controller):
        if(controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].isTemperatureControlOnFreeWheel):
            controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].magnitudesToControl.clearTemperatures()
            freeWheelTemperature = Temperature([self.freeWheelInformation[2].get(), 7*24, 0, 0])
            freeWheelTemperature.setCustomization(self.temperatureCustomizationInformation)
            controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].magnitudesToControl.addTemperature(freeWheelTemperature)
            self.fillTemperatureList(controller)
        position = 0
        for eachTemperature in controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].magnitudesToControl.temperatures:
            controller.valuesTemperatureControl[position] = int(eachTemperature.valueObjective)
            controller.durationTemperatureControl[position] = int(eachTemperature.getDuration())
            position = position + 1

    def runTemperature(self, controller):
        self.setTemperatureControlValues(controller)
        fileTime = datetime.today()
        self.temperatureDataFileTimeStr = "ControlData/Temperature/DATA_Log/"+str(fileTime.strftime("%Y%m%d_%I%M%S"))+"_TEM.txt"
        print("FILE TEMP EN RUN: ", self.temperatureDataFileTimeStr)
        controller.application.systemCurrentStatus.temperatureControlData[0]=self.temperatureDataFileTimeStr
        controller.settingTemperatureControl[4] = int(self.temperatureDataFileTimeStr[42:48])
        controller.settingTemperatureControl[5] = int(self.temperatureDataFileTimeStr[33:41])
        controller.settingTemperatureControl[2] = 0
        controller.settingTemperatureControl[1] = 1
        controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].dataFilenames.append(str(fileTime.strftime("%Y%m%d_%I%M%S")))
        self.isControlInitialized[1] = True
        currentTime = datetime.today()
        currentTimeStr = currentTime.strftime("%b %d %Y %H:%M:%S.%f")
        self.temperatureInformation[0]['text'] = controller.currentLanguage.fermentationPageContent[100] + currentTimeStr
        self.temperatureInformation[1]['text'] = controller.currentLanguage.fermentationPageContent[70]
        controller.application.systemCurrentStatus.temperatureControlData[2]=self.temperatureInformation[0]['text']
        #self.generalInformation[1]['text'] = controller.currentLanguage.fermentationPageContent[101]
        self.isMagnitudeListEditable[1] = False
        controller.application.saveStatusDataToFile()
        self.saveMagnitudeControlStatus(self.temperatureStatusFileTimeStr, currentTimeStr+" - Control INITIATED Successfully")

    def runTemperatureControl(self, controller):
        if(len(controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].magnitudesToControl.temperatures)>0):
            controller.application.systemCurrentStatus.temperatureControlData[1]="1"    
            self.runTemperature(controller)
        else:
            messagebox.showwarning(controller.currentLanguage.fermentationPageContent[99], controller.currentLanguage.fermentationPageContent[72])

    def configureTemperaturePauseState(self, controller):
        currentTime = datetime.today()
        currentTimeStr = currentTime.strftime("%b %d %Y %H:%M:%S.%f")
        if(controller.settingTemperatureControl[2] == 0):
            controller.settingTemperatureControl[2] = 1
            self.temperatureInformation[1]['text'] = controller.currentLanguage.fermentationPageContent[73]
            #self.generalInformation[1]['text'] = controller.currentLanguage.fermentationPageContent[102]
            self.isMagnitudeListEditable[1] = True
            self.saveMagnitudeControlStatus(self.temperatureStatusFileTimeStr, currentTimeStr+" - Control PAUSED Successfully")
        else:
            controller.settingTemperatureControl[2] = 0
            controller.settingTemperatureControl[1] = 1
            self.setTemperatureControlValues(controller)
            self.temperatureInformation[1]['text'] = controller.currentLanguage.fermentationPageContent[75]
            #self.generalInformation[1]['text'] = controller.currentLanguage.fermentationPageContent[103]
            self.isMagnitudeListEditable[1] = False
            self.saveMagnitudeControlStatus(self.temperatureStatusFileTimeStr, currentTimeStr+" - Control RESUMED AFTER PAUSED Successfully")
        controller.application.systemCurrentStatus.temperatureControlData[2]=self.temperatureInformation[0]['text']
        controller.application.systemCurrentStatus.temperatureControlData[3] = self.temperatureInformation[2]['text']
        controller.application.saveStatusDataToFile()

    def pauseTemperatureControl(self, controller):
        if(controller.settingTemperatureControl[1] == 1 or controller.settingTemperatureControl[2] == 2):
            controller.application.systemCurrentStatus.temperatureControlData[1]="2"
            self.configureTemperaturePauseState(controller)
        else:
            messagebox.showwarning(controller.currentLanguage.fermentationPageContent[99], controller.currentLanguage.fermentationPageContent[77])

    def stopTemperature(self, controller):
        controller.settingTemperatureControl[1] = 0
        self.isControlInitialized[1] = False
        controller.settingTemperatureControl[2] = 1
        currentTime = datetime.today()
        currentTimeStr = currentTime.strftime("%b %d %Y %H:%M:%S.%f")
        self.temperatureInformation[0]['text'] = controller.currentLanguage.fermentationPageContent[104] + currentTimeStr
        self.temperatureInformation[1]['text'] = controller.currentLanguage.fermentationPageContent[79]
        #self.generalInformation[1]['text'] = controller.currentLanguage.fermentationPageContent[105]
        controller.application.systemCurrentStatus.temperatureControlData[2]=self.temperatureInformation[0]['text']
        controller.application.systemCurrentStatus.temperatureControlData[3] = self.temperatureInformation[2]['text']
        controller.application.saveStatusDataToFile()
        self.isMagnitudeListEditable[1] = True
        self.saveMagnitudeControlStatus(self.temperatureStatusFileTimeStr, currentTimeStr+" - Control STOPPED Successfully")

    def stopTemperatureControl(self, controller):
        if(controller.settingTemperatureControl[1] == 1):
            controller.application.systemCurrentStatus.temperatureControlData[1]="3" 
            self.stopTemperature(controller)
        else:
            messagebox.showwarning(controller.currentLanguage.fermentationPageContent[99], controller.currentLanguage.fermentationPageContent[81])

    def restartTemperatureControl(self, controller):
        controller.settingTemperatureControl[1] = 0
        controller.settingTemperatureControl[2] = 1
        currentTime = datetime.today()
        currentTimeStr = currentTime.strftime("%b %d %Y %H:%M:%S.%f")
        self.temperatureInformation[0]['text'] = controller.currentLanguage.fermentationPageContent[106] + currentTimeStr
        self.temperatureInformation[1]['text'] = controller.currentLanguage.fermentationPageContent[83]
        #self.generalInformation[1]['text'] = controller.currentLanguage.fermentationPageContent[107]
        self.saveMagnitudeControlStatus(self.temperatureStatusFileTimeStr, currentTimeStr+" - Control RESTARTED AND INITIATED Successfully")
        time.sleep(15)
        fileTime = datetime.today()
        self.temperatureDataFileTimeStr = "ControlData/Temperature/DATA_Log/"+str(fileTime.strftime("%Y%m%d_%I%M%S"))+"_TEM.txt"
        controller.settingTemperatureControl[4] = int(self.temperatureDataFileTimeStr[42:48])
        controller.settingTemperatureControl[5] = int(self.temperatureDataFileTimeStr[33:41])
        controller.settingTemperatureControl[2] = 0
        controller.settingTemperatureControl[1] = 1
        controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].dataFilenames.append(str(fileTime.strftime("%Y%m%d_%I%M%S")))

    def previousStepOnTemperatureControl(self, controller):
        currentTime = datetime.today()
        currentTimeStr = currentTime.strftime("%b %d %Y %H:%M:%S.%f")
        controller.settingTemperatureControl[2] = 3
        self.saveMagnitudeControlStatus(self.temperatureStatusFileTimeStr, currentTimeStr+" - Control WENT BACKWARDS ONE STEP Successfully")
        if(controller.settingTemperatureControl[3]<=0):
            self.temperatureList.itemconfig(0, {'bg':'orange'})
        else:
            self.temperatureList.itemconfig(controller.settingTemperatureControl[3]+1, {'bg':'white'})
            self.temperatureList.itemconfig(controller.settingTemperatureControl[3], {'bg':'orange'})

    def nextStepOnTemperatureControl(self, controller):
        currentTime = datetime.today()
        currentTimeStr = currentTime.strftime("%b %d %Y %H:%M:%S.%f")
        controller.settingTemperatureControl[2] = 4
        self.saveMagnitudeControlStatus(self.temperatureStatusFileTimeStr, currentTimeStr+" - Control WENT FORWARDS ONE STEP Successfully")
        if(controller.settingTemperatureControl[3]<len(controller.application.listOfFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].magnitudesToControl.temperatures)):
            self.temperatureList.itemconfig(controller.settingTemperatureControl[3]-1, {'bg':'white'})
            self.temperatureList.itemconfig(controller.settingTemperatureControl[3], {'bg':'orange'})

    def removeAllListOfTemperatureControl(self, controller):
        if(self.isMagnitudeListEditable[1]):
            controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].magnitudesToControl.clearTemperatures()
            self.fillTemperatureList(controller)
        else:
            messagebox.showwarning(controller.currentLanguage.fermentationPageContent[99], controller.currentLanguage.fermentationPageContent[64])

    def updateTemperatureGlobalInformation(self, controller):
        if(len(self.temperatureFermentorList)>0):
            self.systemInformation[2]['text'] = str(self.temperatureFermentorList[len(self.temperatureFermentorList)-1])
        else:
            self.systemInformation[2]['text'] = "0.00"
        if(len(self.temperatureBathList)>0):
            self.systemInformation[3]['text'] = str(self.temperatureBathList[len(self.temperatureBathList)-1])
        else:
            self.systemInformation[3]['text'] = "0.00"
        if(controller.settingTemperatureControl[6]==0):
            self.systemInformation[2]['text'] = self.systemInformation[2]['text'] + " °C"
            self.systemInformation[3]['text'] = self.systemInformation[3]['text'] + " °C"
        if(controller.settingTemperatureControl[6]==1):
            self.systemInformation[2]['text'] = self.systemInformation[2]['text'] + " K"
            self.systemInformation[3]['text'] = self.systemInformation[3]['text'] + " K"
        if(controller.settingTemperatureControl[6]==2):
            self.systemInformation[2]['text'] = self.systemInformation[2]['text'] + " °F"
            self.systemInformation[3]['text'] = self.systemInformation[3]['text'] + " °F"

    def updateTemperatureGraphic(self, controller):
        #fileData = open("ControlData/Temperature/2018-09-03_1530.txt","r")
        filePath = self.temperatureDataFileTimeStr
        temperatureFile = Path(filePath)
        self.temperatureFermentorList=[]
        self.temperatureBathList=[]
        self.secondsListTemperature=[]
        if(temperatureFile.exists()):
            fileData = open(filePath,"r")
            pulldata = fileData.read()
            dataList = pulldata.split('\n')

            for eachLine in dataList:
                if len(eachLine)>1:
                    try:
                        tempFermentor, tempFermentorObj, tempBath, tempBathObj, pumpStep, sec, mili = eachLine.split(',')
                        self.temperatureFermentorList.append(float(tempFermentor))
                        self.temperatureBathList.append(float(tempBath))
                        self.secondsListTemperature.append(int(sec)+int(mili)*0.000001)
                    except ValueError:
                        print("VALUE ERROR")

            fileData.close()
            self.temperatureGraph.clear()
            self.temperatureGraph.set_xlabel(controller.currentLanguage.fermentationPageContent[42], color='tab:orange')
            if(controller.settingTemperatureControl[6]==0):
                self.temperatureGraph.set_ylabel(controller.currentLanguage.fermentationPageContent[44]+"[°C]", color='tab:orange')
            if(controller.settingTemperatureControl[6]==1):
                self.temperatureGraph.set_ylabel(controller.currentLanguage.fermentationPageContent[44]+"[K]", color='tab:orange')
            if(controller.settingTemperatureControl[6]==2):
                self.temperatureGraph.set_ylabel(controller.currentLanguage.fermentationPageContent[44]+"[°F]", color='tab:orange')
            self.temperatureGraph.tick_params(axis='x', labelcolor='tab:orange')
            self.temperatureGraph.tick_params(axis='y', labelcolor='tab:orange')
            #self.temperatureGraph.yaxis.set_major_locator(ticker.MultipleLocator(10))
            self.temperatureGraph.grid(b=None, which='major', axis='both', linestyle='dashed', linewidth=1)
            self.temperatureGraph.plot(self.secondsListTemperature, self.temperatureFermentorList, color='tab:orange')
            self.temperatureCanvas.draw()
            self.temperatureCanvas.get_tk_widget().place(x=150, y=10)

        if(len(self.temperatureFermentorList)==0):
            return 0
        else:
            return self.temperatureFermentorList[len(self.temperatureFermentorList)-1]
        #self.after(10000,lambda:self.updateTemperatureGraphic(controller))

    def checkTemperatureError(self, controller):
        if(self.isErrorFound[1] and self.stopMagnitudeWhenTemperature[0].get()==1):
            controller.settingVelocityControl[1] = 0
            self.isControlInitialized[0] = False
            controller.settingVelocityControl[2] = 1
        if(self.isErrorFound[1] and self.stopMagnitudeWhenTemperature[1].get()==1):
            controller.settingPotentialControl[1] = 0
            self.isControlInitialized[2] = False
            controller.settingPotentialControl[2] = 1
        self.isErrorFound[1] = False

    def setTemperatureDisplay(self, controller, currentTemperature):
        controller.settingScreensControl[2] = 6 #Page Status
        controller.settingScreensControl[5] = 0 #Error Status - CHANGE WHEN GEMMA
        controller.settingScreensControl[8] = controller.settingTemperatureControl[6] #Unit Status
        controller.settingScreensControl[12] = controller.settingTemperatureControl[8] #Slope
        controller.settingScreensControl[14] = controller.settingScreensControl[14] + 2 #Controls Running
        controller.settingScreensControl[17] = int(currentTemperature*100) #Value
        if(controller.settingScreensControl[1] != 1):
            controller.settingScreensControl[1] = 1

    def checkTemperatureStatus(self, controller):
        if(self.isControlInitialized[1]):
            currentTemperature = self.updateTemperatureGraphic(controller)
        #self.updateTemperatureGlobalInformation(controller)
        self.checkTemperatureError(controller)
        currentTime = datetime.today()
        currentTimeStr = currentTime.strftime("%b %d %Y %H:%M:%S.%f")
        if(controller.settingTemperatureControl[1]!=0):
            self.setTemperatureDisplay(controller, currentTemperature)
            currentStepInformation = self.temperatureList.get(controller.settingTemperatureControl[3])
            self.temperatureInformation[2]['text'] = controller.currentLanguage.fermentationPageContent[85]+currentStepInformation
            if(self.currentMagnitudeControlStep[1]!=currentStepInformation):
                self.saveMagnitudeControlStatus(self.temperatureStatusFileTimeStr, currentTimeStr+" - "+currentStepInformation[3:])
                self.currentMagnitudeControlStep[1] = currentStepInformation
            if(controller.settingTemperatureControl[3]<=0):
                self.temperatureList.itemconfig(0, {'bg':'orange'})
            else:
                self.temperatureList.itemconfig(controller.settingTemperatureControl[3]-1, {'bg':'white'})
                self.temperatureList.itemconfig(controller.settingTemperatureControl[3], {'bg':'orange'})
        else:
            self.temperatureInformation[2]['text'] = controller.currentLanguage.fermentationPageContent[86]
            self.isMagnitudeListEditable[1] = True
            if(self.isControlInitialized[1]):
                self.temperatureInformation[0]['text'] = controller.currentLanguage.fermentationPageContent[108] + currentTimeStr
                self.temperatureInformation[1]['text'] = controller.currentLanguage.fermentationPageContent[88]
                #self.generalInformation[1]['text'] = controller.currentLanguage.fermentationPageContent[109]
                self.isControlInitialized[1] = False
                self.temperatureList.itemconfig(controller.settingTemperatureControl[3], {'bg':'white'})
                self.saveMagnitudeControlStatus(self.temperatureStatusFileTimeStr, currentTimeStr+" - Control FINISHED Successfully")
        controller.application.loadStatusDataFromFile()
        controller.application.systemCurrentStatus.temperatureControlData[3] = self.temperatureInformation[2]['text']
        if(controller.application.systemCurrentStatus.temperatureControlData[1]=="0"):
            print("Velocidad Sin Arrancar")
        if(controller.application.systemCurrentStatus.temperatureControlData[1]=="1" and not self.isControlInitialized[0]):
            self.runTemperature(controller)
            print("Temperatura EJECUTANDOSE")
        if(controller.application.systemCurrentStatus.temperatureControlData[1]=="2" and self.isControlInitialized[0]):
            self.pauseTemperatureControl(controller)
            print("Velocidad PAUSADO")
        if(controller.application.systemCurrentStatus.temperatureControlData[1]=="3" and self.isControlInitialized[0]):
            self.stopTemperature(controller)
            print("Velocidad DETENIDO")
        controller.application.systemCurrentStatus.temperatureControlData[3] = self.temperatureInformation[2]['text']
        controller.application.saveStatusDataToFile()
        self.after(10000,lambda:self.checkTemperatureStatus(controller))

    def configureTemperatureButtons(self, controller, buttonOptions):
        buttonOptions[0].config(image = self.buttonsTemperature[0], command = lambda:self.addTemperature(controller))
        buttonOptions[1].config(image = self.buttonsTemperature[1], command = lambda:self.changeTemperature(controller))
        buttonOptions[2].config(image = self.buttonsTemperature[2], command = lambda:self.removeTemperature(controller))
        buttonOptions[3].config(image = self.buttonsTemperature[3], command = lambda:self.runTemperatureControl(controller))
        buttonOptions[4].config(image = self.buttonsTemperature[4], command = lambda:self.pauseTemperatureControl(controller))
        buttonOptions[5].config(image = self.buttonsTemperature[5], command = lambda:self.stopTemperatureControl(controller))
        buttonOptions[6].config(image = self.buttonsTemperature[6], command = lambda:self.previousStepOnTemperatureControl(controller))
        buttonOptions[7].config(image = self.buttonsTemperature[7], command = lambda:self.nextStepOnTemperatureControl(controller))
        buttonOptions[8].config(image = self.buttonsTemperature[8], command = lambda:self.restartTemperatureControl(controller))
        buttonOptions[9].config(image = self.buttonsTemperature[9], command = lambda:self.removeAllListOfTemperatureControl(controller))

    def fillTemperatureList(self, controller):
        if(controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].isTemperatureControlOnFreeWheel):
            self.temperatureList.delete(0,END)
            self.temperatureList.insert(1, controller.currentLanguage.fermentationPageContent[110]+self.freeWheelInformation[1].get()+" °C")
        else:
            temperatures = controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].magnitudesToControl.temperatures
            self.temperatureList.delete(0,END)
            if(len(temperatures)>0):
                position = 1
                for eachTemperature in temperatures:
                    evolutionInformation = controller.currentLanguage.fermentationPageContent[111]
                    if(position==1):
                        evolutionInformation = controller.currentLanguage.fermentationPageContent[92]
                    elif(float(temperatures[position-2].valueObjective)<eachTemperature.valueObjective):
                        evolutionInformation = controller.currentLanguage.fermentationPageContent[112]
                    self.temperatureList.insert(position, str(position)+". "+evolutionInformation+eachTemperature.showInformation())
                    position = position + 1
                    #print("DURATION: ", eachTemperature.getDuration())
                    #print("INFORMATION: ", eachTemperature.showInformation())
            else:
                self.temperatureList.insert(1, controller.currentLanguage.fermentationPageContent[113])

    def setTemperatureList(self, pageTemperature, controller):
        self.temperatureCanvas = FigureCanvasTkAgg(self.temperatureFigure, pageTemperature)
        self.temperatureCanvas.draw()
        self.temperatureCanvas.get_tk_widget().place(x=150, y=10)

        self.temperatureInformation.append(Label(pageTemperature, text=controller.currentLanguage.fermentationPageContent[114], font=self.infoFont, fg = self.colorORT, bg = 'white', height=2, width=58))
        self.temperatureInformation[0].place(x=150, y=420)
        self.temperatureInformation.append(Label(pageTemperature, text=controller.currentLanguage.fermentationPageContent[96], font=self.infoFont, fg = self.colorORT, bg = 'white', height=2, width=58))
        self.temperatureInformation[1].place(x=150, y=455)
        self.temperatureInformation.append(Label(pageTemperature, text=controller.currentLanguage.fermentationPageContent[97], font=self.infoFont, fg = self.colorORT, bg = 'white', height=2, width=58))
        self.temperatureInformation[2].place(x=150, y=490)
        self.temperatureList = Listbox(pageTemperature, width=50, height=11, font=self.listElementFont)
        self.temperatureList.place(x=840,y=200)
        self.fillTemperatureList(controller)

    def fillPageTemperature(self, pageTemperature, controller):
        self.setImagesOnPageTemperature(pageTemperature)
        self.setTemperatureMagnitudeEntries(pageTemperature, controller)
        self.setMagnitudeOptions(pageTemperature, controller, "TEMPERATURE")
        self.setTemperatureList(pageTemperature, controller)

    def isPotentialInputCorrect(self, potentialInput):
        isPotentialValueCorrect = float(potentialInput[0].get())<=12.0 and float(potentialInput[0].get())>=2.0
        isPotentialDurationCorrect =  self.isTimeCorrect(int(potentialInput[1].get()), 91) and self.isTimeCorrect(int(potentialInput[2].get()), 61) and self.isTimeCorrect(int(potentialInput[3].get()), 61)
        return isPotentialValueCorrect and isPotentialDurationCorrect

    def addPotentialHydrogen(self, controller):
        if(self.isMagnitudeListEditable[2]):
            if(self.isPotentialInputCorrect(self.potentialHydrogenInput)):
                newPotential = PotentialHydrogen([self.potentialHydrogenInput[0].get(), self.potentialHydrogenInput[1].get(), self.potentialHydrogenInput[2].get(), self.potentialHydrogenInput[3].get()])
                newPotential.setCustomization(self.potentialCustomizationInformation)
                controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].magnitudesToControl.addPotentialHydrogen(newPotential)
                self.fillPotentialHydrogenList(controller)
            else:
                messagebox.showerror(controller.currentLanguage.fermentationPageContent[61], controller.currentLanguage.fermentationPageContent[62])
        else:
            messagebox.showwarning(controller.currentLanguage.fermentationPageContent[115], controller.currentLanguage.fermentationPageContent[64])

    def changePotentialHydrogen(self, controller):
        try:
            positionSelected = int(self.potentialHydrogenList.curselection()[0])
            if(self.isMagnitudeListEditable[2] and not controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].isPotentialHydrogenControlOnFreeWheel):
                if(self.isPotentialInputCorrect(self.potentialHydrogenInput)): #[2.0,12.0]
                    controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].magnitudesToControl.potentialsHydrogen[positionSelected].valueObjective = self.potentialHydrogenInput[0].get()
                    controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].magnitudesToControl.potentialsHydrogen[positionSelected].duration = [self.potentialHydrogenInput[1].get(), self.potentialHydrogenInput[2].get(), self.potentialHydrogenInput[3].get()]
                    self.fillPotentialHydrogenList(controller)
                else:
                    messagebox.showerror(controller.currentLanguage.fermentationPageContent[61], controller.currentLanguage.fermentationPageContent[62])
            else:
                messagebox.showwarning(controller.currentLanguage.fermentationPageContent[115], controller.currentLanguage.fermentationPageContent[64])
        except IndexError:
            messagebox.showwarning(controller.currentLanguage.fermentationPageContent[66], controller.currentLanguage.fermentationPageContent[67])

    def removePotentialHydrogen(self, controller):
        try:
            positionSelected = int(self.potentialHydrogenList.curselection()[0])
            if(self.isMagnitudeListEditable[2]):
                controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].magnitudesToControl.removePotentialHydrogen(positionSelected)
                self.fillPotentialHydrogenList(controller)
            else:
                messagebox.showwarning(controller.currentLanguage.fermentationPageContent[115], controller.currentLanguage.fermentationPageContent[64])
        except IndexError:
            messagebox.showwarning(controller.currentLanguage.fermentationPageContent[66], controller.currentLanguage.fermentationPageContent[68])

    def setPotentialHydrogenControlValues(self, controller):
        if(controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].isPotentialHydrogenControlOnFreeWheel):
            controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].magnitudesToControl.clearPotentialsHydrogen()
            freeWheelPotential = PotentialHydrogen([self.freeWheelInformation[4].get(), 7*24, 0, 0])
            freeWheelPotential.setCustomization(self.potentialCustomizationInformation)
            controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].magnitudesToControl.addPotentialHydrogen(freeWheelPotential)
            self.fillPotentialHydrogenList(controller)
        position = 0
        for eachPotential in controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].magnitudesToControl.potentialsHydrogen:
            controller.valuesPotentialHydrogenControl[position] = int(eachPotential.valueObjective*10)
            controller.durationPotentialHydrogenControl[position] = int(eachPotential.getDuration())
            position = position + 1

    def runPotential(self, controller):
        self.setPotentialHydrogenControlValues(controller)
        fileTime = datetime.today()
        self.potentialHydrogenDataFileTimeStr = "ControlData/PotentialHydrogen/DATA_Log/"+str(fileTime.strftime("%Y%m%d_%I%M%S"))+"_POT.txt"
        controller.settingPotentialHydrogenControl[4] = int(self.potentialHydrogenDataFileTimeStr[48:54])
        controller.settingPotentialHydrogenControl[5] = int(self.potentialHydrogenDataFileTimeStr[39:47])
        controller.application.systemCurrentStatus.potentialControlData[0]=self.potentialHydrogenDataFileTimeStr
        controller.settingPotentialHydrogenControl[2] = 0
        controller.settingPotentialHydrogenControl[1] = 1
        controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].dataFilenames.append(str(fileTime.strftime("%Y%m%d_%I%M%S")))
        self.isControlInitialized[2] = True
        currentTime = datetime.today()
        currentTimeStr = currentTime.strftime("%b %d %Y %H:%M:%S.%f")
        self.potentialHydrogenInformation[0]['text'] = controller.currentLanguage.fermentationPageContent[116] + currentTimeStr
        self.potentialHydrogenInformation[1]['text'] = controller.currentLanguage.fermentationPageContent[70]
        #self.generalInformation[2]['text'] = controller.currentLanguage.fermentationPageContent[117]
        controller.application.systemCurrentStatus.potentialControlData[2]=self.potentialHydrogenInformation[0]['text']
        controller.application.saveStatusDataToFile()
        self.isMagnitudeListEditable[2] = False
        self.saveMagnitudeControlStatus(self.potentialHydrogenStatusFileTimeStr, currentTimeStr+" - Control INITIATED Successfully")

    def runPotentialHydrogenControl(self, controller):
        if(len(controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].magnitudesToControl.potentialsHydrogen)>0):
            controller.application.systemCurrentStatus.potentialControlData[1]="1"
            self.runPotential(controller)
        else:
            messagebox.showwarning(controller.currentLanguage.fermentationPageContent[115], controller.currentLanguage.fermentationPageContent[72])

    def configurePotentialPauseState(self, controller):
        currentTime = datetime.today()
        currentTimeStr = currentTime.strftime("%b %d %Y %H:%M:%S.%f")
        if(controller.settingPotentialHydrogenControl[2] == 0):
            controller.settingPotentialHydrogenControl[2] = 1
            self.potentialHydrogenInformation[1]['text'] = controller.currentLanguage.fermentationPageContent[73]
            #self.generalInformation[2]['text'] = controller.currentLanguage.fermentationPageContent[118]
            self.isMagnitudeListEditable[2] = True
            self.saveMagnitudeControlStatus(self.potentialHydrogenStatusFileTimeStr, currentTimeStr+" - Control PAUSED Successfully")
        else:
            controller.settingPotentialHydrogenControl[2] = 0
            controller.settingPotentialHydrogenControl[1] = 1
            self.setPotentialHydroControlValues(controller)
            self.potentialHydrogenInformation[1]['text'] = controller.currentLanguage.fermentationPageContent[75]
            #self.generalInformation[2]['text'] = controller.currentLanguage.fermentationPageContent[119]
            self.isMagnitudeListEditable[2] = False
            self.saveMagnitudeControlStatus(self.potentialHydrogenStatusFileTimeStr, currentTimeStr+" - Control RESUMED AFTER PAUSED Successfully")
        controller.application.systemCurrentStatus.potentialControlData[2]=self.potentialHydrogenInformation[0]['text']
        controller.application.systemCurrentStatus.potentialControlData[3] = self.potentialHydrogenInformation[2]['text']
        controller.application.saveStatusDataToFile()

    def pausePotentialHydrogenControl(self, controller):
        if(controller.settingPotentialHydrogenControl[1] == 1 or controller.settingPotentialHydrogenControl[2] == 2):
            controller.application.systemCurrentStatus.potentialControlData[1]="2"
            self.configurePotentialPauseState(controller)
        else:
            messagebox.showwarning(controller.currentLanguage.fermentationPageContent[115], controller.currentLanguage.fermentationPageContent[77])

    def stopPotential(self, controller):
        controller.settingPotentialHydrogenControl[1] = 0
        self.isControlInitialized[2] = False
        controller.settingPotentialHydrogenControl[2] = 1
        currentTime = datetime.today()
        currentTimeStr = currentTime.strftime("%b %d %Y %H:%M:%S.%f")
        self.potentialHydrogenInformation[0]['text'] = controller.currentLanguage.fermentationPageContent[120] + currentTimeStr
        self.potentialHydrogenInformation[1]['text'] = controller.currentLanguage.fermentationPageContent[79]
        #self.generalInformation[2]['text'] = controller.currentLanguage.fermentationPageContent[121]
        self.isMagnitudeListEditable[2] = True
        controller.application.systemCurrentStatus.potentialControlData[2]=self.potentialHydrogenInformation[0]['text']
        controller.application.systemCurrentStatus.potentialControlData[3] = self.potentialHydrogenInformation[2]['text']
        controller.application.saveStatusDataToFile()
        self.saveMagnitudeControlStatus(self.potentialHydrogenStatusFileTimeStr, currentTimeStr+" - Control STOPPED Successfully")
        #self.colorEveryListElementWhite(self.potentialHydrogenList)

    def stopPotentialHydrogenControl(self, controller):
        if(controller.settingPotentialHydrogenControl[1] == 1):
            controller.application.systemCurrentStatus.potentialControlData[1]="3"
            self.stopPotential(controller)
        else:
            messagebox.showwarning(controller.currentLanguage.fermentationPageContent[115], controller.currentLanguage.fermentationPageContent[81])

    def restartPotentialHydrogenControl(self, controller):
        controller.settingPotentialHydrogenControl[1] = 0
        controller.settingPotentialHydrogenControl[2] = 1
        currentTime = datetime.today()
        currentTimeStr = currentTime.strftime("%b %d %Y %H:%M:%S.%f")
        self.potentialHydrogenInformation[0]['text'] = controller.currentLanguage.fermentationPageContent[122] + currentTimeStr
        self.potentialHydrogenInformation[1]['text'] = controller.currentLanguage.fermentationPageContent[83]
        #self.generalInformation[2]['text'] = controller.currentLanguage.fermentationPageContent[123]
        self.saveMagnitudeControlStatus(self.potentialHydrogenStatusFileTimeStr, currentTimeStr+" - Control RESTARTED AND INITIATED Successfully")
        #time.sleep(15)
        fileTime = datetime.today()
        self.potentialHydrogenDataFileTimeStr = "ControlData/PotentialHydrogen/DATA_Log/"+str(fileTime.strftime("%Y%m%d_%I%M%S"))+"_POT.txt"
        controller.settingPotentialHydrogenControl[4] = int(self.potentialHydrogenDataFileTimeStr[48:54])
        controller.settingPotentialHydrogenControl[5] = int(self.potentialHydrogenDataFileTimeStr[38:47])
        controller.settingPotentialHydrogenControl[2] = 0
        controller.settingPotentialHydrogenControl[1] = 1
        controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].dataFilenames.append(str(fileTime.strftime("%Y%m%d_%I%M%S")))

    def previousStepOnPotentialHydrogenControl(self, controller):
        currentTime = datetime.today()
        currentTimeStr = currentTime.strftime("%b %d %Y %H:%M:%S.%f")
        controller.settingPotentialHydrogenControl[2] = 3
        self.saveMagnitudeControlStatus(self.potentialHydrogenStatusFileTimeStr, currentTimeStr+" - Control WENT BACKWARDS ONE STEP Successfully")
        if(controller.settingPotentialHydrogenControl[3]<=0):
            self.potentialHydrogenList.itemconfig(0, {'bg':'lime green'})
        else:
            self.potentialHydrogenList.itemconfig(controller.settingPotentialHydrogenControl[3]+1, {'bg':'white'})
            self.potentialHydrogenList.itemconfig(controller.settingPotentialHydrogenControl[3], {'bg':'lime green'})

    def nextStepOnPotentialHydrogenControl(self, controller):
        currentTime = datetime.today()
        currentTimeStr = currentTime.strftime("%b %d %Y %H:%M:%S.%f")
        controller.settingPotentialHydrogenControl[2] = 4
        self.saveMagnitudeControlStatus(self.potentialHydrogenStatusFileTimeStr, currentTimeStr+" - Control WENT FORWARDS ONE STEP Successfully")
        if(controller.settingPotentialHydrogenControl[3]<len(controller.application.listOfFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].magnitudesToControl.potentialsHydrogen)):
            self.potentialHydrogenList.itemconfig(controller.settingPotentialHydrogenControl[3]-1, {'bg':'white'})
            self.potentialHydrogenList.itemconfig(controller.settingPotentialHydrogenControl[3], {'bg':'lime green'})

    def removeAllListOfPotentialHydrogenControl(self, controller):
        if(self.isMagnitudeListEditable[2]):
            controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].magnitudesToControl.clearPotentialsHydrogen()
            self.fillPotentialHydrogenList(controller)
        else:
            messagebox.showwarning(controller.currentLanguage.fermentationPageContent[115], controller.currentLanguage.fermentationPageContent[64])

    def updatePotentialHydrogenGlobalInformation(self, controller):
        if(len(self.potHydrogenList)>0):
            self.systemInformation[4]['text'] = str(self.potHydrogenList[len(self.potHydrogenList)-1])
        else:
            self.systemInformation[4]['text'] = "0.000"
        if(len(self.acidDropsList)>0):
            self.systemInformation[5]['text'] = str(self.acidDropsList[len(self.acidDropsList)-1])
        else:
            self.systemInformation[5]['text'] = "0.00"
        if(len(self.baseDropsList)>0):
            self.systemInformation[6]['text'] = str(self.baseDropsList[len(self.baseDropsList)-1])
        else:
            self.systemInformation[6]['text'] = "0.00"
        if(controller.settingPotentialHydrogenControl[6]==0):
            self.systemInformation[5]['text'] = self.systemInformation[5]['text'] + " mL"
            self.systemInformation[6]['text'] = self.systemInformation[6]['text'] + " mL"
        if(controller.settingPotentialHydrogenControl[6]==1):
            self.systemInformation[5]['text'] = self.systemInformation[5]['text'] + " cui"
            self.systemInformation[6]['text'] = self.systemInformation[6]['text'] + " cui"
        if(controller.settingPotentialHydrogenControl[6]==2):
            self.systemInformation[5]['text'] = self.systemInformation[5]['text'] + " L"
            self.systemInformation[6]['text'] = self.systemInformation[6]['text'] + " L"

    def updatePotentialHydrogenGraphic(self, controller):
        #fileData = open("ControlData/Temperature/2018-09-03_1530.txt","r")
        filePath = self.potentialHydrogenDataFileTimeStr
        potentialFile = Path(filePath)
        self.potHydrogenList=[]
        self.acidDropsList=[]
        self.baseDropsList=[]
        self.secondsListPotential=[]
        if(potentialFile.exists()):
            fileData = open(filePath,"r")
            pulldata = fileData.read()
            dataList = pulldata.split('\n')

            for eachLine in dataList:
                if len(eachLine)>1:
                    potentialFermentor, potentialObjective, acidDrops, baseDrops, sec, mili = eachLine.split(',')
                    self.potHydrogenList.append(float(potentialFermentor))
                    if(float(acidDrops)==0.0):
                        self.acidDropsList.append(0.0)
                    else:
                        self.acidDropsList.append(float(acidDrops)-1)
                    if(float(baseDrops)==0.0):
                        self.baseDropsList.append(0.0)
                    else:
                        self.baseDropsList.append(float(baseDrops)-1)
                    self.secondsListPotential.append(int(sec)+int(mili)*0.000001)

            fileData.close()
            self.potentialHydrogenGraph.clear()
            self.potentialHydrogenGraph.set_xlabel(controller.currentLanguage.fermentationPageContent[42], color='tab:green')
            self.potentialHydrogenGraph.set_ylabel(controller.currentLanguage.fermentationPageContent[45], color='tab:green')
            self.potentialHydrogenGraph.tick_params(axis='x', labelcolor='tab:green')
            self.potentialHydrogenGraph.tick_params(axis='y', labelcolor='tab:green')
            #self.potentialHydrogenGraph.yaxis.set_major_locator(ticker.MultipleLocator(10))
            self.potentialHydrogenGraph.grid(b=None, which='major', axis='both', linestyle='dashed', linewidth=1)
            self.potentialHydrogenGraph.plot(self.secondsListPotential, self.potHydrogenList, color='tab:green')
            self.potentialHydrogenCanvas.draw()
            self.potentialHydrogenCanvas.get_tk_widget().place(x=150, y=10)
        
        if(len(self.potHydrogenList)==0):
            return 0
        else:
            return self.potHydrogenList[len(self.potHydrogenList)-1]
        #return self.potHydrogenList[len(self.potHydrogenList)-1]
        #self.after(10000,lambda:self.updatePotentialHydrogenGraphic(controller))

    def checkPotentialError(self, controller):
        if(self.isErrorFound[2] and self.stopMagnitudeWhenPotential[0].get()==1):
            controller.settingVelocityControl[1] = 0
            self.isControlInitialized[0] = False
            controller.settingVelocityControl[2] = 1
        if(self.isErrorFound[2] and self.stopMagnitudeWhenPotential[1].get()==1):
            controller.settingTemperatureControl[1] = 0
            self.isControlInitialized[1] = False
            controller.settingTemperatureControl[2] = 1
        self.isErrorFound[2] = False

    def setPotentialDisplay(self, controller, currentPotential):
        controller.settingScreensControl[2] = 6 #Page Status
        controller.settingScreensControl[4] = 0 #Error Status - CHANGE WHEN GEMMA
        controller.settingScreensControl[11] = int(controller.settingPotentialHydrogenControl[11]/2) #Slope
        controller.settingScreensControl[14] = controller.settingScreensControl[14] + 4 #Controls Running
        controller.settingScreensControl[16] = int(currentPotential*1000) #Value
        if(controller.settingScreensControl[1] != 1):
            controller.settingScreensControl[1] = 1

    def checkPotentialHydrogenStatus(self, controller):
        if(self.isControlInitialized[2]):
            currentPotential = self.updatePotentialHydrogenGraphic(controller)
        #self.updatePotentialHydrogenGlobalInformation(controller)
        self.checkPotentialError(controller)
        currentTime = datetime.today()
        currentTimeStr = currentTime.strftime("%b %d %Y %H:%M:%S.%f")
        if(controller.settingPotentialHydrogenControl[1]!=0):
            self.setPotentialDisplay(controller, currentPotential)
            currentStepInformation = self.potentialHydrogenList.get(controller.settingPotentialHydrogenControl[3])
            self.potentialHydrogenInformation[2]['text'] = controller.currentLanguage.fermentationPageContent[85]+currentStepInformation
            if(self.currentMagnitudeControlStep[2]!=currentStepInformation):
                self.saveMagnitudeControlStatus(self.potentialHydrogenStatusFileTimeStr, currentTimeStr+" - "+currentStepInformation[3:])
                self.currentMagnitudeControlStep[2] = currentStepInformation
            if(controller.settingPotentialHydrogenControl[3]<=0):
                self.potentialHydrogenList.itemconfig(0, {'bg':'lime green'})
            else:
                self.potentialHydrogenList.itemconfig(controller.settingPotentialHydrogenControl[3]-1, {'bg':'white'})
                self.potentialHydrogenList.itemconfig(controller.settingPotentialHydrogenControl[3], {'bg':'lime green'})
        else:
            self.potentialHydrogenInformation[2]['text'] = controller.currentLanguage.fermentationPageContent[86]
            self.isMagnitudeListEditable[2] = True
            if(self.isControlInitialized[2]):
                currentTime = datetime.today()
                currentTimeStr = currentTime.strftime("%b %d %Y %H:%M:%S.%f")
                self.potentialHydrogenInformation[0]['text'] = controller.currentLanguage.fermentationPageContent[124] + currentTimeStr
                self.potentialHydrogenInformation[1]['text'] = controller.currentLanguage.fermentationPageContent[88]
                #self.generalInformation[2]['text'] = controller.currentLanguage.fermentationPageContent[125]
                self.isControlInitialized[2] = False
                self.potentialHydrogenList.itemconfig(controller.settingPotentialHydrogenControl[3], {'bg':'white'})
                self.saveMagnitudeControlStatus(self.potentialHydrogenStatusFileTimeStr, currentTimeStr+" - Control FINISHED Successfully")
        controller.application.loadStatusDataFromFile()
        controller.application.systemCurrentStatus.potentialControlData[3] = self.potentialHydrogenInformation[2]['text']
        if(controller.application.systemCurrentStatus.potentialControlData[1]=="0"):
            print("Velocidad Sin Arrancar")
        if(controller.application.systemCurrentStatus.potentialControlData[1]=="1" and not self.isControlInitialized[0]):
            self.runPotential(controller)
            print("Temperatura EJECUTANDOSE")
        if(controller.application.systemCurrentStatus.potentialControlData[1]=="2" and self.isControlInitialized[0]):
            self.pausePotentialControl(controller)
            print("Velocidad PAUSADO")
        if(controller.application.systemCurrentStatus.potentialControlData[1]=="3" and self.isControlInitialized[0]):
            self.stopPotential(controller)
            print("Velocidad DETENIDO")
        controller.application.systemCurrentStatus.potentialControlData[3] = self.potentialHydrogenInformation[2]['text']
        controller.application.saveStatusDataToFile()
        self.after(10000,lambda:self.checkPotentialHydrogenStatus(controller))

    def configurePotentialHydrogenButtons(self, controller, buttonOptions):
        buttonOptions[0].config(image = self.buttonsPotentialHydrogen[0], command = lambda:self.addPotentialHydrogen(controller))
        buttonOptions[1].config(image = self.buttonsPotentialHydrogen[1], command = lambda:self.changePotentialHydrogen(controller))
        buttonOptions[2].config(image = self.buttonsPotentialHydrogen[2], command = lambda:self.removePotentialHydrogen(controller))
        buttonOptions[3].config(image = self.buttonsPotentialHydrogen[3], command = lambda:self.runPotentialHydrogenControl(controller))
        buttonOptions[4].config(image = self.buttonsPotentialHydrogen[4], command = lambda:self.pausePotentialHydrogenControl(controller))
        buttonOptions[5].config(image = self.buttonsPotentialHydrogen[5], command = lambda:self.stopPotentialHydrogenControl(controller))
        buttonOptions[6].config(image = self.buttonsPotentialHydrogen[6], command = lambda:self.previousStepOnPotentialHydrogenControl(controller))
        buttonOptions[7].config(image = self.buttonsPotentialHydrogen[7], command = lambda:self.nextStepOnPotentialHydrogenControl(controller))
        buttonOptions[8].config(image = self.buttonsPotentialHydrogen[8], command = lambda:self.restartPotentialHydrogenControl(controller))
        buttonOptions[9].config(image = self.buttonsPotentialHydrogen[9], command = lambda:self.removeAllListOfPotentialHydrogenControl(controller))

    def setImagesOnPagePotentialHydrogen(self, pagePotentialHydrogen):
        userElement = Picture(['potentialHydrogenElement','png',115,500,10,40],0)
        userElement.purpose = 'Words'
        userElementPic = userElement.generateLabel(pagePotentialHydrogen)
        userElementPic.place(x=userElement.location[0],y=userElement.location[1])

        userElement2 = Picture(['potentialHydrogenElement','png',115,500,1250,10],180)
        userElement2.purpose = 'Words'
        userElement2Pic = userElement2.generateLabel(pagePotentialHydrogen)
        userElement2Pic.place(x=userElement2.location[0],y=userElement2.location[1])

    def setPotHydrogenMagnitudeEntries(self, pagePotentialHydrogen, controller):
        self.potentialHydrogenInput.append(Spinbox(pagePotentialHydrogen, from_=2, to=12, format="%.1f",increment=0.1, font=self.inputFont, width=7, justify='center'))#(Entry(pageVelocity, font=self.inputFont, width=10, justify='center')) # currentPasswordInput
        self.potentialHydrogenInput[0].place(x=700, y=20)
        self.potentialHydrogenInfo = Label(pagePotentialHydrogen, text=controller.currentLanguage.fermentationPageContent[126], font=self.inputFont, fg = 'white', bg = self.colorORT)
        self.potentialHydrogenInfo.place(x=805, y=20)
        self.potentialHydrogenRangeInfo = Label(pagePotentialHydrogen, text=controller.currentLanguage.fermentationPageContent[127], font=self.infoFont, fg = 'white', bg = self.colorORT)
        self.potentialHydrogenRangeInfo.place(x=710, y=50)
        self.potentialHydrogenInput.append(Spinbox(pagePotentialHydrogen, from_=0, to=90, font=self.inputFont, width=4, justify='center'))#Entry(pageVelocity, font=self.inputFont, width=4, justify='center')) # passwordInput
        self.potentialHydrogenInput[1].place(x=915, y=20)
        potentialHydrogenHoursInfo = Label(pagePotentialHydrogen, text="hs", font=self.inputFont, fg = 'white', bg = self.colorORT)
        potentialHydrogenHoursInfo.place(x=980, y=20)
        self.potentialHydrogenInput.append(Spinbox(pagePotentialHydrogen, from_=0, to=59, font=self.inputFont, width=4, justify='center'))#Entry(pageVelocity, font=self.inputFont, width=4, justify='center')) # confirmPasswordInput
        self.potentialHydrogenInput[2].place(x=1010, y=20)
        potentialHydrogenMinutesInfo = Label(pagePotentialHydrogen, text="min", font=self.inputFont, fg = 'white', bg = self.colorORT)
        potentialHydrogenMinutesInfo.place(x=1080, y=20)
        self.potentialHydrogenInput.append(Spinbox(pagePotentialHydrogen, from_=0, to=59, font=self.inputFont, width=4, justify='center'))#Entry(pageVelocity, font=self.inputFont, width=4, justify='center')) # confirmPasswordInput
        self.potentialHydrogenInput[3].place(x=1120, y=20)
        potentialHydrogenSecondsInfo = Label(pagePotentialHydrogen, text="sec", font=self.inputFont, fg = 'white', bg = self.colorORT)
        potentialHydrogenSecondsInfo.place(x=1185, y=20)

    def fillPotentialHydrogenList(self, controller):
        if(controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].isPotentialHydrogenControlOnFreeWheel):
            self.potentialHydrogenList.delete(0,END)
            self.potentialHydrogenList.insert(1, controller.currentLanguage.fermentationPageContent[128]+self.freeWheelInformation[2].get())
        else:
            potentials = controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].magnitudesToControl.potentialsHydrogen
            self.potentialHydrogenList.delete(0,END)
            if(len(potentials)>0):
                position = 1
                for eachPotential in potentials:
                    evolutionInformation = controller.currentLanguage.fermentationPageContent[129]
                    if(position==1):
                        evolutionInformation = controller.currentLanguage.fermentationPageContent[92]
                    elif(potentials[position-2].valueObjective<eachPotential.valueObjective):
                        evolutionInformation = controller.currentLanguage.fermentationPageContent[130]
                    self.potentialHydrogenList.insert(position, str(position)+". "+evolutionInformation+eachPotential.showInformation())
                    position = position + 1
            else:
                self.potentialHydrogenList.insert(1, controller.currentLanguage.fermentationPageContent[131])

    def setPotentialHydrogenList(self, pagePotentialHydrogen, controller):
        self.potentialHydrogenCanvas = FigureCanvasTkAgg(self.potentialHydrogenFigure, pagePotentialHydrogen)
        self.potentialHydrogenCanvas.draw()
        self.potentialHydrogenCanvas.get_tk_widget().place(x=150, y=10)

        self.potentialHydrogenInformation.append(Label(pagePotentialHydrogen, text=controller.currentLanguage.fermentationPageContent[132], font=self.infoFont, fg = self.colorORT, bg = 'white', height=2, width=58))
        self.potentialHydrogenInformation[0].place(x=150, y=420)
        self.potentialHydrogenInformation.append(Label(pagePotentialHydrogen, text=controller.currentLanguage.fermentationPageContent[96], font=self.infoFont, fg = self.colorORT, bg = 'white', height=2, width=58))
        self.potentialHydrogenInformation[1].place(x=150, y=455)
        self.potentialHydrogenInformation.append(Label(pagePotentialHydrogen, text=controller.currentLanguage.fermentationPageContent[97], font=self.infoFont, fg = self.colorORT, bg = 'white', height=2, width=58))
        self.potentialHydrogenInformation[2].place(x=150, y=490)
        self.potentialHydrogenList = Listbox(pagePotentialHydrogen, width=50, height=11, font=self.listElementFont)
        self.potentialHydrogenList.place(x=840,y=200)
        self.fillPotentialHydrogenList(controller)

    def fillPagePotentialHydrogen(self, pagePotentialHydrogen, controller):
        self.setImagesOnPagePotentialHydrogen(pagePotentialHydrogen)
        self.setPotHydrogenMagnitudeEntries(pagePotentialHydrogen, controller)
        self.setMagnitudeOptions(pagePotentialHydrogen, controller, "POTENTIALHYDROGEN")
        self.setPotentialHydrogenList(pagePotentialHydrogen, controller)

    def setImagesOnPageCustomization(self, pageCustomization):
        userElement = Picture(['customizationElement','png',140,500,10,0],0)
        userElement.purpose = 'Words'
        userElementPic = userElement.generateLabel(pageCustomization)
        userElementPic.place(x=userElement.location[0],y=userElement.location[1])

        userElement2 = Picture(['customizationElement','png',140,500,1240,0],180)
        userElement2.purpose = 'Words'
        userElement2Pic = userElement2.generateLabel(pageCustomization)
        userElement2Pic.place(x=userElement2.location[0],y=userElement2.location[1])

    def setVelocityCustomizationTitles(self, pageCustomization, controller):
        velocityCustomizationBorder = Label(pageCustomization, bg = self.colorORT, height=22, width=70, borderwidth=2, relief='solid', highlightbackground='blue')
        velocityCustomizationBorder.place(x=150, y=5)
        self.velocityCustomizationTitle = Label(pageCustomization, text=controller.currentLanguage.fermentationPageContent[134], font=self.titleFont, fg = 'blue', bg = self.colorORT)
        self.velocityCustomizationTitle.place(x=155, y=10)
        self.velocityUnitTitle = Label(pageCustomization, text=controller.currentLanguage.fermentationPageContent[135], font=self.statusFont, fg = 'blue', bg = self.colorORT)
        self.velocityUnitTitle.place(x=180, y=100)
        self.velocityPrecisionTitle = Label(pageCustomization, text=controller.currentLanguage.fermentationPageContent[136], font=self.statusFont, fg = 'blue', bg = self.colorORT)
        self.velocityPrecisionTitle.place(x=180, y=150)
        self.velocityPrecisionInfo = Label(pageCustomization, text=controller.currentLanguage.fermentationPageContent[137], font=self.bodyMessageFont, fg = 'blue', bg = self.colorORT)
        self.velocityPrecisionInfo.place(x=500, y=150)
        self.velocitySensibilityTitle = Label(pageCustomization, text=controller.currentLanguage.fermentationPageContent[138], font=self.statusFont, fg = 'blue', bg = self.colorORT) # ALCANZAR EL OBJETIVO
        self.velocitySensibilityTitle.place(x=180, y=200)
        self.velocityOrientationTitle = Label(pageCustomization, text=controller.currentLanguage.fermentationPageContent[139], font=self.statusFont, fg = 'blue', bg = self.colorORT)
        self.velocityOrientationTitle.place(x=180, y=250)
        self.velocityDataIntervalTitle = Label(pageCustomization, text=controller.currentLanguage.fermentationPageContent[140], font=self.statusFont, fg = 'blue', bg = self.colorORT)
        self.velocityDataIntervalTitle.place(x=180, y=300)
        self.velocityDataIntervalInfo = Label(pageCustomization, text=controller.currentLanguage.fermentationPageContent[141], font=self.bodyMessageFont, fg = 'blue', bg = self.colorORT)
        self.velocityDataIntervalInfo.place(x=510, y=300)

    def setTemperatureCustomizationTitles(self, pageCustomization, controller):
        temperatureCustomizationBorder = Label(pageCustomization, bg = self.colorORT, height=11, width=123, borderwidth=2, relief='solid', highlightbackground='orange')
        temperatureCustomizationBorder.place(x=150, y=360)
        self.temperatureCustomizationTitle = Label(pageCustomization, text=controller.currentLanguage.fermentationPageContent[142], font=self.titleFont, fg = 'orange', bg = self.colorORT)
        self.temperatureCustomizationTitle.place(x=155, y=380)
        self.pumpStepTitle = Label(pageCustomization, text=controller.currentLanguage.fermentationPageContent[158], font=self.statusFont, fg = 'orange', bg = self.colorORT)
        self.pumpStepTitle.place(x=605, y=380)
        self.temperatureUnitTitle = Label(pageCustomization, text=controller.currentLanguage.fermentationPageContent[143], font=self.statusFont, fg = 'orange', bg = self.colorORT)
        self.temperatureUnitTitle.place(x=180, y=430)
        self.temperaturePrecisionTitle = Label(pageCustomization, text=controller.currentLanguage.fermentationPageContent[144], font=self.statusFont, fg = 'orange', bg = self.colorORT)
        self.temperaturePrecisionTitle.place(x=180, y=480)
        self.temperaturePrecisionInfo = Label(pageCustomization, text=controller.currentLanguage.fermentationPageContent[145], font=self.bodyMessageFont, fg = 'orange', bg = self.colorORT)
        self.temperaturePrecisionInfo.place(x=490, y=480)
        self.temperatureSensibilityTitle = Label(pageCustomization, text=controller.currentLanguage.fermentationPageContent[146], font=self.statusFont, fg = 'orange', bg = self.colorORT)
        self.temperatureSensibilityTitle.place(x=605, y=430)
        self.temperatureDataIntervalTitle = Label(pageCustomization, text=controller.currentLanguage.fermentationPageContent[147], font=self.statusFont, fg = 'orange', bg = self.colorORT)
        self.temperatureDataIntervalTitle.place(x=605, y=480)
        self.temperatureDataIntervalInfo = Label(pageCustomization, text=controller.currentLanguage.fermentationPageContent[141], font=self.bodyMessageFont, fg = 'orange', bg = self.colorORT)
        self.temperatureDataIntervalInfo.place(x=935, y=480)

    def setPotentialHydrogenCustomizationTitles(self, pageCustomization, controller):
        potHydrogenCustomizationBorder = Label(pageCustomization, bg = self.colorORT, height=22, width=85, borderwidth=2, relief='solid', highlightbackground='green')
        potHydrogenCustomizationBorder.place(x=650, y=5)
        self.potHydrogenCustomizationTitle = Label(pageCustomization, text=controller.currentLanguage.fermentationPageContent[148], font=self.titleFont, fg = 'green', bg = self.colorORT)
        self.potHydrogenCustomizationTitle.place(x=670, y=10)
        self.potHydrogenUnitTitle = Label(pageCustomization, text=controller.currentLanguage.fermentationPageContent[149], font=self.statusFont, fg = 'green', bg = self.colorORT)
        self.potHydrogenUnitTitle.place(x=695, y=100)
        self.potHydrogenPrecisionTitle = Label(pageCustomization, text=controller.currentLanguage.fermentationPageContent[150], font=self.statusFont, fg = 'green', bg = self.colorORT)
        self.potHydrogenPrecisionTitle.place(x=695, y=150)
        self.potHydrogenPrecisionInfo = Label(pageCustomization, text=controller.currentLanguage.fermentationPageContent[151], font=self.bodyMessageFont, fg = 'green', bg = self.colorORT)
        self.potHydrogenPrecisionInfo.place(x=1095, y=150)
        #self.potHydrogenBurstModelTitle = Label(pageCustomization, text=controller.currentLanguage.fermentationPageContent[159], font=self.statusFont, fg = 'green', bg = self.colorORT)
        #self.potHydrogenBurstModelTitle.place(x=695, y=150)
        self.potHydrogenBurstTitle = Label(pageCustomization, text=controller.currentLanguage.fermentationPageContent[152], font=self.statusFont, fg = 'green', bg = self.colorORT)
        self.potHydrogenBurstTitle.place(x=695, y=200)
        self.potHydrogenBurstInfo = Label(pageCustomization, text=controller.currentLanguage.fermentationPageContent[153], font=self.bodyMessageFont, fg = 'green', bg = self.colorORT)
        self.potHydrogenBurstInfo.place(x=1095, y=200)
        self.potHydrogenIntervalTitle = Label(pageCustomization, text=controller.currentLanguage.fermentationPageContent[154], font=self.statusFont, fg = 'green', bg = self.colorORT)
        self.potHydrogenIntervalTitle.place(x=695, y=250)
        self.potHydrogenIntervalInfo = Label(pageCustomization, text=controller.currentLanguage.fermentationPageContent[155], font=self.bodyMessageFont, fg = 'green', bg = self.colorORT)
        self.potHydrogenIntervalInfo.place(x=1095, y=250)
        self.potHydrogenDataIntervalTitle = Label(pageCustomization, text=controller.currentLanguage.fermentationPageContent[156], font=self.statusFont, fg = 'green', bg = self.colorORT)
        self.potHydrogenDataIntervalTitle.place(x=695, y=300)
        self.potHydrogenDataIntervalInfo = Label(pageCustomization, text=controller.currentLanguage.fermentationPageContent[141], font=self.bodyMessageFont, fg = 'green', bg = self.colorORT)
        self.potHydrogenDataIntervalInfo.place(x=1055, y=300)

    def setPageCustomizationTitles(self, pageCustomization, controller):
        self.setVelocityCustomizationTitles(pageCustomization, controller)
        self.setTemperatureCustomizationTitles(pageCustomization, controller)
        self.setPotentialHydrogenCustomizationTitles(pageCustomization, controller)

    def setVelocityCustomizationEntries(self, pageCustomization, controller):
        self.customizationInformation.append(Spinbox(pageCustomization, values=("rpm", "m/s", "rad/s"), font=self.inputFont, fg = self.colorORT, width=5, justify='center')) # velocity
        self.customizationInformation[0].place(x=470, y=100)
        self.customizationInformation.append(Spinbox(pageCustomization, from_=1, to=10, format="%.1f",increment=0.1, font=self.inputFont, fg = self.colorORT, width=5, justify='center')) # temperature
        self.customizationInformation[1].place(x=420, y=150)
        self.customizationInformation.append(Spinbox(pageCustomization, values=("Nominal", "Slow", "Very Slow"), font=self.inputFont, fg = self.colorORT, width=10, justify='center'))  # temperature
        self.customizationInformation[2].place(x=450, y=200)
        self.customizationInformation.append(Spinbox(pageCustomization, values=("<-| CLK <-|", "|-> AntiCLK |->"), font=self.inputFont, fg = self.colorORT, width=10, justify='center'))  # potential hydrogen
        self.customizationInformation[3].place(x=450, y=250)
        self.customizationInformation.append(Spinbox(pageCustomization, from_=5, to=20, font=self.inputFont, fg = self.colorORT, width=5, justify='center')) # extraction
        self.customizationInformation[4].place(x=430, y=300)

    def setTemperatureCustomizationEntries(self, pageCustomization, controller):
        self.customizationInformation.append(Spinbox(pageCustomization, values=("°C (Celsius)", "K (Kelvin)", "°F (Fahrenheit)"), font=self.inputFont, fg = self.colorORT, width=15, justify='center')) # velocity
        self.customizationInformation[5].place(x=390, y=430)
        self.customizationInformation.append(Spinbox(pageCustomization, from_=0, to=2, format="%.1f",increment=0.1, font=self.inputFont, fg = self.colorORT, width=5, justify='center')) # temperature
        self.customizationInformation[6].place(x=390, y=480)
        self.customizationInformation.append(Spinbox(pageCustomization, from_=1, to=5, font=self.inputFont, fg = self.colorORT, width=5, justify='center')) # temperature
        self.customizationInformation[7].place(x=880, y=380)
        self.customizationInformation.append(Spinbox(pageCustomization, values=("Nominal", "Fast", "Super Fast"), font=self.inputFont, fg = self.colorORT, width=10, justify='center'))  # temperature
        self.customizationInformation[8].place(x=855, y=430)
        self.customizationInformation.append(Spinbox(pageCustomization, from_=5, to=20, font=self.inputFont, fg = self.colorORT, width=5, justify='center')) # extraction
        self.customizationInformation[9].place(x=855, y=480)

    def setPotentialHydrogenCustomizationEntries(self, pageCustomization, controller):
        self.customizationInformation.append(Spinbox(pageCustomization, values=("mL", "cui", "L"), font=self.inputFont, fg = self.colorORT, width=5, justify='center')) # extraction
        self.customizationInformation[10].place(x=1035, y=100)
        self.customizationInformation.append(Spinbox(pageCustomization, from_=5, to=20, font=self.inputFont, fg = self.colorORT, width=5, justify='center')) # extraction
        self.customizationInformation[11].place(x=1015, y=150)
        #self.customizationInformation.append(Spinbox(pageCustomization, values=("1 Drop", "2 Drops", "3 Drops", "4 Drops"), font=self.inputFont, fg = self.colorORT, width=9, justify='center')) # extraction
        #self.customizationInformation[12].place(x=995, y=150)
        self.customizationInformation.append(Spinbox(pageCustomization, from_=1, to=4, font=self.inputFont, fg = self.colorORT, width=5, justify='center')) # extraction
        self.customizationInformation[12].place(x=1015, y=200)
        self.customizationInformation.append(Spinbox(pageCustomization, from_=150, to=500, font=self.inputFont, fg = self.colorORT, width=5, justify='center')) # extraction
        self.customizationInformation[13].place(x=1005, y=250)
        self.customizationInformation.append(Spinbox(pageCustomization, from_=5, to=20, font=self.inputFont, fg = self.colorORT, width=5, justify='center')) # extraction
        self.customizationInformation[14].place(x=975, y=300)

    def setPageCustomizationEntries(self, pageCustomization, controller):
        self.setVelocityCustomizationEntries(pageCustomization, controller)
        self.setTemperatureCustomizationEntries(pageCustomization, controller)
        self.setPotentialHydrogenCustomizationEntries(pageCustomization, controller)

    def isVelocityCustomizationRight(self):
        return (self.customizationInformation[0].get()=="rpm" or self.customizationInformation[0].get()=="m/s" or self.customizationInformation[0].get()=="rad/s") and ("CLK" in self.customizationInformation[3].get() or "AntiCLK" in self.customizationInformation[3].get()=="|-> AntiCLK |->") and (int(self.customizationInformation[1].get())>=1 and int(self.customizationInformation[1].get())<=10) and (self.customizationInformation[2].get()=="Nominal" or self.customizationInformation[2].get()=="Slow" or self.customizationInformation[2].get()=="Very Slow") and (int(self.customizationInformation[4].get())>=5 and int(self.customizationInformation[4].get())<=20)

    def isTemperatureCustomizationRight(self):
        return (self.customizationInformation[5].get()=="°C (Celsius)" or self.customizationInformation[5].get()=="K (Kelvin)" or self.customizationInformation[5].get()=="°F (Fahrenheit)") and (float(self.customizationInformation[6].get())>=0.1 and float(self.customizationInformation[6].get())<=2) and (int(self.customizationInformation[7].get())>=1 and int(self.customizationInformation[7].get())<=5) and (self.customizationInformation[8].get()=="Nominal" or self.customizationInformation[8].get()=="Fast" or self.customizationInformation[8].get()=="Super Fast") and (int(self.customizationInformation[9].get())>=5 and int(self.customizationInformation[9].get())<=20)

    def isPotentialHydrogenCustomizationRight(self):
        return (self.customizationInformation[10].get()=="mL" or self.customizationInformation[10].get()=="cui" or self.customizationInformation[10].get()=="L") and (int(self.customizationInformation[11].get())>=5 and int(self.customizationInformation[11].get())<=20) and (int(self.customizationInformation[12].get())>=1 and int(self.customizationInformation[12].get())<=4) and (int(self.customizationInformation[13].get())>=150 and int(self.customizationInformation[13].get())<=500) and (int(self.customizationInformation[14].get())>=5 and int(self.customizationInformation[14].get())<=20)

    def isCustomizationRight(self):
        return self.isVelocityCustomizationRight() and self.isTemperatureCustomizationRight() and self.isPotentialHydrogenCustomizationRight()

    def saveVelocityCustomization(self, controller):
        self.velocityCustomizationInformation = [self.customizationInformation[0].get(), float(self.customizationInformation[1].get()), self.customizationInformation[2].get(), self.customizationInformation[3].get(), int(self.customizationInformation[4].get())]

    def configureVelocityCustomization(self, controller):
        if(self.customizationInformation[0].get()=="rpm"):
            controller.settingVelocityControl[6] = 0
        if(self.customizationInformation[0].get()=="m/s"):
            controller.settingVelocityControl[6] = 1
        if(self.customizationInformation[0].get()=="rad/s"):
            controller.settingVelocityControl[6] = 2
        controller.settingVelocityControl[7] = int(float(self.customizationInformation[1].get())*10)
        if(self.customizationInformation[2].get()=="Nominal"):
            controller.settingVelocityControl[8] = 0
        if(self.customizationInformation[2].get()=="Slow"):
            controller.settingVelocityControl[8] = 1
        if(self.customizationInformation[2].get()=="Very Slow"):
            controller.settingVelocityControl[8] = 2
        if("CLK" in self.customizationInformation[3].get()):
            controller.settingVelocityControl[9] = 0
        if("AntiCLK" in self.customizationInformation[3].get()):
            controller.settingVelocityControl[9] = 1
        controller.settingVelocityControl[10] = int(self.customizationInformation[4].get())
        self.saveVelocityCustomization(controller)

    def saveTemperatureCustomization(self, controller):
        self.temperatureCustomizationInformation = [self.customizationInformation[5].get(), int(self.customizationInformation[6].get()), int(self.customizationInformation[7].get()), self.customizationInformation[8].get(), int(self.customizationInformation[9].get())]

    def configureTemperatureCustomization(self, controller):
        if(self.customizationInformation[5].get()=="°C (Celsius)"):
            controller.settingTemperatureControl[6] = 0
        if(self.customizationInformation[5].get()=="K (Kelvin)"):
            controller.settingTemperatureControl[6] = 1
        if(self.customizationInformation[5].get()=="°F (Fahrenheit)"):
            controller.settingTemperatureControl[6] = 2
        controller.settingTemperatureControl[7] = int(float(self.customizationInformation[6].get())*10)
        controller.settingTemperatureControl[10] = int(self.customizationInformation[7].get())
        if(self.customizationInformation[8].get()=="Nominal"):
            controller.settingTemperatureControl[8] = 0
        if(self.customizationInformation[8].get()=="Fast"):
            controller.settingTemperatureControl[8] = 1
        if(self.customizationInformation[8].get()=="Super Fast"):
            controller.settingTemperatureControl[8] = 2
        controller.settingTemperatureControl[9] = int(self.customizationInformation[9].get())
        self.saveTemperatureCustomization(controller)

    def savePotentialCustomization(self, controller):
        self.potentialCustomizationInformation = [self.customizationInformation[10].get(), int(self.customizationInformation[11].get()), int(self.customizationInformation[12].get()), self.customizationInformation[13].get(), int(self.customizationInformation[14].get())]

    def configurePotentialHydrogenCustomization(self, controller):
        if(self.customizationInformation[10].get()=="mL"):
            controller.settingPotentialHydrogenControl[6] = 0
        if(self.customizationInformation[10].get()=="cui"):
            controller.settingPotentialHydrogenControl[6] = 1
        if(self.customizationInformation[10].get()=="L"):
            controller.settingPotentialHydrogenControl[6] = 2
        controller.settingPotentialHydrogenControl[7] = int(self.customizationInformation[11].get())
        controller.settingPotentialHydrogenControl[11] = int(self.customizationInformation[12].get())
        controller.settingPotentialHydrogenControl[9] = int(self.customizationInformation[13].get())
        controller.settingPotentialHydrogenControl[10] = int(self.customizationInformation[14].get())
        self.savePotentialCustomization(controller)

    def initializeCustomizationParameters(self, controller):
        controller.settingVelocityControl[7] = 1
        controller.settingVelocityControl[10] = 10
        controller.settingTemperatureControl[7] = 1 #0.1
        controller.settingTemperatureControl[9] = 10
        controller.settingTemperatureControl[10] = 5
        controller.settingPotentialHydrogenControl[7] = 5
        #controller.settingPotentialHydrogenControl[8] = 1
        controller.settingPotentialHydrogenControl[9] = 500 #0.5
        controller.settingPotentialHydrogenControl[10] = 10
        controller.settingPotentialHydrogenControl[11] = 1
        self.velocityCustomizationInformation = ["rpm", 1.0, "Nominal", "AntiCLK", 10]
        self.temperatureCustomizationInformation = ["°C (Celsius)", 0.1, 5, "Nominal", 10]
        self.potentialCustomizationInformation = ["mL", 0.05, 1, 0.500, 10]

    def configureCustomization(self, controller):
        if(self.isCustomizationRight()):
            self.configureVelocityCustomization(controller)
            self.configureTemperatureCustomization(controller)
            self.configurePotentialHydrogenCustomization(controller)
            messagebox.showinfo(controller.currentLanguage.fermentationPageContent[168], controller.currentLanguage.fermentationPageContent[169])
        else:
            messagebox.showerror(controller.currentLanguage.fermentationPageContent[168], controller.currentLanguage.fermentationPageContent[170])

    def setPageCustomizationButtons(self, pageCustomization, controller):
        self.configureNewCustomization = Button(pageCustomization, text=controller.currentLanguage.fermentationPageContent[157], command=lambda:self.configureCustomization(controller), relief = RAISED, fg='white', bg = 'black', font=self.buttonFont, compound=CENTER, height = 5, width = 20)
        self.configureNewCustomization.place(x=1020, y=370)

    def fillPageCustomization(self, pageCustomization, controller):
        self.setImagesOnPageCustomization(pageCustomization)
        self.setPageCustomizationTitles(pageCustomization, controller)
        self.setPageCustomizationEntries(pageCustomization, controller)
        self.setPageCustomizationButtons(pageCustomization, controller)

    def setImagesOnPageErrors(self, pageErrors, controller):
        controller.setImagesandSeparators(pageErrors, 'errorsElement', [115,270,10,20,115,270,10,300])
        controller.setImagesandSeparators(pageErrors, 'errorsElement', [115,270,1250,20,115,270,1250,300])

    def setPageErrorsTitles(self, pageErrors, controller):
        velocityErrorBorder = Label(pageErrors, bg = self.colorORT, height=10, width=85, borderwidth=2, relief='solid', highlightbackground='blue')
        velocityErrorBorder.place(x=150, y=5)
        self.velocityErrorTitle = Label(pageErrors, text=controller.currentLanguage.fermentationPageContent[161], font=self.buttonFont, fg = 'blue', bg = self.colorORT)
        self.velocityErrorTitle.place(x=155, y=10)

        temperatureErrorBorder = Label(pageErrors, bg = self.colorORT, height=10, width=85, borderwidth=2, relief='solid', highlightbackground='orange')
        temperatureErrorBorder.place(x=150, y=190)
        self.temperatureErrorTitle = Label(pageErrors, text=controller.currentLanguage.fermentationPageContent[162], font=self.buttonFont, fg = 'orange', bg = self.colorORT)
        self.temperatureErrorTitle.place(x=155, y=195)

        potentialErrorBorder = Label(pageErrors, bg = self.colorORT, height=10, width=85, borderwidth=2, relief='solid', highlightbackground='lime green')
        potentialErrorBorder.place(x=150, y=375)
        self.potentialErrorTitle = Label(pageErrors, text=controller.currentLanguage.fermentationPageContent[163], font=self.buttonFont, fg = 'lime green', bg = self.colorORT)
        self.potentialErrorTitle.place(x=155, y=380)

        self.errorInformation.append(Label(pageErrors, text=controller.currentLanguage.fermentationPageContent[164], font=self.inputFont, fg = 'blue', bg = 'white', height=6, width=40))
        self.errorInformation[0].place(x=770, y=10)
        self.errorInformation.append(Label(pageErrors, text=controller.currentLanguage.fermentationPageContent[164], font=self.inputFont, fg = 'orange', bg = 'white', height=6, width=40))
        self.errorInformation[1].place(x=770, y=190)
        self.errorInformation.append(Label(pageErrors, text=controller.currentLanguage.fermentationPageContent[164], font=self.inputFont, fg = 'lime green', bg = 'white', height=6, width=40))
        self.errorInformation[2].place(x=770, y=370)

    def setPageErrorsEntries(self, pageErrors, controller):
        self.errorParameters.append(Checkbutton(pageErrors, text=controller.currentLanguage.fermentationPageContent[166], font=self.groupMessageFont, fg='black', bg=self.colorORT, variable=self.stopMagniudeWhenVelocity[0]))
        self.errorParameters[0].place(x=170, y=60)
        self.errorParameters.append(Checkbutton(pageErrors, text=controller.currentLanguage.fermentationPageContent[167], font=self.groupMessageFont, fg='black', bg=self.colorORT, variable=self.stopMagniudeWhenVelocity[1]))
        self.errorParameters[1].place(x=170, y=110)
        self.errorParameters.append(Checkbutton(pageErrors, text=controller.currentLanguage.fermentationPageContent[165], font=self.groupMessageFont, fg='black', bg=self.colorORT, variable=self.stopMagnitudeWhenTemperature[0]))
        self.errorParameters[2].place(x=170, y=245)
        self.errorParameters.append(Checkbutton(pageErrors, text=controller.currentLanguage.fermentationPageContent[167], font=self.groupMessageFont, fg='black', bg=self.colorORT, variable=self.stopMagnitudeWhenTemperature[1]))
        self.errorParameters[3].place(x=170, y=295)
        self.errorParameters.append(Checkbutton(pageErrors, text=controller.currentLanguage.fermentationPageContent[165], font=self.groupMessageFont, fg='black', bg=self.colorORT, variable=self.stopMagnitudeWhenPotential[0]))
        self.errorParameters[4].place(x=170, y=430)
        self.errorParameters.append(Checkbutton(pageErrors, text=controller.currentLanguage.fermentationPageContent[166], font=self.groupMessageFont, fg='black', bg=self.colorORT, variable=self.stopMagnitudeWhenPotential[1]))
        self.errorParameters[5].place(x=170, y=480)
        for eachButton in self.errorParameters:
            eachButton.select()

    def fillPageErrors(self, pageErrors, controller):
        self.setImagesOnPageErrors(pageErrors, controller)
        self.setPageErrorsTitles(pageErrors, controller)
        self.setPageErrorsEntries(pageErrors, controller)

    def checkMagnitudesStatus(self, controller):
        print("CHECK")
        self.checkVelocityStatus(controller)
        self.checkTemperatureStatus(controller)
        self.checkPotentialHydrogenStatus(controller)
        #self.updateGlobalGraphics(controller)

    def getCurrentUserGamesScores(self, controller):
        if(controller.application.systemCurrentStatus.isUserLogged[1]):
            return controller.application.listStudents.students[controller.application.systemCurrentStatus.userLogged].gamesScore
        else:
            return controller.application.listProfessors.professors[controller.application.systemCurrentStatus.userLogged].gamesScore

    def fillWithGamesInformation(self, pageEntertainment, controller):
        self.informationTitle = Label(pageEntertainment, text=controller.currentLanguage.fermentationPageContent[133], font=self.gameTitleFont, fg = 'chocolate3', bg = self.colorORT)
        self.informationTitle.place(x=910, y=20)
        gamesInformation = controller.currentLanguage.fermentationPageContent[189] #ALL GAMES info
        allGamesInfo = Label(pageEntertainment, text=gamesInformation, font=self.infoFont, fg = 'chocolate3', bg = self.colorORT, justify=LEFT, bd=2, relief='groove', highlightbackground='white')
        allGamesInfo.place(x=855, y=65)

        currentGamesScores = self.getCurrentUserGamesScores(controller)
        self.currentGameStatus.append(Label(pageEntertainment, text=controller.currentLanguage.fermentationPageContent[176]+str(currentGamesScores[0])+controller.currentLanguage.fermentationPageContent[177], font=self.infoFont, fg = 'chocolate3', bg = self.colorORT, justify=LEFT, bd=2, relief='groove', highlightbackground='white', width=60))
        self.currentGameStatus[0].place(x=710, y=190)
        self.currentGameStatus.append(Label(pageEntertainment, text=controller.currentLanguage.fermentationPageContent[178]+str(currentGamesScores[1])+controller.currentLanguage.fermentationPageContent[179], font=self.infoFont, fg = 'chocolate3', bg = self.colorORT, justify=LEFT, bd=2, relief='groove', highlightbackground='white', width=60))
        self.currentGameStatus[1].place(x=710, y=215)
        self.currentGameStatus.append(Label(pageEntertainment, text=controller.currentLanguage.fermentationPageContent[180]+str(currentGamesScores[2])+controller.currentLanguage.fermentationPageContent[181], font=self.infoFont, fg = 'chocolate3', bg = self.colorORT, justify=LEFT, bd=2, relief='groove', highlightbackground='white', width=60))
        self.currentGameStatus[2].place(x=710, y=240)

        dodgerGameRecord = Label(pageEntertainment, text=controller.currentLanguage.fermentationPageContent[188], font=self.infoFont, fg = 'DodgerBlue3', bg = self.colorORT, justify=LEFT, bd=2, relief='groove', highlightbackground='white', width=59)
        dodgerGameRecord.place(x=140, y=185)
        memoryGameRecord = Label(pageEntertainment, text=controller.currentLanguage.fermentationPageContent[188], font=self.infoFont, fg = 'lime green', bg = self.colorORT, justify=LEFT, bd=2, relief='groove', highlightbackground='white', width=59)
        memoryGameRecord.place(x=140, y=465)
        nibblesGameRecord = Label(pageEntertainment, text=controller.currentLanguage.fermentationPageContent[188], font=self.infoFont, fg = 'indian red', bg = self.colorORT, justify=LEFT, bd=2, relief='groove', highlightbackground='white', width=59)
        nibblesGameRecord.place(x=710, y=465)
        #gamesImage = Label(pageEntertainment, text="IMAGE", font=self.infoFont, fg = 'chocolate3', bg = self.colorORT, bd=2, relief='groove', highlightbackground='white', height=6, width=14)
        #gamesImage.place(x=710, y=65)

    def fillWithDodgerInformation(self, pageEntertainment, controller):
        dodgerTitle = Label(pageEntertainment, text="_-_-_-_-_-_- DODGER -_-_-_-_-_-_", font=self.gameTitleFont, fg = 'DodgerBlue3', bg = self.colorORT)
        dodgerTitle.place(x=140, y=20)
        #dodgerInformation = "This game tries to keep the player engaged by throwing at him a continuous\nand each time more hazardous quantity of enemies for him to avoid. Its main \nobjective is to hone the player reaction speed skills and spread fun and happiness \nto the Fermentation. The Dodger game has the player control a small person \nwho must dodge a whole bunch of obstacules that fall from the top of the screen. \nThe longer the player can keep dodging the baddies, the higher the score they will get."
        dodgerInformation = controller.currentLanguage.fermentationPageContent[171] #DODGER info
        dodgerGameInfo = Label(pageEntertainment, text=dodgerInformation, font=self.infoFont, fg = 'DodgerBlue3', bg = self.colorORT, justify=LEFT, bd=2, relief='groove', highlightbackground='white')
        dodgerGameInfo.place(x=280, y=65)
        #dodgerImage = Label(pageEntertainment, text="IMAGE", font=self.infoFont, fg = 'DodgerBlue3', bg = self.colorORT, bd=2, relief='groove', highlightbackground='white', height=6, width=14)
        #dodgerImage.place(x=140, y=65)

    def fillWithMemoryInformation(self, pageEntertainment, controller):
        memoryTitle = Label(pageEntertainment, text="_-_-_-_-_-_- MEMORY -_-_-_-_-_-_", font=self.gameTitleFont, fg = 'lime green', bg = self.colorORT)
        memoryTitle.place(x=135, y=300)
        memoryInformation = controller.currentLanguage.fermentationPageContent[172] #MEMORY info
        memoryGameInfo = Label(pageEntertainment, text=memoryInformation, font=self.infoFont, fg = 'lime green', bg = self.colorORT, justify=LEFT, bd=2, relief='groove', highlightbackground='white')
        memoryGameInfo.place(x=280, y=345)
        memoryImage = Label(pageEntertainment, text="IMAGE", font=self.infoFont, fg = 'lime green', bg = self.colorORT, bd=2, relief='groove', highlightbackground='white', height=6, width=14)
        memoryImage.place(x=140, y=345)

    def fillWithNibblesInformation(self, pageEntertainment, controller):
        nibblesTitle = Label(pageEntertainment, text="_-_-_-_-_-_- NIBBLES -_-_-_-_-_-_", font=self.gameTitleFont, fg = 'indian red', bg = self.colorORT)
        nibblesTitle.place(x=705, y=300)
        nibblesInformation = controller.currentLanguage.fermentationPageContent[173] #NIBBLES info
        nibblesGameInfo = Label(pageEntertainment, text=nibblesInformation, font=self.infoFont, fg = 'indian red', bg = self.colorORT, justify=LEFT, bd=2, relief='groove', highlightbackground='white')
        nibblesGameInfo.place(x=855, y=345)
        #nibblesImage = Label(pageEntertainment, text="IMAGE", font=self.infoFont, fg = 'indian red', bg = self.colorORT, bd=2, relief='groove', highlightbackground='white', height=6, width=14)
        #nibblesImage.place(x=710, y=345)

    def fillPageEntertainmentInformation(self, pageEntertainment, controller):
        self.fillWithDodgerInformation(pageEntertainment, controller)
        self.fillWithMemoryInformation(pageEntertainment, controller)
        self.fillWithNibblesInformation(pageEntertainment, controller)
        #self.fillWithScrambledInformation(pageEntertainment)
        #self.fillWithHangmanInformation(pageEntertainment)
        #self.fillWithTriviaInformation(pageEntertainment)

    def setImagesOfPrimaryGames(self, pageEntertainment):
        print("SHOW IMAGES OF PRIMARY GAMES")

    def setImagesOfSecondaryGames(self, pageEntertainment):
        dodgerLogo = Picture(['dodgerGameLogo','png',130,110,140,65],0)
        dodgerLogo.purpose = 'GamesPic'
        dodgerLogoPic = dodgerLogo.generateLabel(pageEntertainment)
        dodgerLogoPic.config(bd=5, relief='groove', highlightbackground='white')
        dodgerLogoPic.place(x=dodgerLogo.location[0],y=dodgerLogo.location[1])

        nibblesLogo = Picture(['nibblesGameLogo','png',130,110,710,345],0)
        nibblesLogo.purpose = 'GamesPic'
        nibblesLogoPic = nibblesLogo.generateLabel(pageEntertainment)
        nibblesLogoPic.config(bd=5, relief='groove', highlightbackground='white')
        nibblesLogoPic.place(x=nibblesLogo.location[0],y=nibblesLogo.location[1])

        gamesInfoLogo = Picture(['smartGameInfo','png',120,120,710,65],0)
        gamesInfoLogo.purpose = 'Logos'
        gamesInfoLogoPic = gamesInfoLogo.generateLabel(pageEntertainment)
        gamesInfoLogoPic.place(x=gamesInfoLogo.location[0],y=gamesInfoLogo.location[1])

    def fillPageEntertainmentImages(self, pageEntertainment, controller):
        controller.setImagesandSeparators(pageEntertainment, 'playGamesElement', [115,270,10,20,115,270,10,300])
        controller.setImagesandSeparators(pageEntertainment, 'playGamesElement', [115,270,1250,20,115,270,1250,300])
        self.setImagesOfPrimaryGames(pageEntertainment)
        self.setImagesOfSecondaryGames(pageEntertainment)

    def fillPageEntertainmentButtons(self, pageEntertainment, controller):
        self.entertainmentToDisplay = EntertainmentDisplay(self)

        self.playScramblerOption = Button(pageEntertainment, text=controller.currentLanguage.fermentationPageContent[230], command=lambda:self.entertainmentToDisplay.playScrambled(controller), relief = SUNKEN, fg='white', bg = 'DodgerBlue3', font=self.gameFont, compound=CENTER, height = 2, width = 41)
        self.playScramblerOption.place(x=140, y=210)
        self.entertainmentToDisplay.configureInitialScrambledGame(controller)

        self.playHangmanOption = Button(pageEntertainment, text=controller.currentLanguage.fermentationPageContent[230], command=lambda:self.entertainmentToDisplay.playHangman(controller), relief = SUNKEN, fg='white', bg = 'lime green', font=self.gameFont, compound=CENTER, height = 2, width = 41)
        self.playHangmanOption.place(x=140, y=490)
        self.entertainmentToDisplay.configureInitialHangmanGame(controller)

        #self.triviaCorrectAnswerPic = Label(self.triviaCanvas, borderwidth=0, highlightthickness=0)
        #self.triviaWrongAnswerPic = Label(self.triviaCanvas, borderwidth=0, highlightthickness=0)
        self.playTriviaOption = Button(pageEntertainment, text=controller.currentLanguage.fermentationPageContent[230], command=lambda:self.entertainmentToDisplay.playTrivia(controller), relief = SUNKEN, fg='white', bg = 'indian red', font=self.gameFont, compound=CENTER, height = 2, width = 41)
        self.playTriviaOption.place(x=710, y=490)
        self.entertainmentToDisplay.configureInitialTriviaGame(controller)

    def fillPageEntertainment(self, pageEntertainment, controller):
        self.fillWithGamesInformation(pageEntertainment, controller)
        self.fillPageEntertainmentInformation(pageEntertainment, controller)
        self.fillPageEntertainmentImages(pageEntertainment, controller)
        self.fillPageEntertainmentButtons(pageEntertainment, controller)

    def fadeAway(self, controller):
        alpha = controller.attributes("-alpha")
        if alpha > 0:
            alpha = alpha - 0.1
            controller.attributes("-alpha", alpha)
            self.after(50, lambda:self.fadeAway(controller))
        else:
            controller.destroy()

    def closeAllControlProcesses(self, controller):
        controller.settingVelocityControl[0] = 0
        controller.settingTemperatureControl[0] = 0
        #controller.settingPotentialControl[0] = 0
        time.sleep(1)

    def onClosing(self, controller):
        if messagebox.askokcancel(controller.currentLanguage.adminPageContent[21], controller.currentLanguage.adminPageContent[20]):
            #controller.application.updateFermentationControlsData()
            #controller.application.updateFermentationVerificationsData()
            controller.application.saveSmartData("")
            
            self.stopVelocity(controller)
            self.stopTemperature(controller)
            self.stopPotential(controller)
            time.sleep(2)
            
            self.closeAllControlProcesses(controller)
            self.fadeAway(controller)

    def setTabs(self, controller):
        self.pageVelocity = Frame(self.nb)
        self.nb.add(self.pageVelocity, text=controller.currentLanguage.fermentationPageContent[5])
        controller.setBackgroundOfTab(self.pageVelocity)
        self.fillPageVelocity(self.pageVelocity, controller)
        self.pageTemperature = Frame(self.nb)
        self.nb.add(self.pageTemperature, text=controller.currentLanguage.fermentationPageContent[6])
        controller.setBackgroundOfTab(self.pageTemperature)
        self.fillPageTemperature(self.pageTemperature, controller)
        self.pagePotentialHydrogen = Frame(self.nb)
        self.nb.add(self.pagePotentialHydrogen, text=controller.currentLanguage.fermentationPageContent[7])
        controller.setBackgroundOfTab(self.pagePotentialHydrogen)
        self.fillPagePotentialHydrogen(self.pagePotentialHydrogen, controller)

    def __init__(self, parent, controller):

        Frame.__init__(self, parent)
        controller.application.systemCurrentStatus.fermentationActual = 0 #CUIDADO
        self.setFonts()
        self.setVariables()
        self.setFileNames(controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual])
        self.setLists()
        self.setGraphics()
        self.loadStaticPictures(controller)
        self.initializeCustomizationParameters(controller)
        controller.setPersonalStyle()        

        controller.settingScreensControl[2] = 5
        controller.settingScreensControl[1] = 1

        self.fermentationInformation = Label(self, text=controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].showProcessRegistry(), font=self.infoFont, fg = 'white', bg = self.colorORT)
        self.fermentationInformation.place(x=1120, y=120)

        rows = 0
        while rows < 50:
            self.rowconfigure(rows, weight=1)
            self.columnconfigure(rows, weight=1)
            rows = rows + 1

        self.nb = ttk.Notebook(self)
        self.nb.grid(row=10, column=0, columnspan=500, rowspan=490, sticky='NESW')
        self.setTabs(controller)
        self.checkMagnitudesStatus(controller)
        self.setHelpBar(controller)
        #self.animateWords()
