from ckt_sim import *
from time import sleep
import pygame

@ckt 
def LED(C, I):  
  color = C.extra['col']
  if (I != C.extra['c']):
    color = tuple([0.3*col for col in color])
  pygame.draw.circle(C.extra['screen'], color, C.extra['pos'], 10, 0)

@ckt
def LEDController(C):
    while True:
        while C.read('en') != "R":  #while other light is active
          yield {"out": "R"}
          yield C.Wait(5) # 0.5 seconds (max)
        
        yield {"out": "G"}
        yield C.Wait(30) # 3 seconds
    
        yield {"out": "Y"}
        yield C.Wait(10) # 1 second
    
        yield {"out": "R"}
        yield C.Wait(30) # 3 seconds
        
        

def stoplight(id, wire, enable, window, x, y):
    LED(src(I=wire), extra(screen=window, pos=(x,y), c="R", col=(255,0,0)))
    LED(src(I=wire), extra(screen=window, pos=(x,y+20), c="Y", col=(255,255,0)))
    LED(src(I=wire), extra(screen=window, pos=(x,y+40), c="G", col=(0,255,0)))
    LEDController(
      src(en=enable), 
      dest(out=wire)
    )
    

def main():
    pygame.init()
    init_sim()
    
    window = pygame.display.set_mode((120, 60)) 
    net("en1", "en2")
    net_set("en1", "G") #This one starts
    net_set("en2", "R")
    stoplight(1, "en1", "en2", window, 10, 10)
    stoplight(2, "en2", "en1", window, 30, 10)
   
    n = 0
    while True:
        sleep(0.1)
        step()
        pygame.display.flip()
        print ckt_state()
        n = n + 1


if __name__ == "__main__":
    main()