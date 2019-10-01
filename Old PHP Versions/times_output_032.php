<?php
$my_lat = 52.252;
$my_lon = 1.4883;
$today = date("Y-m-d");
$sun_info = date_sun_info(strtotime($today), $my_lat, $my_lon);

#$cam_off =  $sun_info['nautical_twilight_begin'];
#$cam_on = $sun_info['nautical_twilight_end'];

$cam_off =  date("H:i", $sun_info['nautical_twilight_begin']);
$cam_on =  date("H:i", $sun_info['nautical_twilight_end']);

echo $cam_off, $cam_on;

/*
#echo $sun_info;
/*
foreach ($sun_info as $key => $val) {
    echo "$key: " . date("H:i", $val) . "\n";
}
*/
?>