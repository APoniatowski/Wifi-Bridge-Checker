# Wifi Bridge Checker
#### developed in python 3
The purpose of this script, started when I created my own personal wifi AP, consisting of a raspberry pi and a wireless N dongle (54mbps on the generic wifi dongles/cards were too slow for my taste).

So I set my raspberry pi up, installed hostapd and had some issues with brctl (installing it on raspbian lite took a bit of work). 
Once I had those in installed, I proceeded with configuring my interfaces and hostapd config file to make my setup reliable, even after restarts/power outages.

lo and behold it was not keeping my wifi dongle in a bridge after a restart. So I made a bash script to check if wlan0 is in my bridge and add it, if it isn't already there. 
later it evolved and I had it in my crontab and added some logging to track when it has been removed from the bridge for any reason.

Because my bash script was tool and distro directory structure dependant (also partly because of sheer boredom, and hoping it can help someone else who is facing the same issue), I decided to go with python... so there you go.

## Future plans/additions:
* ~~After adding/checking brctl, log it~~
* ~~Check if there is a wlan0 and log it if there isn't~~
* Either log rotation or to keep logs short (around 15 lines or so to prevent insanity from reading a giant log file)
* Do multiple wifi interfaces
* Client<->station logging, to keep track of who is on your network
* Database logging, that might come in handy for a possible node.js project to make it more visible
* ... more ideas will probably follow, once the tool evolves.

### External Python Dependancies:
* netifaces

One will have to install this package via __pip__, __pip3__, or with __python -m pip install__
