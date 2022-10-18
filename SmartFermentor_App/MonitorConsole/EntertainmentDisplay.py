import sys, time
from datetime import datetime, date, timedelta
from tkinter import *
from tkinter import ttk, messagebox
import tkinter.font
from PIL import Image, ImageTk
from MonitorConsole.Picture import Picture
from MonitorConsole.OriginalLanguage import OriginalLanguage
from MonitorConsole.SpanishLanguage import SpanishLanguage
from MonitorConsole.PortugueseLanguage import PortugueseLanguage
from MonitorConsole.GermanLanguage import GermanLanguage

class EntertainmentDisplay():

    def __init__(self, mainWindow):
        self.extensions = [466, 268]
        self.colorORT = "#085454"
        self.superTitleFont = tkinter.font.Font(family = 'Helvetica', size = 48, weight = 'bold')
        self.titleFont = tkinter.font.Font(family = 'Helvetica', size = 20, weight = 'bold')
        self.subtitleFont = tkinter.font.Font(family = 'Comic Sans', size = 16, weight = 'bold')
        self.gameFont = tkinter.font.Font(family = 'Comic Sans MS', size = 16, weight = 'bold')
        self.gameTitleFont = tkinter.font.Font(family = 'Comic Sans MS', size = 20, weight = 'bold')
        self.hangmanFont = tkinter.font.Font(family = 'Comic Sans MS', size = 24, weight = 'bold')
        self.buttonFont = tkinter.font.Font(family = 'Helvetica', size = 14, weight = 'bold')
        self.currentWindow = mainWindow #CUIDADO
        self.scrambledCanvas = Canvas(mainWindow, background=self.colorORT, width= 890+self.extensions[0], height= 320+self.extensions[1], highlightthickness=5, highlightbackground='white')
        self.scrambledPic = Label(self.scrambledCanvas, borderwidth=0, highlightthickness=0)

        self.hangmanCanvas = Canvas(mainWindow, background=self.colorORT, width= 890+self.extensions[0], height= 320+self.extensions[1], highlightthickness=5, highlightbackground='white')
        self.hangmanPic = Label(self.hangmanCanvas, borderwidth=0, highlightthickness=0)

        self.triviaCanvas = Canvas(mainWindow, background=self.colorORT, width= 890+self.extensions[0], height= 320+self.extensions[1], highlightthickness=5, highlightbackground='white')
        self.triviaLeftPic = Label(self.triviaCanvas, borderwidth=0, highlightthickness=0)
        self.triviaRightPic = Label(self.triviaCanvas, borderwidth=0, highlightthickness=0)
        self.triviaOptionSelection = [IntVar(), IntVar(), IntVar(), IntVar()]
        self.gamesDisplayed = [False, False, False]
        self.isGameSolutionShown = [False, False, False]
        self.gameSessionScore = [0, 0, 0]
        self.triviaGameEnded = False
        self.questionsAnswered = 0

    def addPointsToGame(self, controller, pointsToAdd, gameNumber):
        if(self.gamePointsMultiplier <= 4):
            self.gamePointsMultiplier = self.gamePointsMultiplier * 2
        self.gameSessionScore[gameNumber] = self.gameSessionScore[gameNumber] + self.gamePointsMultiplier*pointsToAdd
        self.updatePointsInformation(controller)

    def checkPointsToAdd(self, controller, gameNumber):
        timeUsed = date.today() - self.timeForGames
        pointsToAdd = 5*60 - timeUsed.seconds
        if(pointsToAdd>0):
            self.addPointsToGame(controller, pointsToAdd, gameNumber)

    def updateRecordData(self, controller, gameNumber):
        if(controller.application.systemCurrentStatus.isUserLogged[1]):
            userLogged = controller.application.listStudents.students[controller.application.systemCurrentStatus.userLogged]
        else:
            userLogged = controller.application.listProfessors.professors[controller.application.systemCurrentStatus.userLogged]
        if(gameNumber==0):
            if(controller.application.gamesEntertainment.scrambledData.isScoreOnePersonalRecord(userLogged, gameNumber, self.gamesSessionScore[gameNumber])):
                userLogged.gamesScore[0] = self.gamesSessionScore[0]
            controller.application.gamesEntertainment.scrambledData.setRecordData(userLogged, gameNumber)
        if(gameNumber==1):
            if(controller.application.gamesEntertainment.hangmanData.isScoreOnePersonalRecord(userLogged, gameNumber, self.gamesSessionScore[gameNumber])):
                userLogged.gamesScore[1] = self.gamesSessionScore[1]
            controller.application.gamesEntertainment.hangmanData.setRecordData(userLogged, gameNumber)
        if(gameNumber==2):
            if(controller.application.gamesEntertainment.triviaData.isScoreOnePersonalRecord(userLogged, gameNumber, self.gamesSessionScore[gameNumber])):
                userLogged.gamesScore[2] = self.gamesSessionScore[2]
            controller.application.gamesEntertainment.triviaData.setRecordData(userLogged, gameNumber)

    def updateDisplayInformation(self, controller):
        self.currentWindow.scrambledGameRecord.config(text=controller.currentLanguage.fermentationPageContent[199]+str(self.gameSessionScore[0])+controller.currentLanguage.fermentationPageContent[197])
        self.currentWindow.hangmanGameRecord.config(text=controller.currentLanguage.fermentationPageContent[201]+str(self.gameSessionScore[1])+controller.currentLanguage.fermentationPageContent[197])
        self.currentWindow.triviaGameRecord.config(text=controller.currentLanguage.fermentationPageContent[203]+str(self.gameSessionScore[2])+controller.currentLanguage.fermentationPageContent[197])
        currentGamesScores = self.currentWindow.getCurrentUserGamesScores(controller)
        self.currentWindow.currentGameStatus[0].config(text=controller.currentLanguage.fermentationPageContent[182]+str(currentGamesScores[0])+controller.currentLanguage.fermentationPageContent[183])
        self.currentWindow.currentGameStatus[1].config(text=controller.currentLanguage.fermentationPageContent[184]+str(currentGamesScores[1])+controller.currentLanguage.fermentationPageContent[185])
        self.currentWindow.currentGameStatus[2].config(text=controller.currentLanguage.fermentationPageContent[186]+str(currentGamesScores[2])+controller.currentLanguage.fermentationPageContent[187])

    def updatePointsInformation(self, controller): #NO SE USA
        self.currentPointsScrambled['text'] = controller.currentLanguage.fermentationPageContent[204]+" "+str(self.gameSessionScore[0])
        self.currentPointsHangman['text'] = controller.currentLanguage.fermentationPageContent[204]+" "+str(self.gameSessionScore[1])
        self.currentPointsTrivia['text'] = controller.currentLanguage.fermentationPageContent[204]+" "+str(self.gameSessionScore[2])

