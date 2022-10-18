<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>VELOCITY EVOLUTION</title>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.4.0/Chart.min.js"></script>
</head>
<body>
  <canvas id="myChart" width="400" height="250"></canvas>

 <script>
 var canvas = document.getElementById('myChart');
 var data = {
    labels: [0],
    datasets: [
        {
            label: "Velocity [rpm]",
            fill: false,
            lineTension: 0.1,
            backgroundColor: "rgba(75,192,192,0.4)",
            borderColor: "rgba(75,192,192,1)",
            borderCapStyle: 'butt',
            borderDash: [],
            borderDashOffset: 0.0,
            borderJoinStyle: 'miter',
            pointBorderColor: "rgba(75,192,192,1)",
            pointBackgroundColor: "#fff",
            pointBorderWidth: 1,
            pointHoverRadius: 5,
            pointHoverBackgroundColor: "rgba(75,192,192,1)",
            pointHoverBorderColor: "rgba(220,220,220,1)",
            pointHoverBorderWidth: 2,
            pointRadius: 5,
            pointHitRadius: 10,
            data: [0],
        }
    ]
};

function updateVelocityGraphic(){

<?php
    function getJSONdata(){
        $url = 'SystemData/StatusDataServer.json';
        $data = file_get_contents($url);
        return $data;
    }
?>

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
    var jsonVelocity = '<?php echo getJSONdata() ?>';
    jsonData = JSON.parse(jsonVelocity);
    console.log(jsonData);
    jsonDecoded = (jsonData.velocityControl)[0];
    console.log(jsonDecoded);
    xmlhttp.open("GET", jsonDecoded, true);
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
  updateVelocityGraphic();
  setInterval(function(){updateVelocityGraphic()}, 10000);
}

 </script>


</body>
</html>
