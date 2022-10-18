import sys, time, os, serial, binascii

ser = serial.Serial()
ser.port = '/dev/ttyACM1' #CHECK PORT
ser.baudrate = 19200
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE
ser.bytesize = serial.EIGHTBITS
ser.timeout = 5

def sendFrameToScreensController(ser, frameToSend):
    isMessageReceived = False
    crcMessageToSend = hex(binascii.crc32(frameToSend.encode("utf-8")))
    messageToSend = "X"+str(frameToSend)+(str(crcMessageToSend)[2:]).upper()+'\r\n'
    print("MESSAGE ENVIADO: ", messageToSend)
    ser.write(messageToSend.encode('ascii'))
    #dataReceived = ser.read(14)
    #print("RECIBIDO:!!!! ", dataReceived)
    #messageReceived = dataReceived.decode('ascii')
    #if ("OK" in messageReceived):
    isMessageReceived = True
    return isMessageReceived

def getAppropiateStatusFormat (messageToCheck):
    messageStatusString = ""
    if(len(str(messageToCheck))==3):
        messageStatusString = "000"
    if(len(str(messageToCheck))==4):
        messageStatusString = "00"
    if(len(str(messageToCheck))==5):
        messageStatusString = "0"
    messageStatusString = messageStatusString + str(messageToCheck)[2:]
    return messageStatusString

def getAppropiateValueFormat (valueToCheck, formatLength):
    magnitudeFormat = ""
    if(len(str(valueToCheck))==formatLength-4):
        magnitudeFormat = "0000"
    if(len(str(valueToCheck))==formatLength-3):
        magnitudeFormat = "000"
    if(len(str(valueToCheck))==formatLength-2):
        magnitudeFormat = "00"
    if(len(str(valueToCheck))==formatLength-1):
        magnitudeFormat = "0"
    magnitudeFormat = magnitudeFormat + str(valueToCheck)
    return magnitudeFormat

def configureScreensPort(ser, screensPort):
    ser.port = '/dev/ttyACM1'
    if(screensPort==1):
        ser.port = '/dev/ttyACM0'
    elif(screensPort==2):
        ser.port = '/dev/ttyACM1'
    elif(screensPort==3):
        ser.port = '/dev/ttyACM2'
    elif(screensPort==4):
        ser.port = '/dev/ttyACM3'
    elif(screensPort==5):
        ser.port = '/dev/ttyUSB0'
    elif(screensPort==6):
        ser.port = '/dev/ttyUSB1'
    elif(screensPort==7):
        ser.port = '/dev/ttyUSB2'
    elif(screensPort==8):
        ser.port = '/dev/ttyUSB3'
    elif(screensPort==9):
        ser.port = '/dev/ttyAMA0'
    elif(screensPort==10):
        ser.port = '/dev/ttyAMA1'

def childProcess(manager):
    configureScreensPort(ser, manager[22])
    ser.open()

    while(manager[0]!=0):

        print("SCREENS WAITING")
        time.sleep(2)
        isMessageReceived = True

        if(manager[1]==-3):
            print("APAGO SERIAL LED MATRIX")
            ser.close()
            ser.open()
            manager[1]=-2

        if(manager[1]==-1):
            #ser.open()
            manager[1] = 0
            time.sleep(2)

        if(manager[1]>0):

            print("MANAGER[2] VALE: ", manager[2])

            if(manager[2]==1): # HOME PAGE
                isMessageReceived = sendFrameToScreensController(ser, "10000000000000000000000000")

            #if(manager[2]==2): # ADMIN PAGE
            #isMessageReceived = sendFrameToScreensController(ser, "20000000000000000000000000")

            #if(manager[2]==3): # PROFESSOR PAGE
            #isMessageReceived = sendFrameToScreensController(ser, "30000000000000000000000000")

            #if(manager[2]==4): # STUDENT PAGE
            #isMessageReceived = sendFrameToScreensController(ser, "40000000000000000000000000")

            if(manager[2]==5): # FERMENTATION PAGE
                print("ENVIO MENSAJE FERMENTATION")
                isMessageReceived = sendFrameToScreensController(ser, "50000000000000000000000000")

            if(manager[2]==6): # DATA DISPLAY
                errorMagnitudes = [manager[3], manager[4], manager[5], manager[6]] # [0-2, 0-2, 0-4, 0-4]
                unitMagnitudes = [manager[7], manager[8], manager[9]] # [0-1, 0-2, 0-2]
                motorOrientation = manager[10] # 0-1
                slopeMagnitudes = [manager[11], manager[12], manager[13]] # [0-1, 0-2, 0-2]
                controlsRunning = [manager[14], manager[15], manager[16], manager[17]] # manager[14] # 0-8
                valuesMagnitudes = [manager[18], manager[19], manager[20], manager[21]] # [0-n, 0-n, 0-n, 0-n]

                print("ERROR MAGNITUDES: ", errorMagnitudes)
                print("UNIT MAGNITUDES: ", unitMagnitudes)
                print("motorOrientation: ", motorOrientation)
                print("slopeMagnitudes: ", slopeMagnitudes)
                print("controlsRunning: ", controlsRunning)

                errorStatusSending = hex((errorMagnitudes[0]<<8)+(errorMagnitudes[1]<<6)+(errorMagnitudes[2]<<3)+errorMagnitudes[3])
                messageStatusSending = hex((unitMagnitudes[0]<<14)+(unitMagnitudes[1]<<12)+(unitMagnitudes[2]<<10)+(motorOrientation<<9)+(slopeMagnitudes[0]<<8)+(slopeMagnitudes[1]<<6)+(slopeMagnitudes[2]<<4)+(controlsRunning[0]<<3)+(controlsRunning[1]<<2)+(controlsRunning[2]<<1))
                errorStatusString = getAppropiateStatusFormat(errorStatusSending)
                messageStatusString = getAppropiateStatusFormat(messageStatusSending)

                velocityValue = getAppropiateValueFormat(valuesMagnitudes[0], 4)
                temperatureValue = getAppropiateValueFormat(valuesMagnitudes[1], 4)
                potentialHydrogenValue = getAppropiateValueFormat(valuesMagnitudes[2], 5)
                extractionValue = getAppropiateValueFormat(valuesMagnitudes[3], 4)

                print("ERROR STATUS: ", errorStatusSending)
                print("MESSAGE STATUS: ", messageStatusSending)
                print("ERROR POSTA: ", getAppropiateStatusFormat(errorStatusSending))
                print("MESSAGE POSTA: ", getAppropiateStatusFormat(messageStatusSending))
                print("ERROR STATUS STRING: ", errorStatusString)
                print("MESSAGE STATUS STRING: ", messageStatusString)
                print("VELOCITY VALUE: ", velocityValue)
                print("TEMPERATURE VALUE: ", temperatureValue)
                print("POTENTIAL VALUE: ", potentialHydrogenValue)
                ser.close()
                ser.open()
                time.sleep(2)
                messageToSend = "6"+str(errorStatusString).upper()+str(messageStatusString).upper()+str(velocityValue)+str(temperatureValue)+str(potentialHydrogenValue)+"0000" #str(extractionValue)
                isMessageReceived = sendFrameToScreensController(ser, messageToSend)

            if(manager[2]==7): # ERASE DISPLAY
                ser.close()
                ser.open()
                isMessageReceived = True
                #isMessageReceived = sendFrameToScreensController(ser, "90000000000000000000000000")

            if(isMessageReceived):
                manager[1] = 0
                time.sleep(5)

    ser.close()
