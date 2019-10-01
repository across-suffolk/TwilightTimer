<?php
$cam_on = date_sun_info(strtotime("2019-05-25"), 52.2152, 1.4883);
foreach ($cam_on as $key => $val) {
	echo "$key: " . date("H:i:s", $val) . "\n";
}
?>
