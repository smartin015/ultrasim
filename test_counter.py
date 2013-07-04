from ckt_sim import *   

# --------------------------
# Define circuit components
# --------------------------
from ckt_components import Counter

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
    assert(net_get("Out") == 0)
    print "After 1 step:"
    print ckt_state()
    
    
    for i in xrange(50):
        step()
    
    assert(net_get("Out") == 50)    
    print "State after 51 steps:"
    print ckt_state()

       
    for i in xrange(150):
        step()

    assert(net_get("Out") == 200)
    print "State after 201 steps:"
    print ckt_state()

if __name__ == "__main__":
    main()