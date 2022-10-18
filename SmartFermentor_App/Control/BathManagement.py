import sys
import serial
import os
import time
from datetime import date
from datetime import datetime

ser = serial.Serial()
ser.port = '/dev/ttyUSB1' #CHECK PORT IN RASPBERRY
ser.baudrate = 19200
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE
ser.bytesize = serial.EIGHTBITS
ser.timeout = 10

def saveStatus (deviceStatus, statusMotive) :
    folderName = "ControlData/Temperature/STATUS_Log"
    if not os.path.exists(folderName):
        os.makedirs(folderName)
    monthAndYear = datetime.now().time().strftime("%B_%Y")
    fileName = folderName+"/BATH_"+monthAndYear+".txt"
    timeNow = datetime.now().time().strftime("%H:%M:%S")
    if statusMotive=="BEGIN":
        contentToWrite = timeNow + " - Bath Circulator starting or changing Temp SV: " + deviceStatus
    if statusMotive=="ENDING":
        contentToWrite = timeNow + " - Bath Circulator ending or changing Temp SV: " + deviceStatus
    if statusMotive=="ERROR":
        contentToWrite = timeNow + " - ERROR produced in BATH at GETTING Data: " + deviceStatus
    with open(fileName, 'a') as registerStatus:
        registerStatus.write(contentToWrite+'\n')
        registerStatus.close()

def saveError (deviceError, errorMotive) :
    folderName = "ControlData/Temperature/ERROR_Log"
    if not os.path.exists(folderName):
        os.makedirs(folderName)
    monthAndYear = datetime.now().time().strftime("%B_%Y")
    fileName = folderName+"/BATH_"+monthAndYear+".txt"
    timeNow = datetime.now().time().strftime("%H:%M:%S")
    if errorMotive=="SETTING":
        contentToWrite = timeNow + " - Communication FAILED to Initiate with Serial: " + deviceError
    if errorMotive=="TEMPERATURE":
        contentToWrite = timeNow + " - Device FAILED to GET Temperature Data: " + deviceError
    if errorMotive=="OFFSET":
        contentToWrite = timeNow + " - Device FAILED to GET Offset Data: " + deviceError
    if errorMotive=="TIME":
        contentToWrite = timeNow + " - Device FAILED to GET Time Data: " + deviceError
    if errorMotive=="DELAY":
        contentToWrite = timeNow + " - Device FAILED to GET Delay Data: " + deviceError
    with open(fileName, 'a') as registerError:
        registerError.write(contentToWrite+'\n')
        registerError.close()

def getSettingTimeWhenLessThan10Hours(ser, timerSetHours, timerSetMinutes):
    if(timerSetMinutes<10):
        settingTime = '#06Ot0'+str(timerSetHours)+'0'+str(timerSetMinutes)
    else:
        settingTime = '#06Ot0'+str(timerSetHours)+str(timerSetMinutes)
    return settingTime

def getSettingTimeWhenMoreThan10Hours(ser, timerSetHours, timerSetMinutes):
    if(timerSetMinutes<10):
        settingTime = '#06Ot'+str(timerSetHours)+'0'+str(timerSetMinutes)
    else:
        settingTime = '#06Ot'+str(timerSetHours)+str(timerSetMinutes)

def setTimer (ser, timerSetHours, timerSetMinutes) :
    if(timerSetHours<10):
        settingTime = getSettingTimeWhenLessThan10Hours(ser, timerSetHours, timerSetMinutes)
    else:
        settingTime = getSettingTimeWhenMoreThan10Hours(ser, timerSetHours, timerSetMinutes)
    settingTimeBinary = settingTime.encode("utf-8")
    ser.write(settingTimeBinary)

