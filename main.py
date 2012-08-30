"""
 Intelligent Security System - main.py - v0.1
 Created: 05/2012
 Author: Keaton Taylor - keaton@keatonstaylor.com - www.keatonstaylor.com
 Website: https://github.com/keatontaylor/GuardDog
 
 A continuously running python script that monitors the state of 
 each zone in the system and updates a sqlite databse when the zone
 changes state.

 Copyright 2012 Keaton Taylor

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

# Default libs.
from smtplib import SMTP_SSL
from email.MIMEText import MIMEText
# User libs.
from bbio import *
import inc.config as config # Change this to a .cfg file and parse.
import inc.framework as framework

def setup():
  """ Pre-run setup. Set up pins as Pulldown INPUTS. """
  for zone in framework.zones.getZones():
    pinMode(zone.pin, INPUT, -1)

def loop():
  """ Loops continously pooling each of the pins connected to each zone.
      Checks if the zone has changed state then updates the database. """
  for zone in framework.zones.getZones():
    curstate = digitalRead(zone.pin)
    if curstate == 0 and zone.state:
      print zone.name + " Opened"
      zone.state = False
      zone.lastevent = time.time()
      updatedb(zone)
    elif curstate == 1 and not zone.state:
      print zone.name + " Closed"
      zone.state = True
      zone.lastevent = time.time()
      zone.timeslo = 0
      updatedb(zone)
  toggle(USR3) # Show activity that this script is running.
  delay(500) # Give the CPU a little break.				


def updatedb(zone):
  """ Updates the database with the new zone state and last event time. """
  con = framework.lite.connect('/etc/SmartHome/Databases/Security.sqlite')
  cur = con.cursor()
  cur.execute("INSERT INTO Log(Time, Zone, State) VALUES(?, ?, ?)", [zone.lastevent, zone.name, zone.state])
  con.commit()
  con.close()

run (setup, loop)

