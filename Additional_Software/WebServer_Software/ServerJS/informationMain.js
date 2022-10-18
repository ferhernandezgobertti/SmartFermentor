function updateVelocityInformation(jsonVelocityInfo){
  var jsonVelocityInfoData = JSON.parse(jsonVelocityInfo);
  var currentVelocityControlStep = (jsonVelocityInfoData.velocityControl)[3];
  var currentVelocityControlInformation = (jsonVelocityInfoData.velocityControl)[2];
  document.getElementById('velControlInfo').innerHTML = "Velocity Control: "+(currentVelocityControlInformation.split(": "))[1]
  var currentVelocityControlStatus = (jsonVelocityInfoData.velocityControl)[1];
  if(currentVelocityControlStatus == "0"){
    document.getElementById('velStatusInfo').style.color = "#085454"
    document.getElementById('velStatusInfo').innerHTML = "Velocity Status: ...."
    document.getElementById('velStepInfo').innerHTML = "Velocity Step: ......."
  }
  if(currentVelocityControlStatus == "1"){
    document.getElementById('velStatusInfo').style.color = "#085454"
    document.getElementById('velStatusInfo').innerHTML = "Velocity Status: RUNNING"
    document.getElementById('velStepInfo').innerHTML = "Velocity Step: "+(currentVelocityControlStep.split(": "))[1]
  }
  if(currentVelocityControlStatus == "2"){
    document.getElementById('velStatusInfo').style.color = "#085454"
    document.getElementById('velStatusInfo').innerHTML = "Velocity Status: PAUSED"
    document.getElementById('velStepInfo').innerHTML = "Velocity Step: "+(currentVelocityControlStep.split(": "))[1]
  }
  if(currentVelocityControlStatus == "3"){
    document.getElementById('velStatusInfo').innerHTML = "Velocity Status: STOPPED"
    document.getElementById('velStepInfo').innerHTML = "Velocity Step: ......."
  }
  if(currentVelocityControlStatus == "4"){
    document.getElementById('velStatusInfo').style.color = "red"
    document.getElementById('velStatusInfo').innerHTML = "Velocity Status: ERROR!!! Continuing by default..."
    document.getElementById('velStepInfo').innerHTML = "Velocity Step: "+(currentVelocityControlStep.split(": "))[1]
  }
  if(currentVelocityControlStatus == "5"){
    document.getElementById('velStatusInfo').style.color = "red"
    document.getElementById('velStatusInfo').innerHTML = "Velocity Status: CRITICAL ERROR!!! Control Stopped"
    document.getElementById('velStepInfo').innerHTML = "Velocity Step: ......."
  }
}

function updateTemperatureInformation(jsonTemperatureInfo){
  var jsonTemperatureInfoData = JSON.parse(jsonTemperatureInfo);
  var currentTemperatureControlStep = (jsonTemperatureInfoData.temperatureControl)[3];
  var currentTemperatureControlInformation = (jsonTemperatureInfoData.temperatureControl)[2];
  document.getElementById('temControlInfo').innerHTML = "Temperature Control: "+(currentTemperatureControlInformation.split(": "))[1]
  var currentTemperatureControlStatus = (jsonTemperatureInfoData.temperatureControl)[1];
  if(currentTemperatureControlStatus == "0"){
    document.getElementById('temStatusInfo').style.color = "#085454"
    document.getElementById('temStatusInfo').innerHTML = "Temperature Status: ...."
    document.getElementById('temStepInfo').innerHTML = "Temperature Step: ......."
  }
  if(currentTemperatureControlStatus == "1"){
    document.getElementById('temStatusInfo').style.color = "#085454"
    document.getElementById('temStatusInfo').innerHTML = "Temperature Status: RUNNING"
    document.getElementById('temStepInfo').innerHTML = "Temperature Step: "+(currentTemperatureControlStep.split(": "))[1]
  }
  if(currentTemperatureControlStatus == "2"){
    document.getElementById('temStatusInfo').style.color = "#085454"
    document.getElementById('temStatusInfo').innerHTML = "Temperature Status: PAUSED"
    document.getElementById('temStepInfo').innerHTML = "Temperature Step: "+(currentTemperatureControlStep.split(": "))[1]
  }
  if(currentTemperatureControlStatus == "3"){
    document.getElementById('temStatusInfo').innerHTML = "Temperature Status: STOPPED"
    document.getElementById('temStepInfo').innerHTML = "Temperature Step: ......."
  }
  if(currentTemperatureControlStatus == "4"){
    document.getElementById('temStatusInfo').style.color = "red"
    document.getElementById('temStatusInfo').innerHTML = "Temperature Status: ERROR!!! Continuing by default..."
    document.getElementById('temStepInfo').innerHTML = "Temperature Step: "+(currentTemperatureControlStep.split(": "))[1]
  }
  if(currentTemperatureControlStatus == "5"){
    document.getElementById('temStatusInfo').style.color = "red"
    document.getElementById('temStatusInfo').innerHTML = "Temperature Status: CRITICAL ERROR!!! Control Stopped"
    document.getElementById('temStepInfo').innerHTML = "Temperature Step: ......."
  }
}

