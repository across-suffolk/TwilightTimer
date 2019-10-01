#!/usr/bin/env python

import time

import automationhat

import subprocess

result = subprocess.call("php times_output_031.php", shell=True)

print(result)


#while True:
#    automationhat.relay.one.toggle()
#    time.sleep(0.2)
