import sys, time, os, serial
from datetime import date
from datetime import datetime
from datetime import timedelta

ser = serial.Serial()
ser.port = '/dev/ttyACM3' #'COM4' #'/dev/ttyACM1'
ser.baudrate = 9600
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE
ser.bytesize = serial.EIGHTBITS
ser.timeout = 12

FMT = '%H:%M:%S.%f'

def calculateLRC(input):
    lrc = ord(input[0])
    for i in range(1,len(input)):
        lrc += ord(input[i])
    return lrc

def checkConnectionSensor():
    sensorConnected = False
    val1 = ":01CN02CHSS"
    res = calculateLRC(val1[1:])
    lrcData = hex((((res^0xFF)+1)&0xFF))
    if(len(lrcData)==3):
        lrcData = str(lrcData[0:2]) + "0" + str(lrcData[3:4])
    dataToSend = val1+str(lrcData[2:4]).upper()+'\r\n'
    #ser.open()
    #time.sleep(2)
    ser.write(dataToSend.encode('ascii'))
    dataReceived = ser.read(15)
    if (isSensorWellConnected(dataReceived.decode('ascii'))):
        sensorConnected = True
    #ser.close()
    return sensorConnected

def isSensorWellConnected(dataConnection):
    print("DATA CONNECTION: ", dataConnection)
    if("OK" in dataConnection):
        return True
    else:
        return False

def checkConnectionController():
    controllerConnected = False
    val1 = ":01CN02CHCR"
    res = calculateLRC(val1[1:])
    lrcData = hex((((res^0xFF)+1)&0xFF))
    if(len(lrcData)==3):
        lrcData = str(lrcData[0:2]) + "0" + str(lrcData[3:4])
    dataToSend = val1+str(lrcData[2:4]).upper()+'\r\n'
    #ser.open()
    #time.sleep(2)
    ser.write(dataToSend.encode('ascii'))
    dataReceived = ser.read(15)
    if (isSensorWellConnected(dataReceived.decode('ascii'))):
        controllerConnected = True
    #ser.close()
    return controllerConnected

def checkPotentialModulesConnection():
    potentialConnection = 100
    isSensorConnectionRight = checkConnectionSensor()
    isControllerConnectionRight = checkConnectionController()
    if(isSensorConnectionRight):
        potentialConnection = potentialConnection + 10
    if(isControllerConnectionRight):
        potentialConnection = potentialConnection + 1
    return potentialConnection

def calibrateSensorMiddle():
    print("CALIBRATE MIDDLE")
    sensorCalibratedMiddle = False
    val1 = ":01CB02C7NT"
    res = calculateLRC(val1[1:])
    lrcData = hex((((res^0xFF)+1)&0xFF))
    if(len(lrcData)==3):
        lrcData = str(lrcData[0:2]) + "0" + str(lrcData[3:4])
    dataToSend = val1+str(lrcData[2:4]).upper()+'\r\n'
    #ser.open()
    #time.sleep(2)
    ser.write(dataToSend.encode('ascii'))
    dataReceived = ser.read(15)
    if (isSensorWellConnected(dataReceived.decode('ascii'))):
        sensorCalibratedMiddle = True
    #ser.close()
    return sensorCalibratedMiddle

def calibrateSensorLow():
    print("CALIBRATE LOW")
    sensorCalibratedLow = False
    val1 = ":01CB02C4AC"
    res = calculateLRC(val1[1:])
    lrcData = hex((((res^0xFF)+1)&0xFF))
    if(len(lrcData)==3):
        lrcData = str(lrcData[0:2]) + "0" + str(lrcData[3:4])
    dataToSend = val1+str(lrcData[2:4]).upper()+'\r\n'
    #ser.open()
    #time.sleep(2)
    ser.write(dataToSend.encode('ascii'))
    dataReceived = ser.read(15)
    if (isSensorWellConnected(dataReceived.decode('ascii'))):
        sensorCalibratedLow = True
    #ser.close()
    return sensorCalibratedLow

