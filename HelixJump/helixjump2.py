import pygame as pg, pygame
from time import sleep
import copy
from random import randint, randrange, choice
from os import system
import sys
import msvcrt as ms
from threading import Thread
import math

#colors
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
bgColor = (0, 116, 217)
orange = (228, 106, 107)
invincibleColor = (0,206,209)

#vars

GAME_TITLE = "Arcade Jump"
VERSION = "[BETA]"

won = False

FPS = 75

SLOWMOTION_PERIOD = 105
NORMAL_PERIOD = 55
UPDATE_PERIOD = NORMAL_PERIOD #increasing this would induce slow motion

w = 1400
h = 800

ballOffset = 50
res = (w, h)
pygame.init()
clock = pygame.time.Clock()
rotationSpeed = -50  #negative = clockwise
friction = 2
currentAngle = 0

obs = '@'
surface = "#"

view = 0

block_size = (5, 20) #pixels
ball_size = (30, 30) #has to be square

size = res[0] // block_size[0]
acc = 1500 #pixels per second squared downwards taken positive

pos = [size/2, 0]
vel = 0
currentDisc = 0
game_complete = False

gap = 150 #pixels b/w 2 consecutive discs
max_vel = math.sqrt(2 * (gap - 20) * acc) - 50

move_view_speed = int(max_vel / 3)

level_len = 20 #number of discs total (including blanks)

pre = ball_size[0] // block_size[0] * 3
hole_sizes = [pre, pre+1, pre+2, pre+3]

pre *= 1.5
pre = int(pre)
obs_sizes = [pre+1, pre+3, pre+4, pre+5]
powerup_sizes = obs_sizes

discs = [] #main game array
disc_positions = []


#init stuff
disp = pygame.display.set_mode(res)

pygame.display.set_caption(GAME_TITLE+VERSION)

disp.fill(bgColor)

running = True

viewMoverThreads = []
popperThreads = []

powerups = []
icons = []

viewMoved = 0

multiplier = 1
bounces = 1 #bounces since crossing last disc

scorePerBounce = 20
score = 0
score_string = str(score)
disp_added = None
added = 0


trail = []  #experimental


def genscorestring():
    global score
    global score_string
    global added

    score_string="Score: {}  ".format(score)
    if added != None:
        score_string += " +{}".format(added)

#Classes


class images:
    pass


class fonts:
    score = "resources/6809 chargen.ttf"
    winorlose = "resources/ARCADECLASSIC.ttf"


class Ball:
    global acc
    global w
    def __init__(self):
        self.x = w/2
        self.y = ballOffset
        self.v = 0
        self.vx = 0
        self.a = acc


class origImages:
    pass


class Powerup:
    """ duration: Time for which this powerup will be active
        chance: chance that this will be found on a disc. Out of hundred (%age)"""
    global powerups

    def __init__(self, icon, duration, chance, block):
        self.active = False
        self.icon = icon
        self.blockImage = block #an image reference
        self.duration = duration
        self.chance = chance
        self.range = list(range(chance))

        powerups.append(self)

        self.threadlist = []

    def start(self):
        self.threadlist.append(Thread(target=self.timeout, args=()))
        self.threadlist[-1].start()
        print("EVENT: POWERUP_BEGUN")

    def timeout(self):
        self.active = True
        sleep(self.duration)
        self.active = False


class Powerups:
    pass

#functions

def initpowerups():
    Powerups.invincible = Powerup("&",2,9,images.invincible)
    Powerups.slowmotion = Powerup("$",6,14,images.slowmotion)

    global icons
    for powerup in powerups:
        icons.append(powerup.icon)


def loadImages():
    global block_size
    global ball_size
    global disp

    blockImage = pygame.image.load("resources/block.png")
    blockImage = pygame.transform.scale(blockImage, block_size)
    images.block = blockImage

    ballImage = pygame.image.load("resources/ball.png")
    ballImage = pygame.transform.scale(ballImage,ball_size)
    images.ball = ballImage
    origImages.ball = ballImage

    obsImage=pygame.image.load("resources/obs.png")
    obsImage=pygame.transform.scale(obsImage,block_size)
    images.obs=obsImage

    #They use the same variable to load because your boi samarth is lazy.
    blockImage=pygame.image.load("resources/invincible.png")
    blockImage=pygame.transform.scale(blockImage,block_size)
    images.invincible=blockImage

    blockImage=pygame.image.load("resources/slowmotion.png")
    blockImage=pygame.transform.scale(blockImage,block_size)
    images.slowmotion=blockImage


