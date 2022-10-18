import sys, time, matplotlib, gi
from datetime import datetime, date, timedelta
matplotlib.use("TkAgg")
gi.require_version('Wnck', '3.0')
from gi.repository import Wnck
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
from MonitorConsole.LedHandler import LedHandler

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
        self.controlAvailable = [IntVar(), IntVar(), IntVar()]
        self.triviaOptionSelection = [IntVar(), IntVar(), IntVar(), IntVar()]
        self.frequencySet = IntVar()
        self.isControlInitialized = [False, False, False]
        self.isErrorFound = [False, False, False]
        self.isMagnitudeListEditable = [True, True, True]
        self.currentMagnitudesValues = [0.0, 0.0, 0.0]
        self.extensions = [466, 268]
        self.helpDisplayed = False
        self.semiAutomationSelected = False
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
        self.controlsAvailability = []


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
        self.bathTemperatureFigure = Figure(figsize=(5,4), dpi=100, facecolor=self.colorORT, edgecolor='white')
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

    def changeModeVisualization(self):
        if(self.semiAutomationSelected == False):
            self.canvasSemiAutomation.place(x=0, y=140)
            self.semiAutomationSelected= True
        else:
            self.canvasSemiAutomation.place(x=1000, y=1000)
            self.semiAutomationSelected = False

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

        self.changeModeImage = PhotoImage(file="Images/Logos/changeModeLogo.gif")
        changeModeOption = Button(self, image=self.changeModeImage, command=lambda:self.changeModeVisualization(), relief = SUNKEN, compound=CENTER)
        changeModeOption.place(x=1260, y=25)

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
        self.versionInfo.place(x=142+47+47+47+47, y=470+self.extensions[1])
        self.minimizeSystem = Button(self, text=controller.currentLanguage.adminPageContent[21], command=lambda:self.minimizeWindow(), relief = RAISED, fg='white', bg = 'blue', font=self.bodyMessageFont, compound=CENTER, height = 1, width = 10)
        self.minimizeSystem.place(x=1155, y=470+self.extensions[1])
        #self.minimizeSystem = Button(self, text=controller.currentLanguage.homePageContent[17], relief = RAISED, fg='white', bg = 'blue', font=self.bodyMessageFont, compound=CENTER, height = 1, width = 10)
        #self.minimizeSystem.place(x=1155, y=470+self.extensions[1])
        self.closeSystem = Button(self, text=controller.currentLanguage.adminPageContent[22], command=lambda:self.onClosing(controller), relief = RAISED, fg='white', bg = 'red', font=self.bodyMessageFont, compound=CENTER, height = 1, width = 12)
        self.closeSystem.place(x=1252, y=470+self.extensions[1])
        self.helpSystem = Button(self, text=controller.currentLanguage.adminPageContent[23], command=lambda:self.showHelp(), relief = RAISED, fg='white', bg = 'dark green', font=self.bodyMessageFont, compound=CENTER, height = 1, width = 15)
        self.helpSystem.place(x=0, y=470+self.extensions[1])
        self.canvas = Canvas(self, background="white", width= 890+self.extensions[0], height= 320+self.extensions[1], highlightthickness=5, highlightbackground=self.colorORT)
        self.canvasSemiAutomation = Canvas(self, background=self.colorORT, width= 890+self.extensions[0], height= 320+self.extensions[1], highlightthickness=5, highlightbackground=self.colorORT)
        self.canvasSemiAutomationConfiguration(controller)
        self.canvasConfiguration(controller)

    def setImagesOnCanvasSemiAutomation(self):
        userElement = Picture(['alternativeElement','png',140,500,10,0],0)
        userElement.purpose = 'Words'
        userElementPic = userElement.generateLabel(self.canvasSemiAutomation)
        userElementPic.place(x=userElement.location[0],y=userElement.location[1])

        userElement2 = Picture(['alternativeElement','png',140,500,1240,0],180)
        userElement2.purpose = 'Words'
        userElement2Pic = userElement2.generateLabel(self.canvasSemiAutomation)
        userElement2Pic.place(x=userElement2.location[0],y=userElement2.location[1])

    def changeVelocityControlAvailability(self, controller):
        if(self.controlAvailable[0].get()==1):
            controller.settingVelocityControl[20] = 0
        else:
            controller.settingVelocityControl[19] = 90
            controller.settingVelocityControl[20] = 1
        print("VELOCITY CONTROL AVAILABILITY: ", self.controlAvailable[0].get())

    def changeTemperatureControlAvailability(self, controller):
        if(self.controlAvailable[1].get()==1):
            controller.settingTemperatureControl[20] = 0
        else:
            controller.settingTemperatureControl[20] = 1
        print("TEMPERATURE CONTROL AVAILABILITY: ", self.controlAvailable[1].get())

    def changePotentialControlAvailability(self, controller):
        if(self.controlAvailable[2].get()==1):
            controller.settingPotentialHydrogenControl[20] = 0
        else:
            controller.settingPotentialHydrogenControl[20] = 1
        print("POTENTIAL CONTROL AVAILABILITY: ", self.controlAvailable[2].get())

    def setMotorParametersManually(self, controller):
        if(self.controlAvailable[0].get()==0):
            if(self.frequencySet.get()==1 and float(self.manualMotorFrequency.get())>=9.0 and float(self.manualMotorFrequency.get())<=50.0):
                controller.application.systemCurrentStatus.velocityControlData[1]="1"
                self.velocityInformation[2]['text'] = controller.currentLanguage.fermentationPageContent[232]+ str(self.manualMotorFrequency.get())+" Hz"
                controller.settingVelocityControl[18] = 1
                controller.settingVelocityControl[19] = int(float(self.manualMotorFrequency.get())*10)
                messagebox.showinfo("INFO", controller.currentLanguage.fermentationPageContent[233]+self.manualMotorFrequency.get()+" Hz")
                print("MANUAL MOTOR FREQUENCY: ", float(self.manualMotorFrequency.get()))
            if(self.frequencySet.get()==0 and float(self.manualMotorVelocity.get())>=180.0 and float(self.manualMotorVelocity.get())<=800.0):
                controller.application.systemCurrentStatus.velocityControlData[1]="1"
                controller.settingVelocityControl[18] = 2
                self.velocityInformation[2]['text'] = controller.currentLanguage.fermentationPageContent[232]+ str(self.manualMotorVelocity.get())+" rpm"
                controller.settingVelocityControl[19] = int(float(self.manualMotorVelocity.get())*10)
                messagebox.showinfo("INFO", controller.currentLanguage.fermentationPageContent[234]+self.manualMotorVelocity.get()+" rpm")
                print("MANUAL MOTOR VELOCITY: ", float(self.manualMotorVelocity.get()))
        else:
            messagebox.showerror("ERROR", controller.currentLanguage.fermentationPageContent[236])


    def stopMotorManually(self, controller):
        if(self.controlAvailable[0].get()==0):
            #controller.settingVelocityControl[18] = 3
            self.stopVelocityControl(controller)
            messagebox.showinfo("INFO", controller.currentLanguage.fermentationPageContent[235])
        else:
            messagebox.showerror("ERROR", controller.currentLanguage.fermentationPageContent[236])

    def setBathParametersManually(self, controller):
        if(self.controlAvailable[1].get()==0):
            if(float(self.manualBathTemperature.get())>=10.0 and float(self.manualBathTemperature.get())<=95.0 and int(self.manualBathPumpStep.get())>=1 and int(self.manualBathPumpStep.get())<=5):
                controller.application.systemCurrentStatus.temperatureControlData[1]="1"
                controller.settingTemperatureControl[18] = 1
                self.temperatureInformation[2]['text'] = controller.currentLanguage.fermentationPageContent[237]+ str(self.manualBathTemperature.get())+" Celsius (Pump Level "+str(self.manualBathPumpStep.get())+")"
                controller.settingTemperatureControl[17] = int(float(self.manualBathTemperature.get())*100)
                controller.settingTemperatureControl[19] = int(self.manualBathPumpStep.get())
                messagebox.showinfo("INFO", controller.currentLanguage.fermentationPageContent[238])
            else:
                messagebox.showwarning("WARNING", controller.currentLanguage.fermentationPageContent[239])
        else:
            messagebox.showerror("ERROR", controller.currentLanguage.fermentationPageContent[240])

    def stopBathManually(self, controller):
        if(self.controlAvailable[1].get()==0):
            controller.settingTemperatureControl[18] = 3
            messagebox.showinfo("INFO", controller.currentLanguage.fermentationPageContent[241])
        else:
            messagebox.showerror("ERROR", controller.currentLanguage.fermentationPageContent[240])

    def expulseAcid(self, controller):
        if(self.controlAvailable[2].get()==0):
            if(int(self.expulsionOption[0].get())>=1 and int(self.expulsionOption[0].get())<=4 and int(self.expulsionOption[1].get())>=1 and int(self.expulsionOption[1].get())<=50):
                controller.settingPotentialHydrogenControl[18] = 1
                controller.settingPotentialHydrogenControl[17] = int(self.expulsionOption[0].get())
                controller.settingPotentialHydrogenControl[19] = int(self.expulsionOption[1].get())
                messagebox.showinfo("INFO", "Acid "+controller.currentLanguage.fermentationPageContent[242])
            else:
                messagebox.showwarning("WARNING", controller.currentLanguage.fermentationPageContent[243])
        else:
            messagebox.showerror("ERROR", controller.currentLanguage.fermentationPageContent[244])

    def expulseBase(self, controller):
        if(self.controlAvailable[2].get()==0):
            if(int(self.expulsionOption[0].get())>=1 and int(self.expulsionOption[0].get())<=4 and int(self.expulsionOption[1].get())>=1 and int(self.expulsionOption[1].get())<=50):
                controller.settingPotentialHydrogenControl[18] = 2
                controller.settingPotentialHydrogenControl[17] = int(self.expulsionOption[0].get())
                controller.settingPotentialHydrogenControl[19] = int(self.expulsionOption[1].get())
                messagebox.showinfo("INFO", "Base "+controller.currentLanguage.fermentationPageContent[242])
            else:
                messagebox.showwarning("WARNING", controller.currentLanguage.fermentationPageContent[243])
        else:
            messagebox.showerror("ERROR", controller.currentLanguage.fermentationPageContent[244])

    def fillWithVelocityAlternativesOptions(self, controller):
        velocitySemiAutomationBorder = Label(self.canvasSemiAutomation, bg = self.colorORT, height=26, width=69, borderwidth=2, relief='solid', highlightbackground='blue')
        velocitySemiAutomationBorder.place(x=150, y=5)
        self.velocitySemiAutomationTitle = Label(self.canvasSemiAutomation, text=controller.currentLanguage.fermentationPageContent[134], font=self.titleFont, fg = 'blue', bg = self.colorORT)
        self.velocitySemiAutomationTitle.place(x=155, y=10)
        self.motorFrequencySemiAutomationTitle = Label(self.canvasSemiAutomation, text=controller.currentLanguage.fermentationPageContent[245], font=self.statusFont, fg = 'blue', bg = self.colorORT)
        self.motorFrequencySemiAutomationTitle.place(x=180, y=100)
        self.motorVelocitySemiAutomationTitle = Label(self.canvasSemiAutomation, text=controller.currentLanguage.fermentationPageContent[246], font=self.statusFont, fg = 'blue', bg = self.colorORT)
        self.motorVelocitySemiAutomationTitle.place(x=180, y=150)
        self.motorFrequencyUnitInfo = Label(self.canvasSemiAutomation, text="Hz", font=self.inputFont, fg = 'blue', bg = self.colorORT)
        self.motorFrequencyUnitInfo.place(x=505, y=100)
        self.motorVelocityUnitInfo = Label(self.canvasSemiAutomation, text="rpm", font=self.inputFont, fg = 'blue', bg = self.colorORT)
        self.motorVelocityUnitInfo.place(x=505, y=150)
        self.setAndRunMotor = Button(self.canvasSemiAutomation, text=controller.currentLanguage.fermentationPageContent[247], command = lambda:self.setMotorParametersManually(controller), relief = SUNKEN, fg='white', bg = 'green4', font=self.buttonFont, compound=CENTER, height = 5, width = 16)
        self.setAndRunMotor.place(x=180, y=250)
        self.stopMotor = Button(self.canvasSemiAutomation, text=controller.currentLanguage.fermentationPageContent[248], command = lambda:self.stopMotorManually(controller), relief = SUNKEN, fg='white', bg = 'red', font=self.buttonFont, compound=CENTER, height = 5, width = 16)
        self.stopMotor.place(x=420, y=250)

        self.controlsAvailability.append(Checkbutton(self.canvasSemiAutomation, text=controller.currentLanguage.fermentationPageContent[249], font=self.inputFont, fg='blue', bg=self.colorORT, variable=self.controlAvailable[0], command=lambda:self.changeVelocityControlAvailability(controller)))
        self.controlsAvailability[0].place(x=450, y=20)
        self.setByFrequency = Checkbutton(self.canvasSemiAutomation, text=controller.currentLanguage.fermentationPageContent[250], font=self.inputFont, fg='blue', bg=self.colorORT, variable=self.frequencySet)
        self.setByFrequency.place(x=350, y=200)
        self.manualMotorFrequency = Spinbox(self.canvasSemiAutomation, from_=9, to=50, format="%.1f",increment=0.1, font=self.inputFont, fg = self.colorORT, width=5, justify='center')
        self.manualMotorFrequency.place(x=400, y=100)
        self.manualMotorVelocity = Spinbox(self.canvasSemiAutomation, from_=180, to=800, format="%.1f",increment=0.1, font=self.inputFont, fg = self.colorORT, width=5, justify='center')
        self.manualMotorVelocity.place(x=400, y=150)

    def fillWithTemperatureAlternativesOptions(self, controller):
        temperatureSemiAutomationBorder = Label(self.canvasSemiAutomation, bg = self.colorORT, height=12, width=160, borderwidth=2, relief='solid', highlightbackground='orange')
        temperatureSemiAutomationBorder.place(x=150, y=400)
        self.temperatureSemiAutomationTitle = Label(self.canvasSemiAutomation, text=controller.currentLanguage.fermentationPageContent[142], font=self.titleFont, fg = 'orange', bg = self.colorORT)
        self.temperatureSemiAutomationTitle.place(x=155, y=420)

        self.pumpStepSemiAutomationTitle = Label(self.canvasSemiAutomation, text=controller.currentLanguage.fermentationPageContent[158], font=self.statusFont, fg = 'orange', bg = self.colorORT)
        self.pumpStepSemiAutomationTitle.place(x=180, y=530)
        self.temperatureBathSemiAutomationTitle = Label(self.canvasSemiAutomation, text=controller.currentLanguage.fermentationPageContent[251], font=self.statusFont, fg = 'orange', bg = self.colorORT)
        self.temperatureBathSemiAutomationTitle.place(x=180, y=470)
        self.temperatureBathSemiAutomationInfo = Label(self.canvasSemiAutomation, text=controller.currentLanguage.fermentationPageContent[252], font=self.bodyMessageFont, fg = 'orange', bg = self.colorORT)
        self.temperatureBathSemiAutomationInfo.place(x=510, y=470)
        self.setAndRunBathTemperature = Button(self.canvasSemiAutomation, text=controller.currentLanguage.fermentationPageContent[253], command = lambda:self.setBathParametersManually(controller), relief = SUNKEN, fg='white', bg = 'green4', font=self.buttonFont, compound=CENTER, height = 6, width = 12)
        self.setAndRunBathTemperature.place(x=670, y=410)
        self.stopBathTemperature = Button(self.canvasSemiAutomation, text=controller.currentLanguage.fermentationPageContent[254], command = lambda:self.stopBathManually(controller), relief = SUNKEN, fg='white', bg = 'red', font=self.buttonFont, compound=CENTER, height = 6, width = 12)
        self.stopBathTemperature.place(x=880, y=410)

        self.controlsAvailability.append(Checkbutton(self.canvasSemiAutomation, text=controller.currentLanguage.fermentationPageContent[249], font=self.inputFont, fg='orange', bg=self.colorORT, variable=self.controlAvailable[1], command=lambda:self.changeTemperatureControlAvailability(controller)))
        self.controlsAvailability[1].place(x=400, y=420)
        self.manualBathTemperature = Spinbox(self.canvasSemiAutomation, from_=10, to=95, format="%.1f",increment=0.1, font=self.inputFont, fg = self.colorORT, width=5, justify='center')
        self.manualBathTemperature.place(x=420, y=470)
        self.manualBathPumpStep = Spinbox(self.canvasSemiAutomation, from_=1, to=5, font=self.inputFont, fg = self.colorORT, width=5, justify='center')
        self.manualBathPumpStep.place(x=450, y=530)

    def fillWithPotentialHydrogenAlternativesOptions(self, controller):
        potHydrogenSemiAutomationBorder = Label(self.canvasSemiAutomation, bg = self.colorORT, height=26, width=82, borderwidth=2, relief='solid', highlightbackground='green')
        potHydrogenSemiAutomationBorder.place(x=650, y=5)
        self.potHydrogenSemiAutomationTitle = Label(self.canvasSemiAutomation, text=controller.currentLanguage.fermentationPageContent[148], font=self.titleFont, fg = 'green4', bg = self.colorORT)
        self.potHydrogenSemiAutomationTitle.place(x=670, y=10)
        self.expulseLiquidAcidValve = Button(self.canvasSemiAutomation, text=controller.currentLanguage.userPageContent[25], command = lambda:self.expulseAcid(controller), relief = SUNKEN, fg='white', bg = 'dark red', font=self.buttonFont, compound=CENTER, height = 4, width = 18)
        self.expulseLiquidAcidValve.place(x=700, y=260)
        self.expulseLiquidBaseValve = Button(self.canvasSemiAutomation, text=controller.currentLanguage.userPageContent[26], command = lambda:self.expulseBase(controller), relief = SUNKEN, fg='white', bg = 'purple4', font=self.buttonFont, compound=CENTER, height = 4, width = 18)
        self.expulseLiquidBaseValve.place(x=960, y=260)
        self.dropsExpulsionInfo1 = Label(self.canvasSemiAutomation, text=controller.currentLanguage.userPageContent[123], font=self.inputFont, fg = 'white', bg = self.colorORT)
        self.dropsExpulsionInfo1.place(x=920, y=120)
        self.dropsExpulsionInfo2 = Label(self.canvasSemiAutomation, text=controller.currentLanguage.userPageContent[124], font=self.inputFont, fg = 'white', bg = self.colorORT)
        self.dropsExpulsionInfo2.place(x=840, y=170)
        self.dropsExpulsionInfo3 = Label(self.canvasSemiAutomation, text=controller.currentLanguage.userPageContent[125], font=self.inputFont, fg = 'white', bg = self.colorORT)
        self.dropsExpulsionInfo3.place(x=960, y=170)

        self.controlsAvailability.append(Checkbutton(self.canvasSemiAutomation, text=controller.currentLanguage.fermentationPageContent[249], font=self.inputFont, fg='green4', bg=self.colorORT, variable=self.controlAvailable[2], command=lambda:self.changePotentialControlAvailability(controller)))
        self.controlsAvailability[2].place(x=1050, y=20)
        self.expulsionOption = []
        self.expulsionOption.append(Spinbox(self.canvasSemiAutomation, from_=1, to=4, font=self.inputFont, fg = self.colorORT, width=3, justify='center'))
        self.expulsionOption[0].place(x=850, y=120)
        self.expulsionOption.append(Spinbox(self.canvasSemiAutomation, from_=1, to=50, font=self.inputFont, fg = self.colorORT, width=3, justify='center'))
        self.expulsionOption[1].place(x=900, y=170)

    def configureLedMatrixPower(self, controller):
        if(controller.settingScreensControl[1]==-2):
             controller.settingScreensControl[1]=-1
             print("PRENDO DESDE FERMENTATION PAGE")
             self.manageScreensPower.config(text=controller.currentLanguage.fermentationPageContent[255], fg = 'white', bg = 'black')
        else:
             controller.settingScreensControl[1]=-3
             print("APAGO DESDE FERMENTATION PAGE")
             self.manageScreensPower.config(text=controller.currentLanguage.fermentationPageContent[256], fg = 'black', bg = 'red')

    def canvasSemiAutomationConfiguration(self, controller):
        self.setImagesOnCanvasSemiAutomation()
        self.fillWithVelocityAlternativesOptions(controller)
        self.fillWithTemperatureAlternativesOptions(controller)
        self.fillWithPotentialHydrogenAlternativesOptions(controller)

        self.manageScreensPower = Button(self.canvasSemiAutomation, text=controller.currentLanguage.fermentationPageContent[255], command=lambda:self.configureLedMatrixPower(controller), relief = RAISED, fg='white', bg = 'black', font=self.buttonFont, compound=CENTER, height = 6, width = 12)
        self.manageScreensPower.place(x=1100, y=410)

        self.setByFrequency.select()
        for eachButton in self.controlsAvailability:
            eachButton.select()

    def configureCanvas(self, controller):
        self.ortMessageTitle = Label(self.canvas, text=controller.currentLanguage.fermentationPageContent[0], font=self.subtitleFont, fg=self.colorORT, bg='white')
        self.ortMessageTitle.place(x=20,y=10)
        self.groupMessageBody = Label(self.canvas, text=controller.currentLanguage.fermentationPageContent[1], font=self.groupMessageFont, fg=self.colorORT, bg='white', justify=LEFT)
        self.groupMessageBody.place(x=80,y=35)

    def refreshTabsContent(self, controller):
        self.nb.tab(self.pageSystem, text = controller.currentLanguage.fermentationPageContent[3])
        self.nb.tab(self.pageGlobal, text = controller.currentLanguage.fermentationPageContent[4])
        self.nb.tab(self.pageFreeWheel, text = controller.currentLanguage.fermentationPageContent[10])
        self.nb.tab(self.pageVelocity, text = controller.currentLanguage.fermentationPageContent[5])
        self.nb.tab(self.pageTemperature, text = controller.currentLanguage.fermentationPageContent[6])
        self.nb.tab(self.pagePotentialHydrogen, text = controller.currentLanguage.fermentationPageContent[7])
        self.nb.tab(self.pageCustomization, text = controller.currentLanguage.fermentationPageContent[8])
        self.nb.tab(self.pageEntertainment, text = controller.currentLanguage.fermentationPageContent[9])
        self.nb.tab(self.pageErrors, text = controller.currentLanguage.fermentationPageContent[160])

    def refreshPageSystemContent(self, controller):
        self.frequenceTitle['text'] = controller.currentLanguage.fermentationPageContent[11]
        self.acidTitle['text'] = controller.currentLanguage.fermentationPageContent[12]
        self.baseTitle['text'] = controller.currentLanguage.fermentationPageContent[13]
        self.freeWheelTitle['text'] = controller.currentLanguage.fermentationPageContent[14] + ": "
        self.velocityFreeWheelTitle['text'] = controller.currentLanguage.fermentationPageContent[15]
        self.temperatureFreeWheelTitle['text'] = controller.currentLanguage.fermentationPageContent[16]
        self.potentialHydrogenFreeWheelTitle['text'] = controller.currentLanguage.fermentationPageContent[17]
        self.generalInformation[0]['text'] = controller.currentLanguage.fermentationPageContent[19]
        self.generalInformation[1]['text'] = controller.currentLanguage.fermentationPageContent[20]
        self.generalInformation[2]['text'] = controller.currentLanguage.fermentationPageContent[21]
        self.runAllControlInfo['text'] = controller.currentLanguage.fermentationPageContent[22]
        self.restartAllControlInfo['text'] = controller.currentLanguage.fermentationPageContent[23]
        self.pauseAllControlInfo['text'] = controller.currentLanguage.fermentationPageContent[24]
        self.stopAllControlInfo['text'] = controller.currentLanguage.fermentationPageContent[25]

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

    def refreshPageCustomizationContent(self, controller):
        self.refreshVelocityCustomizationContent(controller)
        self.refreshTemperatureCustomizationContent(controller)
        self.refreshPotentialHydrogenCustomizationContent(controller)
        self.configureNewCustomizationVelocity['text'] = controller.currentLanguage.fermentationPageContent[157]
        self.configureNewCustomizationTemperature['text'] = controller.currentLanguage.fermentationPageContent[157]
        self.configureNewCustomizationPotential['text'] = controller.currentLanguage.fermentationPageContent[157]

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
        self.allGamesInfo['text'] = controller.currentLanguage.fermentationPageContent[189]
        self.scrambledGameInfo['text'] = controller.currentLanguage.fermentationPageContent[174]
        self.hangmanGameInfo['text'] = controller.currentLanguage.fermentationPageContent[175]
        self.triviaGameInfo['text'] = controller.currentLanguage.fermentationPageContent[231]
        self.playScramblerOption['text'] = controller.currentLanguage.fermentationPageContent[230]
        self.playHangmanOption['text'] = controller.currentLanguage.fermentationPageContent[230]
        self.playTriviaOption['text'] = controller.currentLanguage.fermentationPageContent[230]

    def refreshCanvasSemiAutomationContent(self, controller):
        self.velocitySemiAutomationTitle['text'] = controller.currentLanguage.fermentationPageContent[134]
        self.motorFrequencySemiAutomationTitle['text'] = controller.currentLanguage.fermentationPageContent[245]
        self.motorVelocitySemiAutomationTitle['text'] = controller.currentLanguage.fermentationPageContent[246]
        self.setAndRunMotor['text'] = controller.currentLanguage.fermentationPageContent[247]
        self.stopMotor['text'] = controller.currentLanguage.fermentationPageContent[248]
        self.controlsAvailability[0]['text'] = controller.currentLanguage.fermentationPageContent[249]
        self.setByFrequency['text'] = controller.currentLanguage.fermentationPageContent[250]
        self.temperatureSemiAutomationTitle['text'] = controller.currentLanguage.fermentationPageContent[142]
        self.pumpStepSemiAutomationTitle['text'] = controller.currentLanguage.fermentationPageContent[158]
        self.temperatureBathSemiAutomationTitle['text'] = controller.currentLanguage.fermentationPageContent[251]
        self.temperatureBathSemiAutomationInfo['text'] = controller.currentLanguage.fermentationPageContent[252]
        self.setAndRunBathTemperature['text'] = controller.currentLanguage.fermentationPageContent[253]
        self.stopBathTemperature['text'] = controller.currentLanguage.fermentationPageContent[254]
        self.controlsAvailability[1]['text'] = controller.currentLanguage.fermentationPageContent[249]
        self.potHydrogenSemiAutomationTitle['text'] = controller.currentLanguage.fermentationPageContent[148]
        self.expulseLiquidAcidValve['text'] = controller.currentLanguage.userPageContent[25]
        self.expulseLiquidBaseValve['text'] = controller.currentLanguage.userPageContent[26]
        self.dropsExpulsionInfo1['text'] = controller.currentLanguage.userPageContent[123]
        self.dropsExpulsionInfo2['text'] = controller.currentLanguage.userPageContent[124]
        self.dropsExpulsionInfo3['text'] = controller.currentLanguage.userPageContent[125]
        self.controlsAvailability[2]['text']=controller.currentLanguage.fermentationPageContent[249]

    def refreshTextContent(self, controller):
        self.refreshTabsContent(controller)
        self.fermentationInformation['text'] = controller.currentLanguage.fermentationPageContent[2]+controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].dateBeginning
        self.versionInfo['text'] = controller.currentLanguage.adminPageContent[12]
        self.minimizeSystem['text'] = controller.currentLanguage.adminPageContent[22]
        self.closeSystem['text'] = controller.currentLanguage.adminPageContent[23]
        self.helpSystem['text'] = controller.currentLanguage.adminPageContent[24]
        self.ortMessageTitle['text'] = controller.currentLanguage.fermentationPageContent[0]
        self.groupMessageBody['text'] = controller.currentLanguage.fermentationPageContent[1]

        self.refreshPageSystemContent(controller)
        self.refreshMagnitudesInformationContent(controller)
        self.refreshPageEntertainmentContent(controller)
        self.refreshPageCustomizationContent(controller)
        self.refreshPageErrorsContent(controller)
        self.refreshCanvasSemiAutomationContent(controller)

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
        self.refreshTextContent(controller)

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

    def animateVelocityControl(self):
        if(self.isControlInitialized[0]):
            self.motorFunctioningActionPic.place(x=self.motorFunctioningAction.location[0],y=self.motorFunctioningAction.location[1])
            self.motorOrientationPic.place(x=self.motorOrientation.location[0],y=self.motorOrientation.location[1])
            if(self.velocityAnimationStep==0):
                self.bubbleLeftImagePic.place(x=350-self.traslation,y=290)
                self.bubbleRightImagePic.place(x=380-self.traslation,y=290)
                self.bubbleLeftImagePic2.place(x=335-self.traslation,y=270)
                self.bubbleRightImagePic2.place(x=395-self.traslation,y=270)
                self.motorOnArrowClockPic.place(x=344-self.traslation,y=170)
                self.motorOnArrowClock2Pic.place(x=1500-self.traslation,y=170)
            if(self.velocityAnimationStep==1):
                self.bubbleLeftImagePic.place(x=335-self.traslation,y=270)
                self.bubbleRightImagePic.place(x=395-self.traslation,y=270)
                self.bubbleLeftImagePic2.place(x=350-self.traslation,y=250)
                self.bubbleRightImagePic2.place(x=380-self.traslation,y=250)
                self.motorOnArrowClockPic.place(x=344-self.traslation,y=170)
                self.motorOnArrowClock2Pic.place(x=1500-self.traslation,y=170)
            if(self.velocityAnimationStep==2):
                self.bubbleLeftImagePic.place(x=350-self.traslation,y=250)
                self.bubbleRightImagePic.place(x=380-self.traslation,y=250)
                self.bubbleLeftImagePic2.place(x=335-self.traslation,y=230)
                self.bubbleRightImagePic2.place(x=395-self.traslation,y=230)
                self.motorOnArrowClockPic.place(x=1500-self.traslation,y=170)
                self.motorOnArrowClock2Pic.place(x=346-self.traslation,y=170)
            if(self.velocityAnimationStep==3):
                self.bubbleLeftImagePic.place(x=335-self.traslation,y=230)
                self.bubbleRightImagePic.place(x=395-self.traslation,y=230)
                self.bubbleLeftImagePic2.place(x=1500-self.traslation,y=290)
                self.bubbleRightImagePic2.place(x=1500-self.traslation,y=290)
                self.motorOnArrowClockPic.place(x=1500-self.traslation,y=170)
                self.motorOnArrowClock2Pic.place(x=346-self.traslation,y=170)
            if(self.velocityAnimationStep<=2):
                self.velocityAnimationStep = self.velocityAnimationStep + 1
            else:
                self.velocityAnimationStep = 0
        else:
            self.motorFunctioningActionPic.place(x=1500,y=1500)
            self.motorOrientationPic.place(x=1500,y=1500)
            self.bubbleLeftImagePic.place(x=1500,y=1500)
            self.bubbleRightImagePic.place(x=1500,y=1500)
            self.bubbleLeftImagePic2.place(x=1500,y=1500)
            self.bubbleRightImagePic2.place(x=1500,y=1500)
            self.motorOnArrowClockPic.place(x=1500,y=1500)
            self.motorOnArrowClock2Pic.place(x=1500,y=1500)
        self.after(10000,lambda:self.animateVelocityControl())

    def animateTemperatureControl(self):
        if(self.isControlInitialized[1]):
            self.temperatureSensorActionPic.place(x=self.temperatureSensorAction.location[0],y=self.temperatureSensorAction.location[1])
            self.fluidDirectionImagePicIn.place(x=self.fluidDirectionImageIn.location[0],y=self.fluidDirectionImageIn.location[1])
            self.fluidDirectionImagePicOut.place(x=self.fluidDirectionImageOut.location[0],y=self.fluidDirectionImageOut.location[1])
            if(self.temperatureAnimationStep==0):
                self.fluidDirectionImagePic1.place(x=1500,y=1500)
                self.fluidDirectionImagePic2.place(x=1500,y=1500)
                self.fluidDirectionImagePic3.place(x=1500,y=1500)
                self.fluidDirectionImagePic4.place(x=1500,y=1500)
            if(self.temperatureAnimationStep==1):
                self.fluidDirectionImagePic1.place(x=self.fluidDirectionImage1.location[0],y=self.fluidDirectionImage1.location[1])
            if(self.temperatureAnimationStep==2):
                self.fluidDirectionImagePic2.place(x=self.fluidDirectionImage2.location[0],y=self.fluidDirectionImage2.location[1])
            if(self.temperatureAnimationStep==3):
                self.fluidDirectionImagePic3.place(x=self.fluidDirectionImage3.location[0],y=self.fluidDirectionImage3.location[1])
            if(self.temperatureAnimationStep==4):
                self.fluidDirectionImagePic4.place(x=self.fluidDirectionImage4.location[0],y=self.fluidDirectionImage4.location[1])
            if(self.temperatureAnimationStep<=3):
                self.temperatureAnimationStep = self.temperatureAnimationStep + 1
            else:
                self.temperatureAnimationStep = 0
        else:
            self.temperatureSensorActionPic.place(x=1500,y=1500)
            self.fluidDirectionImagePicIn.place(x=1500,y=1500)
            self.fluidDirectionImagePicOut.place(x=1500,y=1500)
            self.fluidDirectionImagePic1.place(x=1500,y=1500)
            self.fluidDirectionImagePic2.place(x=1500,y=1500)
            self.fluidDirectionImagePic3.place(x=1500,y=1500)
            self.fluidDirectionImagePic4.place(x=1500,y=1500)
        self.after(10000,lambda:self.animateTemperatureControl())

    def animatePotentialHydrogenControl(self):
        if(self.isControlInitialized[2]):
            self.potentialHydrogenSensorActionPic.place(x=self.potentialHydrogenSensorAction.location[0],y=self.potentialHydrogenSensorAction.location[1])
            if(self.potentialHydrogenAnimationStep==0):
                self.acidDrop1Pic.place(x=1500,y=1500)
                self.acidDrop2Pic.place(x=1500,y=1500)
                self.baseDrop1Pic.place(x=1500,y=1500)
                self.baseDrop2Pic.place(x=1500,y=1500)
            if(self.potentialHydrogenAnimationStep==1):
                self.acidDrop1Pic.place(x=self.acidDrop1.location[0],y=self.acidDrop1.location[1])
            if(self.potentialHydrogenAnimationStep==2):
                self.acidDrop2Pic.place(x=self.acidDrop2.location[0],y=self.acidDrop2.location[1])
            if(self.potentialHydrogenAnimationStep==3):
                self.baseDrop1Pic.place(x=self.baseDrop1.location[0],y=self.baseDrop1.location[1])
            if(self.potentialHydrogenAnimationStep==4):
                self.baseDrop2Pic.place(x=self.baseDrop2.location[0],y=self.baseDrop2.location[1])
            if(self.potentialHydrogenAnimationStep<=3):
                self.potentialHydrogenAnimationStep = self.potentialHydrogenAnimationStep + 1
            else:
                self.potentialHydrogenAnimationStep = 0
        else:
           self.potentialHydrogenSensorActionPic.place(x=1500,y=1500)
           self.acidDrop1Pic.place(x=1500,y=1500)
           self.acidDrop2Pic.place(x=1500,y=1500)
           self.baseDrop1Pic.place(x=1500,y=1500)
           self.baseDrop2Pic.place(x=1500,y=1500)
        self.after(10000,lambda:self.animatePotentialHydrogenControl())

    def loadAnimationVelocity(self, pageSystem):
        self.motorFunctioningAction = Picture(['motorFunctioningLogo','png',int(228*(8/24))-5,int(218*(8/24)),340-self.traslation,25],0) # 10 o 1260
        self.motorFunctioningAction.purpose = 'Logos'
        self.motorFunctioningActionPic = self.motorFunctioningAction.generateLabel(pageSystem)
        self.motorOrientation = Picture(['turnClockwiseLogo','png',int(172*3/8),int(82*3/8),345-self.traslation,340],0) # 10 o 1260
        self.motorOrientation.purpose = 'Logos'
        self.motorOrientationPic = self.motorOrientation.generateLabel(pageSystem)
        self.bubbleImage = Picture(['bubblesLogo','png',20,20,350-self.traslation,290],0) # 10 o 1260
        self.bubbleImage.purpose = 'Logos'
        self.bubbleLeftImagePic = self.bubbleImage.generateLabel(pageSystem)
        self.bubbleLeftImagePic2 = self.bubbleImage.generateLabel(pageSystem)
        self.bubbleRightImagePic = self.bubbleImage.generateLabel(pageSystem)
        self.bubbleRightImagePic2 = self.bubbleImage.generateLabel(pageSystem)
        self.motorOnArrowClock = Picture(['turnClockLogo','png',int(160*3/8),int(104*3/8),344-self.traslation,170],0) # 10 o 1260
        self.motorOnArrowClock.purpose = 'Logos'
        self.motorOnArrowClockPic = self.motorOnArrowClock.generateLabel(pageSystem)
        self.motorOnArrowClock2 = Picture(['turnClock2Logo','png',int(160*3/8),int(104*3/8),346-self.traslation,170],0) # 10 o 1260
        self.motorOnArrowClock2.purpose = 'Logos'
        self.motorOnArrowClock2Pic = self.motorOnArrowClock2.generateLabel(pageSystem)
        self.velocityAnimationStep = 0

    def loadAnimationTemperature(self, pageSystem):
        self.temperatureSensorAction = Picture(['temperatureSensorActionLogo','png',int(100/4),int(160/4),405-self.traslation,330],0) # 10 o 1260
        self.temperatureSensorAction.purpose = 'Logos'
        self.temperatureSensorActionPic = self.temperatureSensorAction.generateLabel(pageSystem)
        self.fluidDirectionImageIn = Picture(['fluidDirectionLogo','png',int(150/2),int(112/2),130-self.traslation,210],0) # 10 o 1260
        self.fluidDirectionImageIn.purpose = 'Logos'
        self.fluidDirectionImagePicIn = self.fluidDirectionImageIn.generateLabel(pageSystem)
        self.fluidDirectionImageOut = Picture(['fluidDirectionLogo','png',int(150/2),int(112/2),130-self.traslation,320],180) # 10 o 1260
        self.fluidDirectionImageOut.purpose = 'Logos'
        self.fluidDirectionImagePicOut = self.fluidDirectionImageOut.generateLabel(pageSystem)
        self.fluidDirectionImage1 = Picture(['fluidDownLogo','png',int(95*3/8),int(214*3/8),260-self.traslation,260],0) # 10 o 1260
        self.fluidDirectionImage1.purpose = 'Logos'
        self.fluidDirectionImagePic1 = self.fluidDirectionImage1.generateLabel(pageSystem)
        self.fluidDirectionImage2 = Picture(['fluidDownCornerLogo','png',int(204*3/10),int(158*3/10),265-self.traslation,385],0) # 10 o 1260
        self.fluidDirectionImage2.purpose = 'Logos'
        self.fluidDirectionImagePic2 = self.fluidDirectionImage2.generateLabel(pageSystem)
        self.fluidDirectionImage3 = Picture(['fluidUpCornerLogo','png',int(148*3/9),int(166*3/9),430-self.traslation,382],0) # 10 o 1260
        self.fluidDirectionImage3.purpose = 'Logos'
        self.fluidDirectionImagePic3 = self.fluidDirectionImage3.generateLabel(pageSystem)
        self.fluidDirectionImage4 = Picture(['fluidUpLogo','png',int(70*3/8),int(214*3/8),463-self.traslation,260],0) # 10 o 1260
        self.fluidDirectionImage4.purpose = 'Logos'
        self.fluidDirectionImagePic4 = self.fluidDirectionImage4.generateLabel(pageSystem)
        self.temperatureAnimationStep = 0

    def loadAnimationPotentialHydrogen(self, pageSystem):
        self.potentialHydrogenSensorAction = Picture(['pHSensorActionLogo','png',int(104/4),int(164/4),318-self.traslation,330],0) # 10 o 1260
        self.potentialHydrogenSensorAction.purpose = 'Logos'
        self.potentialHydrogenSensorActionPic = self.potentialHydrogenSensorAction.generateLabel(pageSystem)
        self.acidDrop1 = Picture(['dropAcidLogo','png',int(58/4),int(70/4),340-self.traslation,180],0) # 10 o 1260
        self.acidDrop1.purpose = 'Logos'
        self.acidDrop1Pic = self.acidDrop1.generateLabel(pageSystem)
        self.acidDrop2 = Picture(['dropAcidLogo','png',int(58/4),int(70/4),350-self.traslation,200],0) # 10 o 1260
        self.acidDrop2.purpose = 'Logos'
        self.acidDrop2Pic = self.acidDrop1.generateLabel(pageSystem)
        self.baseDrop1 = Picture(['dropBaseLogo','png',int(62/4),int(64/4),400-self.traslation,180],0) # 10 o 1260
        self.baseDrop1.purpose = 'Logos'
        self.baseDrop1Pic = self.baseDrop1.generateLabel(pageSystem)
        self.baseDrop2 = Picture(['dropBaseLogo','png',int(62/4),int(64/4),390-self.traslation,200],0) # 10 o 1260
        self.baseDrop2.purpose = 'Logos'
        self.baseDrop2Pic = self.baseDrop1.generateLabel(pageSystem)
        self.potentialHydrogenAnimationStep = 0

    def fillPicturesOnPageSystem(self, pageSystem, controller):
        systemImage = Picture(['systemScheme','png',346,515,200-self.traslation,20],0) # 10 o 1260
        systemImage.purpose = 'Logos'
        systemImagePic = systemImage.generateLabel(pageSystem)
        systemImagePic.place(x=systemImage.location[0],y=systemImage.location[1])
        self.loadAnimationVelocity(pageSystem)
        self.loadAnimationTemperature(pageSystem)
        self.loadAnimationPotentialHydrogen(pageSystem)
        self.animateVelocityControl()
        self.animateTemperatureControl()
        self.animatePotentialHydrogenControl()

    def setPageSystemLabels(self, pageSystem, controller):
        self.frequenceTitle = Label(pageSystem, text=controller.currentLanguage.fermentationPageContent[11], font=self.inputFont, bg = self.colorORT)
        self.frequenceTitle.place(x=120-self.traslation, y=440)
        self.acidTitle = Label(pageSystem, text=controller.currentLanguage.fermentationPageContent[12], font=self.inputFont, fg = 'red', bg = self.colorORT)
        self.acidTitle.place(x=120-self.traslation, y=470)
        self.baseTitle = Label(pageSystem, text=controller.currentLanguage.fermentationPageContent[13], font=self.inputFont, fg = 'purple', bg = self.colorORT)
        self.baseTitle.place(x=120-self.traslation, y=500)
        self.systemInformation.append(Label(pageSystem, font=self.statusFont, bg = 'white', height=1, width=11, borderwidth=2, relief="groove", highlightbackground='white')) #MOTOR VELOCITY
        self.systemInformation[0].place(x=410-self.traslation, y=25)
        self.systemInformation.append(Label(pageSystem, font=self.magnitudeExtraFont, fg='blue', bg = 'white', height=1, width=11, borderwidth=2, relief="groove", highlightbackground='white')) #VARIATOR FREQUENCY
        self.systemInformation[1].place(x=200-self.traslation, y=440)
        self.systemInformation.append(Label(pageSystem, font=self.statusFont, fg='dark orange', bg = 'white', height=1, width=9, borderwidth=2, relief="groove", highlightbackground='white')) #TEMPERATURE FERM
        self.systemInformation[2].place(x=470-self.traslation, y=120)
        self.systemInformation.append(Label(pageSystem, font=self.statusFont, fg='deep sky blue', bg ='white', height=1, width=9, borderwidth=2, relief="groove", highlightbackground='white')) #TEMPERATURE BATH
        self.systemInformation[3].place(x=170-self.traslation, y=280)
        self.systemInformation.append(Label(pageSystem, font=self.statusFont, fg='green4', bg = 'white', height=1, width=9, borderwidth=2, relief="groove", highlightbackground='white')) #PH FERM
        self.systemInformation[4].place(x=190-self.traslation, y=90)
        self.systemInformation.append(Label(pageSystem, font=self.magnitudeExtraFont, fg='dark red', bg = 'white', height=1, width=11, borderwidth=2, relief="groove", highlightbackground='white')) #VOLUME ACID
        self.systemInformation[5].place(x=200-self.traslation, y=470)
        self.systemInformation.append(Label(pageSystem, font=self.magnitudeExtraFont, fg='purple4', bg = 'white', height=1, width=11, borderwidth=2, relief="groove", highlightbackground='white')) #VOLUME BASE
        self.systemInformation[6].place(x=200-self.traslation, y=500)

    def fillSystemInformation(self, pageSystem, controller):
        self.runAllControlInfo = Label(pageSystem, text=controller.currentLanguage.fermentationPageContent[22], font=self.inputFont, fg = 'green', bg = self.colorORT)
        self.runAllControlInfo.place(x=600-self.traslation, y=105)
        self.restartAllControlInfo = Label(pageSystem, text=controller.currentLanguage.fermentationPageContent[23], font=self.inputFont, fg = 'blue', bg = self.colorORT)
        self.restartAllControlInfo.place(x=580-self.traslation, y=240)
        self.pauseAllControlInfo = Label(pageSystem, text=controller.currentLanguage.fermentationPageContent[24], font=self.inputFont, fg = 'blue', bg = self.colorORT)
        self.pauseAllControlInfo.place(x=585-self.traslation, y=375)
        self.stopAllControlInfo = Label(pageSystem, text=controller.currentLanguage.fermentationPageContent[25], font=self.inputFont, fg = 'red', bg = self.colorORT)
        self.stopAllControlInfo.place(x=595-self.traslation, y=510)

    def getFreeWheelOptions(self):
        freeWheelOption = 0
        if(self.freeWheelSelection[0].get()==1):
            freeWheelOption = freeWheelOption + 1
        if(self.freeWheelSelection[1].get()==1):
            freeWheelOption = freeWheelOption + 2
        if(self.freeWheelSelection[2].get()==1):
            freeWheelOption = freeWheelOption + 4
        return freeWheelOption

    def isPotentialInputCorrectOnFreeWheel(self, potentialFreeWheelInput):
        return int(potentialFreeWheelInput.get())<=12.0 and int(potentialFreeWheelInput.get())>=2.0

    def manageWrongInputFreeWheel(self, controller, optionChosen, isInputCorrect):
        velocityInputCorrect = isInputCorrect[0]
        temperatureInputCorrect = isInputCorrect[1]
        potentialHydrogenInputCorrect = isInputCorrect[2]
        if(optionChosen==1 and not velocityInputCorrect):
            messagebox.showerror(controller.currentLanguage.fermentationPageContent[27], controller.currentLanguage.fermentationPageContent[28])
        if(optionChosen==2 and not temperatureInputCorrect):
            messagebox.showerror(controller.currentLanguage.fermentationPageContent[29], controller.currentLanguage.fermentationPageContent[30])
        if(optionChosen==3 and (not velocityInputCorrect or not temperatureInputCorrect)):
            messagebox.showerror(controller.currentLanguage.fermentationPageContent[31], controller.currentLanguage.fermentationPageContent[32])
        if(optionChosen==4 and not potentialHydrogenInputCorrect):
            messagebox.showerror(controller.currentLanguage.fermentationPageContent[33], controller.currentLanguage.fermentationPageContent[34])
        if(optionChosen==5 and (not velocityInputCorrect or not potentialHydrogenInputCorrect)):
            messagebox.showerror(controller.currentLanguage.fermentationPageContent[35], controller.currentLanguage.fermentationPageContent[36])
        if(optionChosen==6 and (not temperatureInputCorrect or not potentialHydrogenInputCorrect)):
            messagebox.showerror(controller.currentLanguage.fermentationPageContent[37], controller.currentLanguage.fermentationPageContent[38])
        if(optionChosen==7 and (not velocityInputCorrect or not temperatureInputCorrect or not potentialHydrogenInputCorrect)):
            messagebox.showerror(controller.currentLanguage.fermentationPageContent[39], controller.currentLanguage.fermentationPageContent[40])
        if(optionChosen>=1 and (velocityInputCorrect or temperatureInputCorrect or potentialHydrogenInputCorrect)):
            messagebox.showinfo(controller.currentLanguage.fermentationPageContent[10], controller.currentLanguage.fermentationPageContent[257])

    def manageVelocityFreeWheel(self, controller, controlState):
        if(controlState==1):
            controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].isVelocityControlOnFreeWheel = True
            self.runVelocityControl(controller)
        if(controlState==2):
            self.pauseVelocityControl(controller)
        if(controlState==3):
            controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].isVelocityControlOnFreeWheel = False
            self.stopVelocityControl(controller)
        if(controlState==4):
            controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].isVelocityControlOnFreeWheel = True
            self.restartVelocityControl(controller)

    def manageTemperatureFreeWheel(self, controller, controlState):
        if(controlState==1):
            controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].isTemperatureControlOnFreeWheel = True
            self.runTemperatureControl(controller)
        if(controlState==2):
            self.pauseTemperatureControl(controller)
        if(controlState==3):
            controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].isTemperatureControlOnFreeWheel = False
            self.stopTemperatureControl(controller)
        if(controlState==4):
            controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].isTemperatureControlOnFreeWheel = True
            self.restartTemperatureControl(controller)

    def managePotentialHydrogenFreeWheel(self, controller, controlState):
        if(controlState==1):
            controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].isPotentialHydrogenControlOnFreeWheel = True
            self.runPotentialHydrogenControl(controller)
        if(controlState==2):
            self.pausePotentialHydrogenControl(controller)
        if(controlState==3):
            controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].isPotentialHydrogenControlOnFreeWheel = False
            self.stopPotentialHydrogenControl(controller)
        if(controlState==4):
            controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].isPotentialHydrogenControlOnFreeWheel = True
            self.restartPotentialHydrogenControl(controller)

    def configureFreeWheelControls(self, controller, optionChosen, controlState):
        velocityInputCorrect = self.isMagnitudeInputCorrectOnFreeWheel(self.freeWheelInformation[0], [199,801])
        temperatureInputCorrect = self.isMagnitudeInputCorrectOnFreeWheel(self.freeWheelInformation[1], [10,98])
        potentialHydrogenInputCorrect = self.isPotentialInputCorrectOnFreeWheel(self.freeWheelInformation[2])
        if((optionChosen==1 or optionChosen==3 or optionChosen==5 or optionChosen==7) and velocityInputCorrect):
            self.manageVelocityFreeWheel(controller, controlState)
        if((optionChosen==2 or optionChosen==3 or optionChosen==6 or optionChosen==7) and temperatureInputCorrect):
            self.manageTemperatureFreeWheel(controller, controlState)
        if((optionChosen==3 or optionChosen==4 or optionChosen==6 or optionChosen==7) and potentialHydrogenInputCorrect):
            self.managePotentialHydrogenFreeWheel(controller, controlState)
        self.manageWrongInputFreeWheel(controller, optionChosen, [velocityInputCorrect, temperatureInputCorrect, potentialHydrogenCorrect])

    def runAllControl(self, controller):
        optionChosen = self.getFreeWheelOptions()
        if(optionChosen==0):
            if(len(controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].magnitudesToControl.velocities)>0):
                self.runVelocity(controller)
            if(len(controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].magnitudesToControl.temperatures)>0):
                self.runTemperature(controller)
            if(len(controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].magnitudesToControl.potentialsHydrogen)>0):
                self.runPotential(controller)
        elif(messagebox.askokcancel(controller.currentLanguage.fermentationPageContent[14], controller.currentLanguage.fermentationPageContent[26])):
            self.configureFreeWheelControls(controller, optionChosen, 1)

    def restartAllControl(self, controller):
        self.restartVelocityControl(controller)
        self.restartTemperatureControl(controller)
        self.restartPotentialHydrogenControl(controller)

    def pauseAllControl(self, controller):
        if(controller.settingVelocityControl[1] == 1 or controller.settingVelocityControl[2] == 2):
            self.pauseVelocityControl(controller)
        if(controller.settingTemperatureControl[1] == 1 or controller.settingTemperatureControl[2] == 2):
            self.pauseTemperatureControl(controller)
        if(controller.settingPotentialHydrogenControl[1] == 1 or controller.settingPotentialHydrogenControl[2] == 2):
            self.pausePotentialHydrogenControl(controller)

    def stopAllControl(self, controller):
        if(controller.settingVelocityControl[1] == 1):
            controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].isVelocityControlOnFreeWheel = False
            self.stopVelocityControl(controller)
        if(controller.settingTemperatureControl[1] == 1):
            controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].isTemperatureControlOnFreeWheel = False
            self.stopTemperatureControl(controller)
        if(controller.settingPotentialHydrogenControl[1] == 1):
            controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].isPotentialHydrogenControlOnFreeWheel = False
            self.stopPotentialHydrogenControl(controller)

    def setPageSystemButtons(self, pageSystem, controller):
        runAllOption = Button(pageSystem, relief = SUNKEN, image = self.buttonsSystem[3], command = lambda:self.runAllControl(controller))
        runAllOption.place(x=600-self.traslation, y=25) # RUN ALL
        restartAllOption = Button(pageSystem, relief = SUNKEN, image = self.buttonsSystem[8], command = lambda:self.restartAllControl(controller))
        restartAllOption.place(x=600-self.traslation, y=160) # RESTART ALL
        pauseAllOption = Button(pageSystem, relief = SUNKEN, image = self.buttonsSystem[4], command = lambda:self.pauseAllControl(controller))
        pauseAllOption.place(x=600-self.traslation, y=295) # PAUSE ALL
        stopAllOption = Button(pageSystem, relief = SUNKEN, image = self.buttonsSystem[5], command = lambda:self.stopAllControl(controller))
        stopAllOption.place(x=600-self.traslation, y=430) # STOP ALL
        self.fillSystemInformation(pageSystem, controller)

    def fillPageSystem(self, pageSystem, controller):
        self.fillPicturesOnPageSystem(pageSystem, controller)
        self.setPageSystemLabels(pageSystem, controller)
        print("LARGO DE SYSTEMINFO: ", len(self.systemInformation))
        self.setPageSystemButtons(pageSystem, controller)
        self.systemMagnitudesCanvas = FigureCanvasTkAgg(self.systemMagnitudesFigure, pageSystem)

    def fillPageGlobalPictures(self, pageGlobal):
        smartSystemElement = Picture(['smartSystemElement','png',130,530,610,20],0)
        smartSystemElement.purpose = 'Words'
        smartSystemElementPic = smartSystemElement.generateLabel(pageGlobal)
        smartSystemElementPic.place(x=smartSystemElement.location[0],y=smartSystemElement.location[1])

    def updateInterestedMagnitudesGlobalGraphics(self, controller):
        self.systemMagnitudesGraph1.set_xlabel(controller.currentLanguage.fermentationPageContent[42])
        self.freeWheelVelocityGraph.set_xlabel(controller.currentLanguage.fermentationPageContent[42])
        if(controller.settingVelocityControl[6]==0):
            self.systemMagnitudesGraph1.set_ylabel(controller.currentLanguage.fermentationPageContent[43]+"[rpm]", color='tab:blue')
            self.freeWheelVelocityGraph.set_ylabel(controller.currentLanguage.fermentationPageContent[43]+"[rpm]", color='tab:blue')
        if(controller.settingVelocityControl[6]==1):
            self.systemMagnitudesGraph1.set_ylabel(controller.currentLanguage.fermentationPageContent[43]+"[m/s]", color='tab:blue')
            self.freeWheelVelocityGraph.set_ylabel(controller.currentLanguage.fermentationPageContent[43]+"[m/s]", color='tab:blue')
        if(controller.settingVelocityControl[6]==2):
            self.systemMagnitudesGraph1.set_ylabel(controller.currentLanguage.fermentationPageContent[43]+"[rad/s]", color='tab:blue')
            self.freeWheelVelocityGraph.set_ylabel(controller.currentLanguage.fermentationPageContent[43]+"[rad/s]", color='tab:blue')
        self.systemMagnitudesGraph1.plot(self.secondsListVelocity, self.velList, color='tab:blue')
        self.systemMagnitudesGraph1.tick_params(axis='y', labelcolor='tab:blue')

        if(controller.settingTemperatureControl[6]==0):
            self.systemMagnitudesGraph2.set_ylabel(controller.currentLanguage.fermentationPageContent[44]+"[°C]", color='tab:orange')
            self.freeWheelTemperatureGraph.set_ylabel(controller.currentLanguage.fermentationPageContent[44]+"[°C]", color='tab:orange')
        if(controller.settingTemperatureControl[6]==1):
            self.systemMagnitudesGraph2.set_ylabel(controller.currentLanguage.fermentationPageContent[44]+"[K]", color='tab:orange')
            self.freeWheelTemperatureGraph.set_ylabel(controller.currentLanguage.fermentationPageContent[44]+"[K]", color='tab:orange')
        if(controller.settingTemperatureControl[6]==2):
            self.systemMagnitudesGraph2.set_ylabel(controller.currentLanguage.fermentationPageContent[44]+"[°F]", color='tab:orange')
            self.freeWheelTemperatureGraph.set_ylabel(controller.currentLanguage.fermentationPageContent[44]+"[°F]", color='tab:orange')
        self.systemMagnitudesGraph2.plot(self.secondsListTemperature, self.temperatureFermentorList, color='tab:orange')
        self.systemMagnitudesGraph2.tick_params(axis='y', labelcolor='tab:orange')

        self.systemMagnitudesGraph3.set_ylabel(controller.currentLanguage.fermentationPageContent[45], color='tab:green')
        self.systemMagnitudesGraph3.plot(self.secondsListPotential, self.potHydrogenList, color='tab:green')
        self.systemMagnitudesGraph3.tick_params(axis='y', labelcolor='tab:green')

        self.systemMagnitudesFigure.tight_layout()
        self.systemMagnitudesCanvas.draw()
        self.systemMagnitudesCanvas.get_tk_widget().place(x=610, y=0)

        if(controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].isVelocityControlOnFreeWheel):
            self.freeWheelVelocityGraph.plot(self.secondsListVelocity, self.velList, color='tab:blue')
            self.freeWheelVelocityGraph.tick_params(axis='y', labelcolor='tab:blue')
        if(controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].isTemperatureControlOnFreeWheel):
            self.freeWheelTemperatureGraph.plot(self.secondsListTemperature, self.temperatureFermentorList, color='tab:orange')
            self.freeWheelTemperatureGraph.tick_params(axis='y', labelcolor='tab:orange')
        if(controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].isPotentialHydrogenControlOnFreeWheel):
            self.freeWheelPotentialGraph.set_ylabel(controller.currentLanguage.fermentationPageContent[45], color='tab:green')
            self.freeWheelPotentialGraph.plot(self.secondsListPotential, self.potHydrogenList, color='tab:green')
            self.freeWheelPotentialGraph.tick_params(axis='y', labelcolor='tab:green')

        self.freeWheelFigure.tight_layout()
        self.freeWheelCanvas.draw()
        self.freeWheelCanvas.get_tk_widget().place(x=0, y=0)


    def updateSecondaryMagnitudesGlobalGraphics(self, controller):
        self.frequencyGraph.set_xlabel(controller.currentLanguage.fermentationPageContent[42])
        self.frequencyGraph.set_ylabel(controller.currentLanguage.fermentationPageContent[46], color='tab:brown')
        self.frequencyGraph.plot(self.secondsListVelocity, self.freqList, color='tab:brown')
        self.frequencyGraph.tick_params(axis='y', labelcolor='tab:brown')

        if(controller.settingTemperatureControl[6]==0):
            self.bathTemperatureGraph.set_ylabel(controller.currentLanguage.fermentationPageContent[47]+"[°C]", color='tab:cyan')
        if(controller.settingTemperatureControl[6]==1):
            self.bathTemperatureGraph.set_ylabel(controller.currentLanguage.fermentationPageContent[47]+"[K]", color='tab:cyan')
        if(controller.settingTemperatureControl[6]==2):
            self.bathTemperatureGraph.set_ylabel(controller.currentLanguage.fermentationPageContent[47]+"[°F]", color='tab:cyan')
        self.bathTemperatureGraph.plot(self.secondsListTemperature, self.temperatureBathList, color='tab:cyan')
        self.bathTemperatureGraph.tick_params(axis='y', labelcolor='tab:cyan')

        self.frequencyFigure.tight_layout()
        self.frequencyCanvas.draw()
        self.frequencyCanvas.get_tk_widget().place(x=0, y=0)

        self.dropsAcidGraph.set_xlabel(controller.currentLanguage.fermentationPageContent[42])
        self.dropsAcidGraph.set_ylabel(controller.currentLanguage.fermentationPageContent[48], color='tab:red')
        self.dropsAcidGraph.plot(self.secondsListPotential, self.volumeAcidList, color='tab:red')
        self.dropsAcidGraph.tick_params(axis='y', labelcolor='tab:red')

        self.dropsBaseGraph.set_ylabel(controller.currentLanguage.fermentationPageContent[49], color='tab:purple')
        self.dropsBaseGraph.plot(self.secondsListPotential, self.volumeBaseList, color='tab:purple')
        self.dropsBaseGraph.tick_params(axis='y', labelcolor='tab:purple')

        if(controller.settingPotentialHydrogenControl[6]==0):
            self.dropsAcidGraph.set_ylabel(controller.currentLanguage.fermentationPageContent[48]+"[mL]", color='tab:red')
            self.dropsBaseGraph.set_ylabel(controller.currentLanguage.fermentationPageContent[49]+"[mL]", color='tab:purple')
        if(controller.settingPotentialHydrogenControl[6]==1):
            self.dropsAcidGraph.set_ylabel(controller.currentLanguage.fermentationPageContent[48]+"[cui]", color='tab:red')
            self.dropsBaseGraph.set_ylabel(controller.currentLanguage.fermentationPageContent[49]+"[cui]", color='tab:purple')
        if(controller.settingPotentialHydrogenControl[6]==2):
            self.dropsAcidGraph.set_ylabel(controller.currentLanguage.fermentationPageContent[48]+"[L]", color='tab:red')
            self.dropsBaseGraph.set_ylabel(controller.currentLanguage.fermentationPageContent[49]+"[L]", color='tab:purple')

        self.dropsFigure.tight_layout()
        self.dropsCanvas.draw()
        self.dropsCanvas.get_tk_widget().place(x=740, y=0)

    def setScreensDisplay(self, controller):
        if(controller.settingVelocityControl[1]!=0 or controller.settingTemperatureControl[1]!=0 or controller.settingPotentialHydrogenControl[1]!=0):
            controller.settingScreensControl[2] = 6 #Page Status
            self.setVelocityDisplay(controller)
            self.setTemperatureDisplay(controller)
            self.setPotentialDisplay(controller)
            if(controller.settingScreensControl[1] != 1 and controller.settingScreensControl[1] >= 0):
                controller.settingScreensControl[1] = 1

    def setVelocityDisplay(self, controller):
        if(controller.settingVelocityControl[1]!=0):
            controller.settingScreensControl[6] = 0 #Error Status - CHANGE WHEN GEMMA
            controller.settingScreensControl[9] = controller.settingVelocityControl[6] #Unit Status
            controller.settingScreensControl[10] = controller.settingVelocityControl[9] #Orientation
            controller.settingScreensControl[13] = controller.settingVelocityControl[8] #Slope
            controller.settingScreensControl[14] = 1 #Controls Running
            controller.settingScreensControl[18] = int(self.currentMagnitudesValues[0]*10) #Value
        else:
            controller.settingScreensControl[14] = 0

    def setTemperatureDisplay(self, controller):
        print("controller.settingTemperatureControl[1]: ", controller.settingTemperatureControl[1])
        print("int(self.currentMagnitudesValues[1]*100): ", int(self.currentMagnitudesValues[1]*100))
        if(controller.settingTemperatureControl[1]!=0):
            controller.settingScreensControl[5] = 0 #Error Status - CHANGE WHEN GEMMA
            controller.settingScreensControl[8] = controller.settingTemperatureControl[6] #Unit Status
            controller.settingScreensControl[12] = controller.settingTemperatureControl[8] #Slope
            controller.settingScreensControl[15] = 1 #Controls Running
            controller.settingScreensControl[19] = int(self.currentMagnitudesValues[1]*100) #Value
        else:
            controller.settingScreensControl[15] = 0

    def setPotentialDisplay(self, controller):
        if(controller.settingPotentialHydrogenControl[1]!=0):
            controller.settingScreensControl[4] = 0 #Error Status - CHANGE WHEN GEMMA
            controller.settingScreensControl[11] = int(controller.settingPotentialHydrogenControl[11]/2) #Slope
            controller.settingScreensControl[16] = 1 #Controls Running
            controller.settingScreensControl[20] = int(self.currentMagnitudesValues[2]*1000) #Value
        else:
            controller.settingScreensControl[16] = 0

    def checkVelocityError(self, controller):
        if(controller.settingVelocityControl[16]==0):
            self.isErrorFound[0] = False
        if(controller.settingVelocityControl[17]>0 or (controller.settingVelocityControl[16]>0 and self.isErrorFound[0])):
            self.currentLedHandler.setErrorDetected()
        if(controller.settingVelocityControl[16]>0 and not self.isErrorFound[0]):
            self.currentLedHandler.configureErrorAnimation()
            self.isErrorFound[0] = True

    def checkTemperatureError(self, controller):
        if(controller.settingTemperatureControl[23]==0):
            self.isErrorFound[1] = False
        if(controller.settingTemperatureControl[24]>0 or (controller.settingTemperatureControl[23]>0 and self.isErrorFound[1])):
            self.currentLedHandler.setErrorDetected()
        if(controller.settingTemperatureControl[23]>0 and not self.isErrorFound[1]):
            self.currentLedHandler.configureErrorAnimation()
            self.isErrorFound[1] = True

    def checkPotentialError(self, controller):
        if(controller.settingPotentialHydrogenControl[21]==0):
            self.isErrorFound[2] = False
        if(controller.settingPotentialHydrogenControl[23]>0 or (controller.settingPotentialHydrogenControl[21]>0 and self.isErrorFound[2])):
            self.currentLedHandler.setErrorDetected()
        if(controller.settingPotentialHydrogenControl[21]>0 and not self.isErrorFound[2]):
            self.currentLedHandler.configureErrorAnimation()
            self.isErrorFound[2] = True

    def checkErrorMagnitudes(self, controller):
        self.checkVelocityError(controller)
        self.checkTemperatureError(controller)
        self.checkPotentialError(controller)

    def configureVelocityErrorAction(self, controller):
        if(self.isErrorFound[0] and self.stopMagnitudeWhenVelocity[0].get()==1):
            controller.settingTemperatureControl[1] = 0
            self.isControlInitialized[1] = False
            controller.settingVelocityControl[2] = 1
        if(self.isErrorFound[0] and self.stopMagnitudeWhenVelocity[1].get()==1):
            controller.settingPotentialHydrogenControl[1] = 0
            self.isControlInitialized[2] = False
            controller.settingPotentialHydrogenControl[2] = 1
        self.isErrorFound[0] = False

    def configureTemperatureErrorAction(self, controller):
        if(self.isErrorFound[1] and self.stopMagnitudeWhenTemperature[0].get()==1):
            controller.settingVelocityControl[1] = 0
            self.isControlInitialized[0] = False
            controller.settingVelocityControl[2] = 1
        if(self.isErrorFound[1] and self.stopMagnitudeWhenTemperature[1].get()==1):
            controller.settingPotentialHydrogenControl[1] = 0
            self.isControlInitialized[2] = False
            controller.settingPotentialHydrogenControl[2] = 1
        self.isErrorFound[1] = False

    def configurePotentialErrorAction(self, controller):
        if(self.isErrorFound[2] and self.stopMagnitudeWhenPotential[0].get()==1):
            controller.settingVelocityControl[1] = 0
            self.isControlInitialized[0] = False
            controller.settingVelocityControl[2] = 1
        if(self.isErrorFound[2] and self.stopMagnitudeWhenPotential[1].get()==1):
            controller.settingTemperatureControl[1] = 0
            self.isControlInitialized[1] = False
            controller.settingTemperatureControl[2] = 1
        self.isErrorFound[2] = False

    def configureErrorActionMagnitudes(self, controller):
        self.configureVelocityErrorAction(controller)
        self.configureTemperatureErrorAction(controller)
        self.configurePotentialErrorAction(controller)

    def manageVelocityError(self, controller, errorProblems):
        currentTime = datetime.today()
        currentTimeStr = currentTime.strftime("%b %d %Y %H:%M:%S.%f")
        if(errorProblems[0]==1):
            self.errorInformation[0].config(text=controller.currentLanguage.fermentationPageContent[258])
            self.saveMagnitudeControlStatus(self.velocityErrorFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[259])
            self.saveMagnitudeControlStatus(self.velocityStatusFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[260])
        if(errorProblems[0]==2):
            self.errorInformation[0].config(text=controller.currentLanguage.fermentationPageContent[261])
            self.saveMagnitudeControlStatus(self.velocityErrorFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[262])
            self.saveMagnitudeControlStatus(self.velocityStatusFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[260])
        if(errorProblems[0]==3):
            self.errorInformation[0].config(text=controller.currentLanguage.fermentationPageContent[263])
            self.saveMagnitudeControlStatus(self.velocityErrorFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[264])
            self.saveMagnitudeControlStatus(self.velocityStatusFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[260])
        if(errorProblems[0]==4):
            self.errorInformation[0].config(text=controller.currentLanguage.fermentationPageContent[265])
            self.saveMagnitudeControlStatus(self.velocityErrorFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[266])
            self.saveMagnitudeControlStatus(self.velocityStatusFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[267])
        if(errorProblems[0]==5):
            self.errorInformation[0].config(text=controller.currentLanguage.fermentationPageContent[268])
            self.saveMagnitudeControlStatus(self.velocityErrorFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[269])
            self.saveMagnitudeControlStatus(self.velocityStatusFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[260])
        if(errorProblems[1]==1):
            self.errorInformation[0].config(text=controller.currentLanguage.fermentationPageContent[270])
            self.saveMagnitudeControlStatus(self.velocityErrorFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[271])
            self.saveMagnitudeControlStatus(self.velocityStatusFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[272])
        if(errorProblems[1]==2):
            self.errorInformation[0].config(text=controller.currentLanguage.fermentationPageContent[273])
            self.saveMagnitudeControlStatus(self.velocityErrorFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[274])
            self.saveMagnitudeControlStatus(self.velocityStatusFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[272])

    def logAndDisplayVelocityError(self, controller):
        connectionProblem = controller.settingVelocityControl[16]
        sensorProblem = controller.settingVelocityControl[17]
        if(sensorProblem==0 and connectionProblem==0):
            self.errorInformation[0].config(text=controller.currentLanguage.fermentationPageContent[164])
        else:
            self.manageVelocityError(controller, [sensorProblem, connectionProblem])

    def manageTemperatureError(self, controller, errorProblems):
        currentTime = datetime.today()
        currentTimeStr = currentTime.strftime("%b %d %Y %H:%M:%S.%f")
        if(errorProblems[0]==1):
            self.errorInformation[1].config(text=controller.currentLanguage.fermentationPageContent[258])
            elf.saveMagnitudeControlStatus(self.temperatureErrorFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[259])
            self.saveMagnitudeControlStatus(self.temperatureStatusFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[260])
        if(errorProblems[0]==2):
            self.errorInformation[1].config(text=controller.currentLanguage.fermentationPageContent[261])
            self.saveMagnitudeControlStatus(self.temperatureErrorFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[261])
            self.saveMagnitudeControlStatus(self.temperatureStatusFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[260])
        if(errorProblems[0]==3):
            self.errorInformation[1].config(text=controller.currentLanguage.fermentationPageContent[275])
            self.saveMagnitudeControlStatus(self.temperatureErrorFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[276])
            self.saveMagnitudeControlStatus(self.temperatureStatusFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[260])
        if(errorProblems[0]==4):
            self.errorInformation[1].config(text=controller.currentLanguage.fermentationPageContent[277])
            self.saveMagnitudeControlStatus(self.temperatureErrorFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[278])
            self.saveMagnitudeControlStatus(self.temperatureStatusFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[260])
        if(errorProblems[0]==5):
            self.errorInformation[1].config(text=controller.currentLanguage.fermentationPageContent[279])
            self.saveMagnitudeControlStatus(self.temperatureErrorFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[280])
            self.saveMagnitudeControlStatus(self.temperatureStatusFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[260])
        if(errorProblems[0]==6):
            self.errorInformation[1].config(text=controller.currentLanguage.fermentationPageContent[281])
            self.saveMagnitudeControlStatus(self.temperatureErrorFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[282])
            self.saveMagnitudeControlStatus(self.temperatureStatusFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[260])
        if(errorProblems[1]==1):
            self.errorInformation[1].config(text=controller.currentLanguage.fermentationPageContent[283])
            self.saveMagnitudeControlStatus(self.temperatureErrorFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[284])
            self.saveMagnitudeControlStatus(self.temperatureStatusFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[272])
        if(errorProblems[1]==2):
            self.errorInformation[1].config(text=controller.currentLanguage.fermentationPageContent[285])
            self.saveMagnitudeControlStatus(self.temperatureErrorFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[286])
            self.saveMagnitudeControlStatus(self.temperatureStatusFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[272])


    def logAndDisplayTemperatureError(self, controller):
        connectionProblem = controller.settingTemperatureControl[23]
        sensorProblem = controller.settingTemperatureControl[24]
        if(sensorProblem==0 and connectionProblem==0):
            self.errorInformation[1].config(text=controller.currentLanguage.fermentationPageContent[164])
        else:
            self.manageTemperatureError(controller, [sensorProblem, connectionProblem])

    def managePotentialError(self, controller, errorProblems):
        currentTime = datetime.today()
        currentTimeStr = currentTime.strftime("%b %d %Y %H:%M:%S.%f")
        if(errorProblems[0]==1):
            self.errorInformation[2].config(text=controller.currentLanguage.fermentationPageContent[287])
            elf.saveMagnitudeControlStatus(self.potentialHydrogenErrorFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[259])
            self.saveMagnitudeControlStatus(self.potentialHydrogenStatusFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[288])
        if(errorProblems[0]==2):
            self.errorInformation[2].config(text=controller.currentLanguage.fermentationPageContent[290])
            self.saveMagnitudeControlStatus(self.potentialHydrogenErrorFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[262])
            self.saveMagnitudeControlStatus(self.potentialHydrogenStatusFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[288])
        if(errorProblems[0]==3):
            self.errorInformation[2].config(text=controller.currentLanguage.fermentationPageContent[291])
            self.saveMagnitudeControlStatus(self.potentialHydrogenErrorFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[294])
            self.saveMagnitudeControlStatus(self.potentialHydrogenStatusFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[288])
        if(errorProblems[0]==4):
            self.errorInformation[2].config(text=controller.currentLanguage.fermentationPageContent[292])
            self.saveMagnitudeControlStatus(self.potentialHydrogenErrorFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[295])
            self.saveMagnitudeControlStatus(self.potentialHydrogenStatusFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[288])
        if(errorProblems[1]==1):
            self.errorInformation[2].config(text=controller.currentLanguage.fermentationPageContent[293])
            self.saveMagnitudeControlStatus(self.potentialHydrogenErrorFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[296])
            self.saveMagnitudeControlStatus(self.potentialHydrogenStatusFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[289])

    def logAndDisplayPotentialError(self, controller):
        connectionProblem = controller.settingPotentialHydrogenControl[21]
        sensorProblem = controller.settingPotentialHydrogenControl[23]
        if(sensorProblem==0 and connectionProblem==0):
            self.errorInformation[2].config(text=controller.currentLanguage.fermentationPageContent[164])
        else:
            self.managePotentialError(controller, [sensorProblem, connectionProblem])

    def logAndDisplayErrorMagnitudes(self, controller):
        self.logAndDisplayVelocityError(controller)
        self.logAndDisplayTemperatureError(controller)
        self.logAndDisplayPotentialError(controller)

    def checkErrorStatus(self, controller):
        self.checkErrorMagnitudes(controller)
        if(not self.isErrorFound[0] and not self.isErrorFound[1] and not self.isErrorFound[2]):
            self.currentLedHandler.setErrorFixed()
        self.configureErrorActionMagnitudes(controller)
        self.logAndDisplayErrorMagnitudes(controller)

    def updateGlobalGraphics(self, controller):

        if(self.countUntilSave == 359):
            controller.application.saveSmartData("Backup/")
            self.countUntilSave == 0

        self.systemMagnitudesGraph1.clear()
        if(self.systemMagnitudesGraph2!=None):
            self.systemMagnitudesGraph2.clear()

        self.frequencyGraph.clear()
        self.bathTemperatureGraph.clear()

        self.dropsAcidGraph.clear()
        if(self.dropsBaseGraph!=None):
            self.dropsBaseGraph.clear()

        try:
            self.updateInterestedMagnitudesGlobalGraphics(controller)
            self.updateSecondaryMagnitudesGlobalGraphics(controller)
        except ValueError:
            print("VALUE ERROR")

        #self.countUntilSave = self.countUntilSave + 1
        print("UPDATE GLOBAL GRAPHICS: ", self.currentLedHandler.isControlExecuting)
        self.currentLedHandler.verifyLedsState()
        self.setScreensDisplay(controller)
        self.checkErrorStatus(controller)
        self.after(10000,lambda:self.updateGlobalGraphics(controller))

    def fillPageGlobal(self, pageGlobal, controller):
        self.fillPageGlobalPictures(pageGlobal)
        self.frequencyCanvas = FigureCanvasTkAgg(self.frequencyFigure, pageGlobal)
        self.bathTemperatureCanvas = FigureCanvasTkAgg(self.bathTemperatureFigure, pageGlobal)
        self.dropsCanvas = FigureCanvasTkAgg(self.dropsFigure, pageGlobal)

    def fillPageFreeWheelPictures(self, pageFreeWheel):
        freeWheelElement = Picture(['freeWheelElement','png',130,480,1250,50],180)
        freeWheelElement.purpose = 'Words'
        freeWheelElementPic = freeWheelElement.generateLabel(pageFreeWheel)
        freeWheelElementPic.place(x=freeWheelElement.location[0],y=freeWheelElement.location[1])

    def fillPageFreeWheelLabels(self, pageFreeWheel, controller):
        self.generalInformation.append(Label(pageFreeWheel, text=controller.currentLanguage.fermentationPageContent[19], font=self.infoFont, fg = self.colorORT, bg = 'white', height=2, width=59))
        self.generalInformation[0].place(x=720, y=430)
        self.generalInformation.append(Label(pageFreeWheel, text=controller.currentLanguage.fermentationPageContent[20], font=self.infoFont, fg = self.colorORT, bg = 'white', height=2, width=59))
        self.generalInformation[1].place(x=720, y=465)
        self.generalInformation.append(Label(pageFreeWheel, text=controller.currentLanguage.fermentationPageContent[21], font=self.infoFont, fg = self.colorORT, bg = 'white', height=2, width=59))
        self.generalInformation[2].place(x=720, y=500)
        self.freeWheelBorder = Label(pageFreeWheel, bg = self.colorORT, height=18, width=75, borderwidth=5, relief="groove", highlightbackground='white')
        self.freeWheelBorder.place(x=720, y=5)
        self.freeWheelTitle = Label(pageFreeWheel, text=controller.currentLanguage.fermentationPageContent[14], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.freeWheelTitle.place(x=745, y=18)
        self.velocityFreeWheelTitle = Label(pageFreeWheel, text=controller.currentLanguage.fermentationPageContent[15], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.velocityFreeWheelTitle.place(x=785, y=75)
        self.temperatureFreeWheelTitle = Label(pageFreeWheel, text=controller.currentLanguage.fermentationPageContent[16], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.temperatureFreeWheelTitle.place(x=785, y=155)
        self.potentialHydrogenFreeWheelTitle = Label(pageFreeWheel, text=controller.currentLanguage.fermentationPageContent[17], font=self.titleFont, fg = 'white', bg = self.colorORT)
        self.potentialHydrogenFreeWheelTitle.place(x=785, y=235)
        self.runFreeWheelInformation = Label(pageFreeWheel, text=controller.currentLanguage.fermentationPageContent[53], font=self.inputFont, fg = 'green', bg = self.colorORT)
        self.runFreeWheelInformation.place(x=780, y=385)
        self.pauseFreeWheelInformation = Label(pageFreeWheel, text=controller.currentLanguage.fermentationPageContent[54], font=self.inputFont, fg = 'blue', bg = self.colorORT)
        self.pauseFreeWheelInformation.place(x=895, y=385)
        self.stopFreeWheelInformation = Label(pageFreeWheel, text=controller.currentLanguage.fermentationPageContent[55], font=self.inputFont, fg = 'red', bg = self.colorORT)
        self.stopFreeWheelInformation.place(x=1020, y=385)
        self.restartFreeWheelInformation = Label(pageFreeWheel, text=controller.currentLanguage.fermentationPageContent[58], font=self.inputFont, fg = 'blue', bg = self.colorORT)
        self.restartFreeWheelInformation.place(x=1125, y=385)

    def fillPageFreeWheelEntries(self, pageFreeWheel, controller):
        self.freeWheelInformation.append(Spinbox(pageFreeWheel, from_=200, to=800, font=self.inputFont, fg = self.colorORT, width=10, justify='center')) # velocity
        self.freeWheelInformation[0].place(x=940, y=78)
        self.freeWheelInformation.append(Spinbox(pageFreeWheel, values=("rpm", "m/s", "rad/s"), font=self.inputFont, fg = self.colorORT, width=5, justify='center')) # velocity
        self.freeWheelInformation[1].place(x=1120, y=78)
        self.freeWheelInformation.append(Spinbox(pageFreeWheel, from_=10, to=95, font=self.inputFont, fg = self.colorORT, width=10, justify='center')) # temperature
        self.freeWheelInformation[2].place(x=980, y=158)
        self.freeWheelInformation.append(Spinbox(pageFreeWheel, values=("°C", "K", "°F"), font=self.inputFont, fg = self.colorORT, width=5, justify='center'))  # temperature
        self.freeWheelInformation[3].place(x=1120, y=158)
        self.freeWheelInformation.append(Spinbox(pageFreeWheel, from_=2, to=12, format="%.1f",increment=0.1, font=self.inputFont, fg = self.colorORT, width=10, justify='center'))  # potential hydrogen
        self.freeWheelInformation[4].place(x=1070, y=238)

    def runFreeWheelMagnitudes(self, controller):
        optionChosen = self.getFreeWheelOptions()
        self.configureFreeWheelControls(controller, optionChosen, 1)

    def pauseFreeWheelMagnitudes(self, controller):
        optionChosen = self.getFreeWheelOptions()
        self.configureFreeWheelControls(controller, optionChosen, 2)

    def stopFreeWheelMagnitudes(self, controller):
        optionChosen = self.getFreeWheelOptions()
        self.configureFreeWheelControls(controller, optionChosen, 3)

    def restartFreeWheelMagnitudes(self, controller):
        optionChosen = self.getFreeWheelOptions()
        self.configureFreeWheelControls(controller, optionChosen, 4)

    def fillPageFreeWheelButtons(self, pageFreeWheel, controller):
        self.freeWheelOption.append(Checkbutton(pageFreeWheel, height=2, width=2, bg=self.colorORT, variable=self.freeWheelSelection[0]))
        self.freeWheelOption[0].place(x=725, y=78)
        self.freeWheelOption.append(Checkbutton(pageFreeWheel, height=2, width=2, bg=self.colorORT, variable=self.freeWheelSelection[1]))
        self.freeWheelOption[1].place(x=725, y=158)
        self.freeWheelOption.append(Checkbutton(pageFreeWheel, height=2, width=2, bg=self.colorORT, variable=self.freeWheelSelection[2]))
        self.freeWheelOption[2].place(x=725, y=238)
        self.freeWheelAction = []
        self.freeWheelAction.append(Button(pageFreeWheel, image = self.buttonsVelocity[3], relief = SUNKEN, command = lambda:self.runFreeWheelMagnitudes(controller)))
        self.freeWheelAction[0].place(x=765, y=295)
        self.freeWheelAction.append(Button(pageFreeWheel, image = self.buttonsVelocity[4], relief = SUNKEN, command = lambda:self.pauseFreeWheelMagnitudes(controller)))
        self.freeWheelAction[1].place(x=885, y=295)
        self.freeWheelAction.append(Button(pageFreeWheel, image = self.buttonsVelocity[5], relief = SUNKEN, command = lambda:self.stopFreeWheelMagnitudes(controller)))
        self.freeWheelAction[2].place(x=1005, y=295)
        self.freeWheelAction.append(Button(pageFreeWheel, image = self.buttonsVelocity[8], relief = SUNKEN, command = lambda:self.restartFreeWheelMagnitudes(controller)))
        self.freeWheelAction[3].place(x=1125, y=295)

    def fillPageFreeWheel(self, pageFreeWheel, controller):
        self.fillPageFreeWheelPictures(pageFreeWheel)
        self.fillPageFreeWheelLabels(pageFreeWheel, controller)
        self.fillPageFreeWheelEntries(pageFreeWheel, controller)
        self.fillPageFreeWheelButtons(pageFreeWheel, controller)
        self.freeWheelCanvas = FigureCanvasTkAgg(self.freeWheelFigure, pageFreeWheel)

    def isTimeCorrect(self, timeToCheck, maximumValue):
        return timeToCheck<=maximumValue and timeToCheck>=0

    def isMagnitudeInputCorrectOnFreeWheel(self, magnitudInput, extremeValues):
        return magnitudInput.get().isdigit() and int(magnitudInput.get())<=extremeValues[1] and int(magnitudInput.get())>=extremeValues[0]

    def isDurationNotZero(self, magnitudesInput):
        return int(magnitudesInput[0].get()) + int(magnitudesInput[1].get()) + int(magnitudesInput[2].get()) != 0

    def isMagnitudeInputCorrect(self, magnitudInput, extremeValues):
        areFieldsNotEmpty =  magnitudInput[0].get().isdigit() and magnitudInput[1].get().isdigit() and magnitudInput[2].get().isdigit() and magnitudInput[3].get().isdigit()
        isMagnitudeValueCorrect = int(magnitudInput[0].get())<=extremeValues[1] and int(magnitudInput[0].get())>=extremeValues[0]
        isMagnitudeDurationCorrect =  self.isTimeCorrect(int(magnitudInput[1].get()), 91) and self.isTimeCorrect(int(magnitudInput[2].get()), 61) and self.isTimeCorrect(int(magnitudInput[3].get()), 61) and self.isDurationNotZero(magnitudInput)
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
                    #print("VALUE CHANGED: ", controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].magnitudesToControl.velocities[positionSelected].valueObjective)
                    controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].magnitudesToControl.velocities[positionSelected].duration = [self.velocityInput[1].get(), self.velocityInput[2].get(), self.velocityInput[3].get()]
                    #print("DURATION CHANGED: ", controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].magnitudesToControl.velocities[positionSelected].duration)
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
        self.velocityStatusFileTimeStr = "ControlData/Velocity/STATUS_Log/"+str(fileTime.strftime("%Y%m%d_%I%M%S"))+"_VEL.txt"
        self.velocityDataFileTimeStr = "ControlData/Velocity/DATA_Log/"+str(fileTime.strftime("%Y%m%d_%I%M%S"))+"_VEL.txt"
        self.velocityErrorFileTimeStr = "ControlData/Velocity/ERROR_Log/"+str(fileTime.strftime("%Y%m%d_%I%M%S"))+"_VEL.txt"
        print("VELOCITY FILE IN RUN: ", self.velocityDataFileTimeStr)
        controller.application.systemCurrentStatus.velocityControlData[0]=str(fileTime.strftime("%Y%m%d_%I%M%S"))+"_VEL.txt"
        controller.settingVelocityControl[4] = int(self.velocityDataFileTimeStr[39:45])
        controller.settingVelocityControl[5] = int(self.velocityDataFileTimeStr[30:38])
        controller.settingVelocityControl[2] = 0
        controller.settingVelocityControl[1] = 1
        controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].dataFilenames.append(str(fileTime.strftime("%Y%m%d_%I%M%S")))
        self.isControlInitialized[0] = True
        self.currentLedHandler.configureVelocityLeds(self.isControlInitialized[0])
        currentTime = datetime.today()
        currentTimeStr = currentTime.strftime("%b %d %Y %H:%M:%S.%f")
        self.velocityInformation[0]['text'] = controller.currentLanguage.fermentationPageContent[69] + currentTimeStr
        self.velocityInformation[1]['text'] = controller.currentLanguage.fermentationPageContent[70]
        controller.application.systemCurrentStatus.velocityControlData[2]=self.velocityInformation[0]['text']
        self.generalInformation[0]['text'] = controller.currentLanguage.fermentationPageContent[71]
        self.isMagnitudeListEditable[0] = False
        controller.application.saveStatusDataToFile()
        self.saveMagnitudeControlStatus(self.velocityStatusFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[297])

    def runVelocityControl(self, controller):
        if(len(controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].magnitudesToControl.velocities)>0 or controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].isVelocityControlOnFreeWheel):
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
            self.generalInformation[0]['text'] = controller.currentLanguage.fermentationPageContent[74]
            self.isMagnitudeListEditable[0] = True
            self.saveMagnitudeControlStatus(self.velocityStatusFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[298])
        else:
            controller.settingVelocityControl[2] = 0
            controller.settingVelocityControl[1] = 1
            self.setVelocityControlValues(controller)
            self.velocityInformation[1]['text'] = controller.currentLanguage.fermentationPageContent[75]
            self.generalInformation[0]['text'] = controller.currentLanguage.fermentationPageContent[76]
            self.isMagnitudeListEditable[0] = False
            self.saveMagnitudeControlStatus(self.velocityStatusFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[299])
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
        print("CARGO DATOS EN VEL DISPLAY")
        controller.settingScreensControl[2] = 6 #Page Status
        controller.settingScreensControl[14] = 0 #Controls Running
        if(controller.settingScreensControl[1] != 1):
            controller.settingScreensControl[1] = 1
        controller.settingVelocityControl[1] = 0
        self.isControlInitialized[0] = False
        self.currentLedHandler.configureVelocityLeds(self.isControlInitialized[0])
        controller.settingVelocityControl[2] = 1
        currentTime = datetime.today()
        currentTimeStr = currentTime.strftime("%b %d %Y %H:%M:%S.%f")
        self.velocityInformation[0]['text'] =  controller.currentLanguage.fermentationPageContent[78] + currentTimeStr
        self.velocityInformation[1]['text'] = controller.currentLanguage.fermentationPageContent[79]
        self.generalInformation[0]['text'] =  controller.currentLanguage.fermentationPageContent[80]
        self.isMagnitudeListEditable[0] = True
        controller.application.systemCurrentStatus.velocityControlData[2]=self.velocityInformation[0]['text']
        controller.application.systemCurrentStatus.velocityControlData[3] = self.velocityInformation[2]['text']
        controller.application.saveStatusDataToFile()
        self.saveMagnitudeControlStatus(self.velocityStatusFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[300])

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
        self.generalInformation[0]['text'] = controller.currentLanguage.fermentationPageContent[84]
        self.saveMagnitudeControlStatus(self.velocityStatusFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[301])
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
        self.saveMagnitudeControlStatus(self.velocityStatusFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[302])
        time.sleep(1)
        if(controller.settingVelocityControl[3]<=0):
            self.velocityList.itemconfig(0, {'bg':'cornflower blue'})
        else:
            self.velocityList.itemconfig(controller.settingVelocityControl[3]+1, {'bg':'white'})
            self.velocityList.itemconfig(controller.settingVelocityControl[3], {'bg':'cornflower blue'})

    def nextStepOnVelocityControl(self, controller):
        currentTime = datetime.today()
        currentTimeStr = currentTime.strftime("%b %d %Y %H:%M:%S.%f")
        controller.settingVelocityControl[2] = 4
        self.saveMagnitudeControlStatus(self.velocityStatusFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[303])
        time.sleep(1)
        if(controller.settingVelocityControl[3]<len(controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].magnitudesToControl.velocities)):
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

    def checkVelocityStatus(self, controller):
        if(self.isControlInitialized[0]):
            self.currentMagnitudesValues[0] = self.updateVelocityGraphic(controller)
        self.updateVelocityGlobalInformation(controller)
        #self.checkVelocityError(controller)
        currentTime = datetime.today()
        currentTimeStr = currentTime.strftime("%b %d %Y %H:%M:%S.%f")
        if(controller.settingVelocityControl[1]!=0):
            #self.setVelocityDisplay(controller, currentVelocity)
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
            self.velocityList.itemconfig(controller.settingVelocityControl[3], {'bg':'white'}) #TEST
            self.velocityInformation[2]['text'] = controller.currentLanguage.fermentationPageContent[86]
            self.isMagnitudeListEditable[0] = True
            if(self.isControlInitialized[0]):
                self.velocityInformation[0]['text'] = controller.currentLanguage.fermentationPageContent[87] + currentTimeStr
                self.velocityInformation[1]['text'] = controller.currentLanguage.fermentationPageContent[88]
                self.generalInformation[0]['text'] = controller.currentLanguage.fermentationPageContent[89]
                self.isControlInitialized[0] = False
                #self.velocityList.itemconfig(controller.settingVelocityControl[3], {'bg':'white'})
                self.saveMagnitudeControlStatus(self.velocityStatusFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[304])
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
        if(controller.application.systemCurrentStatus.velocityControlData[1]=="6" and self.isControlInitialized[0]):
            self.restartVelocityControl(controller)
            controller.application.systemCurrentStatus.velocityControlData[1]=="1"
            print("Velocidad REINICIADA")
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
            print("VELOCITIES 1 Value: ", velocities[0].valueObjective)
            print("VELOCITIES 1 Duration: ", velocities[0].duration)
            if(len(velocities)>0):
                position = 1
                for eachVelocity in velocities:
                    evolutionInformation = controller.currentLanguage.fermentationPageContent[91]
                    if(position==1):
                        evolutionInformation = controller.currentLanguage.fermentationPageContent[92]
                    elif(float(velocities[position-2].valueObjective)>float(eachVelocity.valueObjective)):
                        evolutionInformation = controller.currentLanguage.fermentationPageContent[93]
                    self.velocityList.insert(position, str(position)+". "+evolutionInformation+eachVelocity.showInformation())
                    position = position + 1
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
        self.temperatureStatusFileTimeStr = "ControlData/Temperature/STATUS_Log/"+str(fileTime.strftime("%Y%m%d_%I%M%S"))+"_TEM.txt"
        self.temperatureDataFileTimeStr = "ControlData/Temperature/DATA_Log/"+str(fileTime.strftime("%Y%m%d_%I%M%S"))+"_TEM.txt"
        self.temperatureErrorFileTimeStr = "ControlData/Temperature/ERROR_Log/"+str(fileTime.strftime("%Y%m%d_%I%M%S"))+"_TEM.txt"
        print("FILE TEMP EN RUN: ", self.temperatureDataFileTimeStr)
        controller.application.systemCurrentStatus.temperatureControlData[0]=str(fileTime.strftime("%Y%m%d_%I%M%S"))+"_TEM.txt"
        controller.settingTemperatureControl[4] = int(self.temperatureDataFileTimeStr[42:48])
        controller.settingTemperatureControl[5] = int(self.temperatureDataFileTimeStr[33:41])
        controller.settingTemperatureControl[2] = 0
        controller.settingTemperatureControl[1] = 1
        controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].dataFilenames.append(str(fileTime.strftime("%Y%m%d_%I%M%S")))
        self.isControlInitialized[1] = True
        self.currentLedHandler.configureTemperatureLeds(self.isControlInitialized[1])
        currentTime = datetime.today()
        currentTimeStr = currentTime.strftime("%b %d %Y %H:%M:%S.%f")
        self.temperatureInformation[0]['text'] = controller.currentLanguage.fermentationPageContent[100] + currentTimeStr
        self.temperatureInformation[1]['text'] = controller.currentLanguage.fermentationPageContent[70]
        controller.application.systemCurrentStatus.temperatureControlData[2]=self.temperatureInformation[0]['text']
        self.generalInformation[1]['text'] = controller.currentLanguage.fermentationPageContent[101]
        self.isMagnitudeListEditable[1] = False
        controller.application.saveStatusDataToFile()
        self.saveMagnitudeControlStatus(self.temperatureStatusFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[297])

    def runTemperatureControl(self, controller):
        if(len(controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].magnitudesToControl.temperatures)>0 or controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].isTemperatureControlOnFreeWheel):
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
            self.generalInformation[1]['text'] = controller.currentLanguage.fermentationPageContent[102]
            self.isMagnitudeListEditable[1] = True
            self.saveMagnitudeControlStatus(self.temperatureStatusFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[298])
        else:
            controller.settingTemperatureControl[2] = 0
            controller.settingTemperatureControl[1] = 1
            self.setTemperatureControlValues(controller)
            self.temperatureInformation[1]['text'] = controller.currentLanguage.fermentationPageContent[75]
            self.generalInformation[1]['text'] = controller.currentLanguage.fermentationPageContent[103]
            self.isMagnitudeListEditable[1] = False
            self.saveMagnitudeControlStatus(self.temperatureStatusFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[299])
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
        controller.settingScreensControl[2] = 6 #Page Status
        controller.settingScreensControl[15] = 0 #Controls Running
        if(controller.settingScreensControl[1] != 1):
            controller.settingScreensControl[1] = 1
        controller.settingTemperatureControl[1] = 0
        self.isControlInitialized[1] = False
        self.currentLedHandler.configureTemperatureLeds(self.isControlInitialized[1])
        controller.settingTemperatureControl[2] = 1
        currentTime = datetime.today()
        currentTimeStr = currentTime.strftime("%b %d %Y %H:%M:%S.%f")
        self.temperatureInformation[0]['text'] = controller.currentLanguage.fermentationPageContent[104] + currentTimeStr
        self.temperatureInformation[1]['text'] = controller.currentLanguage.fermentationPageContent[79]
        self.generalInformation[1]['text'] = controller.currentLanguage.fermentationPageContent[105]
        controller.application.systemCurrentStatus.temperatureControlData[2]=self.temperatureInformation[0]['text']
        controller.application.systemCurrentStatus.temperatureControlData[3] = self.temperatureInformation[2]['text']
        controller.application.saveStatusDataToFile()
        self.isMagnitudeListEditable[1] = True
        self.saveMagnitudeControlStatus(self.temperatureStatusFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[300])

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
        self.generalInformation[1]['text'] = controller.currentLanguage.fermentationPageContent[107]
        self.saveMagnitudeControlStatus(self.temperatureStatusFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[301])
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
        self.saveMagnitudeControlStatus(self.temperatureStatusFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[302])
        if(controller.settingTemperatureControl[3]<=0):
            self.temperatureList.itemconfig(0, {'bg':'orange'})
        else:
            self.temperatureList.itemconfig(controller.settingTemperatureControl[3]+1, {'bg':'white'})
            self.temperatureList.itemconfig(controller.settingTemperatureControl[3], {'bg':'orange'})

    def nextStepOnTemperatureControl(self, controller):
        currentTime = datetime.today()
        currentTimeStr = currentTime.strftime("%b %d %Y %H:%M:%S.%f")
        controller.settingTemperatureControl[2] = 4
        self.saveMagnitudeControlStatus(self.temperatureStatusFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[303])
        if(controller.settingTemperatureControl[3]<len(controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].magnitudesToControl.temperatures)):
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
            if(float(tempFermentor)>60):
                self.currentLedHandler.setWarningState()
            else:
                self.currentLedHandler.setActiveState()
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

    def checkTemperatureStatus(self, controller):
        if(self.isControlInitialized[1]):
            self.currentMagnitudesValues[1] = self.updateTemperatureGraphic(controller)
            print("self.currentMagnitudesValues[1]: ", self.currentMagnitudesValues[1])
        self.updateTemperatureGlobalInformation(controller)
        #self.checkTemperatureError(controller)
        currentTime = datetime.today()
        currentTimeStr = currentTime.strftime("%b %d %Y %H:%M:%S.%f")
        if(controller.settingTemperatureControl[1]!=0):
            #self.setTemperatureDisplay(controller, currentTemperature)
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
            self.temperatureList.itemconfig(controller.settingTemperatureControl[3], {'bg':'white'})
            if(self.isControlInitialized[1]):
                self.temperatureInformation[0]['text'] = controller.currentLanguage.fermentationPageContent[108] + currentTimeStr
                self.temperatureInformation[1]['text'] = controller.currentLanguage.fermentationPageContent[88]
                self.generalInformation[1]['text'] = controller.currentLanguage.fermentationPageContent[109]
                self.isControlInitialized[1] = False
                #self.temperatureList.itemconfig(controller.settingTemperatureControl[3], {'bg':'white'})
                self.saveMagnitudeControlStatus(self.temperatureStatusFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[304])
        controller.application.loadStatusDataFromFile()
        controller.application.systemCurrentStatus.temperatureControlData[3] = self.temperatureInformation[2]['text']
        if(controller.application.systemCurrentStatus.temperatureControlData[1]=="0"):
            print("Velocidad Sin Arrancar")
        if(controller.application.systemCurrentStatus.temperatureControlData[1]=="1" and not self.isControlInitialized[1]):
            self.runTemperature(controller)
            print("Temperatura EJECUTANDOSE")
        if(controller.application.systemCurrentStatus.temperatureControlData[1]=="2" and self.isControlInitialized[1]):
            self.pauseTemperatureControl(controller)
            print("Temp PAUSADO")
        if(controller.application.systemCurrentStatus.temperatureControlData[1]=="3" and self.isControlInitialized[1]):
            self.stopTemperature(controller)
            print("Temp DETENIDO")
        if(controller.application.systemCurrentStatus.temperatureControlData[1]=="6" and self.isControlInitialized[1]):
            self.restartTemperatureControl(controller)
            controller.application.systemCurrentStatus.temperatureControlData[1]=="1"
            print("Temp REINICIADA")
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
                    elif(float(temperatures[position-2].valueObjective)>float(eachTemperature.valueObjective)):
                        evolutionInformation = controller.currentLanguage.fermentationPageContent[112]
                    self.temperatureList.insert(position, str(position)+". "+evolutionInformation+eachTemperature.showInformation())
                    position = position + 1
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
        self.potentialHydrogenStatusFileTimeStr = "ControlData/PotentialHydrogen/STATUS_Log/"+str(fileTime.strftime("%Y%m%d_%I%M%S"))+"_POT.txt"
        self.potentialHydrogenDataFileTimeStr = "ControlData/PotentialHydrogen/DATA_Log/"+str(fileTime.strftime("%Y%m%d_%I%M%S"))+"_POT.txt"
        self.potentialHydrogenErrorFileTimeStr = "ControlData/PotentialHydrogen/ERROR_Log/"+str(fileTime.strftime("%Y%m%d_%I%M%S"))+"_POT.txt"
        controller.settingPotentialHydrogenControl[4] = int(self.potentialHydrogenDataFileTimeStr[48:54])
        controller.settingPotentialHydrogenControl[5] = int(self.potentialHydrogenDataFileTimeStr[39:47])
        controller.application.systemCurrentStatus.potentialControlData[0]=str(fileTime.strftime("%Y%m%d_%I%M%S"))+"_POT.txt"
        controller.settingPotentialHydrogenControl[2] = 0
        controller.settingPotentialHydrogenControl[1] = 1
        controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].dataFilenames.append(str(fileTime.strftime("%Y%m%d_%I%M%S")))
        self.isControlInitialized[2] = True
        self.currentLedHandler.configurePotentialLeds(self.isControlInitialized[2])
        currentTime = datetime.today()
        currentTimeStr = currentTime.strftime("%b %d %Y %H:%M:%S.%f")
        self.potentialHydrogenInformation[0]['text'] = controller.currentLanguage.fermentationPageContent[116] + currentTimeStr
        self.potentialHydrogenInformation[1]['text'] = controller.currentLanguage.fermentationPageContent[70]
        self.generalInformation[2]['text'] = controller.currentLanguage.fermentationPageContent[117]
        controller.application.systemCurrentStatus.potentialControlData[2]=self.potentialHydrogenInformation[0]['text']
        controller.application.saveStatusDataToFile()
        self.isMagnitudeListEditable[2] = False
        self.saveMagnitudeControlStatus(self.potentialHydrogenStatusFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[297])

    def runPotentialHydrogenControl(self, controller):
        if(len(controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].magnitudesToControl.potentialsHydrogen)>0 or controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].isPotentialHydrogenControlOnFreeWheel):
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
            self.generalInformation[2]['text'] = controller.currentLanguage.fermentationPageContent[118]
            self.isMagnitudeListEditable[2] = True
            self.saveMagnitudeControlStatus(self.potentialHydrogenStatusFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[298])
        else:
            controller.settingPotentialHydrogenControl[2] = 0
            controller.settingPotentialHydrogenControl[1] = 1
            self.setPotentialHydroControlValues(controller)
            self.potentialHydrogenInformation[1]['text'] = controller.currentLanguage.fermentationPageContent[75]
            self.generalInformation[2]['text'] = controller.currentLanguage.fermentationPageContent[119]
            self.isMagnitudeListEditable[2] = False
            self.saveMagnitudeControlStatus(self.potentialHydrogenStatusFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[299])
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
        controller.settingScreensControl[2] = 6 #Page Status
        controller.settingScreensControl[16] = 0 #Controls Running
        if(controller.settingScreensControl[1] != 1):
            controller.settingScreensControl[1] = 1
        controller.settingPotentialHydrogenControl[1] = 0
        self.isControlInitialized[2] = False
        self.currentLedHandler.configurePotentialLeds(self.isControlInitialized[2])
        controller.settingPotentialHydrogenControl[2] = 1
        currentTime = datetime.today()
        currentTimeStr = currentTime.strftime("%b %d %Y %H:%M:%S.%f")
        self.potentialHydrogenInformation[0]['text'] = controller.currentLanguage.fermentationPageContent[120] + currentTimeStr
        self.potentialHydrogenInformation[1]['text'] = controller.currentLanguage.fermentationPageContent[79]
        self.generalInformation[2]['text'] = controller.currentLanguage.fermentationPageContent[121]
        self.isMagnitudeListEditable[2] = True
        controller.application.systemCurrentStatus.potentialControlData[2]=self.potentialHydrogenInformation[0]['text']
        controller.application.systemCurrentStatus.potentialControlData[3] = self.potentialHydrogenInformation[2]['text']
        controller.application.saveStatusDataToFile()
        self.saveMagnitudeControlStatus(self.potentialHydrogenStatusFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[300])
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
        self.generalInformation[2]['text'] = controller.currentLanguage.fermentationPageContent[123]
        self.saveMagnitudeControlStatus(self.potentialHydrogenStatusFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[301])
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
        self.saveMagnitudeControlStatus(self.potentialHydrogenStatusFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[302])
        if(controller.settingPotentialHydrogenControl[3]<=0):
            self.potentialHydrogenList.itemconfig(0, {'bg':'lime green'})
        else:
            self.potentialHydrogenList.itemconfig(controller.settingPotentialHydrogenControl[3]+1, {'bg':'white'})
            self.potentialHydrogenList.itemconfig(controller.settingPotentialHydrogenControl[3], {'bg':'lime green'})

    def nextStepOnPotentialHydrogenControl(self, controller):
        currentTime = datetime.today()
        currentTimeStr = currentTime.strftime("%b %d %Y %H:%M:%S.%f")
        controller.settingPotentialHydrogenControl[2] = 4
        self.saveMagnitudeControlStatus(self.potentialHydrogenStatusFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[303])
        if(controller.settingPotentialHydrogenControl[3]<len(controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].magnitudesToControl.potentialsHydrogen)):
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
                        self.acidDropsList.append(float(acidDrops))
                    if(float(baseDrops)==0.0):
                        self.baseDropsList.append(0.0)
                    else:
                        self.baseDropsList.append(float(baseDrops))
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

    def checkPotentialHydrogenStatus(self, controller):
        if(self.isControlInitialized[2]):
            self.currentMagnitudesValues[2] = self.updatePotentialHydrogenGraphic(controller)
        self.updatePotentialHydrogenGlobalInformation(controller)
        #self.checkPotentialError(controller)
        currentTime = datetime.today()
        currentTimeStr = currentTime.strftime("%b %d %Y %H:%M:%S.%f")
        if(controller.settingPotentialHydrogenControl[1]!=0):
            #self.setPotentialDisplay(controller, currentPotential)
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
            self.potentialHydrogenList.itemconfig(controller.settingPotentialHydrogenControl[3], {'bg':'white'})
            if(self.isControlInitialized[2]):
                currentTime = datetime.today()
                currentTimeStr = currentTime.strftime("%b %d %Y %H:%M:%S.%f")
                self.potentialHydrogenInformation[0]['text'] = controller.currentLanguage.fermentationPageContent[124] + currentTimeStr
                self.potentialHydrogenInformation[1]['text'] = controller.currentLanguage.fermentationPageContent[88]
                self.generalInformation[2]['text'] = controller.currentLanguage.fermentationPageContent[125]
                self.isControlInitialized[2] = False
                #self.potentialHydrogenList.itemconfig(controller.settingPotentialHydrogenControl[3], {'bg':'white'})
                self.saveMagnitudeControlStatus(self.potentialHydrogenStatusFileTimeStr, currentTimeStr+" - "+controller.currentLanguage.fermentationPageContent[304])
        controller.application.loadStatusDataFromFile()
        controller.application.systemCurrentStatus.potentialControlData[3] = self.potentialHydrogenInformation[2]['text']
        if(controller.application.systemCurrentStatus.potentialControlData[1]=="0"):
            print("Pot Sin Arrancar")
        if(controller.application.systemCurrentStatus.potentialControlData[1]=="1" and not self.isControlInitialized[2]):
            self.runPotential(controller)
            print("Pot EJECUTANDOSE")
        if(controller.application.systemCurrentStatus.potentialControlData[1]=="2" and self.isControlInitialized[2]):
            self.pausePotentialControl(controller)
            print("Pot PAUSADO")
        if(controller.application.systemCurrentStatus.potentialControlData[1]=="3" and self.isControlInitialized[2]):
            self.stopPotential(controller)
            print("Pot DETENIDO")
        if(controller.application.systemCurrentStatus.potentialControlData[1]=="6" and self.isControlInitialized[2]):
            self.restartPotentialHydrogenControl(controller)
            controller.application.systemCurrentStatus.potentialControlData[1]=="1"
            print("Pot REINICIADA")
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
                    elif(float(potentials[position-2].valueObjective)>float(eachPotential.valueObjective)):
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
        velocityCustomizationBorder = Label(pageCustomization, bg = self.colorORT, height=22, width=75, borderwidth=2, relief='solid', highlightbackground='blue')
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
        temperatureCustomizationBorder = Label(pageCustomization, bg = self.colorORT, height=12, width=160, borderwidth=2, relief='solid', highlightbackground='orange')
        temperatureCustomizationBorder.place(x=150, y=360)
        self.temperatureCustomizationTitle = Label(pageCustomization, text=controller.currentLanguage.fermentationPageContent[142], font=self.titleFont, fg = 'orange', bg = self.colorORT)
        self.temperatureCustomizationTitle.place(x=155, y=380)
        self.pumpStepTitle = Label(pageCustomization, text=controller.currentLanguage.fermentationPageContent[158], font=self.statusFont, fg = 'orange', bg = self.colorORT)
        self.pumpStepTitle.place(x=1025, y=480)
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
        self.customizationInformation[7].place(x=1180, y=480)
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
        print("self.customizationInformation[1].get(): ", self.customizationInformation[1].get())
        return (self.customizationInformation[0].get()=="rpm" or self.customizationInformation[0].get()=="m/s" or self.customizationInformation[0].get()=="rad/s") and ("CLK" in self.customizationInformation[3].get() or "AntiCLK" in self.customizationInformation[3].get()=="|-> AntiCLK |->") and (float(self.customizationInformation[1].get())>=1 and float(self.customizationInformation[1].get())<=10) and (self.customizationInformation[2].get()=="Nominal" or self.customizationInformation[2].get()=="Slow" or self.customizationInformation[2].get()=="Very Slow") and (int(self.customizationInformation[4].get())>=5 and int(self.customizationInformation[4].get())<=20)

    def isTemperatureCustomizationRight(self):
        return (self.customizationInformation[5].get()=="°C (Celsius)" or self.customizationInformation[5].get()=="K (Kelvin)" or self.customizationInformation[5].get()=="°F (Fahrenheit)") and (float(self.customizationInformation[6].get())>=0.1 and float(self.customizationInformation[6].get())<=2) and (float(self.customizationInformation[7].get())>=1 and float(self.customizationInformation[7].get())<=5) and (self.customizationInformation[8].get()=="Nominal" or self.customizationInformation[8].get()=="Fast" or self.customizationInformation[8].get()=="Super Fast") and (int(self.customizationInformation[9].get())>=5 and int(self.customizationInformation[9].get())<=20)

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
        self.temperatureCustomizationInformation = [self.customizationInformation[5].get(), float(self.customizationInformation[6].get()), int(self.customizationInformation[7].get()), self.customizationInformation[8].get(), int(self.customizationInformation[9].get())]

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

    def configureCustomizationVelocity(self, controller):
        if(self.isVelocityCustomizationRight()):
            self.configureVelocityCustomization(controller)
            messagebox.showinfo(controller.currentLanguage.fermentationPageContent[168], controller.currentLanguage.fermentationPageContent[169])
        else:
            messagebox.showerror(controller.currentLanguage.fermentationPageContent[168], controller.currentLanguage.fermentationPageContent[170])

    def configureCustomizationTemperature(self, controller):
        if(self.isTemperatureCustomizationRight()):
            self.configureTemperatureCustomization(controller)
            messagebox.showinfo(controller.currentLanguage.fermentationPageContent[168], controller.currentLanguage.fermentationPageContent[169])
        else:
            messagebox.showerror(controller.currentLanguage.fermentationPageContent[168], controller.currentLanguage.fermentationPageContent[170])

    def configureCustomizationPotential(self, controller):
        if(self.isPotentialHydrogenCustomizationRight()):
            self.configurePotentialHydrogenCustomization(controller)
            messagebox.showinfo(controller.currentLanguage.fermentationPageContent[168], controller.currentLanguage.fermentationPageContent[169])
        else:
            messagebox.showerror(controller.currentLanguage.fermentationPageContent[168], controller.currentLanguage.fermentationPageContent[170])

    def configureCustomization(self, controller): # SEPARADO EN 3 (Velocity, Temperature y Potential)
        if(self.isCustomizationRight()):
            self.configureVelocityCustomization(controller)
            self.configureTemperatureCustomization(controller)
            self.configurePotentialHydrogenCustomization(controller)
            messagebox.showinfo(controller.currentLanguage.fermentationPageContent[168], controller.currentLanguage.fermentationPageContent[169])
        else:
            messagebox.showerror(controller.currentLanguage.fermentationPageContent[168], controller.currentLanguage.fermentationPageContent[170])

    def setPageCustomizationButtons(self, pageCustomization, controller):
        self.configureNewCustomizationVelocity = Button(pageCustomization, text=controller.currentLanguage.fermentationPageContent[157], command=lambda:self.configureCustomizationVelocity(controller), relief = RAISED, fg='white', bg = 'blue', font=self.buttonFont, compound=CENTER, height = 2, width = 20)
        self.configureNewCustomizationVelocity.place(x=400, y=10)
        self.configureNewCustomizationTemperature = Button(pageCustomization, text=controller.currentLanguage.fermentationPageContent[157], command=lambda:self.configureCustomizationTemperature(controller), relief = RAISED, fg='white', bg = 'orange', font=self.buttonFont, compound=CENTER, height = 2, width = 20)
        self.configureNewCustomizationTemperature.place(x=1020, y=370)
        self.configureNewCustomizationPotential = Button(pageCustomization, text=controller.currentLanguage.fermentationPageContent[157], command=lambda:self.configureCustomizationPotential(controller), relief = RAISED, fg='white', bg = 'green4', font=self.buttonFont, compound=CENTER, height = 2, width = 20)
        self.configureNewCustomizationPotential.place(x=1020, y=10)

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
        self.updateGlobalGraphics(controller)

    def getCurrentUserGamesScores(self, controller):
        if(controller.application.systemCurrentStatus.isUserLogged[1]):
            return controller.application.listStudents.students[controller.application.systemCurrentStatus.userLogged].gamesScore
        else:
            return controller.application.listProfessors.professors[controller.application.systemCurrentStatus.userLogged].gamesScore

    def fillWithGamesInformation(self, pageEntertainment, controller):
        self.informationTitle = Label(pageEntertainment, text=controller.currentLanguage.fermentationPageContent[133], font=self.gameTitleFont, fg = 'chocolate3', bg = self.colorORT)
        self.informationTitle.place(x=910, y=10)
        gamesInformation = controller.currentLanguage.fermentationPageContent[189] #ALL GAMES info
        self.allGamesInfo = Label(pageEntertainment, text=gamesInformation, font=self.infoFont, fg = 'chocolate3', bg = self.colorORT, justify=LEFT, bd=2, relief='groove', highlightbackground='white')
        self.allGamesInfo.place(x=855, y=55)

        currentGamesScores = self.getCurrentUserGamesScores(controller)
        self.currentGameStatus.append(Label(pageEntertainment, text=controller.currentLanguage.fermentationPageContent[182]+str(currentGamesScores[0])+controller.currentLanguage.fermentationPageContent[183], font=self.infoFont, fg = 'chocolate3', bg = self.colorORT, justify=LEFT, bd=2, relief='groove', highlightbackground='white', width=60))
        self.currentGameStatus[0].place(x=710, y=180)
        self.currentGameStatus.append(Label(pageEntertainment, text=controller.currentLanguage.fermentationPageContent[184]+str(currentGamesScores[1])+controller.currentLanguage.fermentationPageContent[185], font=self.infoFont, fg = 'chocolate3', bg = self.colorORT, justify=LEFT, bd=2, relief='groove', highlightbackground='white', width=60))
        self.currentGameStatus[1].place(x=710, y=205)
        self.currentGameStatus.append(Label(pageEntertainment, text=controller.currentLanguage.fermentationPageContent[186]+str(currentGamesScores[2])+controller.currentLanguage.fermentationPageContent[187], font=self.infoFont, fg = 'chocolate3', bg = self.colorORT, justify=LEFT, bd=2, relief='groove', highlightbackground='white', width=60))
        self.currentGameStatus[2].place(x=710, y=230)

        self.scrambledGameRecord = Label(pageEntertainment, text=controller.currentLanguage.fermentationPageContent[199]+"0"+controller.currentLanguage.fermentationPageContent[197], font=self.infoFont, fg = 'DodgerBlue3', bg = self.colorORT, justify=LEFT, bd=2, relief='groove', highlightbackground='white', width=59)
        self.scrambledGameRecord.place(x=140, y=175)
        self.hangmanGameRecord = Label(pageEntertainment, text=controller.currentLanguage.fermentationPageContent[201]+"0"+controller.currentLanguage.fermentationPageContent[197], font=self.infoFont, fg = 'lime green', bg = self.colorORT, justify=LEFT, bd=2, relief='groove', highlightbackground='white', width=59)
        self.hangmanGameRecord.place(x=140, y=455)
        self.triviaGameRecord = Label(pageEntertainment, text=controller.currentLanguage.fermentationPageContent[203]+"0"+controller.currentLanguage.fermentationPageContent[197], font=self.infoFont, fg = 'indian red', bg = self.colorORT, justify=LEFT, bd=2, relief='groove', highlightbackground='white', width=59)
        self.triviaGameRecord.place(x=710, y=455)

        #dodgerGameRecord = Label(pageEntertainment, text=controller.currentLanguage.fermentationPageContent[188], font=self.infoFont, fg = 'DodgerBlue3', bg = self.colorORT, justify=LEFT, bd=2, relief='groove', highlightbackground='white', width=59)
        #dodgerGameRecord.place(x=140, y=175)
        #memoryGameRecord = Label(pageEntertainment, text=controller.currentLanguage.fermentationPageContent[188], font=self.infoFont, fg = 'lime green', bg = self.colorORT, justify=LEFT, bd=2, relief='groove', highlightbackground='white', width=59)
        #memoryGameRecord.place(x=140, y=455)
        #nibblesGameRecord = Label(pageEntertainment, text=controller.currentLanguage.fermentationPageContent[188], font=self.infoFont, fg = 'indian red', bg = self.colorORT, justify=LEFT, bd=2, relief='groove', highlightbackground='white', width=59)
        #nibblesGameRecord.place(x=710, y=455)
        #gamesImage = Label(pageEntertainment, text="IMAGE", font=self.infoFont, fg = 'chocolate3', bg = self.colorORT, bd=2, relief='groove', highlightbackground='white', height=6, width=14)
        #gamesImage.place(x=710, y=55)

    def fillWithDodgerInformation(self, pageEntertainment, controller):
        dodgerTitle = Label(pageEntertainment, text="_-_-_-_-_-_- DODGER -_-_-_-_-_-_", font=self.gameTitleFont, fg = 'DodgerBlue3', bg = self.colorORT)
        dodgerTitle.place(x=140, y=10)
        dodgerInformation = controller.currentLanguage.fermentationPageContent[171] #DODGER info
        dodgerGameInfo = Label(pageEntertainment, text=dodgerInformation, font=self.infoFont, fg = 'DodgerBlue3', bg = self.colorORT, justify=LEFT, bd=2, relief='groove', highlightbackground='white')
        dodgerGameInfo.place(x=280, y=55)
        #dodgerImage = Label(pageEntertainment, text="IMAGE", font=self.infoFont, fg = 'DodgerBlue3', bg = self.colorORT, bd=2, relief='groove', highlightbackground='white', height=6, width=14)
        #dodgerImage.place(x=140, y=55)

    def fillWithMemoryInformation(self, pageEntertainment, controller):
        memoryTitle = Label(pageEntertainment, text="_-_-_-_-_-_- MEMORY -_-_-_-_-_-_", font=self.gameTitleFont, fg = 'lime green', bg = self.colorORT)
        memoryTitle.place(x=135, y=290)
        memoryInformation = controller.currentLanguage.fermentationPageContent[172] #MEMORY info
        memoryGameInfo = Label(pageEntertainment, text=memoryInformation, font=self.infoFont, fg = 'lime green', bg = self.colorORT, justify=LEFT, bd=2, relief='groove', highlightbackground='white')
        memoryGameInfo.place(x=280, y=335)
        memoryImage = Label(pageEntertainment, text="IMAGE", font=self.infoFont, fg = 'lime green', bg = self.colorORT, bd=2, relief='groove', highlightbackground='white', height=6, width=14)
        memoryImage.place(x=140, y=335)

    def fillWithNibblesInformation(self, pageEntertainment, controller):
        nibblesTitle = Label(pageEntertainment, text="_-_-_-_-_-_- NIBBLES -_-_-_-_-_-_", font=self.gameTitleFont, fg = 'indian red', bg = self.colorORT)
        nibblesTitle.place(x=705, y=290)
        nibblesInformation = controller.currentLanguage.fermentationPageContent[173] #NIBBLES info
        nibblesGameInfo = Label(pageEntertainment, text=nibblesInformation, font=self.infoFont, fg = 'indian red', bg = self.colorORT, justify=LEFT, bd=2, relief='groove', highlightbackground='white')
        nibblesGameInfo.place(x=855, y=335)
        #nibblesImage = Label(pageEntertainment, text="IMAGE", font=self.infoFont, fg = 'indian red', bg = self.colorORT, bd=2, relief='groove', highlightbackground='white', height=6, width=14)
        #nibblesImage.place(x=710, y=335)

    def fillWithScrambledInformation(self, pageEntertainment, controller):
        scrambledTitle = Label(pageEntertainment, text="-_-_-_-_-_- SCRAMBLED -_-_-_-_-_-", font=self.gameTitleFont, fg = 'DodgerBlue3', bg = self.colorORT)
        scrambledTitle.place(x=140, y=10)
        scrambledInformation = controller.currentLanguage.fermentationPageContent[174] #SCRAMBLED info
        self.scrambledGameInfo = Label(pageEntertainment, text=scrambledInformation, font=self.infoFont, fg = 'DodgerBlue3', bg = self.colorORT, justify=LEFT, bd=2, relief='groove', highlightbackground='white')
        self.scrambledGameInfo.place(x=280, y=55)

    def fillWithHangmanInformation(self, pageEntertainment, controller):
        hangmanTitle = Label(pageEntertainment, text="-_-_-_-_-_- HANGMAN -_-_-_-_-_-", font=self.gameTitleFont, fg = 'lime green', bg = self.colorORT)
        hangmanTitle.place(x=135, y=290)
        hangmanInformation = controller.currentLanguage.fermentationPageContent[175] #HANGMAN info
        self.hangmanGameInfo = Label(pageEntertainment, text=hangmanInformation, font=self.infoFont, fg = 'lime green', bg = self.colorORT, justify=LEFT, bd=2, relief='groove', highlightbackground='white')
        self.hangmanGameInfo.place(x=280, y=335)

    def fillWithTriviaInformation(self, pageEntertainment, controller):
        triviaTitle = Label(pageEntertainment, text="-_-_-_-_-_-_- TRIVIA -_-_-_-_-_-_-", font=self.gameTitleFont, fg = 'indian red', bg = self.colorORT)
        triviaTitle.place(x=705, y=290)
        triviaInformation = controller.currentLanguage.fermentationPageContent[231] #TRIVIA info
        self.triviaGameInfo = Label(pageEntertainment, text=triviaInformation, font=self.infoFont, fg = 'indian red', bg = self.colorORT, justify=LEFT, bd=2, relief='groove', highlightbackground='white')
        self.triviaGameInfo.place(x=855, y=335)

    def fillPageEntertainmentInformation(self, pageEntertainment, controller):
        #self.fillWithDodgerInformation(pageEntertainment, controller)
        #self.fillWithMemoryInformation(pageEntertainment, controller)
        #self.fillWithNibblesInformation(pageEntertainment, controller)
        self.fillWithScrambledInformation(pageEntertainment, controller)
        self.fillWithHangmanInformation(pageEntertainment, controller)
        self.fillWithTriviaInformation(pageEntertainment, controller)

    def setImagesOfPrimaryGames(self, pageEntertainment):
        scrambledLogo = Picture(['scrambledGameLogo','png',130,110,140,55],0)
        scrambledLogo.purpose = 'GamesPic'
        scrambledLogoPic = scrambledLogo.generateLabel(pageEntertainment)
        scrambledLogoPic.config(bd=5, relief='groove', highlightbackground='white')
        scrambledLogoPic.place(x=scrambledLogo.location[0],y=scrambledLogo.location[1])

        hangmanLogo = Picture(['hangmanGameLogo','png',130,110,140,335],0)
        hangmanLogo.purpose = 'GamesPic'
        hangmanLogoPic = hangmanLogo.generateLabel(pageEntertainment)
        hangmanLogoPic.config(bd=5, relief='groove', highlightbackground='white')
        hangmanLogoPic.place(x=hangmanLogo.location[0],y=hangmanLogo.location[1])

        triviaLogo = Picture(['triviaGameLogo','png',130,110,710,335],0)
        triviaLogo.purpose = 'GamesPic'
        triviaLogoPic = triviaLogo.generateLabel(pageEntertainment)
        triviaLogoPic.config(bd=5, relief='groove', highlightbackground='white')
        triviaLogoPic.place(x=triviaLogo.location[0],y=triviaLogo.location[1])

        gamesInfoLogo = Picture(['smartGameInfo','png',120,120,710,55],0)
        gamesInfoLogo.purpose = 'Logos'
        gamesInfoLogoPic = gamesInfoLogo.generateLabel(pageEntertainment)
        gamesInfoLogoPic.place(x=gamesInfoLogo.location[0],y=gamesInfoLogo.location[1])

    def setImagesOfSecondaryGames(self, pageEntertainment):
        dodgerLogo = Picture(['dodgerGameLogo','png',130,110,140,55],0)
        dodgerLogo.purpose = 'GamesPic'
        dodgerLogoPic = dodgerLogo.generateLabel(pageEntertainment)
        dodgerLogoPic.config(bd=5, relief='groove', highlightbackground='white')
        dodgerLogoPic.place(x=dodgerLogo.location[0],y=dodgerLogo.location[1])

        nibblesLogo = Picture(['nibblesGameLogo','png',130,110,710,335],0)
        nibblesLogo.purpose = 'GamesPic'
        nibblesLogoPic = nibblesLogo.generateLabel(pageEntertainment)
        nibblesLogoPic.config(bd=5, relief='groove', highlightbackground='white')
        nibblesLogoPic.place(x=nibblesLogo.location[0],y=nibblesLogo.location[1])

        gamesInfoLogo = Picture(['smartGameInfo','png',120,120,710,55],0)
        gamesInfoLogo.purpose = 'Logos'
        gamesInfoLogoPic = gamesInfoLogo.generateLabel(pageEntertainment)
        gamesInfoLogoPic.place(x=gamesInfoLogo.location[0],y=gamesInfoLogo.location[1])

    def fillPageEntertainmentImages(self, pageEntertainment, controller):
        controller.setImagesandSeparators(pageEntertainment, 'playGamesElement', [115,270,10,10,115,270,10,300])
        controller.setImagesandSeparators(pageEntertainment, 'playGamesElement', [115,270,1250,10,115,270,1250,300])
        self.setImagesOfPrimaryGames(pageEntertainment)
        #self.setImagesOfSecondaryGames(pageEntertainment)

    def fillPageEntertainmentButtons(self, pageEntertainment, controller):
        self.entertainmentToDisplay = EntertainmentDisplay(self)
        self.playScramblerOption = Button(pageEntertainment, text=controller.currentLanguage.fermentationPageContent[230], command=lambda:self.entertainmentToDisplay.playScrambled(controller), relief = SUNKEN, fg='white', bg = 'DodgerBlue3', font=self.gameFont, compound=CENTER, height = 2, width = 41)
        self.playScramblerOption.place(x=140, y=200)
        self.entertainmentToDisplay.configureInitialScrambledGame(controller)

        self.playHangmanOption = Button(pageEntertainment, text=controller.currentLanguage.fermentationPageContent[230], command=lambda:self.entertainmentToDisplay.playHangman(controller), relief = SUNKEN, fg='white', bg = 'lime green', font=self.gameFont, compound=CENTER, height = 2, width = 41)
        self.playHangmanOption.place(x=140, y=480)
        self.entertainmentToDisplay.configureInitialHangmanGame(controller)

        #self.triviaCorrectAnswerPic = Label(self.triviaCanvas, borderwidth=0, highlightthickness=0)
        #self.triviaWrongAnswerPic = Label(self.triviaCanvas, borderwidth=0, highlightthickness=0)
        self.playTriviaOption = Button(pageEntertainment, text=controller.currentLanguage.fermentationPageContent[230], command=lambda:self.entertainmentToDisplay.playTrivia(controller), relief = SUNKEN, fg='white', bg = 'indian red', font=self.gameFont, compound=CENTER, height = 2, width = 41)
        self.playTriviaOption.place(x=710, y=480)
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
        controller.settingPotentialHydrogenControl[0] = 0
        time.sleep(1)

    def onClosing(self, controller):
        if messagebox.askokcancel(controller.currentLanguage.adminPageContent[21], controller.currentLanguage.adminPageContent[20]):
            controller.application.updateFermentationControlsData()
            controller.application.listFermentations.fermentations[controller.application.systemCurrentStatus.fermentationActual].isFermentationContinuing = False
            controller.application.saveSmartData("")
            self.currentLedHandler.setErrorFixed()

            self.stopVelocity(controller)
            self.stopTemperature(controller)
            self.stopPotential(controller)
            time.sleep(2)

            self.closeAllControlProcesses(controller)
            self.fadeAway(controller)

    def setTabs(self, controller):
        self.pageSystem = Frame(self.nb)
        self.nb.add(self.pageSystem, text=controller.currentLanguage.fermentationPageContent[3])
        controller.setBackgroundOfTab(self.pageSystem)
        self.fillPageSystem(self.pageSystem, controller)
        self.pageGlobal = Frame(self.nb)
        self.nb.add(self.pageGlobal, text=controller.currentLanguage.fermentationPageContent[4])
        controller.setBackgroundOfTab(self.pageGlobal)
        self.fillPageGlobal(self.pageGlobal, controller)
        self.pageFreeWheel = Frame(self.nb)
        self.nb.add(self.pageFreeWheel, text=controller.currentLanguage.fermentationPageContent[10])
        controller.setBackgroundOfTab(self.pageFreeWheel)
        self.fillPageFreeWheel(self.pageFreeWheel, controller)
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
        self.pageCustomization = Frame(self.nb)
        self.nb.add(self.pageCustomization, text=controller.currentLanguage.fermentationPageContent[8])
        controller.setBackgroundOfTab(self.pageCustomization)
        self.fillPageCustomization(self.pageCustomization, controller)
        self.pageErrors = Frame(self.nb)
        self.nb.add(self.pageErrors, text=controller.currentLanguage.fermentationPageContent[160])
        controller.setBackgroundOfTab(self.pageErrors)
        self.fillPageErrors(self.pageErrors, controller)
        self.pageEntertainment = Frame(self.nb)
        self.nb.add(self.pageEntertainment, text=controller.currentLanguage.fermentationPageContent[9])
        controller.setBackgroundOfTab(self.pageEntertainment)
        self.fillPageEntertainment(self.pageEntertainment, controller)

    def updateProcessPorts(self, controller, portIndicator, selectedPort):
        portCount = 0
        for eachPort in self.portsPossibilities:
            if(controller.application.systemCurrentStatus.currentControlPorts[selectedPort]==eachPort):
                portIndicator = portCount + 1
            portCount = portCount + 1

    def updateAllProcessPorts(self, controller):
        self.portsPossibilities = ["/dev/ttyACM0", "/dev/ttyACM1", "/dev/ttyACM2", "/dev/ttyACM3", "/dev/ttyUSB0", "/dev/ttyUSB1", "/dev/ttyUSB2", "/dev/ttyUSB3", "/dev/ttyAMA0", "/dev/ttyAMA1"]
        self.updateProcessPorts(controller, controller.settingVelocityControl[21], 0)
        self.updateProcessPorts(controller, controller.settingTemperatureControl[21], 1)
        self.updateProcessPorts(controller, controller.settingPotentialHydrogenControl[21], 2)
        self.updateProcessPorts(controller, controller.settingVelocityControl[22], 3)
        self.updateProcessPorts(controller, controller.settingTemperatureControl[22], 4)
        self.updateProcessPorts(controller, controller.settingScreensControl[22], 5)

    def initializeSystemStatus(self, controller):
        controller.application.systemCurrentStatus.velocityControlData[1] = "0"
        controller.application.systemCurrentStatus.temperatureControlData[1] = "0"
        controller.application.systemCurrentStatus.potentialControlData[1] = "0"
        controller.application.saveStatusDataToFile()

    def __init__(self, parent, controller):

        Frame.__init__(self, parent)
        #controller.application.systemCurrentStatus.fermentationActual = 0 #CUIDADO
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
        self.initializeSystemStatus(controller)

        rows = 0
        while rows < 50:
            self.rowconfigure(rows, weight=1)
            self.columnconfigure(rows, weight=1)
            rows = rows + 1

        self.updateAllProcessPorts(controller)
        self.currentLedHandler = LedHandler()
        self.nb = ttk.Notebook(self)
        self.nb.grid(row=10, column=0, columnspan=500, rowspan=490, sticky='NESW')
        self.setTabs(controller)
        self.checkMagnitudesStatus(controller)
        self.setHelpBar(controller)
