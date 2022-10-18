##################  README SMARTFERMENTOR v1.00 Universidad ORT #################

Se prosiguen a realizar aquí aclaraciones respecto a particularidades en cuanto a permisos de administrador necesarios para la utilización del Software al momento de su instalación. Las carpetas necesarias para el funcionamiento del programa son:

* SmartFermentor_App: Funcionalidades de Consola Local, Controla Automático, Gestión y Servidor Remoto.
* SmartFermentor_OnExec: Funcionalidades de manipulación de luces, acceso a sistema y análisis gráfico por Octave.


++++++++++++++++++ Archivos en SmartFermentor_OnExec ++++++++++++++++++

Los archivos en SmartFermentor_OnExec se encuentran subidividos en carpetas para facilitar la organización de los mismos en la consola. Para utilizarlos, por favor copiar aquellos de las carpetas Desktop y Documents a las carpetas correspondientes (/home/pi/Desktop y /home/pi/Documents respectivamente).

Respecto a los archivos para análisis gráfico en Octave, no se requiere una carpeta de destino específica para ejecutarlos. Sin embargo, se agradece tener las siguientes consideraciones:

(A) Cada archivo contiene el tratamiento de cada magnitud representada por:
    * getVelocityData: Obtención de gráficos referentes a la velocidad de agitación.
    * getTemperatureData: Obtención de gráficos referentes a la temperatura del compuesto.
    * getPotentialHydrogenData: Obtención de gráficos referentes al pH del medio.

(B) Para cada magnitud interesada a graficar, abrir el archivo correspondiente (de los nombrados en (A)) en Octave y ejecutarlo. Luego, ingresar en la línea de comandos la indicación del archivo objetivo en formato día y tiempo (i.e. "20181128_041550"), identificador de la magnitud a graficar y el título del respectivo gráfico, según se indica a continuación:

    * getVelocityData(<nombre_Archivo>, <magnitud_ID>, <título_Gráfico>)
        - Magnitud ID 0: Velocidad de Agitación Actual [rpm] vs Tiempo [seg]
        - Magnitud ID 1: Velocidad de Agitación Actual [rpm] vs Tiempo [seg]
        - Magnitud ID 2: Temperatura de Refrigeración [Celsius] vs Tiempo [seg]
        - Magnitud ID 3: Frecuencia de Entrada al Biorreactor [Hz] vs Tiempo [seg]

    * getTemperatureData(<nombre_Archivo>, <magnitud_ID>, <título_Gráfico>)
        - Magnitud ID 0: Temperatura Actual en Biorreactor [Celsius] vs Tiempo [seg]
        - Magnitud ID 1: Temperatura Objetivo en Biorreactor [Celsius] vs Tiempo [seg]
        - Magnitud ID 2: Temperatura Actual en Circulador [Celsius] vs Tiempo [seg]
        - Magnitud ID 3: Temperatura Objetivo en Circulador [Celsius] vs Tiempo [seg]
        - Magnitud ID 4: Nivel de Bombeo en Circulador [adim] vs Tiempo [seg]

    * getPotentialHydrogenData(<nombre_Archivo>, <magnitud_ID>, <título_Gráfico>)
        - Magnitud ID 0: pH Actual en Biorreactor [adim] vs Tiempo [seg]
        - Magnitud ID 1: pH Objetivo en Biorreactor [adim] vs Tiempo [seg]
        - Magnitud ID 2: Volumen expulsado de Base [mL] vs Tiempo [seg]
        - Magnitud ID 3: Volumen expulsado de Ácido [mL] vs Tiempo [seg]

(C) Manipular la gráfica resultante según conveniencia.


++++++++++++++++++ Permisos de archivos a utilizar ++++++++++++++++++

Una vez adquiridos los archivos para la instalación del Software, se deberá abrir la terminal de comandos Ctrl+T y brindar permisos de ejecución a los siguientes archivos:

//// SmartFermentor_App ////
- managebash.sh
- controlbash.sh
- userPage.php
- StatusServerData.json
- fermentationsDisplay.php
- reservationsDisplay.php
- participantsDisplay.php

//// SmartFermentor_OnExec ////
- setLedsOnBootingDown.py
- setLedsOnBootingUp.py
- ledBarOff.sh
- ledBarOn.sh
- ledStatusOff.sh
- ledStatusOn.sh

Para facilitar estos permisos, se deberá ejecutar esta linea de comando para cada uno:

       raspberry@pi# sudo chmod 775 <dirección absoluta del archivo>


Esto indica al sistema que el archivo a utilizar es de confianza y evita obstáculos de seguridad del sistema. Sepa comprender y disculpe las molestias.
