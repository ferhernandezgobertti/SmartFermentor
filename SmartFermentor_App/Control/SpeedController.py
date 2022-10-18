import sys, minimalmodbus, time, os, serial
from datetime import date
from datetime import datetime
from datetime import timedelta


ser = serial.Serial()
ser.port = '/dev/ttyACM0'
ser.baudrate = 9600
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE
ser.bytesize = serial.EIGHTBITS
ser.timeout = 2

FMT = '%H:%M:%S.%f'

def selectOptimizedConstant(velocityObjective):

    constante = 0.01
    if(velocityObjective<250):
        constante = 0.00550
    elif(velocityObjective<300):
        constante = 0.00200
    elif(velocityObjective<350):
        constante = 0.00098
    elif(velocityObjective<400):
        constante = 0.00082
    elif(velocityObjective<450):
        constante = 0.000698 #0.000282
    elif(velocityObjective<500):
        constante = 0.000452
    elif(velocityObjective<550):
        constante = 0.00032
    elif(velocityObjective<600):
        constante = 0.00030
    elif(velocityObjective<650):
        constante = 0.00028
    elif(velocityObjective<700):
        constante = 0.00020
    return constante

def changeFrequency(instrument, frequencyChanged):

    instrument.write_register(100, frequencyChanged, 1) # Registernumber, value, number of decimals for storage

def saveVelocityData(dataVelocity, tempData, motorTrigger, currentStr, currentFileDay, currentFileTime, controlUnit, dataInterval, intervalCount, velObjective):

    newTime = datetime.today()
    newTimeStr = newTime.strftime("%H:%M:%S.%f")
    tdelta = datetime.strptime(newTimeStr, FMT) - datetime.strptime(currentStr, FMT)

    if(tdelta.seconds>=dataInterval*intervalCount):

        if(currentFileTime<=99999):
            currentFileStr = "0"+str(currentFileTime)
        else:
            currentFileStr = str(currentFileTime)

        dataVelocityToSave = str(dataVelocity)
        informationTempToSave = str(tempData)
        
        if(controlUnit==1): # m/s
            dataVelocityToSave = str(float(dataVelocity*2*3.14*5/60))
        if(controlUnit==2): # rad/s
            dataVelocityToSave = str(float(dataVelocity*2*3.14/60))

        filename = "ControlData/Velocity/DATA_Log/"+str(currentFileDay)+"_"+currentFileStr+"_VEL.txt"
        print("VELOCITY FILE IN CONTROL: ", filename)
        intervalCount = intervalCount+1

        with open(filename, 'a') as registerMotorData:
            registerMotorData.write(dataVelocityToSave+','+str(velObjective)+','+informationTempToSave+','+str(motorTrigger)+','+str(tdelta.seconds)+','+str(tdelta.microseconds)+'\n')
            registerMotorData.close()

    return intervalCount

def calculateLRC(input):

    lrc = ord(input[0])

    for i in range(1,len(input)):
        lrc += ord(input[i])
    return lrc

def readVelocity(ser, dataCount, isDataRequested, errorCount): #LECTURA DE DATOS DEL SERIAL

    velocityRead = 0
    informationTemp = ""

    if(dataCount == 90):
        dataCount = 0
        isDataRequested = False

    if(not isDataRequested):

        val1= ":01DT0190"
        res = calculateLRC(val1[1:])
        lrcData = hex((((res^0xFF)+1)&0xFF))
        dataToSend = val1+str(lrcData[2:4]).upper()+'\r\n'
        ser.write(dataToSend.encode('ascii'))
        dataReceived = ser.read(15)
        
        if(len(dataReceived)>1):
            errorCount[1] = 0
            dataReceivedStr = dataReceived.decode('ascii')
            lrcReceived = dataReceivedStr[11:13]
            resVerification = calculateLRC(dataReceivedStr[1:11])
            lrcVerification = hex((((resVerification^0xFF)+1)&0xFF))
            if(str(lrcVerification[2:4]).upper()!=str(lrcReceived).upper()):
                errorCount[0] = errorCount[0] + 1
                print("LRCVERIFICATION: ", str(lrcVerification[2:4]).upper())
                print("LRCRECEIVED: ", str(lrcReceived).upper())
            else:
                errorCount[0] = 0
        else:
            errorCount[1] = errorCount[1] + 1
        
        isDataRequested = True
        print("DATA RECEIVED: ", dataReceived)


    if(isDataRequested):
        answerVELOCITY = ser.read(14)
        print("DATA RECEIVED: ", answerVELOCITY)

        currentVelocity = answerVELOCITY.decode("utf-8")

        if(len(currentVelocity)>1):
            try:
                velocityRead = float(currentVelocity[0:6])
                informationTemp = str(currentVelocity[6:11])
                errorCount[3] = int(currentVelocity[11:12])
                dataCount = dataCount + 1
            except ValueError:
                print("VALUE ERROR VEL")
        else:
           dataCount = 0
           isDataRequested = False

    if(velocityRead==0 or velocityRead>900.0 or velocityRead<150.0):
        errorCount[2] = errorCount[2] + 1
    else:
        errorCount[2] = 0

    return [velocityRead, dataCount, isDataRequested, informationTemp, errorCount]

