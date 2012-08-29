from bbio import *
import sqlite3 as lite
from smtplib import SMTP_SSL
from email.MIMEText import MIMEText
from config import *

class pinStructure:
    def __init__(self, pin, name, state, lastevent):
        self.pin = pin
	self.name = name
	self.state = state
	self.lastevent = lastevent
	self.timeslo = 0

# Add class that contains the arrays to remove the use of globals.
# Determine if this class needs to be moved to a setup file or if it is okay to stay into here.
zones = []
sqlcache = []

# Setup the GPIO pins for input 
def setup():
	con = lite.connect('/etc/SmartHome/Databases/Security.sqlite')
  	cur = con.cursor()

	for row in cur.execute('SELECT * FROM Zones'):
        	zones.append(pinStructure(row[1], row[2], True, time.time()))
		pinMode(row[1], INPUT)

# Overview: Loops continously pooling each of the pins connected to the alarm door window and motion sensors.
#           Checks if the zone has changed state and then executes commands to update the sql database.	
def loop():
	for zone in zones:
		curstate = digitalRead(zone.pin)

		if curstate == 0 and zone.state == True:
			print zone.name + " Opened"
			zone.state = False
			zone.lastevent = time.time()
			updatedb(zone)
			#sendemail(zone)

		elif curstate == 1 and zone.state == False:
			print zone.name + " Closed"
			zone.state = True
			zone.lastevent = time.time()
			zone.timeslo = 0
			updatedb(zone)
			#sendemail(zone)			

		if curstate == 0:
			if (zone.lastevent + 300) < time.time():
				print zone.name + " Left Opened"
				zone.lastevent = time.time()
				sendemail(zone)

	delay(500) # Give the CPU a little break.				

# Overview: Used to update the database with the zone information.
# Inputs: zone object (zone.pins, zone.name, zone.state, zone.lastevent, zone.timeslo)
def updatedb(zone):
	try:
		con = lite.connect('/etc/SmartHome/Databases/Security.sqlite')
        	cur = con.cursor()
		# This line need to be cleaned up a bit...
        	cur.execute("INSERT INTO Log(Time, Zone, State) VALUES('"+str(zone.lastevent)+"', '"+str(zone.name)+"' , '"+str(zone.state)+"')")
		con.commit()
        	con.close()
		addqueued()
	except:
		sqlcache.append(pinStructure(zone.pin, zone.name, zone.state, zone.lastevent))
		e = sys.exc_info()[1]
		print e
		
# Overview: Used to add the zone values to the database once the mysql database comes back online.
def addqueued():
	con = lite.connect('/etc/SmartHome/Databases/Security.sqlite')
	cur = con.cursor()

	for entries in sqlcache:
		cur.execute("INSERT INTO Log(Time, Zone, State) VALUES('"+str(zone.lastevent)+"', '"+str(zone.name)+"' , '"+str(zone.state)+"')")
		con.commit()		
	con.close()
	del sqlcache[:]

# Overview: Send an email when a zone has been left opened for more than 5 minutes.
# Inputs: zone object (zone.pins, zone.name, zone.state, zone.lastevent, zone.timeslo)
# This needs to be turned into a external class. No real need for it here and it also needs to be used in other places. 
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

