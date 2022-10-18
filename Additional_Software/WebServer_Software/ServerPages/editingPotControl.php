<?php

    $url = "SystemData/StatusDataServer.json";
    $data = file_get_contents($url);
    $characters = json_decode($data, true);
    $characters["potentialControl"][1] = $_POST["recordNumberFromJavascript"];
    $dataJSON = json_encode($characters);
    $resul = file_put_contents("SystemData/StatusDataServer.json", $dataJSON);
    echo $dataJSON;

?>