def isSensorWellConnected(dataConnection):
    if("OK" in dataConnection):
        return True
    else:
        return False

def checkConnectionSensor():
    sensorConnected = False
    val1 = ":01CN01CH"
    res = calculateLRC(val1[1:])
    lrcData = hex((((res^0xFF)+1)&0xFF))
    dataToSend = val1+str(lrcData[2:4]).upper()+'\r\n'
    ser.open()
    time.sleep(2)
    ser.write(dataToSend.encode('ascii'))
    dataReceived = ser.read(13)
    if (isSensorWellConnected(dataReceived.decode('ascii'))):
        sensorConnected = True
    ser.close()
    return sensorConnected

def checkConnectionMotor():
    motorConnected = False
    try:
        motorSerial = minimalmodbus.Instrument('/dev/ttyUSB0', 1) # port name, slave address (in decimal)
        motorSerial.serial.baudrate = 9600
        motorSerial.write_register(100, 20, 1) # Registernumber, value, number of decimals for storage
        time.sleep(1)
        freqRead = motorSerial.read_register(100, 1)
        if(int(freqRead)==20):
            motorConnected = True
    except IOError:
        print("Failed to interact with instrument")
    return motorConnected

def checkSpeedModulesConnection():
    velocityConnection = 100
    isSensorConnectionRight = checkConnectionSensor()
    isMotorConnectionRight = checkConnectionMotor()
    if(isSensorConnectionRight):
        velocityConnection = velocityConnection + 10
    if(isMotorConnectionRight):
        velocityConnection = velocityConnection + 1
    return velocityConnection

def configureSensorPort(ser, velocitySensorPort):
    if(velocitySensorPort==0 or velocitySensorPort==1):
        ser.port = '/dev/ttyACM0'
    elif(velocitySensorPort==2):
        ser.port = '/dev/ttyACM1'
    elif(velocitySensorPort==3):
        ser.port = '/dev/ttyACM2'
    elif(velocitySensorPort==4):
        ser.port = '/dev/ttyACM3'
    elif(velocitySensorPort==5):
        ser.port = '/dev/ttyUSB0'
    elif(velocitySensorPort==6):
        ser.port = '/dev/ttyUSB1'
    elif(velocitySensorPort==7):
        ser.port = '/dev/ttyUSB2'
    elif(velocitySensorPort==8):
        ser.port = '/dev/ttyUSB3'
    elif(velocitySensorPort==9):
        ser.port = '/dev/ttyAMA0'
    elif(velocitySensorPort==10):
        ser.port = '/dev/ttyAMA1'

def configureMotorPort(motorPort):
    motorPortName = '/dev/ttyUSB0'
    if(motorPort==1):
        motorPortName = '/dev/ttyACM0'
    elif(motorPort==2):
        motorPortName = '/dev/ttyACM1'
    elif(motorPort==3):
        motorPortName = '/dev/ttyACM2'
    elif(motorPort==4):
        motorPortName = '/dev/ttyACM3'
    elif(motorPort==5):
        motorPortName = '/dev/ttyUSB0'
    elif(motorPort==6):
        motorPortName = '/dev/ttyUSB1'
    elif(motorPort==7):
        motorPortName = '/dev/ttyUSB2'
    elif(motorPort==8):
        motorPortName = '/dev/ttyUSB3'
    elif(motorPort==9):
        motorPortName = '/dev/ttyAMA0'
    elif(motorPort==10):
        motorPortName = '/dev/ttyAMA1'
    return motorPortName

