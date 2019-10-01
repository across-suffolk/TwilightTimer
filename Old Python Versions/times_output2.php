<?php
$today = date("Y-m-d");
$cam_on = date_sun_info(strtotime($today), 52.2152, 1.4883);
foreach ($cam_on as $key => $val) {
	echo "$key: " . date("H:i:s", $val) . "\n";
}
?>
