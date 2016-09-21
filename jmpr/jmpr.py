import sys
import tty
import termios
import numpy
import threading
import random, time
import colorsys

from operator import itemgetter
from itertools import groupby

try: 
    import unicornhat as uh
    unicorn = 1
    uh.brightness(.8)
    uh.rotation(0)
except ImportError:
    unicorn = 0

def show_matrix(mat):
    for i in mat:
        print " ".join([str(x[0]) for x in i])    

def makefield():
    field = []
    for i in range(8):
        row = []
        for j in range(8):
            row.append([0,0,0])
        field.append(row)
    return field

fd=''
def readchar():
    global old_settings
    global fd
    fd = sys.stdin.fileno()

    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    if ch == '0x03':
        raise KeyboardInterrupt
    return ch

def readkey(getchar_fn=None):
    getchar = getchar_fn or readchar
    c1 = getchar()
    if ord(c1) != 0x1b:
        return c1
    c2 = getchar()
    if ord(c2) != 0x5b:
        return c1
    c3 = getchar()
    return chr(0x10 + ord(c3) - 65)  # 16=Up, 17=Down, 18=Right, 19=Left arrows

level=1
r=[255,0,0]
g=[0,255,0]
b=[0,0,255]
y=[255,255,0]
c = [0,255,255]
colors = [r,g,b]#,y,c]
gameover = 0

bodyc = [[255,0,0]]
for i in range(63):
    bodyc.append([0,255,255])

fieldcolor = [255,255,255]
jmprcolors = [[255,0,0], [255,152,0], [255,255,0]]

class jmpr(threading.Thread):
    def __init__(self):
        self._stopevent = threading.Event()
        self.gameover = 0
        self.score = 0
        self.cycle = .25
        self.field = [fieldcolor for x in range(8)]
        self.dot = {"pos":[0,1], "height":0}
        threading.Thread.__init__(self)
        
    def step(self):
        obstacle = random.random()
        if obstacle > .80 and self.field[0] != [0,255,0]:
            self.field.insert(0, [0,0,0])
            self.field.pop()
        else:
            self.field.insert(0, fieldcolor)
            self.field.pop()
        
        
    def draw(self):
        for c, cell in enumerate(self.field):
            uh.set_pixel(c, 0, cell[0], cell[1], cell[2])
        cycle_jmpr = jmprcolors[self.dot["height"]]
        uh.set_pixel(6, 0, cycle_jmpr[0], cycle_jmpr[1], cycle_jmpr[2])
        if self.dot["height"] > 0:
            self.dot["height"] -= 1
        if self.field[6] == [0,0,0] and self.dot["height"] == 0:
            self.gameover = 1
        uh.show()
        time.sleep(self.cycle)
        

    def run(self):
        while not self.gameover:
            self.draw()
            self.step()
            
        #self.explode()
        self._stopevent.set()
        if self.gameover:
            self.end()
        
    def join(self, timeout=None):
          self._stopevent.set( )
          threading.Thread.join(self, timeout)

    def set_jump(self, press):
        if press == "w":
            if self.dot["height"] < 2:
                self.dot["height"]+=1
        
    
    def explode(self):
        for c in range(4):
            for i, part in enumerate(self.body):
                uh.set_pixel(part[0], part[1], 255, 255, 255)
            uh.show()
            time.sleep(.1)
            for i, part in enumerate(self.body):
                uh.set_pixel(part[0], part[1], 255, 0, 0)
            uh.show()
            time.sleep(.1)
    
    def end(self):
        for row in range(8):
            for j in range(8):
                uh.set_pixel(row, j, 255,0,0)
                uh.show()
                time.sleep(.001)
        self._stopevent.set()  
         
thread1=jmpr()
thread1.daemon = 1
thread1.start()

while 1:
    
    user_input = readkey()
    if user_input == "x":
        thread1.gameover = 1
        thread1.join()
        print "thread gameover"
        break
    if thread1._stopevent.isSet():
        user_input = "x"
        thread1.gameover = 1
        thread1.join()
        print "thread stopevent"
        break
    if user_input != "x":
        thread1.set_jump(user_input)
        print "normal move"
   
    else:
        continue

thread1.gameover = 1
thread1.join()

