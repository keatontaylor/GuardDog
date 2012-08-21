Guard Dog README
=======

After many weeks of not updating this blog I've finally managed to get around to completing the majority of the hardware requirements for the open source security system I've been developing. I've migrated from using an Arduino for detecting events to using a beagle-bone so that I could centralize processing of all the events and provide a single platform that could be used for installation.

The entire project is still a large work in progress but with the bulk of the hardware implementation complete my focus now shifts towards the software aspects of the device. A great deal of though has gone into the exact design of the software and how it will function in an intelligent way.

Using the GPIO pins on the beagle-bone entry and exit events are detected and logged. Using these events an algorithm is being developed to analyze the data. Clustering and the development of a neural net will be used to determine the likelihood of an event trigger for a specific timezone. Overtime the system will learn your habits and patterns will emerge. Using these patterns and the structure provided in the neural net notifications will be sent to assigned users depending on the likelihood of a false entry.

Using this method it is theorized that in a little as a month the system should be able to interpret when it is likely for someone to be home and when it is likely some isn't. Although this system in theory provides an extremely accurate way of detecting events that don't fall within the typical norm, it does present issues that will need to be addressed in future versions of the software.

The largest of the concerns is that data analysis does not inherently have a way of detecting of someone is already home or has been home. This presents itself as an issue when the occupant walks into a zone or triggers an event the system was not able to anticipate, ultimately triggering a notification when in reality no notification needed to be sent out. To resolve this issue the system has to be able to detect occupancy, and to do so a method of detecting the rough number of people in the home needs to be developed.

To accomplish this theory was devised that would allow the system to detect the direction of motion by calculating events triggered down to the nearest 10 milliseconds. This works by detecting a motion event before a door event or vice versa giving the system a reasonable assessment of whether someone entered or left the premisses. To counteract the systems inability to detect the number of occupants that entered the system will calculate the total number of motion detection events within one hour of the entry or exit to determine the approximate occupancy.

During my research this method of determining occupancy  was able to predict with around 80% accuracy the number of occupants in the home with as little as two motion detection sensors strategically place around active areas of the home.

Much work needs to be done and theory needs to be proven in real world testing but all-in-all the development of the system is progressing. Hopefully a large chunk of the system will be completed within the coming months.
