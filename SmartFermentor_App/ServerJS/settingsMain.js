function seeFermentationsInformation(){
    window.location.href='fermentationsDisplay.php';
}
$("#fermentationInfo").click(function() {
    setTimeout(seeFermentationsInformation, 1000);
});

function seeReservationsInformation(){
    window.location.href='reservationsDisplay.php';
}
$("#reservesInfo").click(function() {
    setTimeout(seeReservationsInformation, 1000);
});

function seeParticipantsInformation(){
    window.location.href='participantsDisplay.php';
}
$("#participantsInfo").click(function() {
    setTimeout(seeParticipantsInformation, 1000);
});


function runVelocity(){
    recordNumber = 1;
    jQuery.ajax({
        type: "POST",
        url: "editingVelControl.php",
        data: {
            recordNumberFromJavascript: recordNumber
        },
        dataType: "html"
    }).done(function(result){
        alert("Velocity Control SUCCESFULLY Started");
    });
}

function stopVelocity(){
    recordNumber = 3;
    jQuery.ajax({
        type: "POST",
        url: "editingVelControl.php",
        data: {
            recordNumberFromJavascript: recordNumber
        },
        dataType: "html"
    }).done(function(result){
        alert("Velocity Control SUCCESFULLY Stopped");
    });
}

function pauseVelocity(){
    recordNumber = 2;
    jQuery.ajax({
        type: "POST",
        url: "editingVelControl.php",
        data: {
            recordNumberFromJavascript: recordNumber
        },
        dataType: "html"
    }).done(function(result){
        alert("Velocity Control SUCCESFULLY Paused");
    });
}

function restartVelocity(){
    recordNumber = 6;
    jQuery.ajax({
        type: "POST",
        url: "editingVelControl.php",
        data: {
            recordNumberFromJavascript: recordNumber
        },
        dataType: "html"
    }).done(function(result){
        alert("Velocity Control SUCCESFULLY Restarted");
    });
}

function seeTemperatureEvolution(){
    window.location.href='temperatureEvolution.php';
}
$("#temperatureEvolution").click(function() {
    setTimeout(seeTemperatureEvolution, 1000);
});

function stopTemperature(){
    recordNumber = 3;
    jQuery.ajax({
        type: "POST",
        url: "editingTemControl.php",
        data: {
            recordNumberFromJavascript: recordNumber
        },
        dataType: "html"
    }).done(function(result){
        alert("Temperature Control SUCCESFULLY Stopped");
    });
}

function pauseTemperature(){
    recordNumber = 2;
    jQuery.ajax({
        type: "POST",
        url: "editingTemControl.php",
        data: {
            recordNumberFromJavascript: recordNumber
        },
        dataType: "html"
    }).done(function(result){
        alert("Temperature Control SUCCESFULLY Paused");
    });
}

function restartTemperature(){
    recordNumber = 6;
    jQuery.ajax({
        type: "POST",
        url: "editingTemControl.php",
        data: {
            recordNumberFromJavascript: recordNumber
        },
        dataType: "html"
    }).done(function(result){
        alert("Temperature Control SUCCESFULLY Restarted");
    });
}

function runTemperature(){
    recordNumber = 1;
    jQuery.ajax({
        type: "POST",
        url: "editingTemControl.php",
        data: {
            recordNumberFromJavascript: recordNumber
        },
        dataType: "html"
    }).done(function(result){
        alert("Temperature Control SUCCESFULLY Started");
    });
}

function seePotentialHydrogenEvolution(){
    window.location.href='potentialEvolution.php';
}
$("#potentialEvolution").click(function() {
    setTimeout(seePotentialHydrogenEvolution, 1000);
});

function restartPotentialHydrogen(){
    recordNumber = 6;
    jQuery.ajax({
        type: "POST",
        url: "editingPotControl.php",
        data: {
            recordNumberFromJavascript: recordNumber
        },
        dataType: "html"
    }).done(function(result){
        alert("Potential Hydrogen (pH) Control SUCCESFULLY Restarted");
    });
}

function pausePotentialHydrogen(){
    recordNumber = 2;
    jQuery.ajax({
        type: "POST",
        url: "editingPotControl.php",
        data: {
            recordNumberFromJavascript: recordNumber
        },
        dataType: "html"
    }).done(function(result){
        alert("Potential Hydrogen (pH) Control SUCCESFULLY Paused");
    });
}

function stopPotentialHydrogen(){
    recordNumber = 3;
    jQuery.ajax({
        type: "POST",
        url: "editingPotControl.php",
        data: {
            recordNumberFromJavascript: recordNumber
        },
        dataType: "html"
    }).done(function(result){
        alert("Potential Hydrogen (pH) Control SUCCESFULLY Stopped");
    });
}

function runPotentialHydrogen(){
    recordNumber = 1;
    jQuery.ajax({
        type: "POST",
        url: "editingPotControl.php",
        data: {
            recordNumberFromJavascript: recordNumber
        },
        dataType: "html"
    }).done(function(result){
        alert("Potential Hydrogen (pH) Control SUCCESFULLY Started");
    });
}
