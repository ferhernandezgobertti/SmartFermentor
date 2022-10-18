var canvas = document.getElementById('temperatureChart');
var data = {
  labels: [0],
  datasets: [{
    label: "Temperature [Celsius]",
    fill: false,
    lineTension: 0.1,
    backgroundColor: "rgba(75,192,192,0.4)",
    borderColor: "rgba(255, 105, 0, 1)",
    borderCapStyle: 'butt',
    borderDash: [],
    borderDashOffset: 0.0,
    borderJoinStyle: 'miter',
    pointBorderColor: "rgba(255, 105, 0, 1)",
    pointBackgroundColor: "#fff",
    pointBorderWidth: 1,
    pointHoverRadius: 5,
    pointHoverBackgroundColor: "rgba(255, 105, 0, 1)",
    pointHoverBorderColor: "rgba(220,220,220,1)",
    pointHoverBorderWidth: 2,
    pointRadius: 5,
    pointHitRadius: 10,
    data: [0],
  }]
};

function updateTemperatureGraphic(jsonTemperature, jsonTemperatureFileInfo){

    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var firstNumber = [];
            var timeSeconds = [];

            var str = this.responseText;
            var firstLine = str.split("\n");

            for(var i=0; i<firstLine.length; i+=1){
                var eachLine = firstLine[i].split(",");
                if(!isNaN(eachLine[0]) && !isNaN(eachLine[5]) && !isNaN(eachLine[6])){
                    firstNumber.push(parseFloat(eachLine[0]));
                    timeSeconds.push(parseInt(eachLine[5])+0.000001*parseInt(eachLine[6]));
                }
            }
            myLineChart.data.datasets[0].data = firstNumber;
            myLineChart.data.labels = timeSeconds;
            myLineChart.update();
        }
    };
    var jsonTemperatureData = JSON.parse(jsonTemperature);
    var currentTemperatureControlFilename = "ControlData/Temperature/DATA_Log/"+(jsonTemperatureData.temperatureControl)[0];
    document.getElementById('temInformationData').innerHTML = "Temperature CONTROL Data extracted from "+currentTemperatureControlFilename+", FILESIZE: "+jsonTemperatureFileInfo[0]+" bytes with Permissions "+jsonTemperatureFileInfo[1]+",\nLAST MODIFIED: "+jsonTemperatureFileInfo[2]+", LAST ACCESSED: "+jsonTemperatureFileInfo[3];
    xmlhttp.open("GET", currentTemperatureControlFilename, true);
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

function updateTemperatureStatus(jsonTemperature, jsonTemperatureFileInfo){

    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById('temStatusData').innerHTML = this.responseText;
        }
    };
    var jsonTemperatureData = JSON.parse(jsonTemperature);
    var currentTemperatureStatusFilename = "ControlData/Temperature/STATUS_Log/"+(jsonTemperatureData.temperatureControl)[0];
    document.getElementById('temStatusInformationData').innerHTML = "Temperature STATUS Data extracted from "+currentTemperatureStatusFilename+", FILESIZE: "+jsonTemperatureFileInfo[0]+" bytes with Permissions "+jsonTemperatureFileInfo[1]+",\nLAST MODIFIED: "+jsonTemperatureFileInfo[2]+", LAST ACCESSED: "+jsonTemperatureFileInfo[3];
    xmlhttp.open("GET", currentTemperatureStatusFilename, true);
    xmlhttp.send();
    
}

