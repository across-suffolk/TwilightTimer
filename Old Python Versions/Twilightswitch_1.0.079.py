#!/usr/bin/env python3

#schedule module by Dan Bader (https://github.com/dbader/schedule)
#documentation : https://schedule.readthedocs.io/en/stable/

#076 - Amend Log filename to include date & time.
#077 - Minor amend - comments.
#078 - NOT Worked - Attempt to fix double switch off 2 mins apart
#    - Amend order: update_time() last
#    - Changed if statement to elif & moved initial switch off into Else statement.
#079 - 2nd Attempt:
#    - Moved Global out of update_times() - prevent multiple definition?
#    - Added the time string as name to each switching job.
#    - Moved update log into update_times()
#    - Amended logging method within switching functions
#    - Is there a way to list all schedules that have been set?
#    - Suspect post midnight update has set another switch_off but before first has run. Second would then be later as twilight time has changed.
#    - Try: Incorporate clearing of schedules by tag '_relay'
#    - Consider: use Threading to allow parallel schedules? (see example in Git FAQ)

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
	schedule.every().day.at(off_str).do(switch_off, off_at = off_str)
	schedule.every().day.at(on_str).do(switch_on, on_at = on_str)
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

###-----Test Variables & Halt-----###
#print (fullName)
#print (fileName)
#print (logTimestamp)
#print (logName)
#sys.exit('EXIT:Partial initialisation - to check file name and path')

#Set logging configuration
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S (%Z)', level=logging.DEBUG, filename=logName, filemode='w')

#First run of the script to initialise
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
schedule.every().day.at("01:30").do(update_times)
schedule.every(30).minutes.do(run_check)

while True: #The eternal loop
    schedule.run_pending()
    time.sleep(1)
