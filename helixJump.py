import math as m
from time import sleep
import copy
from random import randint, randrange, choice
from os import system as sys
import msvcrt as ms
from threading import Thread

#vars
skin = '@'
surface = "#"
size = 40 #horizontal size
frame_height = 40 #(lines)
a = 1 #lines per second squared downwards taken positive

pos = [size/2, 0]
vel = 0
discs_passed = 0
game_complete = False

right = ['d', 'w', 'l', 'i']
left = ['a', 's', 'j', 'k']

gap = 4 #lines b/w 2 consecutive discs
level_len = 20 #number of lines total (including blanks)

hole_sizes = [4,5,6,7,8]

main = [] #main game array
discs = []
movement = copy.deepcopy(main)

errmsg = {'invkey':"Invalid Keypress."}
def initialize():
    global main

    for i in range(level_len):
        row = []
        for j in range(size):
            row.append(" ")

        main.append(row)

    dupli()

def dupli():
    global main
    global movement

    movement = copy.deepcopy(main)

def clear():
    sys("cls")

def render():
    global movement
    global pos
    global skin

    for row in movement:
        for item in row:
            print(item, end="")
        print("\n")

def makeRow():
    global size
    global hole_sizes
    global surface
    row = []

    holeSize = choice(hole_sizes)

    start = randint(0, size - holeSize)

    for i in range(size):
        if not(i in range(start, start+holeSize)):
            row.append(surface)
        else:
            row.append(" ")

    return row

def makelevel():
    global main
    global size
    global gap
    global level_len

    for i in range(level_len):
        if (i+1) % gap == 0:
            main.append(makeRow())
            discs.append(i)
        else:
            main.append(list([" "] * size))

def scroll(move):
    """this function scrolls the whole thing one unit to the right or to the left
    move is a boolean value, true means to the right"""
    global size
    global main
    global movement

    if move:
        #move to right
        for i in range(len(main)):
            row = main[i]
            prev = row[-1]
            for i in range(len(row)):
                prev,row[i] = row[i], prev

    else:
        #move to left
        for i in range(len(main)):
            row = list(reversed(main[i]))
            prev = row[-1]
            for j in range(len(row)):
                prev, row[j] = row[j], prev
            main[i] = list(reversed(row))

def process(p):
    if p in right:
        return True
    elif p in left:
        return False
    else:
        return "INVALID_MOVE"

def updateBall():
    global a
    global movement
    global main
    global pos
    global vel
    global skin

    while True:
        dupli()
        pos[1] += vel * 1

        if onHitDisc():
            #player hit a disc, make velocity negative
            vel -= 2 * vel

        vel += a
        movement[int(pos[1])][abs(int(pos[0]))] = skin

def onHitDisc():
    global pos
    global discs_passed
    global discs #y-coordinate of the discs
    global game_complete

    prev = discs_passed
    i = 0
    while discs[i] < pos[1]:
        print(pos[1], discs[i])
        sleep(1)
        if i >= len(discs) - 1:
            game_complete = True
            clear()
            print("You won!")
            sleep(2)
            exit()

        discs_passed += 1
        i += 1

    if prev < discs_passed:
        return True

initialize()
ballUpdater = Thread(target=updateBall)

makelevel()
dupli()
render()
ballUpdater.start()
#GAME LOOP
while 1:
    if ms.kbhit():
        press = ms.getch().decode("utf-8")
        proc = process(press)
        if not(proc == "INVALID_MOVE"):
            scroll(proc)
            dupli()
            clear()
            render()
        else:
            print(errmsg['invkey'])
            sleep(1)
            clear()
            render()


input()