def calibrateSensorHigh():
    print("CALIBRATE HIGH")
    sensorCalibratedHigh = False
    val1 = ":01CB02C10B"
    res = calculateLRC(val1[1:])
    lrcData = hex((((res^0xFF)+1)&0xFF))
    if(len(lrcData)==3):
        lrcData = str(lrcData[0:2]) + "0" + str(lrcData[3:4])
    dataToSend = val1+str(lrcData[2:4]).upper()+'\r\n'
    #ser.open()
    #time.sleep(2)
    ser.write(dataToSend.encode('ascii'))
    dataReceived = ser.read(17)
    if (isSensorWellConnected(dataReceived.decode('ascii'))):
        sensorCalibratedHigh = True
    #ser.close()
    return sensorCalibratedHigh

def expulseLiquid(liquidToExpulse, dropsToExpulse):
    liquidExpulsed = False
    expulsionInformation = str(dropsToExpulse)
    if(dropsToExpulse<1000):
        expulsionInformation = "0"+str(dropsToExpulse)
    val1 = ":01EX03"+str(liquidToExpulse)+expulsionInformation #20"
    res = calculateLRC(val1[1:])
    lrcData = hex((((res^0xFF)+1)&0xFF))
    if(len(lrcData)==3):
        lrcData = str(lrcData[0:2]) + "0" + str(lrcData[3:4])
    dataToSend = val1+str(lrcData[2:4]).upper()+'\r\n'
    print("DATA TO SEND: ", dataToSend)
    #ser.open()
    #time.sleep(2)
    ser.write(dataToSend.encode('ascii'))
    ser.timeout = 65
    dataReceived = ser.read(15)
    ser.timeout = 12
    if (isSensorWellConnected(dataReceived.decode('ascii'))):
        liquidExpulsed = True
    ser.close()
    ser.open()
    return liquidExpulsed

def sendBurstsToPotentialController(ser, burstAcid, burstBase, dropsMode, intervalPerDrops, errorCount):

    isControlConfigured = False
    val1= ":01CR050"+str(burstAcid)+"0"+str(burstBase)+"0"+str(dropsMode)+"0"+str(intervalPerDrops)
    res = calculateLRC(val1[1:])
    lrcData = hex((((res^0xFF)+1)&0xFF))
    if(len(lrcData)==3):
        lrcData = str(lrcData[0:2]) + "0" + str(lrcData[3:4])
    dataToSend = val1+str(lrcData[2:4]).upper()+'\r\n'
    print("DATA TO SEND (BURSTS): ", dataToSend)
    ser.write(dataToSend.encode('ascii'))
    dataReceived = ser.read(15)
    potentialControlData = dataReceived.decode('ascii')
    print("POTENTIAL CONTROL DATA: ", potentialControlData)
    isControlConfigured = True #CHECK
    ser.close()
    ser.open()
    time.sleep(2)

    if(len(potentialControlData)>0):
        try:
            errorCount[1] = 0
            burstsDropped = float(potentialControlData[9:11])
            informationToCheck = potentialControlData[1:11]
            lrcReceived = potentialControlData[11:13]
            lrcToCalculate = calculateLRC(informationToCheck)
            lrcCalculated= hex((((lrcToCalculate^0xFF)+1)&0xFF))
            isControlConfigured = True #CHECK
            if(len(lrcCalculated)==3):
                lrcCalculated = str(lrcCalculated[0:2]) + "0" + str(lrcCalculated[3:4])

            if(("OK" in potentialControlData) and (int(burstsDropped)==int(burstAcid*dropsMode) or int(burstsDropped)==int(burstBase*dropsMode)) and (str(lrcCalculated[2:4]).lower() == lrcReceived)):
                isControlConfigured = True
                print("burstsDropped: ", int(burstsDropped))
                print("burstAcid*dropsMode: ", burstAcid*dropsMode)
                print("burstBase*dropsMode: ", burstBase*dropsMode)
                print("str(lrcCalculated[2:4]).lower(): ", str(lrcCalculated[2:4]).lower())
                print("lrcReceived: ", lrcReceived)
                errorCount[3] = 0
            else:
                errorCount[3] = errorCount[2] + 1
                print("MAL RECIBIDO CONTROL ACTUADOR")
        except ValueError:
            print("VALUE ERROR")
            isControlConfigured = True
    else:
        errorCount[1] = errorCount[1] + 1
        print("NO RECIBIDO NADA del CONTROLA CTUADOR")
        
    return [isControlConfigured, errorCount]

