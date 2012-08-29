class zones:
    zonearr = []
    @classmethod
    def getZones(cls):
		if not cls.zonearr:
			con = lite.connect('/etc/SmartHome/Databases/Security.sqlite')
			cur = con.cursor()
			for row in cur.execute('SELECT * FROM Zones'):
				cls.zonearr.append(pinStructure(row[1], row[2]))
                return cls.zonearr
            else:
                return cls.zonearr

class pinStructure:
    def __init__(self, pin, name):
        self.pin = pin
	self.name = name
	self.state = True
	self.lastevent = time.time()
	self.timeslo = 0
