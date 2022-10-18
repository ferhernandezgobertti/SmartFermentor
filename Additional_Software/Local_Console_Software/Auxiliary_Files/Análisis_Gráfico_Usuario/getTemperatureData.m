#FUNCTION TEMPERATURE
1;
function getTemperatureData (filename, magnitudeIdentifier, chartTitle)
  #filenameInfo = dec2base(filename,10);
  currentFile = csvread(strcat("/var/www/html/ControlData/Temperature/DATA_Log/",filename,"_TEM.txt"));
  currentTemperatureBioreactorData = currentFile(:,1);
  objectiveTemperatureBioreactorData = currentFile(:,2);
  currentTemperatureBathData = currentFile(:,3);
  objectiveTemperatureBathData = currentFile(:,4);
  pumpSelectedBath = currentFile(:,5);
  timeData = currentFile(:,6) + currentFile(:,7).*10^(-6);
  if(magnitudeIdentifier==0) 
    plot(timeData, currentTemperatureBioreactorData, 'b');
    grid minor;
    set(gca, "fontsize", 16);
    title(chartTitle, 'fontsize', 32);
    ylabel("Temperatura en Biorreactor Actual [Celsius]", 'fontsize', 24);
    xlabel("Tiempo [seg]", 'fontsize', 24);
  elseif(magnitudeIdentifier==1)
    plot(timeData, objectiveTemperatureBioreactorData, 'g');
    grid minor;
    set(gca, "fontsize", 16);
    title(chartTitle, 'fontsize', 32);
    ylabel("Temperatura en Biorreactor Objetivo [Celsius]", 'fontsize', 24);
    xlabel("Tiempo [seg]", 'fontsize', 24);
  elseif(magnitudeIdentifier==2)
    plot(timeData, currentTemperatureBathData, 'r');
    grid minor;
    set(gca, "fontsize", 16);
    title(chartTitle, 'fontsize', 32);
    ylabel("Temperatura en Circulador Actual [Celsius]", 'fontsize', 24);
    xlabel("Tiempo [seg]", 'fontsize', 24);
  elseif(magnitudeIdentifier==3) 
    plot(timeData, objectiveTemperatureBathData, 'g');
    grid minor;
    set(gca, "fontsize", 16);
    title(chartTitle, 'fontsize', 32);
    ylabel("Temperatura en Circulador Objetivo [Celsius]", 'fontsize', 24);
    xlabel("Tiempo [seg]", 'fontsize', 24);
  elseif(magnitudeIdentifier==4)
    plot(timeData, pumpSelectedBath);
    grid minor;
    set(gca, "fontsize", 16);
    title(chartTitle, 'fontsize', 32);
    ylabel("Nivel de Bombeo (0-5) [adim]", 'fontsize', 24);
    xlabel("Tiempo [seg]", 'fontsize', 24);
  endif
endfunction