def readPotential(ser, errorCount): #LECTURA DE DATOS DEL SERIAL

    potentialActual = 0.0
    potentialWellReceived = False

    val1= ":01DT02PH01"
    res = calculateLRC(val1[1:])
    lrcData = hex((((res^0xFF)+1)&0xFF))
    if(len(lrcData)==3):
        lrcData = str(lrcData[0:2]) + "0" + str(lrcData[3:4])
    dataToSend = val1+str(lrcData[2:4]).upper()+'\r\n'
    print("DATA SEND: ", dataToSend)
    ser.write(dataToSend.encode('ascii'))
    answerPOTENTIAL = ser.read(17)
    print("DATA RECEIVED: ", answerPOTENTIAL)

    informationReceived = answerPOTENTIAL.decode("utf-8")
    if(len(informationReceived)>0):
        errorCount[1] = 0
        informationToCheck = informationReceived[1:13]
        lrcReceived = informationReceived[13:15]
        lrcToCalculate = calculateLRC(informationToCheck)
        lrcCalculated= hex((((lrcToCalculate^0xFF)+1)&0xFF))
        potentialActual = informationReceived[7:13] # CHECK
        potentialWellReceived = True
        if(len(lrcCalculated)==3):
            lrcCalculated = str(lrcCalculated[0:2]) + "0" + str(lrcCalculated[3:4])
        if(str(lrcCalculated[2:4]).lower() == lrcReceived):
            potentialActual = informationReceived[7:13] #[7:13]
            if(float(potentialActual)<2 or float(potentialActual)>12):
                errorCount[2] = errorCount[2] + 1
            else:
                errorCount[2] = 0
            potentialWellReceived = True
            errorCount[0] = 0
            print("POTENCIAL CORRECTO")
        else:
            potentialActual = informationReceived[7:13] #[7:13]
            potentialWellReceived = True
            errorCount[0] = errorCount[0] + 1
            print("POTENCIAL NO CORRECTO")
    else:
        errorCount[1] = errorCount[1] + 1
        ser.close()
        ser.open()
        time.sleep(2)
        print("POTENCIAL NO RECIBIDO")

    print("CURRENT INFO: ", informationReceived)
    print("ERROR COUNT: ", errorCount)

    return [potentialActual, potentialWellReceived, errorCount]

def getBurstsToDrop(errorPotential, sensitivity):

    bursts = 0
    print("ERROR POTENTIAL: ", errorPotential)
    print("SENSITIVITY: ", sensitivity)
    if(sensitivity<=20):
        if(abs(errorPotential)<=0.2):
            bursts = 2
        else:
            if(abs(errorPotential)<=0.5):
                bursts = 3
            else:
                if(abs(errorPotential)<=1):
                    bursts = 4
                else:
                    bursts = 5
    else:
        if(abs(errorPotential)<=0.2):
            bursts = 1
        else:
            if(abs(errorPotential)<=0.5):
                bursts = 2
            else:
                if(abs(errorPotential)<=1):
                    bursts = 3
                else:
                    if(abs(errorPotential)<=2):
                        bursts = 4
                    else:
                        bursts = 5
    return bursts

def savePotentialData(potentialInformation, currentStr, currentFileDay, currentFileTime, controlUnit, dataInterval, intervalCount, objectivePotential):

    newTime = datetime.today()
    newTimeStr = newTime.strftime("%H:%M:%S.%f")
    tdelta = datetime.strptime(newTimeStr, FMT) - datetime.strptime(currentStr, FMT)

    if(tdelta.seconds>=dataInterval*intervalCount):

        if(currentFileTime<=99999):
            currentFileStr = "0"+str(currentFileTime)
        else:
            currentFileStr = str(currentFileTime)

        currentPotential = str(potentialInformation[0]) #str(potentialInformation)[7:13]
        currentAcidDrops = str(potentialInformation[1])  #str(potentialInformation)[13:20]
        currentBaseDrops = str(potentialInformation[2]) #str(potentialInformation)[20:27]

        volumeAcidToSave = float(currentAcidDrops)*66.67*0.001 # mL
        volumeBaseToSave = float(currentBaseDrops)*66.67*0.001 # mL

        if(controlUnit==1): # cui
            volumeAcidToSave = float(volumeAcidToSave/16.387)
            volumeBaseToSave = float(volumeBaseToSave/16.387)
        if(controlUnit==2): # Litres
            volumeAcidToSave = float(volumeAcidToSave/1000)
            volumeBaseToSave = float(volumeBaseToSave/1000)

        filename = "ControlData/PotentialHydrogen/DATA_Log/"+str(currentFileDay)+"_"+str(currentFileStr)+"_POT.txt" #"ControlData/PotentialHydrogen/DATA_Log/"+str(fileTime.strftime("%Y%m%d_%I%M%S"))+"_POT.txt"
        intervalCount = intervalCount+1

        with open(filename, 'a') as registerPotentialData:
            registerPotentialData.write(str(currentPotential)+','+str(objectivePotential)+','+str(volumeAcidToSave)+','+str(volumeBaseToSave)+','+str(tdelta.seconds)+','+str(tdelta.microseconds)+'\n')
            registerPotentialData.close()

    return intervalCount

