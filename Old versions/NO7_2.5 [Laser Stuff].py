from __future__ import division
import pygame, sys, time, random, os, pickle
from pygame.locals import *

# -------------- Functions and Classes -------------- 

def distance(speed, time):
    distance = time * speed
    return distance

class GameObject(object):
    def __init__(self, position, image, rect): #self, list, pygame loaded image, pygame rectangle
        self.position = position
        self.image = image
        self.rect = rect
    def render(self):
        windowSurface.blit(self.image, (self.position[0], self.position[1]))
    def collision(self, otherRect):
        if self.rect.colliderect(otherRect) == True:
            return True
        elif self.rect.colliderect(otherRect) != True:
            return False

class Enemy(GameObject):
    def __init__(self, name, health, position, image, rect, speed):
        self.name = name
        self.position = position
        self.image = image
        self.health = health
        self.rect = rect
        self.speed = speed
        super(Enemy, self).__init__(self.position, self.image, self.rect)
    def renderHealth(self):
        try:
            pygame.draw.rect(windowSurface, ((100 - self.health) * 2.55, self.health * 2.55, 0), (self.position[0], self.position[1] + 27 * 5, self.health * 1.05, 10))
        except TypeError:
            pygame.draw.rect(windowSurface, RED, (self.position[0], self.position[1] + 27 * 5, self.health * 1.05, 10))

def backgroundScrolling():
    background1.position[1] = background1.position[1] + distance(1, frameTime)
    background2.position[1] = background2.position[1] + distance(1, frameTime)
    if background1.position[1] > 900:
        background1.position[1] = 0
        background2.position[1] = -900
    
    background1.render()
    background2.render()


#-------------- Constants and Variables --------------

"""Colors"""
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 200, 0)

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (700,40)

showDebug = False

"""Initiate pygame and set up quick access variable"""
pygame.init()
mainClock = pygame.time.Clock()
basicFont = pygame.font.SysFont(None, 23)

"""Constants"""
WINDOWWIDTH = 600
WINDOWHEIGHT = 900

PLAYERWIDTH = 21
PLAYERHEIGHT = 27

SHOOTDELAY = 100
BULLETSPEED = 1.7

"""Other variables"""
playerX = WINDOWWIDTH / 2

windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0)

laserList = []
enemyList = []

lastShotTime = pygame.time.get_ticks()
lastSpawn = pygame.time.get_ticks()

loopTrack = 0

heat = 0
overheat = False
collidingEnemies = None
lives = 3
difficulty = 15

backgroundImg = pygame.image.load('background.png')
background1 = GameObject([0, 0], backgroundImg, None)
background2 = GameObject([0, -900], backgroundImg, None)

# -------------- Image and Music Loading --------------

playerImage = pygame.image.load('Player_ship.png')
playerStretchedImage = pygame.transform.scale(playerImage, (PLAYERWIDTH * 4, PLAYERHEIGHT * 4))
playerImageLeft = pygame.image.load('shipLeft.png')
playerStretchedImageLeft = pygame.transform.scale(playerImageLeft, (PLAYERWIDTH * 4, PLAYERHEIGHT * 4))
playerImageRight = pygame.image.load('shipRight.png')
playerStretchedImageRight = pygame.transform.scale(playerImageRight, (PLAYERWIDTH * 4, PLAYERHEIGHT * 4))

laserImage = pygame.image.load('lasers.png')
laserStretchedImage = pygame.transform.scale(laserImage, (1 * 4, 3 * 4))

enemyImage = pygame.image.load('Enemy_Ship.png')
enemyStretchedImage = pygame.transform.scale(enemyImage, (21 * 5, 27 * 5))

lifeImage = pygame.image.load('life.png')
lifeImage = pygame.transform.scale(lifeImage, (18 * 3, 18 * 3))

heatSurface = pygame.Surface((600, 900))
heatSurface.fill((255, 0, 0))