###################### SCRAMBLED HANDLING ##########################

    def setPictureForScrambled(self, controller):
        controller.setImagesandSeparators(self.scrambledCanvas, 'scrambledElement', [100,250,10,10,100,250,10,320])
        controller.setImagesandSeparators(self.scrambledCanvas, 'scrambledElement', [100,250,1240,10,100,250,1240,320])
        scrambledIdentifier = Picture([controller.application.gamesEntertainment.scrambledData.getSelectedImageName(),'png',500,400,130,100],0)
        scrambledIdentifier.purpose = 'GamesPic/ScrambledPic'
        scrambledImage = Image.open(scrambledIdentifier.getCompleteFilename())
        scrambledImageRendered = ImageTk.PhotoImage(scrambledImage.rotate(scrambledIdentifier.orientation))
        self.scrambledPic.config(image = scrambledImageRendered)
        self.scrambledPic.image = scrambledImageRendered
        self.scrambledPic.place(x=scrambledIdentifier.location[0],y=scrambledIdentifier.location[1])

    def setEntriesForScrambled(self, controller, scrambledWords):
        self.currentPointsScrambled = Label(self.scrambledCanvas, text=controller.currentLanguage.fermentationPageContent[204]+" "+str(self.gameSessionScore[0]), font=self.titleFont, fg='white', bg=self.colorORT)
        self.currentPointsScrambled.place(x=200,y=10)
        self.wordScrambledOrganism = Label(self.scrambledCanvas, text=controller.currentLanguage.fermentationPageContent[205]+" "+scrambledWords[0], font=self.buttonFont, fg='white', bg=self.colorORT)
        self.wordScrambledOrganism.place(x=710,y=40)
        self.wordScrambledFamily = Label(self.scrambledCanvas, text=controller.currentLanguage.fermentationPageContent[206]+" "+scrambledWords[1], font=self.buttonFont, fg='white', bg=self.colorORT)
        self.wordScrambledFamily.place(x=710,y=260)
        self.wordOrganismTitle = Label(self.scrambledCanvas, text=controller.currentLanguage.fermentationPageContent[207]+" ", font=self.titleFont, fg='white', bg=self.colorORT)
        self.wordOrganismTitle.place(x=680,y=90)
        self.wordFamilyTitle = Label(self.scrambledCanvas, text=controller.currentLanguage.fermentationPageContent[207]+" ", font=self.titleFont, fg='white', bg=self.colorORT)
        self.wordFamilyTitle.place(x=680,y=310)
        self.wordOrganismTyped = Entry(self.scrambledCanvas, font=self.titleFont, fg=self.colorORT, width=20, justify='center', state='normal')
        self.wordOrganismTyped.place(x=780,y=90)
        self.wordFamilyTyped = Entry(self.scrambledCanvas, font=self.titleFont, fg=self.colorORT, width=20, justify='center', state='normal')
        self.wordFamilyTyped.place(x=780,y=310)
        self.solutionOrganismTyped = Label(self.scrambledCanvas, font=self.superTitleFont, bg=self.colorORT)
        self.solutionOrganismTyped.place(x=730,y=145)
        self.solutionFamilyTyped = Label(self.scrambledCanvas, font=self.superTitleFont, bg=self.colorORT)
        self.solutionFamilyTyped.place(x=730,y=360)

    def showScrambledSolution(self, controller):
        solutionsScrambled = controller.application.gamesEntertainment.scrambledData.getScrambledSolutionWords()
        self.wordOrganismTyped.delete(0, END)
        self.wordOrganismTyped.insert(0, solutionsScrambled[0])
        self.wordOrganismTyped.config(state='disabled')
        self.wordFamilyTyped.delete(0, END)
        self.wordFamilyTyped.insert(0, solutionsScrambled[1])
        self.wordFamilyTyped.config(state='disabled')
        self.isGameSolutionShown[0] = True

    def checkOrganismAnswer(self, controller):
        if(controller.application.gamesEntertainment.scrambledData.verifyOrganismsEntry(self.wordOrganismTyped.get())):
            self.solutionOrganismTyped['text'] = "OK!"
            self.solutionOrganismTyped['fg'] = 'green4'
            self.wordOrganismTyped.config(state='disabled')
            self.checkPointsToAdd(controller, 0)
        else:
            self.solutionOrganismTyped['text'] = "X"
            self.solutionOrganismTyped['fg'] = 'red'
            self.gamePointsMultiplier = 1

    def checkFamilyAnswer(self, controller):
        if(controller.application.gamesEntertainment.scrambledData.verifyFamiliesEntry(self.wordFamilyTyped.get())):
            self.solutionFamilyTyped['text'] = "OK!"
            self.solutionFamilyTyped['fg'] = 'green4'
            self.wordFamilyTyped.config(state='disabled')
            self.checkPointsToAdd(controller, 0)
        else:
            self.solutionFamilyTyped['text'] = "X"
            self.solutionFamilyTyped['fg'] = 'red'
            self.gamePointsMultiplier = 1

    def setButtonsForScrambled(self, controller):
        self.nextScrambledWord = Button(self.scrambledCanvas, text=controller.currentLanguage.fermentationPageContent[208], command=lambda:self.configureNextScrambledGame(controller), relief = SUNKEN, fg='white', bg = 'gold4', font=self.gameFont, compound=CENTER, height = 16, width = 3)
        self.nextScrambledWord.place(x=1150, y=50)
        self.solutionScrambledWord = Button(self.scrambledCanvas, text=controller.currentLanguage.fermentationPageContent[209], command=lambda:self.showScrambledSolution(controller), relief = SUNKEN, fg='white', bg = 'green4', font=self.gameFont, compound=CENTER, height = 2, width = 14)
        self.solutionScrambledWord.place(x=880, y=480)
        self.closeScrambledWord = Button(self.scrambledCanvas, text=controller.currentLanguage.fermentationPageContent[210], command=lambda:self.playScrambled(controller), relief = SUNKEN, fg='white', bg = 'red', font=self.gameFont, compound=CENTER, height = 2, width = 14)
        self.closeScrambledWord.place(x=680, y=480)
        self.answerScrambledWordOrganism = Button(self.scrambledCanvas, text=controller.currentLanguage.fermentationPageContent[211], command=lambda:self.checkOrganismAnswer(controller), relief = SUNKEN, fg='white', bg = 'DodgerBlue3', font=self.gameFont, compound=CENTER, height = 2, width = 20)
        self.answerScrambledWordOrganism.place(x=820, y=145)
        self.answerScrambledWordFamily = Button(self.scrambledCanvas, text=controller.currentLanguage.fermentationPageContent[211], command=lambda:self.checkFamilyAnswer(controller), relief = SUNKEN, fg='white', bg = 'DodgerBlue3', font=self.gameFont, compound=CENTER, height = 2, width = 20)
        self.answerScrambledWordFamily.place(x=820, y=360)

    def configureNextScrambledGame(self, controller):
        scrambledWords = controller.application.gamesEntertainment.scrambledData.startScrambledSequence()
        scrambledIdentifier = Picture([controller.application.gamesEntertainment.scrambledData.getSelectedImageName(),'png',500,400,130,100],0)
        scrambledIdentifier.purpose = 'GamesPic/ScrambledPic'
        #print("IMAGE: ", scrambledIdentifier.getCompleteFilename())
        scrambledImage = Image.open(scrambledIdentifier.getCompleteFilename())
        scrambledImageRendered = ImageTk.PhotoImage(scrambledImage.rotate(scrambledIdentifier.orientation))
        self.scrambledPic.config(image = scrambledImageRendered)
        self.scrambledPic.image = scrambledImageRendered
        self.scrambledPic.place(x=scrambledIdentifier.location[0],y=scrambledIdentifier.location[1])
        self.wordScrambledOrganism['text'] = "ORGANISM: "+scrambledWords[0]
        self.wordScrambledFamily['text'] = "FAMILY: "+scrambledWords[1]
        self.wordOrganismTyped.config(state='normal')
        self.wordOrganismTyped.delete(0, END)
        self.wordFamilyTyped.config(state='normal')
        self.wordFamilyTyped.delete(0, END)
        self.solutionOrganismTyped['text'] = ""
        self.solutionFamilyTyped['text'] = ""
        self.timeForGames = date.today()

    def configureInitialScrambledGame(self, controller):
        scrambledWords = controller.application.gamesEntertainment.scrambledData.startScrambledSequence() #['qiufiAcae', 'sdfsdfs']
        #print("SCRAMBLED WORDS: ", scrambledWords)
        self.setPictureForScrambled(controller)
        self.setEntriesForScrambled(controller, scrambledWords)
        self.setButtonsForScrambled(controller)

    def playScrambled(self, controller):
        if(self.gamesDisplayed[0] == False):
            self.scrambledCanvas.place(x=0, y=140)
            self.gamesDisplayed[0] = True
            self.timeForGames = date.today()
            self.gamePointsMultiplier = 1
            controller.application.systemData.informations[len(controller.application.systemData.informations)-1].addTimesScrambledPlayed()
        else:
            self.scrambledCanvas.place(x=1000, y=1000)
            self.gamesDisplayed[0] = False
            self.updateRecordData(controller, 0)
            self.updateDisplayInformation(controller)

