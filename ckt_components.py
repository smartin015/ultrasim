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
      
@ckt
def NoisyLine(C):
    from random import choice
    while True:
        yield {"vOut": choice([LO, HI])}
      
@ckt  
def Scope(C):
    from scope_window import ScopeWindow
    win = ScopeWindow()
    val = ""
    while True:
        inputs_dict = C.read('inputs_dict')
        val = ""
        for input in sorted(inputs_dict):
            val = val + input + ": " + str(inputs_dict[input]) + "\n"
        win.setText(val)
        yield dict()