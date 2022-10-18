var canvas = document.getElementById('potentialHydrogenChart');
 var data = {
    labels: [0],
    datasets: [
        {
            label: "Potential Hydrogen [no dim.]",
            fill: false,
            lineTension: 0.1,
            backgroundColor: "rgba(75,192,192,0.4)",
            borderColor: "rgba(33, 205, 33, 1)",
            borderCapStyle: 'butt',
            borderDash: [],
            borderDashOffset: 0.0,
            borderJoinStyle: 'miter',
            pointBorderColor: "rgba(33, 205, 33, 1)",
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

function updatePotentialHydrogenGraphic(jsonPotential, jsonPotentialFileInfo){

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
    document.getElementById('potInformationData').innerHTML = "pH CONTROL Data extracted from "+currentPotentialControlFilename+", FILESIZE: "+jsonPotentialFileInfo[0]+" bytes with Permissions "+jsonPotentialFileInfo[1]+",\nLAST MODIFIED: "+jsonPotentialFileInfo[2]+", LAST ACCESSED: "+jsonPotentialFileInfo[3];
    xmlhttp.open("GET", currentPotentialControlFilename, true);
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

function updatePotentialHydrogenStatus(jsonPotential, jsonPotentialFileInfo){

    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById('potStatusData').innerHTML = this.responseText;
        }
    };
    var jsonPotentialData = JSON.parse(jsonPotential);
    var currentPotentialStatusFilename = "ControlData/PotentialHydrogen/STATUS_Log/"+(jsonPotentialData.potentialControl)[0];
    document.getElementById('potStatusInformationData').innerHTML = "pH STATUS Data extracted from "+currentPotentialStatusFilename+", FILESIZE: "+jsonPotentialFileInfo[0]+" bytes with Permissions "+jsonPotentialFileInfo[1]+",\nLAST MODIFIED: "+jsonPotentialFileInfo[2]+", LAST ACCESSED: "+jsonPotentialFileInfo[3];
    xmlhttp.open("GET", currentPotentialStatusFilename, true);
    xmlhttp.send();
    
}
