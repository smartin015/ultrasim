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
        if self.val is None:
            return self.name
        else:
            return "%s (%s)" % (self.name, str(self.val))
    
class Component:
    # Components take input Wires, do some atomic calculation,
    # and produce values on the output Wires.
    # A typical cycle involves calling prep() to 
    # calculate from input values, then drive() to 
    # place the result on output Wires.
    
    class Wait():
        def __init__(self, num):
            self.num = num
            
        def step(self):
            self.num = self.num - 1
            if self.num == 0:
                return None
            return self
            
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
    
    def waiting(self):
        return isinstance(self.next, self.Wait)
    
    def _wait(self):
        if not self.waiting():
            raise Exception("Call to _wait() on non-waiting circuit")
        self.next = self.next.step()
    
    def _mapValues(self, args):
        # Read values from inputs. This supports
        # data structures of arbitrary depth.
        
        if isinstance(args, Wire):
            return args.val
        elif type(args) is str:
            return self._mapValues(self.cin[args])
        elif type(args) is list:
            return [self._mapValues(v) for v in args]
        elif type(args) is dict:
            return {k: self._mapValues(v) for k, v in args.items()}
        else:
            raise Exception("Weird type " + str(type(args)) + " in _getValues()")
        
    def read(self, *args):    
        # No args? Just read all inputs.
        if len(args) == 0:
            return self._mapValues(self.cin)
        elif len(args) == 1:
            #If only one argument, get rid of the extra wrapping
            return self._mapValues(args[0])
        else:
            # Otherwise deep map the values from wires
            return self._mapValues(list(args))
    
    def prep(self):
        if self.waiting():
            self._wait()
        elif self._prep_is_generator:
            self.next = self._prep.next()
        else:
            self.next = self._prep(self, **self.read())
    
    def _driveWire(self, key, args):
        if type(args) is not dict:
            self.cout[key].drive(args)
        else:
            [self._driveWire(k, v) for k, v in args.items()]
    
    def drive(self):
        if not self.next or self.waiting():
            return
        
        if type(self.next) == types.GeneratorType:
            self.next = self.next.next()
        
        self._driveWire(None, self.next)
    
    def __str__(self):
        return "%s" % self._prep.__name__
            
class Simulator():
    def __init__(self):
        self.components = {}
        self.wires = {}
    
    def resolve(self, kwargs):
        # Resolves a series of Wire names into
        # their respective objects
        
        if type(kwargs) is str:
            return self.wires[kwargs]
        elif type(kwargs) is list:
            return [self.resolve(v) for v in kwargs]
        elif type(kwargs) is dict:
            return {k: self.resolve(v) for k, v in kwargs.items()}
        else:
            raise Exception("Weird type " + str(kwargs) + " in sim.resolve()")
        
    def addWire(self, args):
        if type(args) is list:
            for arg in args:
                self.addWire(arg)
        elif type(args) is str:
            name = args
            if self.wires.get(name):
                raise Exception("Simulator wire " + name + " already exists")
            self.wires[name] = Wire(name)
        else:
            raise Exception("Tried to add wire of type " + str(type(args)))
    
    def addComponent(self, name, fn):
        if self.components.get(name):
            raise Exception("Simulator component " + name + " already exists")
        cmp = Component(fn)
        self.components[name] = cmp
        return cmp
    
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
        # TODO: Sort components & wires
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
    
def net(*args):
    # Creates new Wires with given 
    # names and adds to the global netlist
    # TODO: Support arbitrary structure
    for arg in args:
        _sim.addWire(arg)

def net_set(nets, val):
    if type(nets) == list:
        for net in nets:
            wire = _sim.resolve(net)
            wire.prep()
            wire.drive(val)
            
    elif type(nets) == str:
        wire = _sim.resolve(nets)
        wire.prep()
        wire.drive(val)
    else:
        raise Exception("Invalid netlist type " + str(type(nets)))

def net_get(nets):
    if type(nets) == list:
        result = list()
        for net in nets:
            result.append(_sim.resolve(net).val)
        return result
    elif type(nets) == str:
        return _sim.resolve(nets).val
        
def ckt(fn):
    # This decorator allows creating and 
    # registering a new component simply
    # by typing fn('name')
    
    def wrapped(*args):
        
        name = str(len(_sim.components))
        src_kwargs = {}
        dest_kwargs = {}
        
        assert(len(args) <= 3)
        
        for arg in args:
            if type(arg) == str:   
                name = arg
            elif type(arg) == dict:
                if arg.get('src'):
                    src_kwargs = arg['src']
                elif arg.get('dest'):
                    dest_kwargs = arg['dest']
                else:
                    raise Exception('Source or destination arguments for component ' + 
                    name + ' are invalid. Please use src() and dest() functions')
            else:
                raise Exception('Invalid argument type for component ' + name +
                '. Component arguments are (string) name and source/dest lines using src() and dest()')
        
        cmp = _sim.addComponent(name, fn)
        cmp.cin = _sim.resolve(src_kwargs)
        cmp.cout = _sim.resolve(dest_kwargs)
        return cmp
    return wrapped
       
def src(**kwargs):
    # Set input wires for the last created 
    # component by specifying their string names
    return {"src": kwargs}
    
def dest(**kwargs):
    # Set output wires for the last created 
    # component by specifying their string names
    return {"dest": kwargs}
    
       
def step(num=1):
    for i in xrange(num):
        _sim.step()
       
def ckt_state():
    return _sim


# Operations on input arrays (conversions)
def assertTTL(val):
    if val < -0.5 or val > 5.5:
        raise Exception("Value " + str(val) + " outside of acceptible TTL values!")

def isHI(val):
    assertTTL(val)
    return val > 3.7
    
def isLO(val):
    return val < 2.0

def arr2dec(values):
    result = 0
    for val in values:
        result = (result << 1) + isHI(val)
    return result
    