<!DOCTYPE html>
<html lang="en" >
<header><title> PARTICIPANTS </title></header>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="ServerJS/jquery.min.js"></script>
<script src="ServerJS/wow.min.js"></script>
<script src="ServerJS/participantsTable.js"></script>
<link rel="stylesheet" href="ServerCSS/animate.css">
<link rel="stylesheet" href="ServerCSS/tableFormat.css">
</head>
<body style="background-color:#085454;">

<center>
<div class="smartSystem wow fadeInDown animated" data-wow-delay="1s">
<img src="ServerImages/smartFermentorLogo.png" id="smartLogo" height=150></div>

<div class="smartSystem wow fadeInLeft animated" data-wow-delay="2s">
<h1>Fermentations made to Current Date</h1></div>

<div class="smartSystem wow fadeInRight animated" data-wow-delay="2s">
<table>
  <tr>
    <th>SURNAME, Name</th>
    <th>Usernumber</th>
    <th>Contact</th>
    <th>Fermentations Quantity</th>
    <th>Last Login</th>
  </tr>
</table>
When in doubt, feel free to consult your colleagues and/or professors. Both Professors and Students are equally displayed in the previous list.
The administrator is always available for you (smartfermentor@gmail.com)
</div>
</center>

<?php
  function decrypt_aes256($data, $key, $initVector){
    $initVector = str_pad($initVector, 16, "\0");
    $encryptedData = base64_decode($data);
    $decryptedData = openssl_decrypt($encryptedData, "AES-256-CBC", $key, OPENSSL_RAW_DATA, $initVector);
    return $decryptedData;
  }

  function decryptServerProfessorsData(){
    $key = "Biotec.ORT1450";
    $initVector = "CB+I_OrtURU";
    $encryptedData = file_get_contents('SystemData/ProfessorsData.json');
    $usersInformation = json_decode($encryptedData);
    $decryptedData = decrypt_aes256($usersInformation->info, $key, $initVector);
    $hashedData = base64_encode(hash_hmac("sha256", $usersInformation->info, "my_secret", true));
    return $decryptedData;
  }

  function decryptServerStudentsData(){
    $key = "Biotec.ORT1450";
    $initVector = "CB+I_OrtURU";
    $encryptedData = file_get_contents('SystemData/StudentsData.json');
    $usersInformation = json_decode($encryptedData);
    $decryptedData = decrypt_aes256($usersInformation->info, $key, $initVector);
    $hashedData = base64_encode(hash_hmac("sha256", $usersInformation->info, "my_secret", true));
    return $decryptedData;
  }
?>

<script>
  window.onload = function() {
    var jsonProfessors = '<?php echo decryptServerProfessorsData() ?>';
    loadProfessorsToParticipantsTable(jsonProfessors);
    var jsonStudents = '<?php echo decryptServerStudentsData() ?>';
    loadStudentsToParticipantsTable(jsonStudents);
  }
</script>

</body>
</html>
