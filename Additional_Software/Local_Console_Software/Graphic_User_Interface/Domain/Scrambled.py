import sys, time, random
from datetime import datetime, date, timedelta
from Domain.Game import Game

class Scrambled(Game):

    def __init__(self):
        super(Scrambled,self).__init__()
        self.guideImagesNames = ['Image01', 'Image02', 'Image03', 'Image04', 'Image05', 'Image06', 'Image07', 'Image08', 'Image09', 'Image10', 'Image11', 'Image12', 'Image13', 'Image14', 'Image15', 'Image16', 'Image17', 'Image18', 'Image19', 'Image20', 'Image21', 'Image22', 'Image23', 'Image24', 'Image25', 'Image26', 'Image27', 'Image28', 'Image29', 'Image30', 'Image31', 'Image32', 'Image33', 'Image34', 'Image35', 'Image36', 'Image37', 'Image38', 'Image39', 'Image40'] #'Image41', 'Image42', 'Image43', 'Image44', 'Image45', 'Image46', 'Image47', 'Image48', 'Image49', 'Image50', 'Image51', 'Image52', 'Image53', 'Image54', 'Image55', 'Image56' ]
        self.organismsWords = ['Escherichia Coli', 'Actinomyces', 'Bacteroides Biacutis', 'Candidatus Epixenosoma', 'Chlamydia Trachomatis', 'Chloroflexus Aurantiacus', 'Fusobacterium Novum', 'Hypocrea Virens', 'Tolypothrix', 'Tremella Basidium', 'Winogradsky Column', 'Bacillus Subtilis', 'Bacillus Subtilis', 'Caulobacter Crescentus', 'Escherichia Coli', 'Emiliania Huxleyi', 'Eremothecium', 'Mycoplasma Genitalium', 'Neurospora Crassa', 'Pseudomonas Fluorescens', 'Saccharomyces Cerevisiae', 'Schizophyllum Commune', 'Schizosaccharomyces Pombe', 'Stentor Coeruleus', 'Tetrahymena', 'Thalassiosira Pseudonana', 'Ustilago Maydis', 'Brettanomyces', 'Buchnera Aphidicola', 'Candida Albicans', 'Citrobacter', 'Kluyveromyces', 'Pectobacterium', 'Providencia', 'Saccharomyces', 'Salmonella', 'Serratia', 'Shigella', 'Thorsellia Anophelis', 'Yersinia']
        self.familiesWords = ['Enterobacteriaceae', 'Actinomycetaceae', 'Bacteroidaceae', 'Verrucomicrobiae', 'Chlamydiaceae', 'Chloroflexaceae', 'Fusobacteriaceae', 'Hypocreaceae', 'Microchaetaceae', 'Tremellaceae', 'GreenSulfur Bacteria', 'Bacillaceae', 'Bacillaceae', 'Caulobacteraceae', 'Enterobacteriaceae', 'Noelaerhabdaceae', 'Saccharomycetaceae', 'Mycoplasmataceae', 'Sordariaceae', 'Pseudomonadaceae', 'Saccharomycetaceae', 'Schizophyllaceae', 'Schizosaccaromycetaceae', 'Stentoridae', 'Tetrahymenidae', 'Thalassiosiraceae', 'Ustilaginaceae', 'Pichiaceae', 'Enterobacteriaceae', 'Saccharomycetaceae', 'Enterobacteriaceae', 'Saccharomycetaceae', 'Enterobacteriaceae', 'Enterobacteriaceae', 'Saccharomycetaceae', 'Enterobacteriaceae', 'Enterobacteriaceae', 'Enterobacteriaceae', 'Thorselliaceae', 'Yersiniaceae']

    def scrambleSelectedWord(self, wordToScramble):
        wordsToScramble = wordToScramble.split()
        scrambledWord = ""
        for eachWordToScramble in wordsToScramble:
            listOfLettersToScramble = list(eachWordToScramble)
            random.shuffle(listOfLettersToScramble)
            #scrambledWord.join(listOfLettersToScramble)
            scrambledWord = scrambledWord + " " + ''.join(listOfLettersToScramble)
        return scrambledWord
        #newsentence = list(wordToScramble)
        #i, j = random.sample(xrange(1, len(wordToScramble) - 1), 2)
        #newsentence[i], newsentence[j] = newsentence[j], newsentence[i]
        #return newsentence

    def getSelectedImageName(self):
        return self.guideImagesNames[self.selectedWord]

    def getScrambledRegisteredData(self):
        scrambledOrganismsWord = self.scrambleSelectedWord(self.organismsWords[self.selectedWord])
        scrambledFamiliesWord = self.scrambleSelectedWord(self.familiesWords[self.selectedWord])
        return [scrambledOrganismsWord, scrambledFamiliesWord]

    def getScrambledSolutionWords(self):
        solutiondOrganismsWord = self.organismsWords[self.selectedWord]
        solutionFamiliesWord = self.familiesWords[self.selectedWord]
        return [solutiondOrganismsWord, solutionFamiliesWord]

    def verifyOrganismsEntry(self, organismsEntry):
        return self.organismsWords[self.selectedWord] == organismsEntry

    def verifyFamiliesEntry(self, familiesEntry):
        return self.familiesWords[self.selectedWord] == familiesEntry

    def startScrambledSequence(self):
        self.setRandomPositionOfList(len(self.guideImagesNames))
        return self.getScrambledRegisteredData()
