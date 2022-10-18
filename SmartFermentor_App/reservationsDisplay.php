<!DOCTYPE html>
<html lang="en" >
<header><title> RESERVATIONS </title></header>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="ServerJS/jquery.min.js"></script>
<script src="ServerJS/wow.min.js"></script>
<script src="ServerJS/reservationsTable.js"></script>
<link rel="stylesheet" href="ServerCSS/animate.css">
<link rel="stylesheet" href="ServerCSS/tableFormat.css">
</head>
<body style="background-color:#085454;">

<center>
<div class="smartSystem wow fadeInDown animated" data-wow-delay="1s">
<img src="ServerImages/smartFermentorLogo.png" id="smartLogo" height=150></div>

<div class="smartSystem wow fadeInLeft animated" data-wow-delay="2s">
<h1>Reservations scheduled up to Now</h1></div>

<div class="smartSystem wow fadeInRight animated" data-wow-delay="2s">
<table>
  <tr>
    <th>Period</th>
    <th>Interested User</th>
    <th>Responsible</th>
    <th>Precaution</th>
  </tr>
</table><br>
<h2 id="reservationsInformationData">Reservations Information extracted from: </h2>
<br><br>
<p>When in doubt, feel free to consult your colleagues and/or professors. Reservations can be modified only at the Laboratory's Local Console.
The administrator is always available for you (smartfermentor@gmail.com)</p>
</div>
</center>

<?php
  function decrypt_aes256($data, $key, $initVector){
    $initVector = str_pad($initVector, 16, "\0");
    $encryptedData = base64_decode($data);
    $decryptedData = openssl_decrypt($encryptedData, "AES-256-CBC", $key, OPENSSL_RAW_DATA, $initVector);
    return $decryptedData;
  }

  function decryptServerReservationsData(){
    $key = "Biotec.ORT1450";
    $initVector = "CB+I_OrtURU";
    $encryptedData = file_get_contents('SystemData/ReservationsData.json');
    $usersInformation = json_decode($encryptedData);
    $decryptedData = decrypt_aes256($usersInformation->info, $key, $initVector);
    $hashedData = base64_encode(hash_hmac("sha256", $usersInformation->info, "my_secret", true));
    return $decryptedData;
  }

  function getInformationFromReservationsFile($url){
    if(file_exists('SystemData/ReservationsData.json')){
      $fileSize = filesize('SystemData/ReservationsData.json');
      $fileLastAccess = date ("F d Y H:i:s.", fileatime('SystemData/ReservationsData.json'));
      $fileLastModified = date ("F d Y H:i:s.", filemtime('SystemData/ReservationsData.json'));
      return array($fileSize, $fileLastModified, $fileLastAccess);
    } else {
      return array("[Not Found]", "[Not Found]", "[Not Found]");
    }
  }

?>

<script>

  function loadReservationsFileData(){
    var reservationsFilename = 'SystemData/ReservationsData.json';
    var reservationsFileInformation = '<?php echo json_encode(getInformationFromReservationsFile(reservationsFilename)); ?>';
    var resFileInfo1 = reservationsFileInformation.split("[");
    var resFileInfo2 = resFileInfo1[1].split("]");
    var resFileInfo3 = resFileInfo2[0].split(",");
    document.getElementById('reservationsInformationData').innerHTML = "Fermentations Information extracted from "+fermentationsFilename+", FILESIZE: "+fermFileInfo3[0]+" bytes. LAST MODIFIED: "+fermFileInfo3[1]+", LAST ACCESSED: "+fermFileInfo3[2];
  }

  window.onload = function() {
    var jsonReservations = '<?php echo decryptServerReservationsData() ?>';
    loadReservationTable(jsonReservations);
    loadReservationsFileData();
  }
</script>

</body>
</html>
