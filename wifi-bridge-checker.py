#!/usr/bin/env python3

import netifaces
import subprocess
import sys
import os
import traceback
import datetime
import time

# -----------------------------------core prep--------------------------------------------------------------------
ints = netifaces.interfaces()
bridgecheck = subprocess.check_output('sudo brctl show | grep wlan0', shell=True)
bridgecheck_corrected = bridgecheck.strip()
bridgecheck_corrected = bridgecheck_corrected.decode("utf-8")
iface = ""

# -----------------------------------defining functions-----------------------------------------------------------
def log_reduction():
    logs = ['/home/wlan-logs/wlan-success.log', '/home/wlan-logs/wlan-failure.log', '/home/wlan-logs/interface-failure.log']
    for log in logs:
      linecount = 0
      firstlines = []
      with open(log) as readfile, open('/home/wlan-logs/tmp.txt','w') as tmp:
        for index, line in enumerate(readfile):
          linecount +=1
        if linecount > 15:
          for i in xrange(linecount - 15):
            firstlines.append(next(readfile))
          for l in readfile:
            tmp.write(l)
      os.replace('/home/wlan-logs/tmp.txt', log)      

def success_outputter():
  conn_clients = subprocess.check_output('sudo iw dev wlan0 station dump | grep Station | wc -l', shell=True)
  conn_clients = conn_clients.strip()
  conn_clients = conn_clients.decode("utf-8")
  timestamp = time.time()
  timestamp = datetime.datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M:%S')
  success_output = "%s  ---  wlan0 already in brctl show and %s connected" % (timestamp,conn_clients)
  with open('/home/wlan-logs/wlan-success.log','a') as FW:
    FW.write(success_output + '\n')
  
def fail_outputter():
  subprocess.call('sudo brctl addif br0 wlan0', shell=True)
  timestamp = time.time()
  timestamp = datetime.datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M:%S')
  failure_output = timestamp + "  ---  added wlan0 to bridge"
  with open('/home/wlan-logs/wlan-failure.log','a') as FW:
    FW.write(failure_output + '\n')

def interface_check():
  timestamp = time.time()
  timestamp = datetime.datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M:%S')
  interface_output = timestamp + "  ---  Please check your WiFi adaptor, it might be unplugged or faulty"
  with open('/home/wlan-logs/interface-failure.log','a') as FW:
    FW.write(interface_output + '\n')

#-----------------------------------wlan bridge check and output logs----------------------------------------------
try:
  if 'wlan0' in ints:
    if bridgecheck_corrected == "wlan0":
      print("Bridge already established, no need to add it")
      success_outputter()
    else:
      print("Bridge does not contain wlan0. Adding and logging it now...")
      fail_outputter()
  else:
    print("Please check your WiFi adaptor...")
    interface_check()
except Exception as err:
  print('Error -->  '+ str(err))
  print(traceback.format_exc())
finally:
  log_reduction()

