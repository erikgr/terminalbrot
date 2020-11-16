#!/usr/bin/python
#
# Explore the mandelbrot set from the
# linux terminal
#
# WASD - shift the position 
# Q    - zoom in
# E    - zoom out
# Esc  - exit
#
# 2020 :: EJG


import os
import numpy
from pynput.keyboard import Key, Listener

posx = 0
posy = 0
zoom = 1

# increase this for more color resolution,
# but drawing time will increase linearly
iterations = 60


# Zi+1 = Zi² + C
def F(z, c):
    t1 = z[0] * z[0]
    t2 = z[0] * z[1]
    t3 = z[1] * z[0]
    t4 = z[1] * z[1]
    r = t1 + (t4 * -1) + c[0]
    i = t2 + t3 + c[1]
    return (r, i)

def stability(c):
    global iterations
    r, i = (0, 0)
    for n in range(0, iterations):
        r, i = F((r, i), c)
        if(r > 2
            or r < -2
            or i > 2
            or i < -2):
            return n
    return iterations

def draw(pos, zoom):
    global iterations
    winh, winw = os.popen('stty size', 'r').read().split()
    winh = float(winh) -1
    winw = float(winw) -1
    miny = (-2 * zoom) + pos[1]
    maxy = ( 2 * zoom) + pos[1]
    minx = (-2 * zoom) + pos[0]
    maxx = ( 2 * zoom) + pos[0]
    res = (maxx - minx) / winw
    os.system('clear')
    print("Pos  : {},{}".format(pos[0], pos[1]))
    print("Res  : {}".format(res))
    print("Zoom : {}".format(zoom))
    print("X    : {} - {}".format(minx, maxx))
    print("Y    : {} - {}".format(miny, maxy))
    for y in numpy.arange(miny, maxy, 3*res): # terminal chars are roughly 3 times higher than they are wide, YMMV
        for x in numpy.arange(minx, maxx, res):
            n = stability((x, y))
            clr = int(((n/iterations) * 120) + 110)
            print(' ' if n==iterations else "\x1b[38;5;{}m{}".format(clr, '*'), end='')
        print('\x1b[0m')

def on_press(k):
    global posx, posy, zoom
    try:
        if(k == Key.esc):
            return False
        elif(k.char == 'a'):
            posx = posx + 2 * zoom * 0.1
        elif(k.char == 'd'):
            posx = posx - 2 * zoom * 0.1
        elif(k.char == 's'):
            posy = posy - 2 * zoom * 0.1
        elif(k.char == 'w'):
            posy = posy + 2 * zoom * 0.1
        elif(k.char == 'q'):
            zoom = zoom * 0.9
        elif(k.char == 'e'):
            zoom = zoom * 1.1
    except Exception as e:
        pass
    draw((posx,posy), zoom)


draw((posx, posy), zoom)
with Listener(on_press=on_press) as listener:
    listener.join()
