#!/usr/bin/env python3

import datetime, time, schedule, automationhat, logging, os
from subprocess import Popen, PIPE

#-----------------#
#--  Functions  --#
#-----------------#

def update_times():
	global off_t, on_t, off_str, on_str
	p = Popen("php times_output_070.php", shell=True, stdout=PIPE) #Run PHP script needs shell=True to run.
	logging.info('Script activated')
	getResult = p.stdout.read().decode('ascii') #outputs in bytes, needs to be decoded.
	theTimes = getResult #copy Result to prevent shell from running script more than once
	#extract time as integers
	off_H = int(theTimes[4:6])
	off_M = int(theTimes[7:9])
	on_H = int(theTimes[12:14])
	on_M = int(theTimes[15:17])
	#combine extracted integers as time
	off_t = datetime.time(hour = off_H, minute = off_M)
	on_t = datetime.time(hour = on_H, minute = on_M)
	#extract also as string for logging and reporting
	off_str = theTimes[4:9]
	on_str = theTimes[12:17]
	relay_schedule()

def switch_off():
	automationhat.relay.one.off()
	logging.info('Relay switched off')
	return schedule.CancelJob

def switch_on():
	automationhat.relay.one.on()
	logging.info('Relay switched on')
	return schedule.CancelJob

def run_check():
	logging.debug('Still running, will check again in 30 mins.')

def relay_schedule():
	schedule.every().day.at(off_str).do(switch_off)
	schedule.every().day.at(on_str).do(switch_on)
	logging.debug('Schedules are set')


#------------------#
#--  Initialise  --#
#------------------#

#Get just the name of the file without extention - used as the log file name
fullName = os.path.basename(__file__)
logName = os.path.splitext(fullName)[0] + ".log"

#Set logging configuration
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S (%Z)', level=logging.DEBUG, filename=logName, filemode='w')

#Make sure relay is off (shouldn't be on from startup)
switch_off() #automationhat.relay.one.off()
logging.info("Ensuring relay is off during initialisation")

#First run of the script to initialise
update_times()
theLog = 'Initialised. Switch on at: ' + on_str + ' Switch off at: ' + off_str
logging.info(theLog)

now_t = datetime.datetime.now().time()
pre_midnight = datetime.time(23, 59, 59)
aft_midnight = datetime.time(0, 0, 0,)

#Relay should be off unless:
#Current time is before midnight AND after on_t then relay should be on OR
if now_t < pre_midnight and now_t > on_t:
	switch_on()
	logging.info("Initialised before midnight and after twilight begins, relay switched on")

#Current time is after midnight AND before off_t then relay should be on
if now_t > aft_midnight and now_t < off_t:
	switch_on()
	logging.info("Initialised after midnight and before twilight ends, relay switched on")

#-----------------#
#--  Schedules  --#
#-----------------#

schedule.every().day.at("01:30").do(update_times)
schedule.every(30).minutes.do(run_check)

while True: #The eternal loop
    schedule.run_pending()
    time.sleep(1)
