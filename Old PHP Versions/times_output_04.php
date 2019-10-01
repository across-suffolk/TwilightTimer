<?php
$my_lat = 52.252;
$my_lon = 1.4883;
$today = date("Y-m-d");
$sun_info = date_sun_info(strtotime($today), $my_lat, $my_lon);
$cam_on_H = date("H", $sun_info['nautical_twilight_end']);
$cam_on_m = date("i", $sun_info['nautical_twilight_end']);
$cam_off_H = date("H", $sun_info['nautical_twilight_begin']);
$cam_off_m = date("i", $sun_info['nautical_twilight_begin']);


echo $today . " Camera turns on at " . $cam_on_H . ":" . $cam_on_m . "\n";
echo $today . " Camera turns off at " . $cam_off_H . ":" . $cam_off_m . "\n";


/*
foreach ($sun_info as $key => $val) {
    echo "$key: " . date("H:i", $val) . "\n";
}
*/
?>