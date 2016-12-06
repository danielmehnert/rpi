import copy, random
import colorsys
import time
nohat = 0
try:
    #import unicornhat as uh
    import blinkt as blnkt
    blnkt.set_brightness(.1)
except ImportError:
    print "no Unicornhat found"
    nohat = 1
import time

#if not nohat:
#    uh.brightness(.2)

def show_matrix(mat):
    for row in mat:
        print " ".join(str(x[0]) for x in row)

def uh_show_matrix(mat, pause = .075):
    for y in range(len(mat)):
        for x in range(len(mat[0])):
            uh.set_pixel(x, y, mat[x][y][0], mat[x][y][1], mat[x][y][2])
            
    uh.show()
    time.sleep(pause)
        

def pomodoro(color = (255,0,0), min=25):
    for y in range(8):
        for x in range(8):
            uh.set_pixel(x, y, color[0], color[1], color[2])
    uh.show()
    for i in range(7,-1,-1):
        for j in range(7,-1,-1):
            time.sleep(min*60/64)
            uh.set_pixel(j,i, 0,0,0)
            uh.show()

def pomodoro_blnkt(color = (255,0,0), min=25):
    blnkt.set_brightness(.1)
    blnkt.set_all(color[0], color[1], color[2])
    blnkt.show()
    for p in range(8):
        time.sleep(min*60/8)
        blnkt.set_pixel(p, 0,0,0)
        blnkt.set_brightness(0.1*0.9**p)
        blnkt.show()

def pomodoro_fade(color = (255,0,0), min=25):
    blnkt.set_brightness(.1)
    blnkt.set_all(color[0], color[1], color[2])
    blnkt.show()
    for p in range(8):
        for i in range(10):
            time.sleep(min*60/8/10)
            blnkt.set_pixel(p, color[0], color[1], color[2], brightness=0.1-0.01*i)
            #blnkt.set_brightness(0.1*0.9**p)
            blnkt.show()



if __name__ == "__main__":
    while 1: 
        #pomodoro_fade(min=.5)
        #pomodoro_fade(color=(0,255,0),min=.5)
        pomodoro_fade(min=25)
        pomodoro_fade(color=(0,255,0), min=5)
