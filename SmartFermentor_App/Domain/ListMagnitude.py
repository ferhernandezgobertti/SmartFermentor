import sys
from Domain.Velocity import Velocity
from Domain.Temperature import Temperature
from Domain.PotentialHydrogen import PotentialHydrogen

class ListMagnitude():

    velocities = []
    temperatures = []
    potentialsHydrogen = []

    def addVelocity(self, velocityToAdd):
        self.velocities.append(velocityToAdd)

    def addTemperature(self, temperatureToAdd):
        self.temperatures.append(temperatureToAdd)

    def addPotentialHydrogen(self, potentialToAdd):
        self.potentialsHydrogen.append(potentialToAdd)

    def removeVelocity(self, indexOfVelocityToRemove):
        del self.velocities[indexOfVelocityToRemove]

    def removeTemperature(self, indexOfTemperatureToRemove):
        del self.temperatures[indexOfTemperatureToRemove]

    def removePotentialHydrogen(self, indexOfPotentialToRemove):
        del self.potentialsHydrogen[indexOfPotentialToRemove]

    def clearVelocities(self):
        position = 0
        for eachVelocity in self.velocities:
            self.removeVelocity(position)
            position = position+1

    def clearTemperatures(self):
        position = 0
        for eachTemperature in self.temperatures:
            self.removeTemperature(position)
            position = position+1

    def clearPotentialsHydrogen(self):
        position = 0
        for eachPotential in self.potentialsHydrogen:
            self.removePotentialHydrogen(position)
            position = position+1

    def getJSONData(self):
        magnitudesData = {
            "velocities": self.getJSONOfVelocities(),
            "temperatures":self.getJSONOfTemperatures(),
            "potentialsHydrogen": self.getJSONOfPotentialsHydrogen()
         }
        return magnitudesData

    def getJSONOfVelocities(self):
        velocitiesData = []
        for eachVelocity in self.velocities:
            eachVelocityData = {
            "objective": eachVelocity.valueObjective,
            "hours": eachVelocity.duration[0],
            "minutes": eachVelocity.duration[1],
            "seconds": eachVelocity.duration[2],
            "unit": eachVelocity.unit,
            "evolutionSlope": eachVelocity.evolutionSlope,
            "dataInterval": eachVelocity.dataInterval,
            "precision": eachVelocity.precision,
            "direction": eachVelocity.direction
            }
            velocitiesData.append(eachVelocityData)
        return velocitiesData

    def getJSONOfTemperatures(self):
        temperaturesData = []
        for eachTemperature in self.temperatures:
            eachTemperatureData = {
            "objective": eachTemperature.valueObjective,
            "hours": eachTemperature.duration[0],
            "minutes": eachTemperature.duration[1],
            "seconds": eachTemperature.duration[2],
            "unit": eachTemperature.unit,
            "evolutionSlope": eachTemperature.evolutionSlope,
            "dataInterval": eachTemperature.dataInterval,
            "precision": eachTemperature.precision,
            "pumpStep": eachTemperature.pumpStep
            }
            temperaturesData.append(eachTemperatureData)
        return temperaturesData

    def getJSONOfPotentialsHydrogen(self):
        potentialsData = []
        for eachPotential in self.potentialsHydrogen:
            eachPotentialData = {
            "objective": eachPotential.valueObjective,
            "hours": eachPotential.duration[0],
            "minutes": eachPotential.duration[1],
            "seconds": eachPotential.duration[2],
            "unit": eachPotential.unit,
            "evolutionSlope": eachPotential.evolutionSlope,
            "dataInterval": eachPotential.dataInterval,
            "precision": eachPotential.precision,
            "burstMode": eachPotential.burstMode,
            "timeBetweenDrops": eachPotential.timeBetweenDrops
            }
            potentialsData.append(eachPotentialData)
        return potentialsData

    def loadJSONData(self, dataToLoad):
        self.velocities = self.loadJSONOfVelocities(dataToLoad) #dataToLoad
        self.temperatures = self.loadJSONOfTemperatures(dataToLoad)
        self.potentialsHydrogen = self.loadJSONOfPotentials(dataToLoad)

    def loadJSONOfVelocities(self, velocitiesToLoad):
        velocitiesList = []
        for eachElement in velocitiesToLoad['velocities']:
            newVelocity = Velocity([eachElement['objective'], eachElement['hours'], eachElement['minutes'], eachElement['seconds']])
            newVelocity.loadJSONMagnitude(velocitiesToLoad)
            newVelocity.direction = eachElement['direction']
            #print("VELOCITY: ", newVelocity.showInformation())
            velocitiesList.append(newVelocity)
        return velocitiesList

    def loadJSONOfTemperatures(self, temperaturesToLoad):
        temperaturesList = []
        for eachElement in temperaturesToLoad['temperatures']:
            newTemperature = Temperature([eachElement['objective'], eachElement['hours'], eachElement['minutes'], eachElement['seconds']])
            newTemperature.loadJSONMagnitude(temperaturesToLoad)
            newTemperature.pumpStep = eachElement['pumpStep']
            #print("TEMPERATURES: ", newTemperature.showInformation())
            temperaturesList.append(newTemperature)
        return temperaturesList

    def loadJSONOfPotentials(self, potentialsToLoad):
        potentialsList = []
        for eachElement in potentialsToLoad['potentialsHydrogen']:
            newPotential = PotentialHydrogen([eachElement['objective'], eachElement['hours'], eachElement['minutes'], eachElement['seconds']])
            newPotential.loadJSONMagnitude(potentialsToLoad)
            newPotential.burstMode = eachElement['burstMode']
            newPotential.timeBetweenDrops = eachElement['timeBetweenDrops']
            #print("POTENTIALS: ", newPotential.showInformation())
            potentialsList.append(newPotential)
        return potentialsList

    def getVelocityCustomizationData(self):
        customizationData = ["", "", "", "", ""]
        for eachVelocity in self.velocities:
            if(not str(eachVelocity.unit) in customizationData[0]):
                customizationData[0] = customizationData[0] + ","
            if(not str(eachVelocity.precision) in customizationData[1]):
                customizationData[1] = customizationData[1] + ","
            if(not str(eachVelocity.evolutionSlope) in customizationData[2]):
                customizationData[2] = customizationData[2] + ","
            if(not str(eachVelocity.direction) in customizationData[3]):
                customizationData[3] = customizationData[3] + ","
            if(not str(eachVelocity.dataInterval) in customizationData[4]):
                customizationData[4] = customizationData[4] + ","
        return customizationData

    def getTemperatureCustomizationData(self):
        customizationData = ["", "", "", "", ""]
        for eachTemperature in self.temperatures:
            if(not str(eachTemperature.unit) in customizationData[0]):
                customizationData[0] = customizationData[0] + ","
            if(not str(eachTemperature.precision) in customizationData[1]):
                customizationData[1] = customizationData[1] + ","
            if(not str(eachTemperature.pumpStep) in customizationData[2]):
                customizationData[2] = customizationData[2] + ","
            if(not str(eachTemperature.evolutionSlope) in customizationData[3]):
                customizationData[3] = customizationData[3] + ","
            if(not str(eachTemperature.dataInterval) in customizationData[4]):
                customizationData[4] = customizationData[4] + ","
        return customizationData

    def getPotentialCustomizationData(self):
        customizationData = ["", "", "", "", ""]
        for eachPotential in self.potentialsHydrogen:
            if(not str(eachPotential.unit) in customizationData[0]):
                customizationData[0] = customizationData[0] + ","
            if(not str(eachPotential.precision) in customizationData[1]):
                customizationData[1] = customizationData[1] + ","
            if(not str(eachPotential.burstMode) in customizationData[2]):
                customizationData[2] = customizationData[2] + ","
            if(not str(eachPotential.timeBetweenDrops) in customizationData[3]):
                customizationData[3] = customizationData[3] + ","
            if(not str(eachPotential.dataInterval) in customizationData[4]):
                customizationData[4] = customizationData[4] + ","
        return customizationData

    def getMagnitudeDuration(self, listOfMagnitude):
        durationTotal = [0, 0, 0]
        for eachMagnitude in listOfMagnitude:
            durationTotal[0] = durationTotal[0] + eachMagnitude.duration[0]
            durationTotal[1] = durationTotal[1] + eachMagnitude.duration[1]
            durationTotal[2] = durationTotal[2] + eachMagnitude.duration[2]
        return str(durationTotal[0])+" hs : "+str(durationTotal[1])+" min : "+str(durationTotal[2])+" sec"

    def getConditions(self):
        velocityConditions = self.getVelocityCustomizationData()
        temperatureConditions = self.getTemperatureCustomizationData()
        potentialConditions = self.getPotentialCustomizationData()
        conditionsData = ""
        if(velocityConditions[1]!="" and velocityConditions[2]!="" and velocityConditions[1]!="," and velocityConditions[2]!=","):
            conditionsData = conditionsData + "\nVEL: Precision "+velocityConditions[1]+" rpm and Slope "+velocityConditions[2]
        if(temperatureConditions[1]!="" and temperatureConditions[3]!="" and temperatureConditions[1]!="," and temperatureConditions[3]!=","):
            conditionsData = conditionsData + "\nTEM: Precision "+temperatureConditions[1]+" C and Slope "+temperatureConditions[3]
        if(potentialConditions[1]!="" and potentialConditions[2]!="" and potentialConditions[1]!="," and potentialConditions[2]!=","):
            conditionsData = conditionsData + "\nPOT: Precision "+potentialConditions[1]+" and Bursts of "+potentialConditions[2]+" Drops"
        return conditionsData
