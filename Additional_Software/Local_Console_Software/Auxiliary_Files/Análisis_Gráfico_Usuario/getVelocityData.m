#FUNCTION VELOCITY
1;
function getVelocityData (filename, magnitudeIdentifier, chartTitle)
  #filenameInfo = dec2base(filename,10);
  currentFile = csvread(strcat("/var/www/html/ControlData/Velocity/DATA_Log/",filename,"_VEL.txt"));
  velocityData = currentFile(:,1);
  velocityObjective = currentFile(:,2);
  refTemperatureData = currentFile(:,3);
  frequencyData = currentFile(:,4);
  timeData = currentFile(:,5) + currentFile(:,6).*10^(-6);
  if(magnitudeIdentifier==0) 
    plot(timeData, velocityData, 'b');
    grid minor;
    set(gca, "fontsize", 16);
    title(chartTitle, 'fontsize', 32);
    ylabel("Velocidad Actual [rpm]", 'fontsize', 24);
    xlabel("Tiempo [seg]", 'fontsize', 24);
  elseif(magnitudeIdentifier==2)
    plot(timeData, velocityObjective, 'g');
    grid minor;
    set(gca, "fontsize", 16);
    title(chartTitle, 'fontsize', 32);
    ylabel("Velocidad Objetivo [rpm]", 'fontsize', 24);
    xlabel("Tiempo [seg]", 'fontsize', 24);
  elseif(magnitudeIdentifier==3)
    plot(timeData, refTemperatureData, 'r');
    grid minor;
    set(gca, "fontsize", 16);
    title(chartTitle, 'fontsize', 32);
    ylabel("Temperatura [Celsius]", 'fontsize', 24);
    xlabel("Tiempo [seg]", 'fontsize', 24);
  elseif(magnitudeIdentifier==4)
    plot(timeData, frequencyData);
    grid minor;
    set(gca, "fontsize", 16);
    title(chartTitle, 'fontsize', 32);
    ylabel("Frecuencia [Hz]", 'fontsize', 24);
    xlabel("Tiempo [seg]", 'fontsize', 24);
  endif
endfunction