###################### HANGMAN HANDLING ############################

    def configureNextHangmanGame(self, controller):
        hangmanWords = controller.application.gamesEntertainment.hangmanData.startHangmanSequence()
        self.setUpdateHangmanImage(controller)
        self.wordToGuessHangman['text'] = hangmanWords[0]
        self.wordHintHangman['text'] = "HINT: "+hangmanWords[1]
        self.lettersMistakenToShow['text'] = ""
        self.wordGuessedTyped.config(state='normal')
        self.wordGuessedTyped.delete(0, END)
        self.letterGuessedTyped.config(state='normal')
        self.letterGuessedTyped.delete(0, END)
        self.endGameMessageTitle['text'] = ""
        self.endGameMessageBody['text'] = ""
        self.timeForGames = date.today()

    def setUpdateHangmanImage(self, controller):
        hangmanIdentifier = Picture([controller.application.gamesEntertainment.hangmanData.getCurrentImageName(),'png',430,550,150,40],0)
        hangmanIdentifier.purpose = 'GamesPic/HangmanPic'
        hangmanImage = Image.open(hangmanIdentifier.getCompleteFilename())
        hangmanImageRendered = ImageTk.PhotoImage(hangmanImage.rotate(hangmanIdentifier.orientation))
        self.hangmanPic.config(image = hangmanImageRendered)
        self.hangmanPic.image = hangmanImageRendered

    def setPictureForHangman(self, controller):
        controller.setImagesandSeparators(self.hangmanCanvas, 'hangmanElement', [100,250,10,10,100,250,10,320])
        controller.setImagesandSeparators(self.hangmanCanvas, 'hangmanElement', [100,250,1240,10,100,250,1240,320])
        hangmanIdentifier = Picture([controller.application.gamesEntertainment.hangmanData.getCurrentImageName(),'png',430,550,150,40],0)
        hangmanIdentifier.purpose = 'GamesPic/HangmanPic'
        hangmanImage = Image.open(hangmanIdentifier.getCompleteFilename())
        hangmanImageRendered = ImageTk.PhotoImage(hangmanImage.rotate(hangmanIdentifier.orientation))
        self.hangmanPic.config(image = hangmanImageRendered)
        self.hangmanPic.image = hangmanImageRendered
        self.hangmanPic.place(x=hangmanIdentifier.location[0],y=hangmanIdentifier.location[1])

    def setEntriesForHangman(self, controller, hangmanWords):
        self.currentPointsHangman = Label(self.hangmanCanvas, text=controller.currentLanguage.fermentationPageContent[204]+" "+str(self.gameSessionScore[1]), font=self.titleFont, fg='white', bg=self.colorORT)
        self.currentPointsHangman.place(x=200,y=10)
        self.hangmanTitle = Label(self.hangmanCanvas, text=controller.currentLanguage.fermentationPageContent[212], font=self.titleFont, fg='white', bg=self.colorORT)
        self.hangmanTitle.place(x=750,y=10)
        self.wordToGuessHangman = Label(self.hangmanCanvas, text=hangmanWords[0], font=self.hangmanFont, fg='white', bg=self.colorORT)
        self.wordToGuessHangman.place(x=700,y=60)
        self.lettersMistakenHangman = Label(self.hangmanCanvas, text=controller.currentLanguage.fermentationPageContent[213], font=self.buttonFont, fg='white', bg=self.colorORT) #controller.application.gamesEntertainment.hangmanData.lettersMistaken
        self.lettersMistakenHangman.place(x=120,y=470)
        self.lettersMistakenToShow = Label(self.hangmanCanvas, font=self.hangmanFont, fg='red', bg=self.colorORT) #controller.application.gamesEntertainment.hangmanData.lettersMistaken
        self.lettersMistakenToShow.place(x=140,y=500)
        self.guessWordTitle = Label(self.hangmanCanvas, text=controller.currentLanguage.fermentationPageContent[214], font=self.titleFont, fg='white', bg=self.colorORT)
        self.guessWordTitle.place(x=680,y=170)
        self.wordHintHangman = Label(self.hangmanCanvas, text=controller.currentLanguage.fermentationPageContent[215]+hangmanWords[1], font=self.titleFont, fg='snow4', bg=self.colorORT)
        self.wordHintHangman.place(x=710,y=290)
        self.guessLetterTitle = Label(self.hangmanCanvas, text=controller.currentLanguage.fermentationPageContent[216], font=self.titleFont, fg='white', bg=self.colorORT)
        self.guessLetterTitle.place(x=680,y=380)
        self.wordGuessedTyped = Entry(self.hangmanCanvas, font=self.titleFont, fg=self.colorORT, width=18, justify='center', state='normal')
        self.wordGuessedTyped.place(x=680,y=220)
        self.letterGuessedTyped = Entry(self.hangmanCanvas, font=self.titleFont, fg=self.colorORT, width=2, justify='center', state='normal')
        self.letterGuessedTyped.place(x=890,y=380)
        self.endGameMessageTitle = Label(self.hangmanCanvas, font=self.hangmanFont, fg='white', bg=self.colorORT)
        self.endGameMessageTitle.place(x=480,y=100)
        self.endGameMessageBody = Label(self.hangmanCanvas, font=self.titleFont, fg='white', bg=self.colorORT)
        self.endGameMessageBody.place(x=480,y=220)

    def showHangmanSolution(self, controller):
        controller.application.gamesEntertainment.hangmanData.getCurrentSolution()
        self.wordToGuessHangman['text'] = controller.application.gamesEntertainment.hangmanData.wordState
        self.wordGuessedTyped.config(state='disabled')
        self.letterGuessedTyped.config(state='disabled')

    def configureHangmanGameOver(self, controller):
        self.endGameMessageTitle['text'] = controller.currentLanguage.fermentationPageContent[217]
        self.endGameMessageTitle['fg'] = 'red'
        self.endGameMessageBody['text'] = controller.currentLanguage.fermentationPageContent[218]
        self.endGameMessageBody['fg'] = 'red'

    def showHangmanSolutionWhenAsked(self, controller):
        self.showHangmanSolution(controller)
        self.configureHangmanGameOver(controller)

    def configureHangmanVictory(self, controller):
        self.endGameMessageTitle['text'] = controller.currentLanguage.fermentationPageContent[219]
        self.endGameMessageTitle['fg'] = 'green4'
        self.endGameMessageBody['text'] = controller.currentLanguage.fermentationPageContent[220]
        self.endGameMessageBody['fg'] = 'green4'

    def checkHangmanWord(self, controller):
        if(controller.application.gamesEntertainment.hangmanData.isWholeAnswerRight(self.wordGuessedTyped.get())):
            self.checkPointsToAdd(controller, 1)
            self.showHangmanSolution(controller)
            self.configureHangmanVictory(controller)
        else:
            controller.application.gamesEntertainment.hangmanData.addIncorrectLetter("Inc Word")
            self.gamePointsMultiplier = 1
            self.setUpdateHangmanImage(controller)
            if(controller.application.gamesEntertainment.hangmanData.isGameOver()):
                self.showHangmanSolution(controller)
                self.configureHangmanGameOver(controller)
        self.wordGuessedTyped.delete(0,END)

    def checkHangmanLetter(self, controller):
        if(controller.application.gamesEntertainment.hangmanData.isLetterTypedCorrect(self.letterGuessedTyped.get())):
            self.wordToGuessHangman['text'] = controller.application.gamesEntertainment.hangmanData.wordState
            self.checkPointsToAdd(controller, 1)
            if(controller.application.gamesEntertainment.hangmanData.isEveryLetterGuessed()):
                self.showHangmanSolution(controller)
                self.configureHangmanVictory(controller)
        else:
            self.lettersMistakenToShow['text'] = controller.application.gamesEntertainment.hangmanData.getLettersMistaken()
            self.gamePointsMultiplier = 1
            self.setUpdateHangmanImage(controller)
            if(controller.application.gamesEntertainment.hangmanData.isGameOver()):
                self.showHangmanSolution(controller)
                self.configureHangmanGameOver(controller)
        self.letterGuessedTyped.delete(0,END)

    def setButtonsForHangman(self, controller):
        self.nextHangmandWord = Button(self.hangmanCanvas, text=controller.currentLanguage.fermentationPageContent[208], command=lambda:self.configureNextHangmanGame(controller), relief = SUNKEN, fg='white', bg = 'gold4', font=self.gameFont, compound=CENTER, height = 16, width = 3)
        self.nextHangmandWord.place(x=1150, y=50)
        self.solutionHangmanWord = Button(self.hangmanCanvas, text=controller.currentLanguage.fermentationPageContent[221], command=lambda:self.showHangmanSolutionWhenAsked(controller), relief = SUNKEN, fg='white', bg = 'green4', font=self.gameFont, compound=CENTER, height = 2, width = 14)
        self.solutionHangmanWord.place(x=880, y=480)
        self.closeHangmanWord = Button(self.hangmanCanvas, text=controller.currentLanguage.fermentationPageContent[222], command=lambda:self.playHangman(controller), relief = SUNKEN, fg='white', bg = 'red', font=self.gameFont, compound=CENTER, height = 2, width = 14)
        self.closeHangmanWord.place(x=680, y=480)
        self.answerHangmanWord = Button(self.hangmanCanvas, text=controller.currentLanguage.fermentationPageContent[223], command=lambda:self.checkHangmanWord(controller), relief = SUNKEN, fg='white', bg = 'lime green', font=self.gameFont, compound=CENTER, height = 2, width = 7)
        self.answerHangmanWord.place(x=970, y=200)
        self.answerHangmanLetter = Button(self.hangmanCanvas, text=controller.currentLanguage.fermentationPageContent[223], command=lambda:self.checkHangmanLetter(controller), relief = SUNKEN, fg='white', bg = 'lime green', font=self.gameFont, compound=CENTER, height = 2, width = 7)
        self.answerHangmanLetter.place(x=970, y=360)

    def configureInitialHangmanGame(self, controller):
        hangmanWords = controller.application.gamesEntertainment.hangmanData.startHangmanSequence() #['qiufiAcae', 'sdfsdfs']
        self.setPictureForHangman(controller)
        self.setEntriesForHangman(controller, hangmanWords)
        self.setButtonsForHangman(controller)

    def playHangman(self, controller):
        if(self.gamesDisplayed[1] == False):
            self.hangmanCanvas.place(x=0, y=140)
            self.gamesDisplayed[1] = True
            self.timeForGames = date.today()
            self.gamePointsMultiplier = 1
            controller.application.systemData.informations[len(controller.application.systemData.informations)-1].addTimesHangmanPlayed()
        else:
            self.hangmanCanvas.place(x=1000, y=1000)
            self.gamesDisplayed[1] = False
            self.updateRecordData(controller, 1)
            self.updateDisplayInformation(controller)