def setTemperature (ser, temperatureSet) :
    if temperatureSet>=1000:
        settingTemperature = '#08TS00'+str(temperatureSet)
        settingTempBinary = settingTemperature.encode("utf-8")
        ser.write(settingTempBinary)
    if temperatureSet<1000 and temperatureSet!=0:
        settingTemperature = '#08TS000'+str(temperatureSet)
        settingTempBinary = settingTemperature.encode("utf-8")
        ser.write(settingTempBinary)
    if temperatureSet==0:
        settingTemperature = '#08TS000000'
        settingTempBinary = settingTemperature.encode("utf-8")
        ser.write(settingTempBinary)

def setPump (ser, pumpStep) :
    settingPump = '#06PS000'+str(pumpStep)
    settingPumpBinary = settingPump.encode("utf-8")
    ser.write(settingPumpBinary)

def startTimer (ser) :
    ser.write(b'#03OTS')

def startTemp (ser) :
    ser.write(b'#02OP')

def startPump (ser) :
    ser.write(b'#04MS')

def sendReceivePackageSetting (ser, contentWrite, bytesRead, bytesStep, magnitudMeasured) :
    ser.write(contentWrite)
    answer = ser.readline(bytesRead)
    stepCode = answer[0:bytesStep:1]
    contentRead = answer[bytesStep:bytesRead:1]
    return stepCode

def idleStateSetting (ser, n) :
    print("ESTOY EN IDLE")
    if n==0:
        return 1  
    else:
        ser.write(b'#02id') #'#02id' - IDENTIFICACION
        answerID = ser.readline(7)
        if answerID == b'#04id05':
            ser.write(b'#02ER') #'#02ER' - RELLENO
            answerRELL = ser.readline(15)
            if answerRELL == b'#12ER0000000000':
                ser.write(b'#02OA') #'#02OA' - CODIGO DE ACTIVIDAD
                answerCODE = ser.readline(14)
                stepCode = answerCODE[0:5:1]
                if stepCode == b'#11OA':
                    stepCode = sendReceivePackageSetting (ser, b'#02tp', 11, 7, "TEMP_CURRENT")
                    if stepCode == b'#08tp00':
                        stepCode = sendReceivePackageSetting (ser, b'#02ts', 11, 7, "TEMP_OBJECTIVE")
                        if stepCode == b'#08ts00':
                            stepCode = sendReceivePackageSetting (ser, b'#02to', 10, 6, "OFFSET")
                            if stepCode == b'#07to0':
                                stepCode = sendReceivePackageSetting (ser, b'#03ots', 10, 6, "TIME_OBJECTIVE")
                                if stepCode == b'#07ots':
                                    stepCode = sendReceivePackageSetting (ser, b'#03otp', 10, 6, "TIME_CURRENT")
                                    if stepCode == b'#07otp':
                                        stepCode = sendReceivePackageSetting (ser, b'#03dts', 10, 6, "DELAY_OBJECTIVE")
                                        if stepCode == b'#07dts':
                                            stepCode = sendReceivePackageSetting (ser, b'#03dtp', 10, 6, "DELAY_CURRENT")
                                            if stepCode == b'#07dtp':
                                                idleStateSetting(ser, n-1)
                                            else: #Delay Actual Time else
                                                saveError("Couldn't Get CURRENT DELAY Time", "DELAY")
                                                return analizeStepCode(stepCode)
                                        else: #Delay Objective Time else
                                            saveError("Couldn't Get OBJECTIVE DELAY Time", "DELAY")
                                            return analizeStepCode(stepCode)
                                    else: #Actual Time else
                                        saveError("Couldn't Get CURRENT TIME", "TIME")
                                        return analizeStepCode(stepCode)
                                else: #Objective Time else
                                    saveError("Couldn't Get OBJECTIVE TIME", "TIME")
                                    return analizeStepCode(stepCode)
                            else: #Offset Temperature else
                                saveError("Couldn't Get OFFSET TEMPERATURE", "OFFSET")
                                return analizeStepCode(stepCode)
                        else: #Objective Temperature else
                            saveError("Couldn't Get OBJECTIVE TEMPERATURE", "TEMPERATURE")
                            return analizeStepCode(stepCode)
                    else: #Actual Temperature else
                        saveError("Couldn't Get CURRENT TEMPERATURE", "TEMPERATURE")
                        return analizeStepCode(stepCode)
                else: #Activity else
                    saveError("Couldn't Get ACTIVITY CODE", "TEMPERATURE")
                    return analizeStepCode(stepCode)
            else: #Filling else
                saveError("Couldn't Get FILLING INFO", "TEMPERATURE")
                return analizeStepCode(stepCode)
        else: #Identification else
            saveError("Couldn't Get IDENTIFICATION INFO", "TEMPERATURE")
            return analizeStepCode(stepCode)

         

