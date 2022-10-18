<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>TEMPERATURE</title>
  <script src="ServerJS/Chart.min.js"></script>
  <script src="ServerJS/temperatureChartConfiguration.js"></script>
  <script src="ServerJS/jquery.min.js"></script>
  <script src="ServerJS/wow.min.js"></script>
  <link rel="stylesheet" href="ServerCSS/chartPageFormat.css">
</head>
<body>
  <div class="wow fadeInUp animated" data-wow-delay="1s">
  <h1>TEMPERATURE EVOLUTION</h1></div>
  <div class="wow fadeInDown animated" data-wow-delay="2s">
  <canvas id="temperatureChart" width="320" height="200"></canvas></div>
  <div class="wow fadeInRight animated" data-wow-delay="2s">
  <p id="temInformationData">Temperature CONTROL Data extracted from: </p>
  <br><br>
  <h2 id="temStatusTitle">STATUS of Temperature Control:</h2><br><br>
  <h3 id="temStatusData">NO Data Received</h3><br>
  <p id="temStatusInformationData">Temperature STATUS Data extracted from: </p></div>
 
  <?php

  function getJSONdata(){
    $url = 'SystemData/StatusDataServer.json';
    $data = file_get_contents($url);
    return $data;
  }


  function getFilePermissionsFormat($url){
    $perms = fileperms($url);

    switch ($perms & 0xF000) {
      case 0xC000: // socket
        $info = 's';
        break;
      case 0xA000: // symbolic link
        $info = 'l';
        break;
      case 0x8000: // regular
        $info = 'r';
        break;
      case 0x6000: // block special
        $info = 'b';
        break;
      case 0x4000: // directory
        $info = 'd';
        break;
      case 0x2000: // character special
        $info = 'c';
        break;
      case 0x1000: // FIFO pipe
        $info = 'p';
        break;
      default: // unknown
        $info = 'u';
    }

    // Owner
    $info .= (($perms & 0x0100) ? 'r' : '-');
    $info .= (($perms & 0x0080) ? 'w' : '-');
    $info .= (($perms & 0x0040) ?
            (($perms & 0x0800) ? 's' : 'x' ) :
            (($perms & 0x0800) ? 'S' : '-'));

    // Group
    $info .= (($perms & 0x0020) ? 'r' : '-');
    $info .= (($perms & 0x0010) ? 'w' : '-');
    $info .= (($perms & 0x0008) ?
            (($perms & 0x0400) ? 's' : 'x' ) :
            (($perms & 0x0400) ? 'S' : '-'));

    // World
    $info .= (($perms & 0x0004) ? 'r' : '-');
    $info .= (($perms & 0x0002) ? 'w' : '-');
    $info .= (($perms & 0x0001) ?
            (($perms & 0x0200) ? 't' : 'x' ) :
            (($perms & 0x0200) ? 'T' : '-'));

    return $info;
  }

  function getInformationFromTemperatureFile($url){
    if(file_exists($url)){
      $fileSize = filesize($url);
      $fileLastAccess = date ("F d Y H:i:s.", fileatime($url));
      $fileLastModified = date ("F d Y H:i:s.", filemtime($url));
      $filePermissions = getFilePermissionsFormat($url)
      return array($fileSize, $filePermissions, $fileLastModified, $fileLastAccess);
    } else {
      return array("[Not Found]", "[Not Found]", "[Not Found]", "[Not Found]");
    }
  }

  ?>

  <script>
 
  function updateTemperatureData(){
    var jsonTemperature = '<?php echo getJSONdata() ?>';
    var currentTemperatureControlFilename = "ControlData/Temperature/DATA_Log/"+(jsonTemperatureData.temperatureControl)[0];
    var jsonTemperatureDataFileInfo = '<?php echo json_encode(getInformationFromTemperatureFile(currentTemperatureControlFilename)); ?>';
    var temDataFileInfo1 = jsonTemperatureDataFileInfo.split("[");
    var temDataFileInfo2 = temDataFileInfo1[1].split("]");
    var temDataFileInfo3 = temDataFileInfo2[0].split(",");
    var currentTemperatureStatusFilename = "ControlData/Temperature/STATUS_Log/"+(jsonTemperatureData.temperatureControl)[0];   
    var jsonTemperatureStatusFileInfo = '<?php echo json_encode(getInformationFromTemperatureFile(currentTemperatureStatusFilename)); ?>';
    var temStatusFileInfo1 = jsonTemperatureStatusFileInfo.split("[");
    var temStatusFileInfo2 = temStatusFileInfo1[1].split("]");
    var temStatusFileInfo3 = temStatusFileInfo2[0].split(",");
    updateTemperatureGraphic(jsonTemperature, temDataFileInfo3);
    updateTemperatureStatus(jsonTemperature, temStatusFileInfo3);
  }

  window.onload = function() {
    updateTemperatureData();
    setInterval(function(){updateTemperatureData()}, 10000);
  }

  </script>

</body>
</html>
