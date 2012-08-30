""" Default libs. """
from smtplib import SMTP_SSL
from email.MIMEText import MIMEText
""" User libs. """
from bbio import *
import inc.config as config # Change this to a .cfg file and parse.
import inc.framework as framework

""" Does initial setup of the pins by settings them to pulldown inputs. """
def setup():
  for zone in framework.zones.getZones():
    pinMode(zone.pin, INPUT, -1)


""" Loops continously pooling each of the pins connected to each zone.
    Checks if the zone has changed state then updates the database. """
def loop():
  for zone in framework.zones.getZones():
    curstate = digitalRead(zone.pin)
    if curstate == 0 and zone.state == True:
      print zone.name + " Opened"
      zone.state = False
      zone.lastevent = time.time()
      updatedb(zone)
    elif curstate == 1 and zone.state == False:
      print zone.name + " Closed"
      zone.state = True
      zone.lastevent = time.time()
      zone.timeslo = 0
      updatedb(zone)
    if curstate == 0: 
      if (zone.lastevent + 300) < time.time():
        print zone.name + " Left Opened"
        zone.lastevent = time.time()
        sendemail(zone)
  toggle(USR3) # Show activity that this script is running.
  delay(500) # Give the CPU a little break.				

""" Updates the database with the new zone state and last event time. """
def updatedb(zone):
  con = framework.lite.connect('/etc/SmartHome/Databases/Security.sqlite')
  cur = con.cursor()
  cur.execute("INSERT INTO Log(Time, Zone, State) VALUES(?, ?, ?)", [zone.lastevent, zone.name, zone.state])
  con.commit()
  con.close()

""" Sends email to the recepients in the config file using the smtp credentials
    in the config file. """
# TODO: Move into framework.
def sendemail(zone):
  zone.timeslo = zone.timeslo + 1
  timeslo = (zone.timeslo * 5)
  msg = MIMEText(zone.name + " Left Opened For: " + str(timeslo)  + "min." , "plain")
  msg['Subject']= ""
  msg['From'] = "emailuser" # some SMTP servers will do this automatically, not all

  try:
    smtpserver = smtplib.SMTP("emailserver",587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login('emailuser', 'emailpass')
    smtpserver.sendmail('emailuser', 'to', msg.as_string())
    smtpserver.close()
  except: 
    print "Message could not be sent. Likely due to the internet connection being down."

run (setup, loop)