def endFrame(ser):
    ser.write(b'#02id') #'#02id' - IDENTIFICACION
    ser.write(b'#02ER') #'#02ER' - RELLENO
    answerRELL = ser.readline(15)
    if answerRELL == b'#12ER0000000000':
        ser.write(b'#02OA') #'#02OA' - CODIGO DE ACTIVIDAD
        answerCODE = ser.readline(14)
        stepCode = answerCODE[0:5:1]
        if stepCode == b'#11OA':
            stepCode = sendReceivePackageSetting (ser, b'#02tp', 11, 7, "/TemperaturaActual")
            if stepCode == b'#08tp00':
                stepCode = sendReceivePackageSetting (ser, b'#02ts', 11, 7, "/TemperaturaObjetivo")
                if stepCode == b'#08ts00':
                    stepCode = sendReceivePackageSetting (ser, b'#02to', 10, 6, "/TiempoOffset")
                    if stepCode == b'#07to0':
                        stepCode = sendReceivePackageSetting (ser, b'#03ots', 10, 6, "/TiempoObjetivo")
                        if stepCode == b'#07ots':
                            stepCode = sendReceivePackageSetting (ser, b'#03otp', 10, 6, "/TiempoActual")
                            if stepCode == b'#07otp':
                                stepCode = sendReceivePackageSetting (ser, b'#03dts', 10, 6, "/TiempoDelayObjetivo")
                                if stepCode == b'#07dts':
                                    stepCode = sendReceivePackageSetting (ser, b'#03dtp', 10, 6, "/TiempoDelayActual")
                                    return 1
                                else: #Delay Objective Time else
                                    saveError("Couldn't Get OBJECTIVE DELAY Time", "DELAY")
                                    return analizeStepCode(stepCode)
                            else: #Actual Time else
                                saveError("Couldn't Get CURRENT TIME", "TIME")
                                return analizeStepCode(stepCode)
                        else: #Objective Time else
                            saveError("Couldn't Get OBJECTIVE TIME", "TIME")
                            return analizeStepCode(stepCode)
                    else: #Offset Temperature else
                        saveError("Couldn't Get OFFSET TEMPERATURE", "OFFSET")
                        return analizeStepCode(stepCode)
                else: #Objective Temperature else
                    saveError("Couldn't Get OBJECTIVE TEMPERATURE", "TEMPERATURE")
                    return analizeStepCode(stepCode)
            else: #Actual Temperature else
                saveError("Couldn't Get CURRENT TEMPERATURE", "TEMPERATURE")
                return analizeStepCode(stepCode)
        else: #Activity else
            saveError("Couldn't Get ACTIVITY CODE", "SETTING")
            return analizeStepCode(stepCode)
    else: #Filling else
        saveError("Couldn't Get FILLING INFO", "SETTING")
        return analizeStepCode(stepCode)


#settingEnd: beginManager[0]
#timeObjective Hours: beginManager[1]
#timeObjective Minutes: beginManager[2]
#temperatureObjective: beginManager[3]
#pumpObjective: beginManager[4]