###################### TRIVIA HANDLING ###########################

    def setPictureForTrivia(self):
        triviaElementLeft = Picture(['knowItAllElement','png',130,530,10,40],0)
        triviaElementLeft.purpose = 'Words'
        triviaElementLeftPic = triviaElementLeft.generateLabel(self.triviaCanvas)
        triviaElementLeftPic.place(x=triviaElementLeft.location[0],y=triviaElementLeft.location[1])

        triviaElementRight = Picture(['knowItAllElement','png',130,530,1220,10],180)
        triviaElementRight.purpose = 'Words'
        triviaElementRightPic = triviaElementRight.generateLabel(self.triviaCanvas)
        triviaElementRightPic.place(x=triviaElementRight.location[0],y=triviaElementRight.location[1])

        triviaLeftIdentifier = Picture(['questionDnaLogoReverse','png',120,120,150,10],0)
        triviaLeftIdentifier.purpose = 'GamesPic/TriviaPic'
        triviaLeftImage = Image.open(triviaLeftIdentifier.getCompleteFilename()).resize((triviaLeftIdentifier.dimensions[0],triviaLeftIdentifier.dimensions[1]), Image.ANTIALIAS)
        triviaLeftImageRendered = ImageTk.PhotoImage(triviaLeftImage.rotate(triviaLeftIdentifier.orientation))
        self.triviaLeftPic = Label(self.triviaCanvas, image=triviaLeftImageRendered, borderwidth=0, highlightthickness=0)
        self.triviaLeftPic.image = triviaLeftImageRendered
        self.triviaLeftPic.place(x=triviaLeftIdentifier.location[0],y=triviaLeftIdentifier.location[1])
        triviaRightIdentifier = Picture(['questionDnaLogo','png',120,120,1100,10],0)
        triviaRightIdentifier.purpose = 'GamesPic/TriviaPic'
        triviaRightImage = Image.open(triviaRightIdentifier.getCompleteFilename()).resize((triviaRightIdentifier.dimensions[0],triviaRightIdentifier.dimensions[1]), Image.ANTIALIAS)
        triviaRightImageRendered = ImageTk.PhotoImage(triviaRightImage.rotate(triviaRightIdentifier.orientation))
        self.triviaRightPic = Label(self.triviaCanvas, image=triviaRightImageRendered, borderwidth=0, highlightthickness=0)
        self.triviaRightPic.image = triviaRightImageRendered
        self.triviaRightPic.place(x=1100,y=10)

    def optionASelected(self, event=None):
        #if(self.optionASelection.get()==1):
        self.optionBTrivia.deselect()
        self.optionCTrivia.deselect()
        self.optionDTrivia.deselect()

    def optionBSelected(self, event=None):
        #if(self.optionBSelection.get()==1):
        self.optionATrivia.deselect()
        self.optionCTrivia.deselect()
        self.optionDTrivia.deselect()

    def optionCSelected(self, event=None):
        #if(self.optionCSelection.get()==1):
        self.optionATrivia.deselect()
        self.optionBTrivia.deselect()
        self.optionDTrivia.deselect()

    def optionDSelected(self, event=None):
        #print("DETECTADO OPCION D")
        #if(self.optionDSelection.get()==1):
        #self.optionASelection = 0
        self.optionATrivia.deselect()
        #self.optionBSelection = 0
        self.optionBTrivia.deselect()
        #self.optionCSelection = 0
        self.optionCTrivia.deselect()
        #self.optionATrivia.config(state=NORMAL)
        #self.optionBTrivia.config(state=NORMAL)
        #self.optionCTrivia.config(state=NORMAL)

    def setEntriesForTrivia(self, controller, triviaWords):
        self.currentPointsTrivia = Label(self.triviaCanvas, text=controller.currentLanguage.fermentationPageContent[204]+" "+str(self.gameSessionScore[2]), font=self.titleFont, fg='white', bg=self.colorORT) #Actualiza GamesSessionScore en Original
        self.currentPointsTrivia.place(x=200,y=470)
        self.triviaQuestionNumber = Label(self.triviaCanvas, text=controller.currentLanguage.fermentationPageContent[224]+" "+str(self.questionsAnswered), font=self.titleFont, fg='white', bg=self.colorORT)
        self.triviaQuestionNumber.place(x=200,y=510)
        self.questionTitle = Label(self.triviaCanvas, text=triviaWords[0], font=self.titleFont, fg='white', bg=self.colorORT)
        self.questionTitle.place(x=320,y=50)
        self.optionATrivia = Checkbutton(self.triviaCanvas, text="A. "+triviaWords[1], bg=self.colorORT, font=self.subtitleFont, variable=self.triviaOptionSelection[0])
        self.optionATrivia.place(x=220, y=150)
        self.optionBTrivia = Checkbutton(self.triviaCanvas, text="B. "+triviaWords[2], bg=self.colorORT, font=self.subtitleFont, variable=self.triviaOptionSelection[1])
        self.optionBTrivia.place(x=220, y=300)
        self.optionCTrivia = Checkbutton(self.triviaCanvas, text="C. "+triviaWords[3], bg=self.colorORT, font=self.subtitleFont, variable=self.triviaOptionSelection[2])
        self.optionCTrivia.place(x=700, y=150)
        self.optionDTrivia = Checkbutton(self.triviaCanvas, text="D. "+triviaWords[4], bg=self.colorORT, font=self.subtitleFont, variable=self.triviaOptionSelection[3])
        self.optionDTrivia.place(x=700, y=300)
        self.optionATrivia.config(command=self.optionASelected)
        self.optionBTrivia.config(command=self.optionBSelected)
        self.optionCTrivia.config(command=self.optionCSelected)
        self.optionDTrivia.config(command=self.optionDSelected)

    def checkCurrentAnswer(self):
        currentAnswer = ""
        if(self.triviaOptionSelection[0].get()==1):
            currentAnswer = self.optionATrivia['text'][3:]
        if(self.triviaOptionSelection[1].get()==1):
            currentAnswer = self.optionBTrivia['text'][3:]
        if(self.triviaOptionSelection[2].get()==1):
            currentAnswer = self.optionCTrivia['text'][3:]
        if(self.triviaOptionSelection[3].get()==1):
            currentAnswer = self.optionDTrivia['text'][3:]
        return currentAnswer

    def showCurrentWrongOption(self):
        if(self.triviaOptionSelection[0].get()==1):
            self.optionATrivia['fg']='red'
        if(self.triviaOptionSelection[1].get()==1):
            self.optionBTrivia['fg']='red'
        if(self.triviaOptionSelection[2].get()==1):
            self.optionCTrivia['fg']='red'
        if(self.triviaOptionSelection[3].get()==1):
            self.optionDTrivia['fg']='red'

    def disableAllOptions(self):
        self.optionATrivia.deselect()
        self.optionBTrivia.deselect()
        self.optionCTrivia.deselect()
        self.optionDTrivia.deselect()

    def showOptionCorrect(self, controller):
        if(controller.application.gamesEntertainment.triviaData.isOptionCorrect(self.optionATrivia['text'][3:])):
            self.optionATrivia['fg']='green'
        if(controller.application.gamesEntertainment.triviaData.isOptionCorrect(self.optionBTrivia['text'][3:])):
            self.optionBTrivia['fg']='green'
        if(controller.application.gamesEntertainment.triviaData.isOptionCorrect(self.optionCTrivia['text'][3:])):
            self.optionCTrivia['fg']='green'
        if(controller.application.gamesEntertainment.triviaData.isOptionCorrect(self.optionDTrivia['text'][3:])):
            self.optionDTrivia['fg']='green'

    def checkOptionSelected(self, controller, answerChosen):
        if(controller.application.gamesEntertainment.triviaData.isOptionCorrect(answerChosen)):
            self.showOptionCorrect(controller)
            self.checkPointsToAdd(controller, 2)
            self.updatePicturesOfTrivia(['correctAnswerLogo', 'correctAnswerLogo'])
            #messagebox.showinfo("TRIVIA", "CORRECT!!!")
        else:
            self.showOptionCorrect(controller)
            self.showCurrentWrongOption()
            self.gamePointsMultiplier = 1
            self.updatePicturesOfTrivia(['wrongAnswerLogo', 'wrongAnswerLogo'])
            #messagebox.showinfo("TRIVIA", "WRONG!!! Ups...")
        self.triviaGameEnded = True

    def checkQuestionAnswer(self, controller):
        if(not self.triviaGameEnded):
            answerChosen = self.checkCurrentAnswer()
            if(answerChosen==""):
                messagebox.showwarning("TRIVIA", controller.currentLanguage.fermentationPageContent[225])
            else:
                self.checkOptionSelected(controller, answerChosen)
        else:
            messagebox.showwarning("TRIVIA", controller.currentLanguage.fermentationPageContent[226])

    def updatePicturesOfTrivia(self, imagesNames):
        triviaLeftIdentifier = Picture([imagesNames[0],'png',120,120,150,10],0)
        triviaLeftIdentifier.purpose = 'GamesPic/TriviaPic'
        triviaLeftImage = Image.open(triviaLeftIdentifier.getCompleteFilename()).resize((triviaLeftIdentifier.dimensions[0],triviaLeftIdentifier.dimensions[1]), Image.ANTIALIAS)
        triviaLeftImageRendered = ImageTk.PhotoImage(triviaLeftImage.rotate(triviaLeftIdentifier.orientation))
        self.triviaLeftPic.config(image=triviaLeftImageRendered)
        self.triviaLeftPic.image = triviaLeftImageRendered
        triviaRightIdentifier = Picture([imagesNames[1],'png',120,120,1100,10],0)
        triviaRightIdentifier.purpose = 'GamesPic/TriviaPic'
        triviaRightImage = Image.open(triviaRightIdentifier.getCompleteFilename()).resize((triviaRightIdentifier.dimensions[0],triviaRightIdentifier.dimensions[1]), Image.ANTIALIAS)
        triviaRightImageRendered = ImageTk.PhotoImage(triviaRightImage.rotate(triviaRightIdentifier.orientation))
        self.triviaRightPic.config(image=triviaRightImageRendered)
        self.triviaRightPic.image = triviaRightImageRendered

    def configureNextTriviaGame(self, controller):
        if(self.triviaGameEnded):
            triviaWords = controller.application.gamesEntertainment.triviaData.startTriviaSequence()
            self.triviaGameEnded = False
            self.questionTitle['text'] = triviaWords[0]
            self.optionATrivia['text'] = "A. "+triviaWords[1]
            self.optionATrivia['fg'] = 'gray1'
            self.optionBTrivia['text'] = "B. "+triviaWords[2]
            self.optionBTrivia['fg'] = 'gray1'
            self.optionCTrivia['text'] = "C. "+triviaWords[3]
            self.optionCTrivia['fg'] = 'gray1'
            self.optionDTrivia['text'] = "D. "+triviaWords[4]
            self.optionDTrivia['fg'] = 'gray1'
            self.disableAllOptions()
            self.updatePicturesOfTrivia(['questionDnaLogoReverse', 'questionDnaLogo'])
            self.questionsAnswered = self.questionsAnswered + 1
            self.triviaQuestionNumber['text'] = controller.currentLanguage.fermentationPageContent[224]+" "+str(self.questionsAnswered)
            self.timeForGames = date.today()
        else:
            messagebox.showwarning("TRIVIA", "Answer this Question First!!!")

    def setButtonsForTrivia(self, controller):
        self.nextTriviaQuestion = Button(self.triviaCanvas, text=controller.currentLanguage.fermentationPageContent[227], command=lambda:self.configureNextTriviaGame(controller), relief = SUNKEN, fg='white', bg = 'gold4', font=self.gameFont, compound=CENTER, height = 2, width = 12)
        self.nextTriviaQuestion.place(x=1000, y=480)
        self.checkTriviaAnswer = Button(self.triviaCanvas, text=controller.currentLanguage.fermentationPageContent[228], command=lambda:self.checkQuestionAnswer(controller), relief = SUNKEN, fg='white', bg = 'blue', font=self.gameFont, compound=CENTER, height = 2, width = 12)
        self.checkTriviaAnswer.place(x=800, y=480)
        self.closeTrivia = Button(self.triviaCanvas, text=controller.currentLanguage.fermentationPageContent[229], command=lambda:self.playTrivia(controller), relief = SUNKEN, fg='white', bg = 'red', font=self.gameFont, compound=CENTER, height = 2, width = 10)
        self.closeTrivia.place(x=630, y=480)

    def configureInitialTriviaGame(self, controller):
        triviaWords = controller.application.gamesEntertainment.triviaData.startTriviaSequence()
        self.setPictureForTrivia()
        self.setEntriesForTrivia(controller, triviaWords)
        self.setButtonsForTrivia(controller)
        self.questionsAnswered = 0
        self.triviaQuestionNumber['text'] = controller.currentLanguage.fermentationPageContent[224]+" "+str(self.questionsAnswered)

    def playTrivia(self, controller):
        if(self.gamesDisplayed[2] == False):
            self.triviaCanvas.place(x=0, y=140)
            self.gamesDisplayed[2] = True
            self.timeForGames = date.today()
            self.gamePointsMultiplier = 1
            controller.application.systemData.informations[len(controller.application.systemData.informations)-1].addTimesTriviaPlayed()
        else:
            self.triviaCanvas.place(x=1000, y=1000)
            self.gamesDisplayed[2] = False
            self.questionsAnswered = 0
            self.triviaQuestionNumber['text'] = controller.currentLanguage.fermentationPageContent[224]+" "+str(self.questionsAnswered)
            self.updateRecordData(controller, 2)
            self.updateDisplayInformation(controller)

