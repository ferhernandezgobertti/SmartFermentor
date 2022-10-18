function loadProfessorsToParticipantsTable(jsonProfessors){
  if(jsonProfessors.length==0){
    var newRow = table.insertRow(1);
    var cel0 = newRow.insertCell(0);
    var cel1 = newRow.insertCell(1);
    var cel2 = newRow.insertCell(2);
    var cel3 = newRow.insertCell(3);
    var cel4 = newRow.insertCell(4);
    cel0.innerHTML = "NO PROFESSORS DATA";
    cel1.innerHTML = "NO PROFESSORS DATA";
    cel2.innerHTML = "NO PROFESSORS DATA";
    cel3.innerHTML = "NO PROFESSORS DATA";
    cel4.innerHTML = "NO PROFESSORS DATA";
  } else {
    var jsonData =  JSON.parse(jsonProfessors);
    var table = document.getElementsByTagName('table')[0];

    for (var i=0; i<jsonData.length; i++){
      var newRow = table.insertRow(1);
      var cel0 = newRow.insertCell(0);
      var cel1 = newRow.insertCell(1);
      var cel2 = newRow.insertCell(2);
      var cel3 = newRow.insertCell(3);
      var cel4 = newRow.insertCell(4);
      cel0.innerHTML = jsonData[i]['surname'].toUpperCase()+", "+jsonData[i]['name'];
      cel1.innerHTML = jsonData[i]['usernumber'];
      cel2.innerHTML = jsonData[i]['email'];
      cel3.innerHTML = jsonData[i]['fermentsQuantity'];
      cel4.innerHTML = jsonData[i]['lastEntry'];
    }
  }
}

function loadStudentsToParticipantsTable(jsonStudents){
  if(jsonStudents.length==0){
    var newRow = table.insertRow(1);
    var cel0 = newRow.insertCell(0);
    var cel1 = newRow.insertCell(1);
    var cel2 = newRow.insertCell(2);
    var cel3 = newRow.insertCell(3);
    var cel4 = newRow.insertCell(4);
    cel0.innerHTML = "NO STUDENTS DATA";
    cel1.innerHTML = "NO STUDENTS DATA";
    cel2.innerHTML = "NO STUDENTS DATA";
    cel3.innerHTML = "NO STUDENTS DATA";
    cel4.innerHTML = "NO STUDENTS DATA";
  } else {
    var jsonData =  JSON.parse(jsonStudents);
    var table = document.getElementsByTagName('table')[0];

    for (var i=0; i<jsonData.length; i++){
      var newRow = table.insertRow(1);
      var cel0 = newRow.insertCell(0);
      var cel1 = newRow.insertCell(1);
      var cel2 = newRow.insertCell(2);
      var cel3 = newRow.insertCell(3);
      var cel4 = newRow.insertCell(4);
      cel0.innerHTML = jsonData[i]['surname'].toUpperCase()+", "+jsonData[i]['name'];
      cel1.innerHTML = jsonData[i]['usernumber'];
      cel2.innerHTML = jsonData[i]['email'];
      cel3.innerHTML = jsonData[i]['fermentsQuantity'];
      cel4.innerHTML = jsonData[i]['lastEntry'];
    }
  }
}
