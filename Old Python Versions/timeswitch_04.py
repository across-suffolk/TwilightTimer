#!/usr/bin/env python3

import time

import automationhat

import subprocess

p = subprocess.Popen("php times_output_061.php", shell=True, stdout=subprocess.PIPE)


theResult = p.communicate()

print (theResult)

#print(result)


#while True:
#    automationhat.relay.one.toggle()
#    time.sleep(0.2)
