#!/usr/bin/env python3

# /etc/init.d/sample.py
### BEGIN INIT INFO
# Provides:          sample.py
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start daemon at boot time
# Description:       Enable service provided by daemon.
### END INIT INFO

#schedule module by Dan Bader (https://github.com/dbader/schedule)
#documentation : https://schedule.readthedocs.io/en/stable/

#### - TO DO list
#### - Run script in background
#### - Return all three twilight options and parse into variables
#### - Allow choice of times
#### - Add button control to start and stop the script (schedules)
#### - Add buttons to adjust the times by 15min increments

import datetime, time, schedule, automationhat, logging, os, sys
from subprocess import Popen, PIPE

#-----------------#
#--  Functions  --#
#-----------------#

def switch_off(off_at):
	automationhat.relay.one.off()
	theLog = 'Relay switched off. Defined time = ' + off_at
	logging.info(theLog)
	return schedule.CancelJob

def switch_on(on_at):
	automationhat.relay.one.on()
	theLog = 'Relay switched on. Defined time = ' + on_at
	logging.info(theLog)
	return schedule.CancelJob

def run_check():
	#logging.debug('Still running, will check again in 30 mins.')
	toSender = "GNDN-30"
	return toSender

def update_times():
	global off_t, on_t, off_str, on_str
	schedule.clear('relays') #Clear schedules tagged with 'relays' to prevent doubles
	p = Popen("php times_output_070.php", shell=True, stdout=PIPE) #Run PHP script needs shell=True to run.
	logging.info('update_times() Script activated')
	getResult = p.stdout.read().decode('ascii') #outputs in bytes, needs to be decoded.
	theTimes = getResult #copy Result to prevent shell from running script more than once?
	#extract time as integers
	off_H = int(theTimes[4:6])
	off_M = int(theTimes[7:9])
	on_H = int(theTimes[12:14])
	on_M = int(theTimes[15:17])
	#combine extracted integers as time for init check
	off_t = datetime.time(hour = off_H, minute = off_M)
	on_t = datetime.time(hour = on_H, minute = on_M)
	#extract also as string for schedules and logging
	off_str = theTimes[4:9]
	on_str = theTimes[12:17]
	#Set relay schedules
	schedule.every().day.at(off_str).do(switch_off, off_at = off_str).tag('relays')
	schedule.every().day.at(on_str).do(switch_on, on_at = on_str).tag('relays')
	theLog = 'Times updated. Switch on at: ' + on_str + ' Switch off at: ' + off_str
	logging.info(theLog)

#------------------#
#--  Initialise  --#
#------------------#

#Set up the time variable so it can be used in the filename
now_t = datetime.datetime.now().time()
pre_midnight = datetime.time(23, 59, 59)
aft_midnight = datetime.time(0, 0, 0,)

#Set up the log file name including a timestamp
fullName = os.path.basename(__file__)                               #Get the full directory
fileName = os.path.splitext(fullName)[0]                            #Extract just the name of this file
logTimestamp = datetime.datetime.now().strftime('_%Y-%m-%d_%H-%M')  #Get time and date and set the format
logName = fileName + logTimestamp + ".log"                          #Combine it all together with the file extension

#Set logging configuration
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S (%Z)', level=logging.DEBUG, filename=logName, filemode='w')

#First run of the script to obtain times and set globals
update_times()

#Check if relay should be on right now:
if now_t < pre_midnight and now_t > on_t:
	logging.info("Initialised before midnight and after twilight begins, switch relay on")
	switch_on("Initialise")
elif now_t > aft_midnight and now_t < off_t: 
	logging.info("Initialised after midnight and before twilight ends, ")
	switch_on("Initialise")
else:
	logging.info("Initialised when relay should be switched OFF")
	switch_off("Initialise") #automationhat.relay.one.off()

#Set update schedule and a check to log that the system is still running
schedule.every().day.at("01:30").do(update_times).tag('system')
schedule.every(30).minutes.do(run_check).tag('system')

while True: #The eternal loop
    schedule.run_pending()
    time.sleep(1)
