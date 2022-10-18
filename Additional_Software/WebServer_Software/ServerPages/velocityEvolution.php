<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>VELOCITY</title>
  <script src="ServerJS/Chart.min.js"></script>
  <script src="ServerJS/jquery.min.js"></script>
  <script src="ServerJS/wow.min.js"></script>
  <link rel="stylesheet" href="ServerCSS/chartPageFormat.css">
</head>
<body>
  <div class="wow fadeInUp animated" data-wow-delay="1s">
  <h1>VELOCITY EVOLUTION</h1></div>
  <div class="wow fadeInDown animated" data-wow-delay="2s">
  <canvas id="velocityChart" width="320" height="200"></canvas><br></div>
  <div class="wow fadeInRight animated" data-wow-delay="2s">
  <p id="velInformationData">Velocity CONTROL Data extracted from: </p>
  <br><br>
  <h2 id="velStatusTitle">STATUS of Velocity Control:</h2><br><br>
  <h3 id="velStatusData">NO Data Received</h3><br>
  <p id="velStatusInformationData">Velocity STATUS Data extracted from: </p></div>
 
  <script>
  var canvas = document.getElementById('velocityChart');
  var data = {
  labels: [0],
  datasets: [{
      label: "Velocity [rpm]",
      fill: false,
      lineTension: 0.1,
      backgroundColor: "rgba(75,192,192,0.4)",
      borderColor: "rgba(33,33,233,1)",
      borderCapStyle: 'butt',
      borderDash: [],
      borderDashOffset: 0.0,
      borderJoinStyle: 'miter',
      pointBorderColor: "rgba(33,33,233,1)", //(75,192,192,1)
      pointBackgroundColor: "#fff",
      pointBorderWidth: 1,
      pointHoverRadius: 5,
      pointHoverBackgroundColor: "rgba(75,192,192,1)",
      pointHoverBorderColor: "rgba(220,220,220,1)",
      pointHoverBorderWidth: 2,
      pointRadius: 5,
      pointHitRadius: 10,
      data: [0],
  }]
};

  <?php

  function getJSONdata(){
    $url = 'SystemData/StatusDataServer.json';
    $data = file_get_contents($url);
    return $data;
  }

 
  function updateVelocityData(){
    var jsonVelocity = '<?php echo getJSONdata() ?>';
    console.log(jsonVelocity);
    var jsonVelocityData = JSON.parse(jsonVelocity);
    var currentVelocityControlFilename = "ControlData/Velocity/DATA_Log/"+(jsonVelocityData.velocityControl)[0];
    console.log(currentVelocityControlFilename);
    var jsonVelocityDataFileInfo = '<?php echo json_encode(getInformationFromVelocityFile(currentVelocityControlFilename)); ?>';
    var velDataFileInfo1 = jsonVelocityDataFileInfo.split("[");
    var velDataFileInfo2 = velDataFileInfo1[1].split("]");
    var velDataFileInfo3 = velDataFileInfo2[0].split(",");
    var currentVelocityStatusFilename = "ControlData/Velocity/STATUS_Log/"+(jsonVelocityData.velocityControl)[0];   
    var jsonVelocityStatusFileInfo = '<?php echo json_encode(getInformationFromVelocityFile(currentVelocityStatusFilename)); ?>';
    var velStatusFileInfo1 = jsonVelocityStatusFileInfo.split("[");
    var velStatusFileInfo2 = velStatusFileInfo1[1].split("]");
    var velStatusFileInfo3 = velStatusFileInfo2[0].split(",");
    updateVelocityGraphic(jsonVelocity, velDataFileInfo3);
    }

  
function updateVelocityGraphic(jsonVelocity, jsonVelocityFileInfo){

    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var firstNumber = [];
            var timeSeconds = [];

            var str = this.responseText;
            var firstLine = str.split("\n");

            for(var i=0; i<firstLine.length; i+=1){
                var eachLine = firstLine[i].split(",");
                if(!isNaN(eachLine[0]) && !isNaN(eachLine[3]) && !isNaN(eachLine[4])){
                    firstNumber.push(parseFloat(eachLine[0]));
                    timeSeconds.push(parseInt(eachLine[3])+0.000001*parseInt(eachLine[4]));
                }
            }
            myLineChart.data.datasets[0].data = firstNumber;
            myLineChart.data.labels = timeSeconds;
            myLineChart.update();
        }
    };
    var jsonVelocityData = JSON.parse(jsonVelocity);
    var currentVelocityControlFilename = "ControlData/Velocity/DATA_Log/"+(jsonVelocityData.velocityControl)[0];
    document.getElementById('velInformationData').innerHTML = "Velocity CONTROL Data extracted from "+currentVelocityControlFilename+", FILESIZE: "+jsonVelocityFileInfo[0]+" bytes with Permissions "+jsonVelocityFileInfo[1]+",\nLAST MODIFIED: "+jsonVelocityFileInfo[2]+", LAST ACCESSED: "+jsonVelocityFileInfo[3];
    xmlhttp.open("GET", currentVelocityControlFilename, true);
    xmlhttp.send();
    
}

var option = {
        showLines: true
};
var myLineChart = new Chart(canvas , {
    type: "line",
    data: data, 
    options: option
});

  window.onload = function() {
    alert("ENTRASTE A VELOCITY")
    updateVelocityData();
    setInterval(function(){updateVelocityData()}, 10000);
  }

  </script>

</body>
</html>
