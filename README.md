ULTRASIM
========

What is ULTRASIM?
-------------

ULTRASIM is an environment for quickly prototyping electronics.

No, really - What is this?
-------------------------

Have you ever had an awesome idea for an embedded systems project or 
thought up some cool electronics scenario, tried to prototype it, 
and ended up daisy-chaining breadboards together and spending hours
stripping wire? 

Yeah, me too. 

It seems like a no-brainer that people should simulate or draw up their
projects before they go straight to hardware, but actually sitting down, 
creating components, wiring out the circuit, and then realizing there's 
no way to simulate your micro on whatever simulator you're using - it's 
just a lot of work!

The real problem here is the level of detail.  Most simulators aim for
perfect simulation; this one aims for *fast prototyping*. It's a tool 
to make sure you've covered all your bases and haven't left anything out
of your design before you dive into your project. There's no fixed level
of detail - your sim could be a single black box module or you could 
describe everything all the way down to the individual resistor. 

In the end, your simulator is exactly as complex as you need it to be.
And that's all that really matters when you're just starting to
plan out your next project.

Can I build X with ULTRASIM?
----------------------------

You sure can! 

Cool. So how does it work?
--------------------------

This simulator operates under the abstraction that any part 
of your project - any *component* - can be represented by a function
that takes in values, does some computation on them, and outputs 
other values. Components that have a certain state (such as microcontrollers
or FSMs) are also functions, but they can yield multiple values without 
returning. 

Just having components would be kind of boring, so we can hook them together
using *Wires*. These aren't wires in the traditional sense (note the capital 'W'), 
since a wire can have any conceivable value on it, up to and including other components 
or circuit simulations. This offers a number of advantages: emulating serial? 
put a string on the wire! Counting something? Put the actual value on there! 
No more do you have to fiddle with multi-wire buses (here's looking at you, Verilog) - 
there's just no need!

Once components are hooked up to wires, call *step()* in a loop to step through the 
simulation. A simulator step can represent any length of time you want it to, but keep
in mind any wire a function drives takes at least one step for all attached components
to see the value as an input.

The TL;DR: 
- Components are functions, hooked up by Wires. 
- Stateful components can use yield instead of return
- Initialize the sim, create your components/wires, and step through to simulate.

If you ever feel lost, take a look at the tests folder for examples!