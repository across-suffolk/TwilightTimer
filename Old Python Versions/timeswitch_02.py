#!/usr/bin/env python

import time

import automationhat

import subprocess

result = subprocess.Popen(
	"php times_output_031.php",
	shell=True
	stdout=subprocess.PIPE)

print(result.stdout)


#while True:
#    automationhat.relay.one.toggle()
#    time.sleep(0.2)
