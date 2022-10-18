function showPasswordOption() {
  var x = document.getElementById("userpassword");
  var y = document.getElementById("radioPassword");
  if (x.type === "password") {
    x.type = "text";
    y.checked = true;
  } else {
    x.type = "password";
    y.checked = false;
  }
}

function checkUser(){
  console.log("LLEGO A CHECKUSER");
  var userIdentified = 0;
  var usernumberTyped = document.getElementById("usernumber").value;
  var passwordTyped = document.getElementById("userpassword").value;
  var professorsData = JSON.parse(loadProfessorsInformation());
  for (var i=0; i<professorsData.length; i+=1){
    if(professorsData[i].usernumber == usernumberTyped && professorsData[i].password == passwordTyped){
      userIdentified = 1;
      break;
    }
  }
  var studentsData = JSON.parse(loadStudentsInformation());
  for (var i=0; i<studentsData.length; i+=1){
    if(studentsData[i].usernumber == usernumberTyped && studentsData[i].password == passwordTyped){
      userIdentified = 1;
      break;
    }
  }
  return userIdentified;
}