def removeAdded(delay):
    "Removes the 'added' portion of the score string after sometime"
    global disp_added
    global added

    while 1:
        if not added is None:
            sleep(delay)
            disp_added = None
        sleep(1)


addedRemoverThread = Thread(target=removeAdded, args=(2,))
addedRemoverThread.start()


def cap(x, u, l):
    if x < l:
        return l
    elif x > u:
        return u
    else:
        return x


def addObstacles():
    global discs
    global obs_sizes
    global size
    global obs

    for each in discs:
        n=choice([1,2])
        for i in range(n):
            obsize = choice(obs_sizes)
            start = randrange(0, size)
            r = list(range(start, start + obsize))
            for j in range(len(each)):
                if j in r and each[j] != " ":
                    each[j] = "@"
                elif each[j] == " ":
                    r.append(r[-1] % len(r))


def addPowerups():
    global discs
    global power
    global powerup_sizes
    global size

    for powerup in powerups:
        for disc in discs:
            if randint(0, 100) in powerup.range:
                psize = choice(powerup_sizes)


                start = randint(0,size - psize - 1)
                end = start + psize

                indices = list(range(start, end))
                for index in indices:
                    if disc[index] == "#":
                        disc[index] = powerup.icon


def makeLevel():
    global discs
    global hole_sizes
    global gap
    global level_len
    global disc_positions
    global ballOffset

    pos = gap + ballOffset
    #Make discs
    for i in range(level_len):
        row=[]

        holeSize=choice(hole_sizes)

        start=randint(0,size - holeSize)

        for i in range(size):
            if not (i in range(start,start + holeSize)):
                row.append(surface)
            else:
                row.append(" ")

        discs.append(row)
        disc_positions.append(pos)
        pos += gap

    addObstacles()

    addPowerups()


def updateBall():
    global ball
    global disp
    global max_vel
    global currentDisc
    global ball_size
    global rotationSpeed
    global currentAngle
    global UPDATE_PERIOD
    global SLOWMOTION_PERIOD
    global NORMAL_PERIOD

    if Powerups.slowmotion.active:
        UPDATE_PERIOD = SLOWMOTION_PERIOD
    else:
        UPDATE_PERIOD = NORMAL_PERIOD

    delta =1 / UPDATE_PERIOD

    currentAngle += rotationSpeed * delta

    new = pygame.transform.rotate(origImages.ball, currentAngle)
    images.ball = new

    offset = 0
    if collision():
        ball.v -= 2 * ball.v

    minus = max_vel * -1

    if ball.v > max_vel:
        ball.v = max_vel

    if ball.v < minus:
        ball.v = minus

    ball.y += ball.v * delta + offset
    ball.v += ball.a * delta

    ball.x += ball.vx * delta
    disp.blit(images.ball, (ball.x, ball.y))