def bathBeginning(beginManager, errorCount): 

    timerInitialized = False
    ser.open()
    print("Init Starting")
    timerObjectiveHours = beginManager[1]
    timerObjectiveMinutes = beginManager[2]

    timerStatusSet = 1
    timerStatusStart = 1

    if(int(timerObjectiveHours) + int(timerObjectiveMinutes) != 0):
        setTimer(ser, timerObjectiveHours, timerObjectiveMinutes) # TIMER in MINUTES = Max 99:99
        timerStatusSet = idleStateSetting(ser,2) #Frames between SetTimer and SetTemperature
        if(timerStatusSet==0):
            errorCount[0] = errorCount[0]+1
    
    tempObjetive = int(beginManager[3]*100)
    setTemperature(ser, tempObjetive) #HEAT or REF = Temperature Objective
    tempStatusSet = idleStateSetting(ser, 2) #Frames between SetTemperature and SetPump

    pumpObjective = int(beginManager[4])
    setPump(ser, pumpObjective) #Pump Step = 5 (Max)
    pumpStatusSet = idleStateSetting(ser, 2) #Frames between SetPump and StartTimer or StartTemp

    if(int(timerObjectiveHours) + int(timerObjectiveMinutes) != 0):
        startTimer(ser)
        timerStatusStart = idleStateSetting(ser, 2) #Frames between StartTimer and StartTemp
        if(timerStatusStart==0):
            errorCount[0] = errorCount[0]+1
        timerInitialized = True

    startTemp(ser)
    tempStatusStart = idleStateSetting(ser, 2) #Frames between StartTemp and StartPump
    startPump(ser)
    pumpStatusStartEnd = endFrame(ser)
    pumpStatusStart = idleStateSetting(ser, 1) #Frames between StartPump and Next Instruction
    if(pumpStatusStart==0 or pumpStatusStartEnd==0 or tempStatusStart==0 or pumpStatusSet==0 or tempStatusSet==0):
        errorCount[0] = errorCount[0]+1
    else:
        saveStatus("Temp: "+str(beginManager[3])+"; Pump: "+str(beginManager[4]), "BEGIN")
        errorCount[0] = 0
    ser.close()
    beginManager[0] = 1
    return [timerInitialized, 7, errorCount] #timerStatusSet+tempStatusSet+pumpStatusSet+timerStatusStart+tempStatusStart+pumpStatusStartEnd+pumpStatusStart]


def sendReceivePackageData (ser, contentWrite, bytesRead, bytesStep, magnitudMeasured, dataBath, posData) :
    ser.write(contentWrite)
    answer = ser.readline(bytesRead)
    stepCode = answer[0:bytesStep:1]
    contentRead = answer[bytesStep:bytesRead:1].decode("utf-8")
    if(posData == 0 or posData == 1):
        dataBath[posData] = round(float(contentRead)/100,2)
    else:
        dataBath[posData] = round(float(contentRead),2)
    #saveData(contentRead, magnitudMeasured);
    return stepCode

def analizeStepCode(stepCode):
    if(len(stepCode)>0):
        return 0
    else:
        return -1

