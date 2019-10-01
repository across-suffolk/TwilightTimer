# TwilightTimer
Off-line variable twilight timer written in Python, using PHP.

## Objective
(1) A simple timer running on a Raspberry Pi Zero-W (PiZ), with a relay to control activation of a sky camera. 

(2) The camera is very light sensitive and needs to switch off at Astronomical Twilight (https://www.timeanddate.com/astronomy/different-types-twilight.html)

(2) The timer must continue to operate regardless of whether internet access is available.

(3) Ideally the Pi-Z would be powered by the same 12v supply used by the camera (less power bricks).

(4) Adjustment of times *may* be needed via simple buttons. Power off button will be useful to prevent sd-card corruption.

## Solution
PHP includes a function called 'date_sun_info' to calculate twilight times as an array, using current time, latitude and longitude.
The Python script uses the subprocess module to activate a PHP script (preset with lat/long) and echo the times, which are piped back into Python.
Python then decodes the byte data into strings and timestamps for use in scheduling and logging.

The smaller AutomationPhat by Pimoroni is used to switch the camera on and off, controlled by the automationhat module (note: this is the same module as used by the larger AutomationHat, hence the spelling).

The system is to run headerless and without any echo or text output. The logging module is used to record activity, which also picks up logging output from the schedule module. The os module is used to create a timestamp file name for the log file each time the script is run.

## Issues yet to resolve
(a)The log shows that the job function 'switch_off' is being called twice, two minutes apart. First is on time according to the schedule times obtained by PHP. Unusual that the second event occurs exactly 2 minutes later. 

(b) Script needs to auto run at boot.

(c) Run script in the background.

(d) Need some method to stop the script and reset or shutdown the PiZ