# -------------- Game Loop -------------- 
while True:
    # -------- Update loop specific variables --------
    loopTrack = loopTrack + 1
    frameTime = mainClock.tick(1000)
    currentTime = pygame.time.get_ticks()
    mousePosition = pygame.mouse.get_pos()

    # -------- Background --------
    backgroundScrolling()

    # -------- Render Lives --------
    for i in range(0, lives + 1):
        windowSurface.blit(lifeImage, (WINDOWWIDTH - 18 * 3 * i, WINDOWHEIGHT - 18 * 3))

    # -------- Movement -------- 
    mouseX = pygame.mouse.get_pos()[0] - PLAYERWIDTH * 2
    if playerX != pygame.mouse.get_pos()[0] - PLAYERWIDTH * 2:
        if int(playerX) > int(pygame.mouse.get_pos()[0] - PLAYERWIDTH * 2):
            playerX = playerX - distance(1, frameTime)
            #windowSurface.blit(playerStretchedImageLeft, (playerX, 770))
        elif int(playerX) < int(pygame.mouse.get_pos()[0] - PLAYERWIDTH * 2):
            playerX = playerX + distance(1, frameTime)
            #windowSurface.blit(playerStretchedImageRight, (playerX, 770))
    else:
        windowSurface.blit(playerStretchedImage, (playerX, 770))
    windowSurface.blit(playerStretchedImage, (playerX, 770))

    # -------- Enemies --------
    """Keep list filled with enemies and check for overlapping enemies"""
    if difficulty < 7:
        difficulty = 7
    if currentTime - lastSpawn >= 100 * difficulty:
        lastSpawn = pygame.time.get_ticks()
        randomX = random.randint(0, WINDOWWIDTH - 21 * 5)
        randomY = random.randint(-700, -300)
        enemyList.append(Enemy(loopTrack, 100, [randomX, randomY], enemyStretchedImage, pygame.Rect(randomX, randomY, 21 * 5, 27 * 5), random.randint(1, 4) / 10))
        for enemy in enemyList:
            if enemy.name == loopTrack:
                continue
            elif enemy.rect.colliderect(pygame.Rect(randomX, randomY, 21 * 5, 27 * 5)):
                removed = True
                enemyList.remove(enemy)

    """For loop with objects in EnemyList"""
    for enemy in enemyList:
        if enemy.health <= 0:
            enemyList.remove(enemy)
            difficulty = difficulty / 1.01
        if enemy.position[1] > 910:
            enemyList.remove(enemy)
            lives = lives - 1
        enemy.position[1] = enemy.position[1] + distance(enemy.speed, frameTime)
        enemy.rect = pygame.Rect(enemy.position[0], enemy.position[1], 21 * 5, 27 * 5) #while loop
        enemy.render()
        enemy.renderHealth()

    # -------- Shooting Conditions and Overheating -------- 
    if currentTime - lastShotTime >= SHOOTDELAY  and (pygame.mouse.get_pressed()[0] == True or pygame.key.get_pressed()[32] == True):
        if overheat == False:
            laserList.append(GameObject([int(playerX) + 4, 826], laserStretchedImage, pygame.Rect(int(playerX), 826, 4, 3 * 4)))
            laserList.append(GameObject([int(playerX) + PLAYERWIDTH * 4 - 8, 826], laserStretchedImage, pygame.Rect(int(playerX), 826, 4, 3 * 4)))
            lastShotTime = pygame.time.get_ticks()
            heat = heat + 5
    if pygame.time.get_ticks() - lastShotTime >= 10:
        heat = heat - 0.1

    if heat <= 0:
        heat = 0
        #overheat = False                       #< Cheat mode!
    elif heat > 100:
        heat = 100
        #overheat = True                        #< Cheat mode!

    if overheat == False:
        pygame.draw.rect(windowSurface, (heat * 2.55, (100 - heat) * 2.55, 0), (playerX, 880, heat * 0.84, 10))
    elif overheat == True:
        pygame.draw.rect(windowSurface, (255, 0, 0), (playerX, 880, heat * 0.84, 10))

    if True:
        heatSurface.set_alpha(heat * 2 - 100)
        windowSurface.blit(heatSurface, (0, 0))

    # -------- Laser (Rendering & Collision) -------- 
    for laser in laserList:
        laser.rect = pygame.Rect(laser.position[0], laser.position[1], 4, 3 * 4)
        for enemy in enemyList:
            if laser.collision(enemy.rect) == True:
                enemy.health = enemy.health - 10
                enemy.speed = enemy.speed / 1.05
                try:
                    laserList.remove(laser)
                except ValueError:
                    pass
            elif laser.collision(enemy.rect) == False:
                hasHit = False
        try:
            laser.render()
            laser.position[1] = laser.position[1] - int(distance(1.7, frameTime))
            if laser.position[1] < -10:
                laserList.remove(laser)
        except:
            pass

    # -------- Debug text -------- 
    if showDebug == True:
        try:
            debug = enemyList[0].speed
        except:
            debug = "Loading"
        debugText = basicFont.render(str(debug), True, YELLOW) #text | antialiasing | color
        windowSurface.blit(debugText, (1, 1))

    # -------- Debugging --------
    """
    for laser in laserList:
        pygame.draw.rect(windowSurface, RED, laser.rect)
    for enemy in enemyList:
        pygame.draw.rect(windowSurface, GREEN, enemy.rect)
    """
    # -------- Events -------- 
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == KEYUP:
            if event.key == 284:
                showDebug = not showDebug
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
