function loadFermentationTable(jsonFermentation){
  if(jsonFermentation.length==0){
    var newRow = table.insertRow(1);
    var cel0 = newRow.insertCell(0);
    var cel1 = newRow.insertCell(1);
    var cel2 = newRow.insertCell(2);
    var cel3 = newRow.insertCell(3);
    var cel4 = newRow.insertCell(4);
    var cel5 = newRow.insertCell(5);
    cel0.innerHTML = "NO DATA";
    cel1.innerHTML = "NO DATA";
    cel2.innerHTML = "NO DATA";
    cel3.innerHTML = "NO DATA";
    cel4.innerHTML = "NO DATA";
    cel5.innerHTML = "NO DATA";
  } else {
    var jsonData =  JSON.parse(jsonFermentation);
    var table = document.getElementsByTagName('table')[0];

    for (var i=0; i<jsonData.length; i++){
      var newRow = table.insertRow(1);
      var cel0 = newRow.insertCell(0);
      var cel1 = newRow.insertCell(1);
      var cel2 = newRow.insertCell(2);
      var cel3 = newRow.insertCell(3);
      var cel4 = newRow.insertCell(4);
      var cel5 = newRow.insertCell(5);
      cel0.innerHTML = jsonData[i]['beginning'];
      cel1.innerHTML = jsonData[i]['sustance'].toUpperCase();
      cel2.innerHTML = jsonData[i]['objective'];
      cel3.innerHTML = jsonData[i]['motive'];
      cel4.innerHTML = jsonData[i]['description'];
      cel5.innerHTML = jsonData[i]['user']['title'].charAt(0)+jsonData[i]['user']['title'].charAt(1)+jsonData[i]['user']['title'].charAt(2)+". "+jsonData[i]['user']['name']+" "+jsonData[i]['user']['surname'];
    }
  }
}