function updatePotentialHydrogenInformation(jsonPotentialInfo){
  var jsonPotentialInfoData = JSON.parse(jsonPotentialInfo);
  var currentPotentialControlStep = (jsonPotentialInfoData.potentialControl)[3];
  var currentPotentialControlInformation = (jsonPotentialInfoData.potentialControl)[2];
  document.getElementById('potControlInfo').innerHTML = "Potential Hydrogen Control: "+(currentPotentialControlInformation.split(": "))[1]
  var currentPotentialControlStatus = (jsonPotentialInfoData.potentialControl)[1];
  if(currentPotentialControlStatus == "0"){
    document.getElementById('potStatusInfo').style.color = "#085454"
    document.getElementById('potStatusInfo').innerHTML = "Potential Hydrogen Status: ...."
    document.getElementById('potStepInfo').innerHTML = "Potential Hydrogen Step: ......."
  }
  if(currentPotentialControlStatus == "1"){
    document.getElementById('potStatusInfo').style.color = "#085454"
    document.getElementById('potStatusInfo').innerHTML = "Potential Hydrogen Status: RUNNING"
    document.getElementById('potStepInfo').innerHTML = "Potential Hydrogen Step: "+(currentPotentialControlStep.split(": "))[1]
  }
  if(currentPotentialControlStatus == "2"){
    document.getElementById('potStatusInfo').style.color = "#085454"
    document.getElementById('potStatusInfo').innerHTML = "Potential Hydrogen Status: PAUSED"
    document.getElementById('potStepInfo').innerHTML = "Potential Hydrogen Step: "+(currentPotentialControlStep.split(": "))[1]
  }
  if(currentPotentialControlStatus == "3"){
    document.getElementById('potStatusInfo').innerHTML = "Potential Hydrogen Status: STOPPED"
    document.getElementById('potStepInfo').innerHTML = "Potential Hydrogen Step: ......."
  }
  if(currentPotentialControlStatus == "4"){
    document.getElementById('potStatusInfo').style.color = "red"
    document.getElementById('potStatusInfo').innerHTML = "Potential Hydrogen Status: ERROR!!! Continuing by default..."
    document.getElementById('potStepInfo').innerHTML = "Potential Hydrogen Step: "+(currentPotentialControlStep.split(": "))[1]
  }
  if(currentPotentialControlStatus == "5"){
    document.getElementById('potStatusInfo').style.color = "red"
    document.getElementById('potStatusInfo').innerHTML = "Potential Hydrogen Status: CRITICAL ERROR!!! Control Stopped"
    document.getElementById('potStepInfo').innerHTML = "Potential Hydrogen Step: ......."
  }
}

function updateFermentationInformation(jsonFermentationInformation, fermentationsData){
  var jsonStatusInfoData = JSON.parse(jsonFermentationInformation);
  if((document.getElementById('velStatusInfo').innerHTML == "Velocity Status: RUNNING")||(document.getElementById('temStatusInfo').innerHTML == "Temperature Status: RUNNING")||(document.getElementById('potStatusInfo').innerHTML == "Potential Hydrogen Status: RUNNING")){
    var fermentationActual = parseInt(jsonStatusInfoData['fermentationActual'], 10);
    
    var jsonFermentationInfoData = JSON.parse(fermentationsData);
    var currentFermentationData = jsonFermentationInfoData[fermentationActual];
    document.getElementById('fermInfo').innerHTML = "CURRENT FERMENTATION INFORMATION: \nSubstance: "+currentFermentation['sustance']+"\nObjective: "+currentFermentation['objective']+"\nMotive: "+currentFermentation['motive']+"\nBeginning Date: "+currentFermentation['beginning'];
  } else {
    document.getElementById('fermInfo').innerHTML = "NO FERMENTATION RUNNING";
  }
}

function updateInformation(fermentationsData){

  var xmlhttp = new XMLHttpRequest();
  xmlhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      var jsonInformation = this.responseText;
      updateVelocityInformation(jsonInformation);
      updateTemperatureInformation(jsonInformation);
      updatePotentialHydrogenInformation(jsonInformation);
      updateFermentationInformation(jsonInformation, fermentationsData);
    }
  };
  xmlhttp.open("GET", 'SystemData/StatusDataServer.json', true);
  xmlhttp.send();
}

function showFermentationsTable(){
  window.location.href = 'fermentationsDisplay.php';
}

function showReservationsTable(){
  window.location.href = 'reservationsDisplay.php';
}

function showParticipantsTable(){
  window.location.href = 'participantsDisplay.php';
}