def idleStateData (ser, dataBath) :
    
    ser.write(b'#02id') #'#02id' - IDENTIFICACION
    answerID = ser.readline(7)
    if answerID == b'#04id05':
        ser.write(b'#02ER') #'#02ER' - RELLENO
        answerRELL = ser.readline(15)
        if answerRELL == b'#12ER0000000000':
            ser.write(b'#02OA') #'#02OA' - CODIGO DE ACTIVIDAD
            answerCODE = ser.readline(14)
            stepCode = answerCODE[0:5:1]
            if stepCode == b'#11OA':
                stepCode = sendReceivePackageData (ser, b'#02tp', 11, 7, "TEMP_CURRENT", dataBath, 0)
                if stepCode == b'#08tp00':
                    stepCode = sendReceivePackageData (ser, b'#02ts', 11, 7, "TEMP_OBJECTIVE", dataBath, 1)
                    if stepCode == b'#08ts00':
                        stepCode = sendReceivePackageData (ser, b'#02to', 10, 6, "OFFSET", dataBath, 2)
                        if stepCode == b'#07to0':
                            stepCode = sendReceivePackageData (ser, b'#03ots', 10, 6, "TIME_OBJECTIVE", dataBath, 3)
                            if stepCode == b'#07ots':
                                stepCode = sendReceivePackageData (ser, b'#03otp', 10, 6, "TIME_CURRENT", dataBath, 4)
                                if stepCode == b'#07otp':
                                    stepCode = sendReceivePackageData (ser, b'#03dts', 10, 6, "DELAY_OBJECTIVE", dataBath, 5)
                                    if stepCode == b'#07dts':
                                        stepCode = sendReceivePackageData (ser, b'#03dtp', 10, 6, "DELAY_CURRENT", dataBath, 6)
                                        if stepCode == b'#07dtp':
                                            return 1
                                        else: #Delay Actual Time else
                                            saveError("Couldn't Get CURRENT DELAY Time", "DELAY")
                                            return analizeStepCode(stepCode)
                                    else: #Delay Objective Time else
                                        saveError("Couldn't Get OBJECTIVE DELAY Time", "DELAY")
                                        return analizeStepCode(stepCode)
                                else: #Actual Time else
                                    saveError("Couldn't Get CURRENT TIME", "TIME")
                                    return analizeStepCode(stepCode)
                            else: #Objective Time else
                                saveError("Couldn't Get OBJECTIVE TIME", "TIME")
                                return analizeStepCode(stepCode)
                        else: #Offset Temperature else
                            saveError("Couldn't Get OFFSET TEMPERATURE", "OFFSET")
                            return analizeStepCode(stepCode)
                    else: #Objective Temperature else
                        saveError("Couldn't Get OBJECTIVE TEMPERATURE", "TEMPERATURE")
                        return analizeStepCode(stepCode)
                else: #Actual Temperature else
                    saveError("Couldn't Get CURRENT TEMPERATURE", "TEMPERATURE")
                    return analizeStepCode(stepCode)
            else: #Activity else
                saveError("Couldn't Get ACTIVITY CODE", "TEMPERATURE")
                return analizeStepCode(stepCode)
        else: #Filling else
            saveError("Couldn't Get FILLING INFO", "TEMPERATURE")
            return analizeStepCode(stepCode)
    else: #Identification else
        saveError("Couldn't Get IDENTIFICATION INFO", "TEMPERATURE")
        return analizeStepCode(stepCode)

                                            
    


#getTemp: bathManager[9]
#dataCaught: bathManager[5]
#dataBath: bathInformation

def checkErrorCount(bathManager, errorCount):
    if(errorCount[0]>5):
        bathManager[11] = 1
    elif(errorCount[1]>5):
        bathManager[11] = 2
    elif(errorCount[2]>10):
        bathManager[11] = 3
    else:
        bathManager[11] = 0

def bathData(bathManager, bathInformation, errorCount):

    ser.open()
    gettingData=1
    tempPreviousBath = 25.00
    while(bathManager[9]==1):
        bathManager[5] = 0
        gettingData = idleStateData(ser, bathInformation)
        if(gettingData==0):
            errorCount[0] = errorCount[0]+1
            checkErrorCount(bathManager, errorCount)
        else:
            errorCount[0] = 0
        if(gettingData==-1):
            errorCount[1] = errorCount[1]+1
            checkErrorCount(bathManager, errorCount)
        else:
            errorCount[1] = 0
        if(bathInformation[0]>98.00 or bathInformation[0]<10.00 or abs(bathInformation[0]-tempPreviousBath)>5):
            errorCount[2] = errorCount[2]+1
            checkErrorCount(bathManager, errorCount)
        else:
            errorCount[2] = 0
        tempPreviousBath = bathInformation[0]
        print("Temp in Get: ", bathInformation[0])
        bathManager[5] = 1
        time.sleep(1)

    ser.close()
    return [gettingData, errorCount]


