import schedule
import time

def chk_times():
	print('I am checking the times...')
	
def sw_on():
	print('switching on')

def sw_off():
	print('switching camera OFF')

schedule.every(10).seconds.do(chk_times)
schedule.every(13).seconds.do(sw_on)
schedule.every(16).seconds.do(sw_off)

while True:
	schedule.run_pending()
	time.sleep(1)
