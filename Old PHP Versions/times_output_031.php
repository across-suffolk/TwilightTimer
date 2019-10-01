<?php
$my_lat = 52.252;
$my_lon = 1.4883;
$today = date("Y-m-d");
$sun_info = date_sun_info(strtotime($today), $my_lat, $my_lon);
echo date("H:i", $sun_info['nautical_twilight_begin']) . "\n";
echo date("H:i", $sun_info['nautical_twilight_end']) . "\n";

/*
foreach ($sun_info as $key => $val) {
    echo "$key: " . date("H:i", $val) . "\n";
}
*/
?>