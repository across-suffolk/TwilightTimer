#!/usr/bin/env python3

import time, schedule, automationhat, logging
from subprocess import Popen, PIPE

#Set logging configuration
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S (%Z)', level=logging.INFO, filename='timeswitch.log', filemode='w')

def update_times():
	global off_t, on_t
	
	#Run PHP script and decode bytes output
	p = Popen("php times_output_060.php", shell=True, stdout=PIPE)
	logging.info('Script activated')
	
	theResult = p.stdout.read().decode('ascii')
	
	#extract times
	off_t = theResult[4:9]
	on_t = theResult[12:17]
	#print ('Times checked', off_t, on_t)

#run the update to initialise
logging.info('Initialising')
update_times()

#Write to the log
theLog = 'Initialised. Switch on at: ' + on_t + ' Switch off at: ' + off_t
logging.info(theLog)

def switch_off():
	automationhat.relay.one.off()
	logging.info('Relay switched off')
	return schedule.CancelJob

def switch_on():
	automationhat.relay.one.on()
	logging.info('Relay switched on')
	return schedule.CancelJob

#Core scheduling
schedule.every().day.at("01:30").do(update_times)
schedule.every().day.at(off_t).do(switch_off)
schedule.every().day.at(on_t).do(switch_on)

#The eternal loop
while True:
    schedule.run_pending()
    time.sleep(1)
