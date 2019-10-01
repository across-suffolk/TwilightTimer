<?php
$my_lat = 52.252;
$my_lon = 1.4883;
$today = date("Y-m-d");
$sun_info = date_sun_info(strtotime($today), $my_lat, $my_lon);

#$cam_off =  $sun_info['nautical_twilight_begin'];
#$cam_on = $sun_info['nautical_twilight_end'];

$cam_off =  date("H:i", $sun_info['nautical_twilight_begin']);
$cam_on =  date("H:i", $sun_info['nautical_twilight_end']);
$civil_start = date("H:i", $sun_info['civil_twilight_begin']);
$civil_end = date("H:i", $sun_info['civil_twilight_end']);
$astro_start = date("H:i", $sun_info['astronomical_twilight_begin']);
$astro_end = date("H:i", $sun_info['astronomical_twilight_end']);

echo "[Nautical Twilight Begin], camera switches off: ", $cam_off, "\n";
echo "[Nautical Twilight End], camera switch on: ", $cam_on, "\n";
echo "Civil Twilight Begin:", $civil_start, "\n";
echo "Civil Twilight Ends:", $civil_end, "\n";
echo "Astronomical Twilight Begin:", $astro_start, "\n";
echo "Astronomical Twilight Ends:", $astro_end, "\n";

/*
#echo $sun_info;
/*
foreach ($sun_info as $key => $val) {
    echo "$key: " . date("H:i", $val) . "\n";
}
*/
?>