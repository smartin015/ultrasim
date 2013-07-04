from ckt_sim import *   

# --------------------------
# Define circuit components
# --------------------------

@ckt
def Micro(C):
    count = 0
    while True: 
        yield {"nCount": count}
        yield C.Wait(5)
        count = (count + 1) % 8
        
@ckt
def Mux(C, nSelect, vInputs):
    if nSelect is not None:
        return {"vOut": vInputs[nSelect]}
      
def main():    
    init_sim()  
    # --------------------------
    # Build the circuit 
    # --------------------------
    vIns = ["vI"+str(x) for x in xrange(8)]
    net("vOut", vIns, "nSel")
    net_set(vIns, LO)
    net_set(["vI2", "vI4"], HI)

    Mux()
    src(nSelect="nSel", vInputs=vIns)
    dest(vOut="vOut")

    Micro()
    dest(nCount="nSel")

    # --------------------------
    # Simulate!
    # --------------------------

    step(5)
    assert(net_get("vOut") == LO)
    step(25)
    assert(net_get("vOut") == HI)
    print ckt_state()

if __name__ == "__main__":
    main()