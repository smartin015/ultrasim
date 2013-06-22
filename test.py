from ckt_sim import *   

# --------------------------
# Define circuit components
# --------------------------

@ckt
def DC5V(C):
    return {"out": 5}

@ckt
def Amp2X(C, i1):
    if i1: # On init, all inputs will be None
        return {"out": i1*2}

# --------------------------
# Build the circuit 
# --------------------------
        
# Define nets (i.e. wires).
# Any number of wires can be defined
# at once in this same function.
net("5V", "Out")        

# Define voltage source.
# Note how source doesn't need
# to be specified for the circuit to run.
DC5V("DC Source")
dest(out="5V")

#Define amplifier circuit. 
Amp2X("Amplifier O' Doom")
src(i1="5V")
dest(out="Out")

# --------------------------
# Simulate!
# --------------------------
print "Initial circuit state:"
print ckt_state()

step()

print "State after step 1:"
print ckt_state()

step()

print "State after step 2:"
print ckt_state()