########################## SECONDARY GAMES MANAGEMENT ##############################

    def playDodger(self, controller):
        controller.gamesManager[0] = 1
        while(controller.gamesManager[0]!=0):
            self.currentGameStatus[0]['text'] = controller.currentLanguage.fermentationPageContent[190]
        self.currentGameStatus[0]['text'] = controller.currentLanguage.fermentationPageContent[191]+controller.currentLanguage.fermentationPageContent[196]+controller.currentLanguage.fermentationPageContent[197] #AGREGAR

    def playMemory(self, controller):
        controller.gamesManager[0] = 2
        while(controller.gamesManager[0]!=0):
            self.currentGameStatus[1]['text'] = controller.currentLanguage.fermentationPageContent[192]
        self.currentGameStatus[1]['text'] = controller.currentLanguage.fermentationPageContent[193]+controller.currentLanguage.fermentationPageContent[196]+controller.currentLanguage.fermentationPageContent[197] #AGREGAR

    def playNibbles(self, controller):
        controller.gamesManager[0] = 3
        while(controller.gamesManager[0]!=0):
            self.currentGameStatus[2]['text'] = controller.currentLanguage.fermentationPageContent[194]
        self.currentGameStatus[2]['text'] = controller.currentLanguage.fermentationPageContent[195]+controller.currentLanguage.fermentationPageContent[196]+controller.currentLanguage.fermentationPageContent[197] #AGREGAR