def weight(x):
    return abs(x // 6)


def initialize():
    "Everything required to init this game"
    loadImages()
    initpowerups()
    makeLevel()


def scroll(move):
    """this function scrolls the whole thing one unit to the right or to the left
    move is a boolean value, true means to the right"""
    global size
    global discs
    global movement

    if move:
        #move to right
        for i in range(len(discs)):
            row = discs[i]
            prev = row[-1]
            for i in range(len(row)):
                prev,row[i] = row[i], prev

    else:
        #move to left
        for i in range(len(discs)):
            row = list(reversed(discs[i]))
            prev = row[-1]
            for j in range(len(row)):
                prev, row[j] = row[j], prev
            discs[i] = list(reversed(row))


def renderDiscs():
    global discs
    global disc_positions
    global block_size
    global disp
    global currentDisc
    global view
    global obs
    global icons

    block_image = images.block
    obs_image = images.obs
    count = 0


    for powerup in powerups:
        icons.append(powerup.icon)

    for disc in discs:
        x = 0
        for block in disc:
            if block == "#":
                disp.blit(block_image, (x,disc_positions[count] + view))
            elif block == "@":
                disp.blit(obs_image, (x,disc_positions[count] + view))
            elif block != " ":
                disp.blit(powerups[icons.index(block)].blockImage,(x,disc_positions[count] + view))

            x += block_size[0]
        count += 1


def generateText(s, font, size):
    global orange

    "Generates text of the string passed as parameter"
    im = pygame.font.Font(font, size).render(s, True, orange)
    return im


def render():
    global disp
    global ball
    global view
    global bgColor
    global view
    global h
    global score_string
    global invincibleColor

    if ball.y + view > h - h/2:
        addMoverThread()
        viewMoverThreads[-1].start()
        print("EVENT: VIEW_STABILIZER INSTANTIATED")

    if isInvincible():
        disp.fill(invincibleColor)
    else:
        disp.fill(bgColor)  #Clear screen

    rect = images.ball.get_rect()
    rect.center = (ball.x, int(ball.y) + view)
    disp.blit(images.ball, rect)

    renderDiscs()

    genscorestring()

    text = generateText(score_string,fonts.score, 50)

    disp.blit(text, (0, 0))


def isInvincible():
    return Powerups.invincible.active

def addToScore():
    global bounces, added, scorePerBounce, multiplier, disp_added, score
    """Add to the score, if the player is invincible or also when he is crossing a disc"""
    if not bounces:
        multiplier+=1

    bounces=0
    added = scorePerBounce * multiplier
    disp_added = added
    score += added


def collision():
    global disc_positions
    global currentDisc
    global ball
    global block_size
    global discs
    global viewMover
    global move_view_speed
    global viewMoverThreads
    global won
    global popperThreads
    global running
    global multiplier
    global bounces
    global score
    global added
    global scorePerBounce
    global disp_added
    global rotationSpeed
    global icons

    block = block_size[0]
    prev = currentDisc
    offset = 10

    count = 0
    for each in disc_positions:
        if each - offset <= ball.y:
            count += 1
        else:
            break

    if count >= len(discs):
        won = True


    currentDisc = count
    if count > prev: #hit a disc level
        curr = discs[count - 1][int(ball.x / block) + 1]
        if  curr == " ":
            #Crossing a disc
            if not bounces:
                multiplier += 1

            bounces = 0
            added = scorePerBounce * multiplier
            disp_added = added
            score += added

            print(score)
            print(f"EVENT: DISC_{currentDisc - 1}_CROSSED")


            addMoverThread()
            viewMoverThreads[-1].start()

            print("EVENT: MOVING_VIEW\n")
            return False
        elif curr == "@":
            #Hit an obstacle
            print("EVENT: HIT OBSTACLE")
            if not isInvincible():
                running = False

            if isInvincible():
                addToScore()

            return not isInvincible()

        elif curr in icons:
            index = icons.index(curr)
            powerups[index].start()

            if isInvincible():
                addToScore()

            return not isInvincible()
        else:
            #Bounced off a disc

            #move a little because of ball's spin
            ball.vx = rotationSpeed * -1 * friction / 20

            rotationSpeed /= 2

            bounces += 1
            multiplier = 1
            added = None

            if isInvincible():
                addToScore()

            return not isInvincible()
    else:
        #Just in air
        return False


def moveView(speed):
    global gap
    global view

    orig = view
    target = orig - gap

    while view > target:
        view -= 1
        sleep(1/speed)

    sys.exit()


def popper():
    pass


def addMoverThread():
    newThread = Thread(target=moveView, args=(move_view_speed, ))
    viewMoverThreads.append(newThread)
    print("NEW_THREAD_ADDED", viewMoverThreads)


def addPopperThread():
    global popperThreads
    popperThreads.append(Thread(target=popper, args=()))


def renderText(txt):
    global w, h
    image=generateText(txt,fonts.winorlose,90)
    rect=image.get_rect()
    rect.center=(w / 2,h / 2)
    disp.blit(image,rect)
    pygame.display.update()


initialize()
ball = Ball()

print("This info is meant for debugging, as the game is still in BETA. Please ignore this info.\n")
while running and not won:
    updateBall()
    render()

    for event in pygame.event.get():
        if event == pygame.QUIT:
            running = False
        if event.type == pg.MOUSEMOTION:
            relx, rely = event.rel
            relx = cap(relx, 20, -20)

            rotationSpeed += relx * friction

            ball.x -= relx // 8
            if relx != 0:
                wei = weight(relx)
                relx += abs(relx)

                for i in range(wei + 1):
                    scroll(relx)
            if rely != 0:
                if ball.v > 0:
                    #ball.v += rely * 3
                    pass

    pygame.display.update()
    clock.tick(FPS)

if won:
    renderText("You Won!")
else:
    renderText("Not that Easy!")

sleep(3)
pygame.quit()
quit()