<!DOCTYPE html>
<html lang="en" >
<header><title> USER PAGE </title></header>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="ServerJS/wow.min.js"></script>
<script src="ServerJS/jquery.min.js"></script>
<script src="ServerJS/settingsMain.js"></script>
<script src="ServerJS/informationMain.js"></script>
<script src="ServerJS/animationsMain.js"></script>
<script src="ServerJS/translationsMain.js"></script>
<link rel="stylesheet" href="ServerCSS/animate.css">
<link rel="stylesheet" href="ServerCSS/styleMain.css">
</head>

<body style="background-color:#085454;">
<center>
<div class="smartSystem wow fadeInDown animated" data-wow-delay="1s">
<img src="ServerImages/smartFermentorLogo.png" id="smartLogo" height=150>
</div>



<div class="smartSystem wow fadeInUp animated" data-wow-delay="1s">
<button class="systemInformation lang" key="fermDataInfo" id="fermentationInfo"><img src="ServerImages/chemicalReactionLogo.png" height=120px width=120px onclick="showFermentationsTable()"><br>Fermentations Data</button>
<button class="systemInformation lang" key="reservesDataInfo" id="reservesInfo"><img src="ServerImages/calendarReservesLogo.png" height=120px width=120px onclick="showReservationsTable()"><br>Reserves Information</button>
<button class="systemInformation lang" key="contactsDataInfo" id="participantsInfo"><img src="ServerImages/contactsLogo.png" height=120px width=120px onclick="showParticipantsTable()"><br>Participants</button>
<button class="systemInformation lang" key="cameraDataInfo" id="cameraInfo"><img src="ServerImages/camaraStreamingLogo.png" height=120px width=120px><br>Live Streaming</button>
</div>

<br><br>

<div class="smartSystem wow slideInDown animated" data-wow-delay="1s">
<img src="ServerImages/systemScheme.png" id="smartScheme" height=800>
</div>

<img class="turnLogo1" src="ServerImages/turnClockLogo.png" height=45>
<img class="turnLogo2" src="ServerImages/turnClock2Logo.png" height=45>
<img class="turnLogo1Liquid" src="ServerImages/turnClockwiseLogo.png" height=45>
<img class="turnLogo2Liquid" src="ServerImages/turnAntiClockwiseLogo.png" height=45>
<img class="fluidIn" src="ServerImages/fluidDirectionLogo.png" height=45>
<img class="fluidDirection1" src="ServerImages/fluidDownLogo.png" height=90>
<img class="fluidDirection2" src="ServerImages/fluidDownCornerLogo.png" height=75>
<img class="fluidDirection3" src="ServerImages/fluidUpCornerLogo.png" height=75>
<img class="fluidDirection4" src="ServerImages/fluidUpLogo.png" height=90>
<img class="temperatureSensor" src="ServerImages/temperatureSensorActionLogo.png" height=75>
<img class="potentialSensor" src="ServerImages/pHSensorActionLogo.png" height=75>
<img class="dropsBase1" src="ServerImages/dropBaseLogo.png" height=25>
<img class="dropsBase2" src="ServerImages/dropBaseLogo.png" height=25>
<img class="dropsAcid1" src="ServerImages/dropAcidLogo.png" height=25>
<img class="dropsAcid2" src="ServerImages/dropAcidLogo.png" height=25>
<img class="bubblesLiquid1" src="ServerImages/bubblesLogo.png" height=25>
<img class="bubblesLiquid2" src="ServerImages/bubblesLogo.png" height=25>
<img class="bubblesLiquid3" src="ServerImages/bubblesLogo.png" height=25>
<img class="bubblesLiquid4" src="ServerImages/bubblesLogo.png" height=25>
<img class="bubblesLiquid5" src="ServerImages/bubblesLogo.png" height=25>
<img class="bubblesLiquid6" src="ServerImages/bubblesLogo.png" height=25>
<img class="fluidOut" src="ServerImages/fluidDirectionOutLogo.png" height=45>

<div class="smartSystem wow lightSpeedIn animated" data-wow-delay="1s">
<button class="styled buttonVelocity lang" key="evolVel" id="velocityEvolution"><img src="ServerImages/velocityMotor.png" height=200px width=200px><br>VELOCITY Evolution</button>
<button class="velRun buttonVelocity lang" key="runControl" id="runControlOption"><img src="ServerImages/runControlLogo.png" height=100px width=100px onclick="runVelocity();"><br>RUN</button>
<button class="velPause buttonVelocity lang" key="pauseControl" id="pauseControlOption"><img src="ServerImages/pauseControlLogo.png" height=100px width=100px onclick="pauseVelocity();"><br>PAUSE</button>
<button class="velStop buttonVelocity lang" key="stopControl" id="stopControlOption"><img src="ServerImages/stopControlLogo.png" height=100px width=100px onclick="stopVelocity();"><br>STOP</button>
<button class="buttonVelocity lang" key="restartControl" id="restartControlOption"><img src="ServerImages/restartControlLogo.png" height=100px width=100px onclick="restartVelocity();"><br>RESTART</button>
</div>

<br><br>

<div class="smartSystem wow zoomIn animated" data-wow-delay="1s">
<label for="velocityControl" class="velocityInformation" id="velControlInfo">Velocity Control: ...</label><br>
<label for="velocityStatus" class="velocityInformation" id="velStatusInfo">Velocity Status: ....</label><br>
<label for="velocityStep" class="velocityInformation" id="velStepInfo">Velocity Step: .......</label><br></div>

