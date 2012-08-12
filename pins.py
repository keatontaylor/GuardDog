from bbio import *

class pinStructure:

    def __init__(self, pin, name, state, lastevent):
        self.pin = pin
	self.name = name
	self.state = state
	self.lastevent = lastevent
	self.timeslo = 0

zones = []

zones.append(pinStructure(GPIO1_12, "Back Door", True, time.time()))
zones.append(pinStructure(GPIO0_26, "Front Windows", True, time.time()))
zones.append(pinStructure(GPIO1_14, "Front Door", True, time.time()))
zones.append(pinStructure(GPIO2_22, "Attic Door", True, time.time()))
zones.append(pinStructure(GPIO1_31, "Garage Door", True, time.time()))
zones.append(pinStructure(GPIO1_5, "Upstairs Windows", True, time.time()))
zones.append(pinStructure(GPIO1_1, "Garage Windows", True, time.time()))
zones.append(pinStructure(GPIO1_29, "Bedroom Windows", True, time.time()))
zones.append(pinStructure(GPIO2_24, "Hallway Motion", True, time.time()))
zones.append(pinStructure(GPIO2_25, "Livingroom Motion", True, time.time()))
zones.append(pinStructure(GPIO2_23, "Livingroom/Kitchen Windows", True, time.time()))
