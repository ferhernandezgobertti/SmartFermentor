function loadReservationTable(jsonReservations){
  if(jsonReservations.length==0){
    var newRow = table.insertRow(1);
    var cel0 = newRow.insertCell(0);
    var cel1 = newRow.insertCell(1);
    var cel2 = newRow.insertCell(2);
    var cel3 = newRow.insertCell(3);
    cel0.innerHTML = "NO DATA";
    cel1.innerHTML = "NO DATA";
    cel2.innerHTML = "NO DATA";
    cel3.innerHTML = "NO DATA";
  } else {
    var jsonData =  JSON.parse(jsonReservations);
    var table = document.getElementsByTagName('table')[0];

    for (var i=0; i<jsonData.length; i++){
      var newRow = table.insertRow(1);
      var cel0 = newRow.insertCell(0);
      var cel1 = newRow.insertCell(1);
      var cel2 = newRow.insertCell(2);
      var cel3 = newRow.insertCell(3);
      cel0.innerHTML = jsonData[i]['dateBeginning']+" - "+jsonData[i]['dateEnding'];
      cel1.innerHTML = jsonData[i]['userToReserve']['name']+" "+jsonData[i]['userToReserve']['surname'];
      cel2.innerHTML = jsonData[i]['professorResponsible']['title'].charAt(0)+jsonData[i]['professorResponsible']['title'].charAt(1)+jsonData[i]['professorResponsible']['title'].charAt(2)+". "+jsonData[i]['professorResponsible']['name']+" "+jsonData[i]['professorResponsible']['surname'];
      cel3.innerHTML = jsonData[i]['precaution'].toUpperCase();
    }
  }
}