def configureVelocityPorts(ser, manager):
    velocitySensorPort = manager[21]
    motorPort = manager[22]
    configureSensorPort(ser, velocitySensorPort)
    return configureMotorPort(motorPort)

def turnFanOff(ser, errorCount):
    val1=":01TF01VT"
    res=calculateLRC(val1[1:])
    lrcData = hex((((res^0xFF)+1)&0xFF))
    dataToSend = val1+str(lrcData[2:4]).upper()+'\r\n'
    ser.write(dataToSend.encode('ascii'))
    dataReceived = ser.read(13)
    if(len(dataReceived)>1):
        errorCount[1] = 0
        dataReceivedStr = dataReceived.decode('ascii')
        lrcReceived = dataReceivedStr[9:11]
        resVerification = calculateLRC(dataReceivedStr[1:11])
        lrcVerification = hex((((resVerification^0xFF)+1)&0xFF))
        if(str(lrcVerification[2:4]).upper()!=str(lrcReceived).upper() and (not "OK" in dataReceivedStr)):
            errorCount[0] = errorCount[0] + 1
            errorCount[3] = 2
        else:
            errorCount[0] = 0
            errorCount[3] = 0
    return errorCount

def childProcess(manager, velocityObjective, duration):

    isDataRequested = False
    velocityStep = 0
    dataCount = 0

    while(manager[0]!=0):

        exactT = datetime.today()
        exactStr = exactT.strftime("%H:%M:%S.%f")
        motorPortName = configureVelocityPorts(ser, manager)
        print("MOTOR CONTROL WAITING")
        intervalCount = 1
        time.sleep(1)

        if(manager[0]==2):

            manager[0] = checkSpeedModulesConnection()

        while(manager[1]!=0):

            if(manager[2]==3 or manager[2]==4):

                manager[2] = 0

            objectiveVel = velocityObjective[velocityStep]
            objectiveFreq = objectiveVel/20
            objectiveTime = duration[velocityStep]
            fileTime = manager[4]
            fileDay = manager[5]
            controlUnit = manager[6]
            controlPrecision = int(manager[7])/10
            speedSensitivity = manager[8] # IMPLEMENTAR
            motorOrientation = manager[9] # IMPLEMENTAR
            dataInterval = manager[10]
            manager[16] = 0 #ERROR CONEXION
            manager[17] = 0 #ERROR SENSADO
            
            errorCount = [0, 0, 0, 0, 0] # [REDUNDANCIA, TIMEOUT, FALLOS SENSADO VEL, FALLOS SENSADO TEMP, FALLA CONTROL]
            errorPrev = 0
            motorFrequency = 9

            constI = selectOptimizedConstant(objectiveVel)

            errorInt = 0
            errorPastI = 0 #e[k-1]
            errorCurrent = 0 #e[k+1]

            prevTime = datetime.today()
            prevTimeStr = prevTime.strftime("%H:%M:%S.%f")

            stepBeginTime = datetime.today()
            stepBeginTimeStr = stepBeginTime.strftime("%H:%M:%S.%f")

            currentTime = datetime.today()
            currentTimeStr = currentTime.strftime("%H:%M:%S.%f")

            timeDifference = datetime.strptime(currentTimeStr, FMT) - datetime.strptime(stepBeginTimeStr, FMT)
            currentDuration = timeDifference.seconds + timeDifference.microseconds*(0.000001)

            period = 0

            try:

                ser.open()

                instrument = minimalmodbus.Instrument(motorPortName, 1) # port name, slave address (in decimal)
                instrument.serial.baudrate = 9600

                registryFreq = changeFrequency(instrument, motorFrequency)

                instrument.write_register(8192, 2)

                while(currentDuration<=objectiveTime and manager[2]==0):

                    actualTime = datetime.today()
                    actualTimeStr = actualTime.strftime("%H:%M:%S.%f")
                    actualTDelta = datetime.strptime(actualTimeStr, FMT) - datetime.strptime(prevTimeStr, FMT)
                    period = actualTDelta.seconds + actualTDelta.microseconds*(0.000001)

                    returnedData = readVelocity(ser, dataCount, isDataRequested, errorCount)

                    if(returnedData[0]>0):
                        dataVelocity = returnedData[0]
                    else:
                        dataVelocity = objectiveVel

                    dataCount = returnedData[1]

                    isDataRequested = returnedData[2]

                    informationTemp = returnedData[3]
                    
                    errorCount = returnedData[4]

                    if(manager[20]==0):

                        if(dataVelocity==0):
                            dataVelocity = objectiveVel

                        prevSpeed = dataVelocity

                        errorCurrent = objectiveVel - dataVelocity

                        if(abs(errorCurrent)<controlPrecision): #1): # BANDA MUERTA

                            errorCurrent = 0
                        
                        if(errorPrev<errorCurrent):
                            errorCount[4] = errorCount[4] + 1
                        else:
                            errorCount[4] = 0

                        errorInt = errorInt + (errorCurrent+errorPastI)*period/2

                        errorPastI = errorCurrent

                        controlI = constI * errorInt

                        if (controlI>2):

                            controlI = 2

                        if (controlI<-2):

                            controlI = -2

                        motorFrequency = objectiveFreq + controlI
                        
                        
                    else:
                        if(manager[18]==1):
                            manager[18] = 0
                            motorFrequency = manager[19]/10
                        if(manager[18]==2):
                            manager[18] = 0
                            motorFrequency = float(round(manager[19]/200,1))
                        if(manager[18]==3):
                            manager[18] = 0
                            #motorFrequency = 0.0
                            manager[2] = 1

                    if(errorCount[0]>5 or errorCount[1]>5 or errorCount[2]>18 or errorCount[4]>18):
                        motorFrequency = (objectiveVel/20)+0.3
                        if(errorCount[0]>5):
                            manager[17] = 1
                        if(errorCount[1]>5):
                            manager[17] = 2
                        if(errorCount[2]>18):
                            manager[17] = 3
                        if(errorCount[4]>18):
                            manager[17] = 5

                    elif(errorCount[3]!=0 and errorCount[3]!=1):
                        manager[17] = 4
                    
                    else:
                        manager[17] = 0

                    changeFrequency(instrument, motorFrequency)
                    print("ERROR COUNT: ", errorCount)
                    print("manager[16]: ", manager[16])
                    print("manager[17]: ", manager[17])
                    if(isDataRequested):

                        intervalCount = saveVelocityData(dataVelocity, informationTemp, motorFrequency, exactStr, fileDay, fileTime, controlUnit, dataInterval, intervalCount, objectiveVel)

                    prevTime = actualTime

                    prevTimeStr = prevTime.strftime("%H:%M:%S.%f")

                    currentTime = datetime.today()
                    currentTimeStr = currentTime.strftime("%H:%M:%S.%f")

                    timeDifference = datetime.strptime(currentTimeStr, FMT) - datetime.strptime(stepBeginTimeStr, FMT)
                    currentDuration = timeDifference.seconds + timeDifference.microseconds*(0.000001)
                    
                    errorPrev = errorCurrent

                if(manager[2]==0 or manager[2]==4):

                    velocityStep = velocityStep + 1
                    manager[3] = velocityStep

                    ser.close()

                if(manager[2]==3):

                    velocityStep = velocityStep - 1

                    if(velocityStep<0):

                        velocityStep = 0

                    manager[3] = velocityStep

                    ser.close()

                if(manager[2]==2):

                    manager[1] = 0
                    #isDataRequested = False

                    ser.close()

                if((velocityObjective[velocityStep]==0 and duration[velocityStep]==0) or manager[2]==1):

                   manager[1]=0

                   ser.close()

                   instrument.write_register(8192, 1)
               
                   ser.open()
                   time.sleep(1)
                   ser.close()
                   velocityStep = 0

                   isDataRequested = False

                   print("CONTROL END")

            except SerialException:
                manager[1] = 0
                ser.close()
                instrument.write_register(8192, 1)
                isDataRequested = False
                manager[16] = 1

            except IOError:
                manager[1] = 0
                ser.close()
                instrument.write_register(8192, 1)
                isDataRequested = False
                manager[16] = 2