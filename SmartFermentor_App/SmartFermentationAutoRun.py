import sys, time
from MonitorConsole.SmartFermentationInterface import SmartFermentationInterface
import Control.SpeedController
import Control.TemperatureController
import Control.PotHydrogenController
import Control.ScreensManagement
#import Control.GameController
from multiprocessing import Process, Array

if __name__ == '__main__':

    interfaceController = SmartFermentationInterface()
    #print("SMART AUTO RUN CARGADO")
    processVelocity = Process(target = Control.SpeedController.childProcess, args=(interfaceController.settingVelocityControl, interfaceController.valuesVelocityControl, interfaceController.durationVelocityControl, ))
    processVelocity.start()

    processTemperature = Process(target = Control.TemperatureController.childProcess, args=(interfaceController.settingTemperatureControl, interfaceController.valuesTemperatureControl, interfaceController.durationTemperatureControl, ))
    processTemperature.start()

    processPotential = Process(target = Control.PotHydrogenController.childProcess, args=(interfaceController.settingPotentialHydrogenControl, interfaceController.valuesPotentialHydrogenControl, interfaceController.durationPotentialHydrogenControl, ))
    processPotential.start()

    processScreens = Process(target = Control.ScreensManagement.childProcess, args=(interfaceController.settingScreensControl, ))
    processScreens.start()

    #processGames = Process(target = Control.GameController.GameController, args=(app.gamesManager, ))
    #processGames.start()

    interfaceController.title('SMARTFERMENTOR ORT 2019')
    interfaceController.geometry('1366x768-5-1') #('1366x768-5-1')
    #offsetLocation = 50
    #appGeometry = str(app.winfo_screenwidth()) + 'x' + str(app.winfo_screenheight()-offsetLocation) + '+0+' + str(offsetLocation)
    #app.geometry(appGeometry)
    #app.iconbitmap(r'Images/Logos/iconADN.ico')
    interfaceController.resizable(0,0)
    interfaceController.mainloop()

    interfaceController.settingScreensControl[2] = 7
    interfaceController.settingScreensControl[1] = 1

    interfaceController.settingVelocityControl[1] = 0
    interfaceController.settingVelocityControl[0] = 0
    processVelocity.join()

    interfaceController.settingTemperatureControl[1] = 0
    interfaceController.settingTemperatureControl[0] = 0
    processTemperature.join()

    interfaceController.settingPotentialHydrogenControl[1] = 0
    interfaceController.settingPotentialHydrogenControl[0] = 0
    processPotential.join()

    time.sleep(5) # CHECK APAGADO DE PANTALLAS
    interfaceController.settingScreensControl[0] = 0
    processScreens.join()



    #app.gamesManager[0] = -1
    #processGames.join()
    print("TERMINO")
    #sys.exit()