def configurePotentialPorts(ser, potentialPort):
    ser.port = '/dev/ttyACM3'
    if(potentialPort==1):
        ser.port = '/dev/ttyACM0'
    elif(potentialPort==2):
        ser.port = '/dev/ttyACM1'
    elif(potentialPort==3):
        ser.port = '/dev/ttyACM2'
    elif(potentialPort==4):
        ser.port = '/dev/ttyACM3'
    elif(potentialPort==5):
        ser.port = '/dev/ttyUSB0'
    elif(potentialPort==6):
        ser.port = '/dev/ttyUSB1'
    elif(potentialPort==7):
        ser.port = '/dev/ttyUSB2'
    elif(potentialPort==8):
        ser.port = '/dev/ttyUSB3'
    elif(potentialPort==9):
        ser.port = '/dev/ttyAMA0'
    elif(potentialPort==10):
        ser.port = '/dev/ttyAMA1'

def childProcess(manager, potentialObjective, duration):

    isDataRequested = False
    potentialStep = 0
    dataCount = 0
    configurePotentialPorts(ser, manager[22])
        
    ser.open()

    while(manager[0]!=0):

        try:
            exactT = datetime.today()
            exactStr = exactT.strftime("%H:%M:%S.%f")
            print("PH CONTROL WAITING")
            intervalCount = 1
            isControlStopped = True
            errorCount = [0, 0, 0, 0] # [REDUNDANCIA, TIMEOUT, FALLOS SENSADO PH, FALLOS BOMBAS]
            manager[21] = 0
            manager[23] = 0
            time.sleep(1)

            if(manager[0]==2):

                manager[0] = checkPotentialModulesConnection()

            if(manager[0]==3):
                isCalibratedMiddle = calibrateSensorMiddle()
                if(isCalibratedMiddle):
                    manager[0] = 31
                else:
                    manager[0] = 30

            if(manager[0]==4):
                isCalibratedLow = calibrateSensorLow()
                if(isCalibratedLow):
                    manager[0] = 41
                else:
                    manager[0] = 40

            if(manager[0]==5):
                isCalibratedHigh = calibrateSensorHigh()
                if(isCalibratedHigh):
                    manager[0] = 51
                else:
                    manager[0] = 50

            if(manager[0]==6):
                acidDropsToExpulse = manager[8]
                hasAcidBeenExpulsed = expulseLiquid("AC", acidDropsToExpulse)
                if(hasAcidBeenExpulsed):
                    manager[0] = 61
                else:
                    manager[0] = 60

            if(manager[0]==7):
                baseDropsToExpulse = manager[8]
                hasBaseBeenExpulsed = expulseLiquid("BA", baseDropsToExpulse)
                if(hasBaseBeenExpulsed):
                    manager[0] = 71
                else:
                    manager[0] = 70

            if(manager[0]==12):
                #ser.open()
                #time.sleep(2)
                val1= ":01TS02PH05"
                res = calculateLRC(val1[1:])
                lrcData = hex((((res^0xFF)+1)&0xFF))
                if(len(lrcData)==3):
                    lrcData = str(lrcData[0:2]) + "0" + str(lrcData[3:4])
                dataToSend = val1+str(lrcData[2:4]).upper()+'\r\n'
                ser.write(dataToSend.encode('ascii'))
                answerPOTENTIAL = ser.read(17)
                print("DATA RECEIVED: ", answerPOTENTIAL)
                informationReceived = answerPOTENTIAL.decode("utf-8")
                if(len(informationReceived)>0 and not "ERROR" in informationReceived):
                    manager[11] = int(float(str(informationReceived[7:13]))*1000)
                answerPOTENTIAL = ser.read(17)
                print("DATA RECEIVED: ", answerPOTENTIAL)
                informationReceived = answerPOTENTIAL.decode("utf-8")
                if(len(informationReceived)>0 and not "ERROR" in informationReceived):
                    manager[12] = int(float(str(informationReceived[7:13]))*1000)
                answerPOTENTIAL = ser.read(17)
                print("DATA RECEIVED: ", answerPOTENTIAL)
                informationReceived = answerPOTENTIAL.decode("utf-8")
                if(len(informationReceived)>0 and not "ERROR" in informationReceived):
                    manager[13] = int(float(str(informationReceived[7:13]))*1000)
                answerPOTENTIAL = ser.read(17)
                print("DATA RECEIVED: ", answerPOTENTIAL)
                informationReceived = answerPOTENTIAL.decode("utf-8")
                if(len(informationReceived)>0 and not "ERROR" in informationReceived):
                    manager[14] = int(float(str(informationReceived[7:13]))*1000)
                answerPOTENTIAL = ser.read(17)
                print("DATA RECEIVED: ", answerPOTENTIAL)
                informationReceived = answerPOTENTIAL.decode("utf-8")
                if(len(informationReceived)>0 and not "ERROR" in informationReceived):
                    manager[15] = int(float(str(informationReceived[7:13]))*1000)
                #ser.close()
                manager[0] = 1

            if(manager[0]==13):
                val1= ":01VS01PH"
                res = calculateLRC(val1[1:])
                lrcData = hex((((res^0xFF)+1)&0xFF))
                if(len(lrcData)==3):
                    lrcData = str(lrcData[0:2]) + "0" + str(lrcData[3:4])
                dataToSend = val1+str(lrcData[2:4]).upper()+'\r\n'
                ser.write(dataToSend.encode('ascii'))
                answerVersionPOT = ser.read(15)
                print("DATA RECEIVED: ", answerVersionPOT)
                informationReceived = answerVersionPOT.decode("utf-8")
                if(len(informationReceived)>0 and not "ERROR" in informationReceived):
                    manager[16] = int(float(str(informationReceived[7:11]))*100)
                manager[0] = 1

            while(manager[1]!=0):

                if(manager[2]==3 or manager[2]==4):
                    manager[2] = 0

                objectivePotential = float(potentialObjective[potentialStep]/10)
                objectiveTime = duration[potentialStep]
                fileTime = manager[4]
                fileDay = manager[5]
                controlUnit = manager[6]
                controlPrecision = float(int(manager[7])*0.001)
                #dropsPerBurst = manager[8] # NO USAGE
                intervalPerDrops = int(manager[9]) #float(int(manager[9])*0.001)
                dataInterval = manager[10]
                burstMode = manager[11]

                pHPrevious = 0.0
                acidDropsQuantity = 1
                baseDropsQuantity = 1
                isFirstData = True
                bursts = 1

                stepBeginTime = datetime.today()
                stepBeginTimeStr = stepBeginTime.strftime("%H:%M:%S.%f")

                currentTime = datetime.today()
                currentTimeStr = currentTime.strftime("%H:%M:%S.%f")

                timeDifference = datetime.strptime(currentTimeStr, FMT) - datetime.strptime(stepBeginTimeStr, FMT)
                currentDuration = timeDifference.seconds + timeDifference.microseconds*(0.000001)

                #ser.open()

                while(currentDuration<=objectiveTime and manager[2]==0):

                    returnedData = readPotential(ser, errorCount)

                    potentialInformation = float(returnedData[0])

                    errorCount = returnedData[2]

                    print("DATA POTENTIAL LUEGO DE RETURNED: ", potentialInformation)

                    isDataRequested = returnedData[1]

                    if(errorCount[0]>5 or errorCount[1]>10 or errorCount[2]>10 or errorCount[3]>10):
                        potentialInformation = objectivePotential
                        if(errorCount[0]>5):
                            manager[23] = 1
                        if(errorCount[1]>10):
                            manager[23] = 2
                        if(errorCount[2]>10):
                            manager[23] = 3
                        if(errorCount[3]>10):
                            manager[23] = 4
                    else:
                        manager[23] = 0

                    print("MANAGER[21]: ", manager[21])
                    print("MANAGER[23]: ", manager[23])

                    if(isDataRequested):

                        intervalCount = savePotentialData([potentialInformation, acidDropsQuantity, baseDropsQuantity], exactStr, fileDay, fileTime, controlUnit, dataInterval, intervalCount, objectivePotential)

                        if(not isFirstData and manager[20]==0):
                            print("ENTRA IF IS FIRST DATA")
                            errorPotential = potentialInformation - objectivePotential
                            print("BURSTMODE: ", burstMode)
                            sensitivity = abs(1000*(potentialInformation - pHPrevious)/(bursts*burstMode))
                            bursts = getBurstsToDrop(errorPotential, sensitivity)
                            print("GET BURSTS TO DROP: ", bursts)

                            if(errorPotential>controlPrecision):
                                returnedBursts = sendBurstsToPotentialController(ser, bursts, 0, burstMode, intervalPerDrops, errorCount)
                                hasAcidBeenDropped = returnedBursts[0]
                                errorCount = returnedBursts[1]
                                if(hasAcidBeenDropped):
                                    acidDropsQuantity = acidDropsQuantity + bursts*burstMode;
                                else:
                                    print("NO TIRA GOTAS ACIDO")
                            if(errorPotential<=(controlPrecision*(-1))):
                                returnedBursts = sendBurstsToPotentialController(ser, 0, bursts, burstMode, intervalPerDrops, errorCount)
                                hasBaseBeenDropped = returnedBursts[0]
                                errorCount = returnedBursts[1]
                                if(hasBaseBeenDropped):
                                    baseDropsQuantity = baseDropsQuantity + bursts*burstMode;
                                else:
                                    print("NO TIRA GOTAS BASE")
                        
                        isFirstData = False
                        pHPrevious = potentialInformation
                        #time.sleep(2)

                    if(manager[20]==1):
                        burstModeManual = manager[17]
                        burstsManual = manager[19]
                        if(manager[18]==1):
                            manager[18] = 0
                            returnedBursts = sendBurstsToPotentialController(ser, burstsManual, 0, burstModeManual, intervalPerDrops, errorCount)
                            hasAcidBeenDropped = returnedBursts[0]
                            errorCount = returnedBursts[1]
                            if(hasAcidBeenDropped):
                                acidDropsQuantity = acidDropsQuantity + burstsManual*burstModeManual;
                        if(manager[18]==2):
                            manager[18] = 0
                            returnedBursts = sendBurstsToPotentialController(ser, 0, burstsManual, burstModeManual, intervalPerDrops, errorCount)
                            hasBaseBeenDropped = returnedBursts[0]
                            errorCount = returnedBursts[1]
                            if(hasBaseBeenDropped):
                                baseDropsQuantity = baseDropsQuantity + burstsManual*burstModeManual;
                            
                    controlUnit = manager[6]
                    controlPrecision = float(int(manager[7])*0.001)
                    intervalPerDrops = int(manager[9]) #float(int(manager[9])*0.001)
                    dataInterval = manager[10]
                    burstMode = manager[11]

                    currentTime = datetime.today()
                    currentTimeStr = currentTime.strftime("%H:%M:%S.%f")

                    timeDifference = datetime.strptime(currentTimeStr, FMT) - datetime.strptime(stepBeginTimeStr, FMT)
                    currentDuration = timeDifference.seconds + timeDifference.microseconds*(0.000001)

                if(manager[2]==0 or manager[2]==4):

                    potentialStep = potentialStep + 1
                    manager[3] = potentialStep

                    #ser.close()

                if(manager[2]==3):

                    potentialStep = potentialStep - 1

                    if(potentialStep<0):

                        potentialStep = 0

                    manager[3] = potentialStep

                    #ser.close()

                if(manager[2]==2):

                    manager[1] = 0
                    #isDataRequested = False

                    #ser.close()

                if((potentialObjective[potentialStep]==0 and duration[potentialStep]==0) or manager[2]==1):

                    manager[1]=0

                    #ser.close()

                    potentialStep = 0

                    isDataRequested = False

                    print("CONTROL END")


        except IOError:
            manager[1] = 0
            ser.close()
            isDataRequested = False
            manager[21] = 1

    if(manager[21]==0):
        ser.close()