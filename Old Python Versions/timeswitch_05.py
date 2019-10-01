#!/usr/bin/env python3

import time, schedule, automationhat
from subprocess import Popen, PIPE


def update_times():
	global off_t, on_t
	
	#Run PHP script and decode bytes output
	p = Popen("php times_output_060.php", shell=True, stdout=PIPE)
	theResult = p.stdout.read().decode('ascii')
	
	#extract times
	off_t = theResult[4:9]
	on_t = theResult[12:17]

#run the update to initialise
update_times()

#What am i doing now? Oh, yeah I am printing the initialise settings. Dhoh!
print (off_t, on_t)

def switch_off():
	automationhat.relay.one.off()
	return schedule.CancelJob

def switch_on():
	automationhat.relay.one.on()
	return schedule.CancelJob


schedule.every().day.at("01:30").do(update_times)
schedule.every().day.at(off_t).do(switch_off)
schedule.every().day.at(on_t).do(switch_on)

while True:
    schedule.run_pending()
    time.sleep(1)