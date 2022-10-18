import sys
import datetime
from datetime import date
from datetime import timedelta

class Version():

    def __init__(self, number, commentary):
        self.number = number
        self.commentary = commentary
        self.dateAdded = date.today()

    def isSameVersion(self, otherVersion):
        return self.number == otherVersion.number

    def showInformation(self):
        return "VERSION "+self.number+" - "+self.commentary

    def getJSONData(self):
        versionData = {
            'number': self.number,
            'commentary': self.commentary,
            'dateAdded': self.dateAdded.strftime("%M:%H-%d/%m/%y")
        }
        return versionData
