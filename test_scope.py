from ckt_sim import *   
from time import sleep

# --------------------------
# Define circuit components
# --------------------------
from ckt_components import Scope, Counter

def main():    
    init_sim()  
    net("A","B","C")
    net_set("A", 5)
    net_set("B", 2)
    net_set("C", 7)
    
    Counter(
        "testcnt",
        dest(out="A")
    )
    
    Scope(
        "testscope",
        src(inputs_dict={"A": "A", "B": "B", "C": "C"})
    )
    
    for i in xrange(50):
        sleep(0.1)
        step()

if __name__ == "__main__":
    main()