from ckt_sim import *   

# --------------------------
# Define circuit components
# --------------------------
from ckt_components import DC5V

@ckt
def Amp2X(C, i1):
    if i1: # On init, all inputs will be None
        return {"out": i1*2}

def main():
    init_sim()
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
    assert(net_get("5V") == 5)

    print "State after step 1:"
    print ckt_state()

    step()
    assert(net_get("5V") == 5)
    assert(net_get("Out") == 10)

    print "State after step 2:"
    print ckt_state()
    
    
if __name__ == "__main__":
    main()