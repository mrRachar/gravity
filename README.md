![logo](logo.svg)

*I really didn't spend long enough on that name, did I...*

## What?
A library and application to allow the 3-D simulation of massive objects through a gravitational fields.
It is designed to be highly extensible, and any part of it can be easily changed programmatically:

 * You want a different G value? Sure thing
 * You want multiple gravitational fields? Sure, I guess, but why not just change the G value...
 * You want to create you own kinds of mechanical fields? Definitely *(Just extend Field)*
 * You want a nice interactive GUI in which you can do all of this. ***Not yet...***
 
## Progress
Simulating is fine. I still need to create a GUI to control things, but simulations such as the earth
and the moon work, and graph, fine. I plan to also change how the process happens, with the whole
process simulated first, and then controlled playback can occur, and the simulation can be saved. This
should reduce the current problem of either having way to slow a simulation, but decent accuracy, or
sacrificing on accuracy completely, for the sake of simulation time.