<br><br><br>

<div class="smartSystem wow lightSpeedIn animated" data-wow-delay="1s">
<button class="buttonTemperature lang" key="evolTem" id="temperatureEvolution"><img src="ServerImages/temperatureBath.png" height=200px width=150px><img src="ServerImages/temperatureSensor.png" height=200px width=150px><br>TEMPERATURE Evolution</button>
<button class="buttonTemperature lang" key="runControl" id="runControlOption"><img src="ServerImages/runControlLogo.png" height=100px width=100px onclick="runTemperature();"><br>RUN</button>
<button class="buttonTemperature lang" key="pauseControl" id="pauseControlOption"><img src="ServerImages/pauseControlLogo.png" height=100px width=100px onclick="pauseTemperature();"><br>PAUSE</button>
<button class="buttonTemperature lang" key="stopControl" id="stopControlOption"><img src="ServerImages/stopControlLogo.png" height=100px width=100px onclick="stopTemperature();"><br>STOP</button>
<button class="buttonTemperature lang" key="restartControl" id="restartControlOption"><img src="ServerImages/restartControlLogo.png" height=100px width=100px onclick="restartTemperature();"><br>RESTART</button>
</div>

<br><br>

<div class="smartSystem wow zoomIn animated" data-wow-delay="1s">
<label for="temperatureControl" class="temperatureInformation" id="temControlInfo">Temperature Control: ...</label><br>
<label for="temperatureStatus" class="temperatureInformation" id="temStatusInfo">Temperature Status: ....</label><br>
<label for="temperatureStep" class="temperatureInformation" id="temStepInfo">Temperature Step: .......</label><br></div>

<br><br><br>

<div class="smartSystem wow lightSpeedIn animated" data-wow-delay="1s">
<button class="buttonPotential lang" key="evolPot" id="potentialEvolution"><img src="ServerImages/potentialBox.png" height=200px width=150px><img src="ServerImages/potentialSensor.png" height=200px width=150px><br>POT HYDROGEN Evolution</button>
<button class="buttonPotential lang" key="runControl" id="runControlOption"><img src="ServerImages/runControlLogo.png" height=100px width=100px onclick="runPotentialHydrogen();"><br>RUN</button>
<button class="buttonPotential lang" key="pauseControl" id="pauseControlOption"><img src="ServerImages/pauseControlLogo.png" height=100px width=100px onclick="pausePotentialHydrogen();"><br>PAUSE</button>
<button class="buttonPotential lang" key="stopControl" id="stopControlOption"><img src="ServerImages/stopControlLogo.png" height=100px width=100px onclick="stopPotentialHydrogen();"><br>STOP</button>
<button class="buttonPotential lang" key="restartControl" id="restartControlOption"><img src="ServerImages/restartControlLogo.png" height=100px width=100px onclick="restartPotentialHydrogen();"><br>RESTART</button>
</div>

<br><br>

<div class="smartSystem wow zoomIn animated" data-wow-delay="1s">
<label for="potentialControl" class="potentialInformation" id="potControlInfo">Potential Control: ... </label><br>
<label for="potentialStatus" class="potentialInformation" id="potStatusInfo">Potential Status: .... </label><br>
<label for="potentialStep" class="potentialInformation" id="potStepInfo">Potential Step: .......</label><br></div>

<br><br><br>
<h1></h1><br>
<label for="fermControl" class="fermentationInformation" id="fermInfo">NO FERMENTATION RUNNING</label>
<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>


<button class="translate" id="en"><img src="ServerImages/englandFlag.png"></button>
<button class="translate" id="es"><img src="ServerImages/spainFlag.png"></button>
<button class="translate" id="pt"><img src="ServerImages/brazilFlag.png"></button>
<button class="translate" id="de"><img src="ServerImages/germanyFlag.png"></button>
</center>
 
<?php

  function decrypt_aes256($data, $key, $initVector){
    $initVector = str_pad($initVector, 16, "\0");
    $encryptedData = base64_decode($data);
    $decryptedData = openssl_decrypt($encryptedData, "AES-256-CBC", $key, OPENSSL_RAW_DATA, $initVector);
    return $decryptedData;
  }

  function decryptServerData(){
    $key = "Biotec.ORT1450";
    $initVector = "CB+I_OrtURU";
    $encryptedData = file_get_contents('SystemData/FermentationsData.json');
    $professorsUsers = json_decode($encryptedData);
    $decryptedData = decrypt_aes256($professorsUsers->info, $key, $initVector);
    $hashedData = base64_encode(hash_hmac("sha256", $professorsUsers->info, "my_secret", true));
    return $decryptedData;
  }
?>

<script>

function seeVelocityEvolution(){
    window.location.href='velocityEvolution.php';
}

$("#velocityEvolution").click(function() {
    setTimeout(seeVelocityEvolution, 1000);
});

window.onload = function() {
  var countAnimation = [0, 0, 0, 0];
  var isAnimationEnabled = [false, false, false, false];
  var fermentationsData = '<?php echo decryptServerData() ?>';
  updateInformation(fermentationsData);
  setInterval(function(){updateInformation(fermentationsData)}, 10000);
  checkGeneralAnimations(countAnimation, isAnimationEnabled);
  setInterval(function(){checkGeneralAnimations(countAnimation, isAnimationEnabled)}, 1000);
}
</script>

</body>
</html>
