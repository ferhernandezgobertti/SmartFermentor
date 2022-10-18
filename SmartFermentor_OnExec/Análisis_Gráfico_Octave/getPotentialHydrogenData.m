#FUNCTION PH
1;
function getPotentialHydrogenData (filename, magnitudeIdentifier, chartTitle)
  #filenameInfo = dec2base(filename,10);
  currentFile = csvread(strcat("/var/www/html/ControlData/PotentialHydrogen/DATA_Log/",filename,"_POT.txt"));
  currentPotentialHydrogenData = currentFile(:,1);
  objectivePotentialHydrogenData = currentFile(:,2);
  baseDropsData = currentFile(:,3);
  acidDropsData = currentFile(:,4);
  timeData = currentFile(:,5) + currentFile(:,6).*10^(-6);
  if(magnitudeIdentifier==0) 
    plot(timeData, currentPotentialHydrogenData, 'b');
    grid minor;
    set(gca, "fontsize", 16);
    title(chartTitle, 'fontsize', 32);
    ylabel("pH Actual [adim]", 'fontsize', 24);
    xlabel("Tiempo [seg]", 'fontsize', 24);
  elseif(magnitudeIdentifier==1)
    plot(timeData, objectivePotentialHydrogenData, 'g');
    grid minor;
    set(gca, "fontsize", 16);
    title(chartTitle, 'fontsize', 32);
    ylabel("pH Objetivo [adim]", 'fontsize', 24);
    xlabel("Tiempo [seg]", 'fontsize', 24);
  elseif(magnitudeIdentifier==2)
    plot(timeData, baseDropsData);
    grid minor;
    set(gca, "fontsize", 16);
    title(chartTitle, 'fontsize', 32);
    ylabel("Volumen de Base [mL]", 'fontsize', 24);
    xlabel("Tiempo [seg]", 'fontsize', 24);
  elseif(magnitudeIdentifier==3) 
    plot(timeData, acidDropsData, 'r');
    grid minor;
    set(gca, "fontsize", 16);
    title(chartTitle, 'fontsize', 32);
    ylabel("Volumen de çcido [mL]", 'fontsize', 24);
    xlabel("Tiempo [seg]", 'fontsize', 24);
  endif
endfunction
