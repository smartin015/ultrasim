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
        print "Yielding",count
        yield {"out": count}
        count = count + 1

def main():
    init_sim()
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

    step()
    print "After 1 step:"
    print ckt_state()
    assert(net_get("Out") == 1)
    
    for i in xrange(50):
        step()
    
    assert(net_get("Out") == 50)    
    print "State after 50 steps:"
    print ckt_state()

       
    for i in xrange(150):
        step()

    assert(net_get("Out") == 200)
    print "State after 200 steps:"
    print ckt_state()

if __name__ == "__main__":
    main()