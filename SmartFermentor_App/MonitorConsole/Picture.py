import sys
import time
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter.font
from PIL import Image, ImageTk

class Picture():

    def __init__(self, pictureInformation, angle):
        self.filename = pictureInformation[0]
        self.extension = pictureInformation[1]
        self.dimensions = [pictureInformation[2],pictureInformation[3]]
        self.location = [pictureInformation[4],pictureInformation[5]]
        self.orientation = angle
        self.purpose = 'Background'

    def setDimensions(self, width, height):
        self.dimensions[0] = width
        self.dimensions[1] = height

    def setLocation(self, locationX, locationY):
        self.location[0] = locationX
        self.location[1] = locationY

    def getCompleteFilename(self):
        return "Images/"+self.purpose+"/"+self.filename+'.'+self.extension

    def hasSameFilename(self, otherPicture):
        sameFilename = 0
        if(self.getCompleteFilename()==otherPicture.getCompleteFilename()):
            sameFilename=1
        return sameFilename

    def hasSameDimensions(self, otherPicture):
        sameDimensions = 0
        if(self.dimensions[0]==otherPicture.dimensions[0] and self.dimensions[1]==otherPicture.dimensions[1]):
            sameDimensions=1
        return sameDimensions

    def isSamePicture(self, otherPicture):
        samePicture = 0
        if(self.hasSameFilename(otherPicture)==1 and self.hasSameDimensions(otherPicture)==1):
            samePicture=1

    def generateLabel(self, frameLocation):
        oneImage = Image.open(self.getCompleteFilename()).resize((self.dimensions[0],self.dimensions[1]), Image.ANTIALIAS)
        oneImageRendered = ImageTk.PhotoImage(oneImage.rotate(self.orientation))
        imagePic = Label(frameLocation, image=oneImageRendered, borderwidth=0, highlightthickness=0)
        imagePic.image = oneImageRendered
        return imagePic
