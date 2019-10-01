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
        $sinfo[$key] = $time->format('H:i');
    }

    asort($sinfo);
    return $sinfo;
}

$time = new \DateTime($today, new \DateTimeZone('UTC'));
#var_dump(adjustedSunInfo($time, $my_lat, $my_lon));

#----

#######
# USE #
#######

#This script must be ran at 01:00 every day to provide the days alarm times
#Use of the adjustedSunInfo function above gives greater accuracy for GMT(UTC)
#and should remove the risk of british summer time affecting the activation.

# Pull all elements into an array variable
$adj_Sun_Info = adjustedSunInfo($time, $my_lat, $my_lon);

# Select which array element
$cam_off =  $adj_Sun_Info['nautical_twilight_begin'];
$cam_on =  $adj_Sun_Info['nautical_twilight_end'];

# Display element
echo "off_" . $cam_off;
echo "on_" . $cam_on;

?>