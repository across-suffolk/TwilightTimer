<?php
$my_lat = 52.252;
$my_lon = 1.4883;
$today = date("Y-m-d");
$sun_info = date_sun_info(strtotime($today), $my_lat, $my_lon);
foreach ($sun_info as $key => $val) {
    echo "$key: " . date("H:i", $val) . "\n";
}
?>