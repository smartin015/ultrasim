from ckt_sim import *   

# --------------------------
# Define circuit components
# --------------------------

@ckt
def Counter(C):
    #Setup phase
    count = 0
    
    #Loop phase.
    # use yield instead of return here,
    # but everything else works as normal.
    while True: 
        count = count + 1
        yield {"out": count}

# --------------------------
# Build the circuit 
# --------------------------
        
# Define nets (i.e. wires).
# Any number of wires can be defined
# at once in this same function.
net("Out")        

# Define voltage source.
# Note how source doesn't need
# to be specified for the circuit to run.
Counter("Counter generator")
dest(out="Out")


# --------------------------
# Simulate!
# --------------------------
print "Initial circuit state:"
print ckt_state()

for i in xrange(50):
    step()
    
print "State after 50 steps:"
print ckt_state()

   
for i in xrange(150):
    step()

print "State after 200 steps:"
print ckt_state()
