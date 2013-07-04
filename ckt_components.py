from ckt_sim import *

@ckt
def DC5V(C):
    return {"out": 5}
    
@ckt
def Counter(C):
    #Setup phase
    count = 0
    
    #Loop phase.
    # use yield instead of return here,
    # but everything else works as normal.
    while True: 
        yield {"out": count}
        count = count + 1
        
@ckt
def Mux(C, nSelect, vInputs):
    if nSelect is not None:
        return {"vOut": vInputs[nSelect]}