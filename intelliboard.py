from ckt_sim import *
from time import sleep
 
from ckt_components import Mux

@ckt
def RandomBit(C):
    from random import choice
    while True:
        yield C.Wait(50)
        yield {"vOut": choice([LO, HI])}

@ckt
def Intelliboard(C):
    from scope_window import ScopeWindow
    win = ScopeWindow()
    
    sel = 0
    outstr = ""
    
    win.setText("Waiting for board to be stable...")
    yield C.Wait(100) 
    
    while True:
        yield {'nSelect': sel}
        yield C.Wait(5) #Propagation delay
        
        outstr = outstr + "\n" + str(C.read('muxes'))
        
        sel = (sel + 1) % 8
        if sel == 0: #Next selection loops over
            win.setText(outstr)
            outstr = ""
        
        
        

def main():
    init_sim()
    breadboard_wires = ["vPin"+str(i) for i in xrange(64)]
    mux_wires = ["vMuxOut"+str(i) for i in xrange(8)]
    
    #Initialize the wires
    net("nSelect", breadboard_wires, mux_wires)
    
    #Assign random bit generators to each breadboard wire
    for wire in breadboard_wires:
        RandomBit(
            dest(vOut=wire)
        )
    
    #Use muxes to gather inputs
    for i in xrange(8):
        Mux(
            "mux"+str(i),
            src(nSelect="nSelect", vInputs=["vPin"+str(j + 8*i) for j in xrange(8)]),
            dest(vOut = mux_wires[i])
        )
    
    Intelliboard(
        "ATMEGA88P",
        src(muxes=mux_wires),
        dest(nSelect="nSelect")
    )
    
    while True:
        sleep(0.01)
        step()


if __name__ == "__main__":
    main()