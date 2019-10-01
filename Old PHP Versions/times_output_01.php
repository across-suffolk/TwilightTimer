<?php
$sun_info = date_sun_info(strtotime("2019-05-25"), 31.7667, 35.2333);
foreach ($sun_info as $key => $val) {
    echo "$key: " . date("H:i", $val) . "\n";
}
?>