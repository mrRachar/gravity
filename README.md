# gravity
*I really didn't spend long enough on that name, did I...*

## What?
A library and application to allow the 3-D simulation of massive objects through a gravitational fields.
It is designed to be highly extensible, and any part of it can be easily changed programmatically:

 * You want a different G value? Sure thing
 * You want multiple gravitational fields? Sure, I guess, but why not just change the G value...
 * You want to create you own kinds of mechanical fields? Definitely *(Just extend Field)*
 * You want a nice interactive GUI in which you can do all of this. ***Not yet...***
 
## Progress
Generally OK. I mean, the 3-D forces, motion, distance, accelerations and positions work fine, the 
matplotlib-base graphing is doing something, *finally*, however fields, or at least the built in
gravitational field, doesn't seem to be doing what it should, which is a real shame, seeing as that
is the whole point of this, isn't it.