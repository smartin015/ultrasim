import types
import inspect

# High and low logic (voltage) levels.
# Follows TTL spec
HI = 5
LO = 0

# Z or "High Impedence" value. Indicates electrical disconnect.
# This is a "safe" value for starting inputs/outputs
class ZVal():
    def __str__(self):
        return "Z"
Z = ZVal()


class Wire():
    # Routes multiple outputs to multiple inputs of components.
    # Only one component can "drive" the wire (or specify its value)
    # per prep/drive cycle.
    
    def __init__(self, name):
        self.val = None
        self.name = name
        self.valchange = False
    
    def prep(self):
        self.valchange = False
        
    def drive(self, val):
        # If disconnected, don't change the value
        if val == Z:
            return
    
        if self.valchange:
            raise Exception("Wire "+str(self)+" driven by multiple Components!")
        
        self.val = val
        self.valchange = True
        
    def __str__(self):
        if not self.val:
            return self.name
        else:
            return "%s (%s)" % (self.name, self.val)
    
class Component:
    # Components take input Wires, do some atomic calculation,
    # and produce values on the output Wires.
    # A typical cycle invoels calling prep() to 
    # calculate from input values, then drive() to 
    # place the result on output Wires.
    
    def __init__(self, prep_func):
        self._prep = self._prepare_prep_func(prep_func)
        self._prep_is_generator = (type(self._prep) == types.GeneratorType)
        self.cin = {}       # Input wires
        self.cout = {}      # Output wires
        self.next = {}      # Next output value
    
    def _prepare_prep_func(self, prep_func):
        # Generators should not have inputs
        # other than this component object
        argspec = inspect.getargspec(prep_func)
        if len(argspec.args) == 1 and argspec.varargs == None:
            generator = prep_func(self)
            if (type(generator) == types.GeneratorType):
                return generator
        
        return prep_func
        
    def read(self, *args):
        # Read values from inputs. Note this 
        # is a shallow mapping operation, so
        # nested wires are a no-no.
        
        ivals = {}
        if len(args) == 0:
            for i in self.cin:
                ivals[i] = self.cin[i].val
                
        elif len(args) == 1 and type(args[0]) is not list:
            return self.cin[args[0]].val
            
        elif len(args) == 1 and type(args[0]) is list:
            for wire in args[0]:
                ivals[i] = wire.val
                
        else: # Many args
            for wire in args:
                ivals[i] = wire.val
                
        return ivals
    
    def prep(self):
        if self._prep_is_generator:
            self.next = self._prep.next()
        else:
            self.next = self._prep(self, **self.read())
    
    def drive(self):
        if not self.next:
            return
    
        for o in self.cout:
            self.cout[o].drive(self.next[o])
    
    def input(self, t):
        print t
    
    def __str__(self):
        return "%s" % self._prep.__name__
            
class Simulator():
    def __init__(self):
        self.lastComponent = None
        self.components = {}
        self.wires = {}
    
    def resolve(self, kwargs):
        # Resolves a series of Wire names into
        # their respective objects
        result = {}
        for k in kwargs:
            result[k] = self.wires[kwargs[k]]
        return result
    
    def addWire(self, name):
        self.wires[name] = Wire(name)
    
    def addComponent(self, name, fn):
        cmp = Component(fn)
        self.components[name] = cmp
        self.lastComponent = cmp
    
    def step(self):
        # Go through a single prep/drive cycle.
        # After this step, wire values are 
        # the results of the previous wire and 
        # component states.
        
        # Prep wires first to clear exception case
        for w in self.wires:
            self.wires[w].prep()
    
        for c in self.components:
            self.components[c].prep()
    
        for c in self.components:
            self.components[c].drive()
        
    def __str__(self):
        cmpstr = ""
        for c in self.components:
            cmpstr += "- %s (%s)\n" % (c, str(self.components[c]))
        
        wirestr = ""
        for w in self.wires:
            wirestr += "- " + str(self.wires[w]) + "\n"
    
        return "Components:\n%sWires:\n%s" % (cmpstr, wirestr)
        

# Every circuit project should have a global
# simulator object to manage the list of 
# wires and components.
_sim = None
def init_sim():
    global _sim
    _sim = Simulator()
init_sim()
    

def net(*args):
    # Creates new Wires with given 
    # names and adds to the global netlist
    for name in args:
        _sim.addWire(name)

def ckt(fn):
    # This decorator allows creating and 
    # registering a new component simply
    # by typing fn('name')
    
    def wrapped(name = None):
        if not name:
            name = str(len(_sim.components))
        _sim.addComponent(name, fn)
        return _sim.components[name]
    return wrapped
       
def src(**kwargs):
    # Set input wires for the last created 
    # component by specifying their string names
    _sim.lastComponent.cin = _sim.resolve(kwargs)
        
       
def dest(**kwargs):
    # Set output wires for the last created 
    # component by specifying their string names
    _sim.lastComponent.cout = _sim.resolve(kwargs)
       
def step():
    _sim.step()
       
def ckt_state():
    return _sim
