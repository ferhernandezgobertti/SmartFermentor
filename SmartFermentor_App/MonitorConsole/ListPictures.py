import sys
import time
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter.font
from PIL import Image, ImageTk
from MonitorConsole.Picture import Picture

class ListPictures():

    pictures = []

    def addPictures(self, picturesToAdd, picturesQuantity):
        picturesAdded = 0
        pictureSuccessfullyAdded = 0
        while(picturesAdded<picturesQuantity):
            self.pictures.append(picturesToAdd[picturesAdded])
            picturesAdded = picturesAdded + 1
            pictureSuccessfullyAdded = 1
        return pictureSuccessfullyAdded

    def removePicture(self, pictureToRemove):
        picturesChecked = 0
        pictureRemoved = 0
        while(picturesChecked<len(self.pictures) and self.pictures.isPictureRegistered(pictureToRemove)==1):
            pictureBeingChecked = self.pictures[picturesChecked]
            if(pictureBeingChecked.isSamePicture(pictureToRemove)):
                self.pictures.remove(picturesChecked)
                pictureRemoved = 1
        return pictureRemoved

    def isPictureRegistered(self, pictureToCheck):
        picturesCounted = 0
        pictureRegistered = 0
        while(picturesCounted<len(self.pictures)):
            pictureBeingChecked = self.pictures[picturesCounted]
            if(pictureBeingChecked.isSamePicture(pictureToCheck)):
                pictureRegistered = 1
                break
        return pictureRegistered
