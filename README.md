# TwilightTimer
Off-line variable twilight timer written in Python, using PHP.

## Objective
1. A simple timer running on a Raspberry Pi Zero-W (PiZ), with a relay to control activation of a sky camera. 
2. The camera is very light sensitive and needs to switch on at [Astronomical Twilight](https://www.timeanddate.com/astronomy/different-types-twilight.html)
3. The timer must continue to operate regardless of whether internet access is available.
4. Ideally the Pi-Z would be powered by the same 12v supply used by the camera (less power bricks).
5. Adjustment of times *may* be needed via simple buttons. Power off button will be useful to prevent sd-card corruption.

## Solution
PHP includes a function called [date_sun_info](https://www.php.net/manual/en/function.date-sun-info.php) to calculate twilight times as an array, using current time, latitude and longitude. 
The Python script uses the subprocess module to activate a PHP script (preset with lat/long) and echo the times, which are piped back into Python.
Python then decodes the byte data into strings and timestamps for use in scheduling and logging.

The [schedule module](https://github.com/dbader/schedule) by @dbader is used to create four jobs.
 1. Call PHP script to update times. Runs every day at 01:30.
 2. Trigger a log entry every 30 minutes, to approximate time if system fails.
 3. One-off relay_on job.
 4. One-off relay_off job.

The smaller AutomationPhat by Pimoroni is used to switch the camera on and off, controlled by the [automationhat module](https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-automation-hat-and-phat). Note: this is the same module as used by the larger AutomationHat, hence the spelling. 

The system is to run headerless and without any echo or text output. The logging module is used to record activity, which also picks up logging output from the schedule module. The os module is used to create a timestamp file name for the log file each time the script is run. https://realpython.com/python-logging/

## Issues yet to resolve
1. The log shows that the job function 'switch_off' is being called twice, two minutes apart, with the first occuring on time according to the schedule times obtained by PHP. Unusual that the second event occurs exactly 2 minutes later. 
* Could this be caused by serial schedules being set, one before midnight and one after
* The two minute difference may vary if the first schedule is set based on the previous days calculated times
* (currently very near to equinox).
* Possible solutions
  * Run one-off jobs as tagged scheules (relayJob) and clear these jobs each time PHP is run.
  * Run schedules as multi-treaded.

2. SSH login needs to be secure - use SHA keys.

3. Script needs to auto run at boot.

4. Run script in the background (use $ in shell).

5. Need some method to stop the script and reset or shutdown the PiZ - short press or long press of button (GPIO).

6. May want LED indicators to show current settings and aid changing of settings - simple feedback and input.
