<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>POTENTIAL HYDROGEN (pH)</title>
  <script src="ServerJS/Chart.min.js"></script>
  <script src="ServerJS/potentialChartConfiguration.js"></script>
  <script src="ServerJS/jquery.min.js"></script>
  <script src="ServerJS/wow.min.js"></script>
  <link rel="stylesheet" href="ServerCSS/chartPageFormat.css">
</head>
<body>
  <div class="wow fadeInUp animated" data-wow-delay="1s">
  <h1>POTENTIAL HYDROGEN (pH) EVOLUTION</h1></div>
  <div class="wow fadeInDown animated" data-wow-delay="2s">
  <canvas id="potentialHydrogenChart" width="320" height="200"></canvas></div>
  <div class="wow fadeInRight animated" data-wow-delay="2s">
  <p id="potInformationData">pH CONTROL Data extracted from: </p>
  <br><br>
  <h2 id="potStatusTitle">STATUS of pH Control:</h2><br><br>
  <h3 id="potStatusData">NO Data Received</h3><br>
  <p id="potStatusInformationData">pH STATUS Data extracted from: </p></div>
 
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

  function getInformationFromPotentialFile($url){
    if(file_exists($url)){
      $fileSize = filesize($url);
      $fileLastAccess = date ("F d Y H:i:s.", fileatime($url));
      $fileLastModified = date ("F d Y H:i:s.", filemtime($url));
      $filePermissions = getFilePermissionsFormat($url)
      return [$fileSize, $filePermissions, $fileLastModified, $fileLastAccess];
    } else {
      return ["[Not Found]", "[Not Found]", "[Not Found]", "[Not Found]"];
    }
  }

  ?>

  <script>
 
  function updatePotentialHydrogenData(){
    var jsonPotential = '<?php echo getJSONdata() ?>';
    var currentPotentialControlFilename = "ControlData/PotentialHydrogen/DATA_Log/"+(jsonPotentialData.potentialControl)[0];
    var jsonPotentialDataFileInfo = '<?php echo json_encode(getInformationFromPotentialFile(currentPotentialControlFilename)); ?>';
    var potDataFileInfo1 = jsonPotentialDataFileInfo.split("[");
    var potDataFileInfo2 = potDataFileInfo1[1].split("]");
    var potDataFileInfo3 = potDataFileInfo2[0].split(",");
    var currentPotentialStatusFilename = "ControlData/PotentialHydrogen/STATUS_Log/"+(jsonPotentialData.potentialControl)[0];   
    var jsonPotentialStatusFileInfo = '<?php echo json_encode(getInformationFromPotentialFile(currentPotentialStatusFilename)); ?>';
    var potStatusFileInfo1 = jsonPotentialStatusFileInfo.split("[");
    var potStatusFileInfo2 = potStatusFileInfo1[1].split("]");
    var potStatusFileInfo3 = potStatusFileInfo2[0].split(",");
    updatePotentialGraphic(jsonPotential, potDataFileInfo3);
    updatePotentialStatus(jsonPotential, potStatusFileInfo3);
  }

  window.onload = function() {
    updatePotentialHydrogenData();
    setInterval(function(){updatePotentialHydrogenData()}, 10000);
  }

  </script>

</body>
</html>
