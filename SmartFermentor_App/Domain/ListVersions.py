import sys
from Domain.Version import Version

class ListVersions():

    def __init__(self):
        self.velocityVersions = []
        self.temperatureVersions = []
        self.potentialVersions = []

    def addMagnitudeVersion(self, magnitudeList, versionToAdd):
        if(not self.isVersionOnList(magnitudeList, versionToAdd)):
            magnitudeList.append(versionToAdd)

    def removeMagnitudeVersion(self, magnitudeList, indexOfVersionToRemove):
        del magnitudeList[indexOfVersionToRemove]

    def removeAllVersionsOfMagnitude(self, magnitudeList):
        position = 0
        for eachVersion in magnitudeList:
            self.removeMagnitudeVersion(position)
            position = position+1

    def isVersionOnList(self, magnitudeList, otherVersion):
        isVersionPresent = False
        for eachVersion in magnitudeList:
            if(eachVersion.isSameVersion(otherVersion)):
                isVersionPresent = True
                break
        return isVersionPresent

    def getCommentaryOfMagnitudeVersion(self, magnitudeList, interestedVersion, noCommentaryPhrase):
        commentaryOfVersion = ""+str(noCommentaryPhrase)
        for eachVersion in magnitudeList:
            if(eachVersion.isSameVersion(interestedVersion)):
                commentaryOfVersion = eachVersion.commentary
                break
        return commentaryOfVersion

    def setCommentaryOfMagnitudeVersion(self, magnitudeList, interestedVersion, interestedCommentary):
        for eachVersion in magnitudeList:
            if(eachVersion.isSameVersion(interestedVersion)):
                eachVersion.commentary = interestedCommentary
                break

    def getJSONData(self):
        versionsData = {
            "velocityVersions": self.getJSONOfMagnitudeVersions(self.velocityVersions),
            "temperatureVersions": self.getJSONOfMagnitudeVersions(self.temperatureVersions),
            "potentialVersions": self.getJSONOfMagnitudeVersions(self.potentialVersions)
         }
        return versionsData

    def getJSONOfMagnitudeVersions(self, magnitudeToGet):
        versionData = []
        for eachVersion in magnitudeToGet:
            eachVersionData = eachVersion.getJSONData()
            versionData.append(eachVersionData)
        return versionData

    def loadJSONData(self, versionsToLoad):
        print("VERSIONS TO LOAD: ", versionsToLoad)
        self.velocityVersions = self.loadJSONOfMagnitudeVersions(versionsToLoad['velocityVersions']) #versionsToLoad
        self.temperatureVersions = self.loadJSONOfMagnitudeVersions(versionsToLoad['temperatureVersions'])
        self.potentialVersions = self.loadJSONOfMagnitudeVersions(versionsToLoad['potentialVersions'])

    def loadJSONOfMagnitudeVersions(self, versionsToLoad):
        versionsList = []
        for eachVersion in versionsToLoad:
            newVersion = Version([eachVersion['number'], eachVersion['commentary']])
            newVersion.dateAdded.strptime(eachVersion['dateAdded'],"%M:%H-%d/%m/%y")
            #print("VERSION: ", newVersion.showInformation())
            versionsList.append(newVersion)
        return versionsList
