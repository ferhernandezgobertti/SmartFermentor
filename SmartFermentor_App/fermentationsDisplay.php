<!DOCTYPE html>
<html lang="en" >
<header><title> FERMENTATIONS </title></header>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="ServerJS/jquery.min.js"></script>
<script src="ServerJS/wow.min.js"></script>
<script src="ServerJS/fermentationsTable.js"></script>
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
    <th>Beginning</th>
    <th>Substance</th>
    <th>Objective</th>
    <th>Motive</th>
    <th>Description</th>
    <th>Responsible</th>
  </tr>
</table><br>
<h2 id="fermInformationData">Fermentations Information extracted from: </h2>
<br><br>
<p>When in doubt, feel free to consult your colleagues and/or professors. Either Initiated Fermentations and Continued Fermentations are displayed independently and treated as such.
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

  function decryptServerFermentationsData(){
    $key = "Biotec.ORT1450";
    $initVector = "CB+I_OrtURU";
    $encryptedData = file_get_contents('SystemData/FermentationsData.json');
    $usersInformation = json_decode($encryptedData);
    $decryptedData = decrypt_aes256($usersInformation->info, $key, $initVector);
    $hashedData = base64_encode(hash_hmac("sha256", $usersInformation->info, "my_secret", true));
    return $decryptedData;
  }

  function getInformationFromFermentationsFile($url){
    if(file_exists('SystemData/FermentationsData.json')){
      $fileSize = filesize('SystemData/FermentationsData.json');
      $fileLastAccess = date ("F d Y H:i:s.", fileatime('SystemData/FermentationsData.json'));
      $fileLastModified = date ("F d Y H:i:s.", filemtime('SystemData/FermentationsData.json'));
      return array($fileSize, $fileLastModified, $fileLastAccess);
    } else {
      return array('[Not Found]', '[Not Found]', '[Not Found]');
    }
  }
?>

<script>

  function loadFermentationsFileData(){
    var fermentationsFilename = 'SystemData/FermentationsData.json';
    var fermentationFileInformation = '<?php echo json_encode(getInformationFromFermentationsFile(fermentationsFilename)); ?>';
    var fermFileInfo1 = fermentationFileInformation.split("[");
    var fermFileInfo2 = fermFileInfo1[1].split("]");
    var fermFileInfo3 = fermFileInfo2[0].split(",");
    document.getElementById('fermInformationData').innerHTML = "Fermentations Information extracted from "+fermentationsFilename+", FILESIZE: "+fermFileInfo3[0]+" bytes. LAST MODIFIED: "+fermFileInfo3[1]+", LAST ACCESSED: "+fermFileInfo3[2];
  }

  window.onload = function() {
    var jsonFermentation = '<?php echo decryptServerFermentationsData() ?>';
    loadFermentationTable(jsonFermentation);
    loadFermentationsFileData();
  }
</script>

</body>
</html>
