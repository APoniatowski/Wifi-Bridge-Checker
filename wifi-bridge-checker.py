#!/usr/bin/env python3

import netifaces
import subprocess
import sys
import datetime
import time

# -----------------------------------core prep--------------------------------------------------------------------
ints = netifaces.interfaces()
bridgecheck = subprocess.check_output('sudo brctl show | grep wlan0', shell=True)
bridgecheck_corrected = bridgecheck.strip()
bridgecheck_corrected = bridgecheck_corrected.decode("utf-8")
iface = ""

# -----------------------------------defining functions-----------------------------------------------------------
def success_outputter():
  conn_clients = subprocess.check_output('sudo iw dev wlan0 station dump | grep Station | wc -l', shell=True)
  conn_clients = conn_clients.strip()
  conn_clients = conn_clients.decode("utf-8")
  timestamp = time.time()
  timestamp = datetime.datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M:%S')
  success_output = "%s  ---  wlan0 already in brctl show and %s connected" % (timestamp,conn_clients)
  success_write = open('/home/wlan-logs/wlan-success.log','a')
  success_write.write(success_output + '\n')
  success_write.close()

def fail_outputter():
  subprocess.call('sudo brctl addif br0 wlan0', shell=True)
  timestamp = time.time()
  timestamp = datetime.datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M:%S')
  failure_output = timestamp + "  ---  added wlan0 to bridge"
  failure_write = open('/home/wlan-logs/wlan-success.log','a')
  failure_write.write(failure_output + '\n')
  failure_write.close()

def interface_check():
  timestamp = time.time()
  timestamp = datetime.datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M:%S')
  interface_output = timestamp + "  ---  Please check your WiFi adaptor, it might be unplugged or faulty"
  interface_write = open('/home/wlan-logs/interface-failure.log','a')
  interface_write.write(interface_output + '\n')
  interface_write.close()

#-----------------------------------wlan bridge check and output logs----------------------------------------------

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

