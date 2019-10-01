<?php

/**
* Get an array of human readable times for sun events
* @param \DateTime $date A \DateTime Object set to the desired date
*                        and the correct timezone for the place in question
* @param float $lat The latitude of the place in question
* @param float $lon The longitude of the place in question
*
* @return array An associative array of human readable times sorted in chronological order.
*/

$my_lat = 52.252;
$my_lon = 1.4883;
$today = date('Y-m-d');

function adjustedSunInfo(\DateTime $date,$lat,$lon) {
    $sinfo=date_sun_info ($date->getTimestamp() ,$lat,$lon );

    foreach($sinfo as $key=>$val) {
        //You should check that $val isn't 1 or empty first
        $time = new \DateTime('@' . $val);
        $time->setTimezone($date->getTimeZone());
        $sinfo[$key] = $time->format('Y m d H:i:s');
    }

    asort($sinfo);
    return $sinfo;
}

$time = new \DateTime($today, new \DateTimeZone('UTC'));
var_dump(adjustedSunInfo($time, $my_lat, $my_lon));

/*
$my_lat = 52.252;
$my_lon = 1.4883;
$today = date("Y-m-d");
$sun_info = date_sun_info(strtotime($today), $my_lat, $my_lon);


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
*/

?>