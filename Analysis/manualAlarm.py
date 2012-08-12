# This class handles manual operation of the household alarm


class alarm():
   alarmSet = false       # If set, send alerts whenever events are triggered
   alertOnMotion = false  # If set, send alerts even when only motion events are triggered

   def newEvent(alarmEvent):
      if (alarmSet):
         if ((alarmEvent.type == "motionEvent"):
            if (alertOnMotion == true):
               sendAlert()
         else
            sendAlert(alarmEvent)

      