def endTimer (ser) :
    ser.write(b'#03OTQ')

def endTemp (ser) :
    ser.write(b'#02OQ')

def endPump (ser) :
    ser.write(b'#04MQ')

def bathEnding(bathManager, timerInitialized, errorCount):

    #if (ser.isOpen()):
    #    print("ESTA ABIERTO EN END")
    timerStatus = 1
    isTimerRunning = True
    ser.open()
    if(timerInitialized):
        endTimer(ser)
        timerStatus = idleStateSetting(ser, 2) #Frames between EndTimer and Next Instruction
        if(timerStatus==0):
            errorCount[0] = errorCount[0]+1
        isTimerRunning = False
            
    endTemp(ser)
    tempStatus = idleStateSetting(ser, 2) #Frames between EndTemp and Next Instruction
    
    endPump (ser)
    pumpStatusEnd = endFrame(ser)
    pumpStatus = idleStateSetting(ser, 2) #Frames between EndPump and Next Instruction
    
    bathManager[0] = 0
    ser.close()
    if(tempStatus==0 or pumpStatusEnd==0 or pumpStatus==0):
        errorCount[0] = errorCount[0]+1
    else:
        saveStatus("Successful", "ENDING")
        errorCount[0] = 0
    return [isTimerRunning, 4, errorCount] #timerStatus+tempStatus+pumpStatusEnd+pumpStatus]

def configureBathPort(ser, bathPort):
    ser.port = '/dev/ttyUSB1'
    if(bathPort==1):
        ser.port = '/dev/ttyACM0'
    elif(bathPort==2):
        ser.port = '/dev/ttyACM1'
    elif(bathPort==3):
        ser.port = '/dev/ttyACM2'
    elif(bathPort==4):
        ser.port = '/dev/ttyACM3'
    elif(bathPort==5):
        ser.port = '/dev/ttyUSB0'
    elif(bathPort==6):
        ser.port = '/dev/ttyUSB1'
    elif(bathPort==7):
        ser.port = '/dev/ttyUSB2'
    elif(bathPort==8):
        ser.port = '/dev/ttyUSB3'
    elif(bathPort==9):
        ser.port = '/dev/ttyAMA0'
    elif(bathPort==10):
        ser.port = '/dev/ttyAMA1'

def childProcess(bathManager, bathInformation):

    timerInitialized = False
    configureBathPort(ser, bathManager[10])    

    while(bathManager[0]>=0):
        try:
            print("BATH MANAGER WAITING")
            time.sleep(1)
            errorCount = [0, 0, 0]
            if(bathManager[0]==1):
                print("BATH BEGINNING")
                outBeginning = bathBeginning(bathManager, errorCount)
                timerInitialized = outBeginning[0]
                bathManager[6] = outBeginning[1] #IDEAL: 7
                errorCount = outBeginning[2]
                bathManager[0] = 0
                print("SALGO DE BATH BEGINNING")
            if(bathManager[0]==2):
                print("BATH DATA")
                outData = bathData(bathManager, bathInformation, errorCount)
                bathManager[7] = outData[0]
                errorCount = outData[1]
                bathManager[0] = 0
                print("SALGO DE BATH DATA")
            if(bathManager[0]==3):
                print("BATH ENDING")
                outEnding = bathEnding(bathManager, timerInitialized, errorCount)
                timerInitialized = outEnding[0]
                bathManager[8] = outEnding[1] #IDEAL: 4
                errorCount = outEnding[2]
                bathManager[0] = 0
                print("SALGO DE BATH ENDING")
            checkErrorCount(bathManager, errorCount)
        except IOError:
            ser.close()
            bathManager[12] = 1