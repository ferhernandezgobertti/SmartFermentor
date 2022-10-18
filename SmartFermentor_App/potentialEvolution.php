<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>POT. HYDROGEN</title>
<script src="ServerJS/Chart.min.js"></script>
<script src="ServerJS/jquery.min.js"></script>
<script src="ServerJS/wow.min.js"></script>
<link rel="stylesheet" href="ServerCSS/chartPageFormat.css">
</head>
<body>
<div class="wow fadeInUp animated" data-wow-delay="1s">
<h1>pH EVOLUTION</h1></div>
<div class="wow fadeInDown animated" data-wow-delay="2s">
<canvas id="potentialChart" width="320" height="200"></canvas><br></div>
<div class="wow fadeInRight animated" data-wow-delay="2s">
<p id="potInformationData">pH CONTROL Data extracted from: </p></div>

<script>
var canvas = document.getElementById('potentialChart');
var data = {
labels: [0],
datasets: [
    {
    label: "Potential Hydrogen Data",
    fill: false,
    lineTension: 0.1,
    backgroundColor: "rgba(75,192,192,0.4)",
    borderColor: "rgba(33, 205, 33, 1)",
    borderCapStyle: 'butt',
    borderDash: [],
    borderDashOffset: 0.0,
    borderJoinStyle: 'miter',
    pointBorderColor: "rgba(33, 205, 33, 1)", //(75,192,192,1)
    pointBackgroundColor: "#fff",
    pointBorderWidth: 1,
    pointHoverRadius: 5,
    pointHoverBackgroundColor: "rgba(33, 205, 33, 1)",
    pointHoverBorderColor: "rgba(220,220,220,1)",
    pointHoverBorderWidth: 2,
    pointRadius: 5,
    pointHitRadius: 10,
    data: [0],
    }
    ]
};


function updatePotentialHydrogenData(){
    
    <?php
    function getJSONdata(){
        $url = 'SystemData/StatusDataServer.json'; // path to your JSON file
        $data = file_get_contents($url); // put the contents of the file into a variable
        return $data;
    }
    ?>
    
    var jsonPotential = '<?php echo getJSONdata() ?>';
    var jsonPotentialData = JSON.parse(jsonPotential);
    var currentPotentialControlFilename = "ControlData/PotentialHydrogen/DATA_Log/"+(jsonPotentialData.potentialControl)[0];
    updatePotentialHydrogenGraphic(jsonPotential);
}


function updatePotentialHydrogenGraphic(jsonPotential){
    
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var firstNumber = [];
            var timeSeconds = [];
            
            var str = this.responseText;
            var firstLine = str.split("\n");
            
            for(var i=0; i<firstLine.length; i+=1){
                var eachLine = firstLine[i].split(",");
                if(!isNaN(eachLine[0]) && !isNaN(eachLine[4]) && !isNaN(eachLine[5])){
                    firstNumber.push(parseFloat(eachLine[0]));
                    timeSeconds.push(parseInt(eachLine[4])+0.000001*parseInt(eachLine[5]));
                }
            }
            myLineChart.data.datasets[0].data = firstNumber;
            myLineChart.data.labels = timeSeconds;
            myLineChart.update();
        }
    };
    var jsonPotentialData = JSON.parse(jsonPotential);
    var currentPotentialControlFilename = "ControlData/PotentialHydrogen/DATA_Log/"+(jsonPotentialData.potentialControl)[0];
    document.getElementById('potInformationData').innerHTML = "pH CONTROL Data extracted from "+currentPotentialControlFilename;
    xmlhttp.open("GET", currentPotentialControlFilename, true);
    xmlhttp.send();
    
}

var option = {
showLines: true
    
};
var myLineChart = new Chart(canvas , {
                            type: "line",
                            data: data,
                            options: {
                            showLines: true,
                            title: {
                            display: true,
                            text: 'Potential Hydrogen [adim.]',
                            fontSize: 48,
                            fontColor: "#085454"
                            }
                            }
                            });

window.onload = function() {
    updatePotentialHydrogenData();
    setInterval(function(){updatePotentialHydrogenData()}, 10000);
}

</script>

</body>
</html>
