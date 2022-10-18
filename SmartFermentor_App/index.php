<!DOCTYPE html>
<html lang="en" >
<header><title> SMARTFERMENTOR </title></header>
<head>
  <title>SmartFermentor - ORT University</title>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script src="ServerJS/jquery.min.js"></script>
  <script src="ServerJS/wow.min.js"></script>
  <script src="ServerJS/translationsLogin.js"></script>
  <script src="ServerJS/animationsLogin.js"></script>
  <script src="ServerJS/functionsLogin.js"></script>
  <link rel="stylesheet" href="ServerCSS/w3.css">
  <link rel="stylesheet" href="ServerCSS/normalize.min.css">
  <link rel="stylesheet" href="ServerCSS/animate.css">
  <link rel="stylesheet" href="ServerCSS/styleLogin.css">
  <link rel="stylesheet" href="ServerCSS/fontLogin.css">
</head>


<body style="background-color:#085454;">

  <div class="container fadeInUp animated" id="axis">

	<svg viewBox="0 0 1900 400" version="1.1">
		<title>Smart Fermentor</title>
		<g stroke="none" fill="none" fill-rule="evenodd" fill-opacity="0">
	        <text id="SmartFermentor" stroke="#fff" fill="#085454"  font-weight="normal" font-size="250">
				           <tspan x="4" y="240"><!--
					--><tspan>S</tspan><!--
					--><tspan>m</tspan><!--
					--><tspan>a</tspan><!--
					--><tspan>r</tspan><!--
					--><tspan>t</tspan><!--
					--><tspan> </tspan><!--
					--><tspan>F</tspan><!--
					--><tspan>e</tspan><!--
					--><tspan>r</tspan><!--
					--><tspan>m</tspan><!--
					--><tspan>e</tspan><!--
					--><tspan>n</tspan><!--
					--><tspan>t</tspan><!--
					--><tspan>o</tspan><!--
					--><tspan>r</tspan><!--
				--></tspan>
			</text>
		</g>
	</svg>

</div>

<br>

<div class="smartSystem wow fadeInLeft animated" data-wow-delay="2s">
<img class="smartSystemImage" align="left" src="ServerImages/SmartSystem08.png" height=680>
</div>

<div class="container wow fadeInRight animated" data-wow-delay="2s">
<label for="usernumber" class="lang" key="userTitle" id="usernumberTitle">Usernumber: </label>
<input type="text" id="usernumber" name="fname" style="float:left; text-align:center;" size="15" maxlength="6">
</div>

<div class="container wow fadeInRight animated" data-wow-delay="2s">
<label for="userpassword" class="lang" key="passTitle" id="userpasswordTitle">Password: </label>
<input type="password" id="userpassword" name="lname" style="float:right; text-align:center;" size="15" maxlength="12">
</div>

<div class="container wow fadeInDown animated" data-wow-delay="2s">
<label class="passwordShow lang" key="passShow">Show Password
  <input type="radio" name="radio" id="radioPassword" onclick="showPasswordOption()">
  <span class="checkmark"></span>
</label>
</div>

<br>

<div class="container wow fadeInDown animated" data-wow-delay="2s">
<button class="styled animate lang" key="logInSession">LOG IN</button> <!--  -->
</div>

<script>
function changePage(){
  window.location.href = 'userPage.php';
}
</script>

<?php

  function decrypt_aes256($data, $key, $initVector){
    $initVector = str_pad($initVector, 16, "\0");
    $encryptedData = base64_decode($data);
    $decryptedData = openssl_decrypt($encryptedData, "AES-256-CBC", $key, OPENSSL_RAW_DATA, $initVector);
    return $decryptedData;
  }

  function decryptServerProfessorData(){
    $key = "Biotec.ORT1450";
    $initVector = "CB+I_OrtURU";
    $encryptedData = file_get_contents('/var/www/html/SystemData/ProfessorsData.json');
    $usersInformation = json_decode($encryptedData);
    $decryptedData = decrypt_aes256($usersInformation->info, $key, $initVector);
    $hashedData = base64_encode(hash_hmac("sha256", $usersInformation->info, "my_secret", true));
    return $decryptedData;
  }

  function decryptServerStudentData(){
    $key = "Biotec.ORT1450";
    $initVector = "CB+I_OrtURU";
    $encryptedData = file_get_contents('/var/www/html/SystemData/StudentsData.json');
    $usersInformation = json_decode($encryptedData);
    $decryptedData = decrypt_aes256($usersInformation->info, $key, $initVector);
    $hashedData = base64_encode(hash_hmac("sha256", $usersInformation->info, "my_secret", true));
    return $decryptedData;
  }
