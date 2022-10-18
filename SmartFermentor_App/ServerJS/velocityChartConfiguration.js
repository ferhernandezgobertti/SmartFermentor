

function updateVelocityStatus(jsonVelocity, jsonVelocityFileInfo){

    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById('velStatusData').innerHTML = this.responseText;
        }
    };
    var jsonVelocityData = JSON.parse(jsonVelocity);
    var currentVelocityStatusFilename = "ControlData/Velocity/STATUS_Log/"+(jsonVelocityData.velocityControl)[0];   
    document.getElementById('velStatusInformationData').innerHTML = "Velocity STATUS Data extracted from "+currentVelocityControlFilename+", FILESIZE: "+jsonVelocityFileInfo[0]+" bytes with Permissions "+jsonVelocityFileInfo[1]+",\nLAST MODIFIED: "+jsonVelocityFileInfo[2]+", LAST ACCESSED: "+jsonVelocityFileInfo[3];
    xmlhttp.open("GET", currentVelocityStatusFilename, true);
    xmlhttp.send();
    
}
