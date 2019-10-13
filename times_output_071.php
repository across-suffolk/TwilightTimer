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
$n_off =  $adj_Sun_Info['nautical_twilight_begin'];
$n_on =  $adj_Sun_Info['nautical_twilight_end'];
$a_off =  $adj_Sun_Info['astronomical_twilight_begin'];
$a_on =  $adj_Sun_Info['astronomical_twilight_end'];
$c_off =  $adj_Sun_Info['civil_twilight_begin'];
$c_on =  $adj_Sun_Info['civil_twilight_end'];

# Display element
echo "naut" . $n_off . $n_on;
echo "astr" . $a_off . $a_on;
echo "civl" . $c_off . $c_on;

?>