?>
<script>
function loadProfessorsInformation(){ 
  var professorsData = '<?php echo decryptServerProfessorData() ?>';
  return professorsData;
}

function loadStudentsInformation(){
  var studentsData = '<?php echo decryptServerStudentData() ?>';
  return studentsData;
}
</script>
<br>

<div class="smartSystem wow fadeInUp animated" data-wow-delay="2s"><center>
<img src="ServerImages/smartFermentorTheme.png" id="smartTheme" height=200></center>
</div>

<br><br>

<div class="smartSystem wow flipInX animated" data-wow-delay="1s">
<label class="messageInformation lang" style="text-align:center;" key="smartMessage">-We're honored to present the result of months of hard work and perseverence, and to be able to introduce something useful to the scientific society. We thank ORT Uruguay University for the given opportunity - SmartFermentor Group</label>
</div>
<div class="smartSystem wow fadeInUp animated" data-wow-delay="1s"><center>
<img src="ServerImages/ortLogo.png" id="smartORTLogo" height=120>
</center></div>

<div class="smartSystem wow fadeInDown animated" data-wow-delay="1s">
<label class="evolutionInformation lang" style="text-align:center;" key="smartEvolution">When in doubt, feel free to read our User and Equipment Manual. Also, see the Manufacturing Evolution and Developing Process through this Slideshow:
</div>

<!--Slideshow de Imagenes -->
<div class="w3-content w3-section wow fadeInRight animated" style="max-width:540px" data-wow-delay="1s" id="smartSlideshow"><center>
  <img class="mySlides w3-animate-fading" src="ServerImages/SmartSystem08.png" width=540 height=490>
  <img class="mySlides w3-animate-fading" src="ServerImages/SmartSystem01.png" width=540 height=490>
  <img class="mySlides w3-animate-fading" src="ServerImages/SmartSystem02.png" width=540 height=490>
  <img class="mySlides w3-animate-fading" src="ServerImages/SmartSystem03.png" width=540 height=490>
  <img class="mySlides w3-animate-fading" src="ServerImages/SmartSystem04.png" width=540 height=490>
  <img class="mySlides w3-animate-fading" src="ServerImages/SmartSystem05.png" width=540 height=490>
  <img class="mySlides w3-animate-fading" src="ServerImages/SmartSystem06.png" width=540 height=490>
  <img class="mySlides w3-animate-fading" src="ServerImages/SmartSystem07.png" width=540 height=490>
</center></div>

<center>
<button class="translate" id="en"><img src="ServerImages/englandFlag.png"></button>
<button class="translate" id="es"><img src="ServerImages/spainFlag.png"></button>
<button class="translate" id="pt"><img src="ServerImages/brazilFlag.png"></button>
<button class="translate" id="de"><img src="ServerImages/germanyFlag.png"></button>
</center>
</body>

<script> carousel();

$(".styled").click(function() {
  console.log("ENTRO FUNCTION");
  userIdentified = checkUser();
  console.log(userIdentified);
  if(userIdentified == 1){
    $(".container").addClass("fadeOutLeft animated");
    $("#usernumberTitle").addClass("fadeOutRight animated");
    $("#usernumber").addClass("fadeOutRight animated");
    $("#userpasswordTitle").addClass("fadeOutRight animated");
    $("#userpassword").addClass("fadeOutRight animated");
    $(".smartSystemImage").addClass("fadeOutLeft animated");
    $(".passwordShow").addClass("fadeOutLeft animated");
    $(".styled").addClass("fadeOutDown animated");
    $("#smartTheme").addClass("fadeOutDown animated");
    $(".messageInformation").addClass("fadeOutRight animated");
    $("#smartORTLogo").addClass("fadeOutDown animated");
    $("#smartANIILogo").addClass("fadeOutDown animated");
    $(".evolutionInformation").addClass("fadeOutLeft animated");
    $("#smartSlideshow").addClass("fadeOutRight animated");
    setTimeout(changePage, 1000);
  } else {
    alert("Failed to Identify You. Please try again");
  }  
});

</script>
</html>

