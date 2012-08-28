# This class will create and update the Neural Network (hereafter referred to as the NN).
# Created Aug. 27, 2012 by P3+J3^u!

class DBM():
   def readDB():
	   # TODO: write code to populate dpList with points containing zone, time and day
       # from entries in the database.
	
   def developClusters():
      # TODO: write code to take an input database  containing motion and pass-through events 
      # and then perform a clustering algorithm on the data, and finally output a DB/file
      # describing those clusters

      # Loop through each zone and develop its cluster
      for zone in Zones
         # Find the nearest neighbor of each point
         for dp in zone.dpList
            if zone.matchupDict[dp] == NULL
	            # add the zone to the hash
               zone.matchupDict[dp] = {-1, -1, 2147483647}
               distance = 2147483647
               # remove the point from the list
               dpList.pop(dp)
            else 
               distance = zone.matchupDict[dp[2]]
            
            # now cycle through all the remaining points in the db so that each point
            # is eventually compared with every other point
            for partner in zone.dpList
               if temp = findDistance(dp, partner) < distance
                  newPartner = partner
                  distance = temp
            
            # Update hash if new match is found
            if distance < zone.matchup[dp[2]]
               zone.matchupDict[dp] = {newPartner[0], newPartner[1], distance}
               if zone.matchupDict[newPartner]
                  if zone.matchupDict[newPartner[2]] < distance
                     zone.matchupDict[newParter] = zone.matchupDict[dp[0], dp[1], distance]
               else
	              zone.matchupDict[newParter] = zone.matchupDict[dp[0], dp[1], distance]
	
         # TODO: Find the mean and standard deviation of the min distances in this cluster
         
         # TODO: Put each point into a cluster with its nearest neighbor if its distance
         # is within two standard deviations of the mean.

         # TODO: Test this code and evaluate whether this clustering method is useful.

   def developNN():
      # TODO: write code to take an input database containing cluster info and then write a neural
      # network to perform classification of a new entry into one of those clusters, then output
      # that neural network to a DB/file
   
   # This function finds the distance between two points in a given zone based on time of day
   # and weekday.
   def findDistance(point1, point2):
      distDay = point1.day - point2.day
      distTime = point1.time - point2.time

      return sqrt(distDay^2 + distTime^2)

   def findWeekday():
      # TODO: write code to find the weekday based on the time value.  Weekdays are Sunday (0) through
      # Sunday (7).

   def findTimeOfDay():
      # TODO: write code to find the time of day based on the time value returned by the DB.

	