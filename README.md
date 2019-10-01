# TwilightTimer
Off-line variable twilight timer written in Python, using PHP.

## Objective
(1) A simple timer running on a Raspberry Pi Zero-W (PiZ), with a relay to control activation of a sky camera. 

(2) The camera is very light sensitive and needs to switch off at Astronomical Twilight (https://www.timeanddate.com/astronomy/different-types-twilight.html)

(2) The timer must continue to operate regardless of whether internet access is available.

(3) Ideally the Pi-Z would be powered by the same 12v supply used by the camera (less power bricks).

(4) Adjustment of times *may* be needed via simple buttons. Power off button will be useful to prevent sd-card corruption.

## Solution
PHP includes a function called 'date_sun_info' to calculate twilight times as an array, using current time, latitude and longitude. (https://www.php.net/manual/en/function.date-sun-info.php)
The Python script uses the subprocess module to activate a PHP script (preset with lat/long) and echo the times, which are piped back into Python.
Python then decodes the byte data into strings and timestamps for use in scheduling and logging.

The smaller AutomationPhat by Pimoroni is used to switch the camera on and off, controlled by the automationhat module. Note: this is the same module as used by the larger AutomationHat, hence the spelling. https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-automation-hat-and-phat

The system is to run headerless and without any echo or text output. The logging module is used to record activity, which also picks up logging output from the schedule module. The os module is used to create a timestamp file name for the log file each time the script is run. https://realpython.com/python-logging/

## Issues yet to resolve
(a)The log shows that the job function 'switch_off' is being called twice, two minutes apart, with the first occuring on time according to the schedule times obtained by PHP. Unusual that the second event occurs exactly 2 minutes later. 
    * Could this be caused by serial schedules being set, one before midnight and one after
    * The two minute difference may vary if the first schedule is set based on the previous days calculated times
    * (currently very near to equinox).
    * Possible solutions
        * Run one-off jobs as tagged scheules (relayJob) and clear these jobs each time PHP is run.
        * Run schedules as multi-treaded.

(b) SSH login needs to be secure - use SHA keys.

(c) Script needs to auto run at boot.

(d) Run script in the background.

(e) Need some method to stop the script and reset or shutdown the PiZ - short press or long press of button (GPIO).

(f) May want LED indicators to show current settings and aid changing of settings - simple feedback and input.
