import Tkinter
import threading
from time import sleep

class ScopeWindowThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()
    def callback(self):
       self.root.quit()
    def setText(self, val):
        self.s.set(val)
    def run(self):
        self.root=Tkinter.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.s = Tkinter.StringVar()
        l = Tkinter.Label(self.root,textvariable=self.s)
        l.pack()
        self.root.mainloop()
     
def ScopeWindow():
    thread = ScopeWindowThread()
    sleep(0.2) #Ensure scope window thread starts up
    return thread
     
def main():
    from time import sleep
    app = ScopeWindow()
    sleep(1)
    print 'Changing value'
    app.setText('herp SUPER LONG STRING OF LONGNESS')
    
if __name__ == "__main__":
    main()