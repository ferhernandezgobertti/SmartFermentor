import sys, time, random
from datetime import datetime, date, timedelta
from Domain.Game import Game

class Hangman(Game):

    def __init__(self):
        super(Hangman,self).__init__()
        self.wordsToGuess = ['ESCHERICHIA COLI', 'ACTINOMYCES', 'BACTEROIDES BIACUTIS', 'CANDIDATUS EPIXENOSOMA', 'CHLAMYDIA TRACHOMATIS', 'CHLOROFLEXUS AURANTIACUS', 'FUSOBACTERIUM NOVUM', 'HYPOCREA VIRENS', 'TOLYPOTHRIX', 'TREMELLA BASIDIUM', 'WINOGRADSKY COLUMN', 'BACILLUS SUBTILIS', 'BACILLUS SUBTILIS', 'CAULOBACTER CRESCENTUS', 'ESCHERICHIA COLI', 'EMILIANIA HUXLEYI', 'EREMOTHECIUM', 'MYCOPLASMA GENITALIUM', 'NEUROSPORA CRASSA', 'PSEUDOMONAS FLUORESCENS', 'SACCHAROMYCES CEREVISIAE', 'SCHIZOPHYLLUM COMMUNE', 'SCHIZOSACCHAROMYCES POMBE', 'STENTOR COERULEUS', 'TETRAHYMENA', 'THALASSIOSIRA PSEUDONANA', 'USTILAGO MAYDIS', 'BRETTANOMYCES', 'BUCHNERA APHIDICOLA', 'CANDIDA ALBICANS', 'CITROBACTER', 'KLUYVEROMYCES', 'PECTOBACTERIUM', 'PROVIDENCIA', 'SACCHAROMYCES', 'SALMONELLA', 'SERRATIA', 'SHIGELLA', 'THORSELLIA ANOPHELIS', 'YERSINIA']
        #for eachWord in self.wordsToGuess:
        #    eachWord = eachWord.upper()
        self.hints = ['Enterobacteriaceae', 'Actinomycetaceae', 'Bacteroidaceae', 'Verrucomicrobiae', 'Chlamydiaceae', 'Chloroflexaceae', 'Fusobacteriaceae', 'Hypocreaceae', 'Microchaetaceae', 'Tremellaceae', 'GreenSulfur Bacteria', 'Bacillaceae', 'Bacillaceae', 'Caulobacteraceae', 'Enterobacteriaceae', 'Noelaerhabdaceae', 'Saccharomycetaceae', 'Mycoplasmataceae', 'Sordariaceae', 'Pseudomonadaceae', 'Saccharomycetaceae', 'Schizophyllaceae', 'Schizosaccaromycetaceae', 'Stentoridae', 'Tetrahymenidae', 'Thalassiosiraceae', 'Ustilaginaceae', 'Pichiaceae', 'Enterobacteriaceae', 'Saccharomycetaceae', 'Enterobacteriaceae', 'Saccharomycetaceae', 'Enterobacteriaceae', 'Enterobacteriaceae', 'Saccharomycetaceae', 'Enterobacteriaceae', 'Enterobacteriaceae', 'Enterobacteriaceae', 'Thorselliaceae', 'Yersiniaceae']
        self.wordState = ""
        self.lettersMistaken = []
        self.lettersCorrect = []
        self.images = ['initGame','Error1','Error2','Error3','Error4','Error5','gameOver']

    def isWholeAnswerRight(self, answerTyped):
        return self.wordsToGuess[self.selectedWord] == answerTyped.upper()

    def getCurrentSolution(self):
        for eachLetter in self.wordsToGuess[self.selectedWord]:
            self.lettersCorrect.append(eachLetter)
        self.updateWordState()

    def getCurrentImageName(self):
        return self.images[len(self.lettersMistaken)]

    def setWordState(self):
        currentWordsToGuess = self.wordsToGuess[self.selectedWord]
        wordsToGuess = currentWordsToGuess.split()
        for eachWordToGuess in wordsToGuess:
            if(len(eachWordToGuess)>1):
                for eachLetterOfWord in eachWordToGuess:
                    if(len(self.lettersCorrect)>0 and eachLetterOfWord in self.lettersCorrect):
                        self.wordState = self.wordState+eachLetterOfWord+" "
                    else:
                        self.wordState = self.wordState+"_ "
                self.wordState = self.wordState+"/ \n"

    def getHintOfCurrentWordToGuess(self):
        return self.hints[self.selectedWord]

    def getLettersMistaken(self):
        lettersMistakenToShow = ""#
        if(len(self.lettersMistaken)>0):
            for eachLetterMistaken in self.lettersMistaken:
                lettersMistakenToShow = lettersMistakenToShow + eachLetterMistaken + ", "
        return lettersMistakenToShow

    def updateWordState(self):
        position = 0
        newWordToGuess = ""
        self.setWordState()
        print("WORD STATE BEFORE: ", self.wordState)
        print("WORDS TO GUESS BEFORE: ", self.wordsToGuess[self.selectedWord])
        for eachLetter in self.wordsToGuess[self.selectedWord]:
            if(eachLetter==" "):
                newWordToGuess = newWordToGuess+"/ \n"
                position = position + 3
            else:
                if(eachLetter in self.lettersCorrect):
                    newWordToGuess = newWordToGuess+eachLetter+" "
                else:
                    newWordToGuess = newWordToGuess+self.wordState[position:position+2]
                position = position + 2
        print("POSITION: ", position)
        print("NEWWORD: ", newWordToGuess)
        print("WORDS TO GUESS AFTER: ", self.wordsToGuess[self.selectedWord])
        self.wordState = newWordToGuess

    def isLetterTypedCorrect(self, letterTyped):
        letterTypedCorrect = False
        print("LENGTH LETTERTYPED: ", len(letterTyped))
        print("IS ALPHA: ", letterTyped.isalpha())
        print("LETTERTYPED UPPER: ", letterTyped.upper() in self.wordsToGuess[self.selectedWord])
        if(len(letterTyped)==1 and letterTyped.isalpha() and letterTyped.upper() in self.wordsToGuess[self.selectedWord]):
            letterTypedCorrect = True
            self.lettersCorrect.append(letterTyped.upper())
            self.updateWordState()
        else:
            self.addIncorrectLetter(letterTyped)
        return letterTypedCorrect

    def isEveryLetterGuessed(self):
        return (not "_" in self.wordState)

    def addIncorrectLetter(self, incorrectLetter):
        self.lettersMistaken.append(incorrectLetter.upper())

    def isGameOver(self):
        return len(self.lettersMistaken)==6

    def startHangmanSequence(self):
        self.wordState = ""
        self.lettersMistaken = []
        self.lettersCorrect = []
        self.setRandomPositionOfList(len(self.wordsToGuess))
        self.setWordState()
        return [self.wordState, self.getHintOfCurrentWordToGuess()]
