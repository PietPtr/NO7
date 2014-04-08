from __future__ import division
import pygame, sys, time, random, os, pickle
from pygame.locals import *

# -------------- Functions and Classes -------------- 

def quitgame():
    pygame.quit()
    sys.exit()

def distance(speed, time):
    distance = time * speed
    return distance

def backgroundScrolling():
    background1.position[1] = background1.position[1] + distance(1, frameTime)
    background2.position[1] = background2.position[1] + distance(1, frameTime)
    if background1.position[1] > 900:
        background1.position[1] = 0
        background2.position[1] = -900
    
    background1.render()
    background2.render()

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

class Button(object):
    def __init__(self, position, text): #position list [0, 0], list of two images: regular and hovering, boolean
        self.position = position
        self.text = text
        self.image = [pygame.image.load('button.png'), pygame.image.load('buttonH.png')]
        self.hovering = False
    def doTasks(self, button): #Render button, check for hovering mouse and check for clicks
        if self.hovering == False:
            windowSurface.blit(self.image[0], (self.position[0], self.position[1]))
        elif self.hovering == True:
            windowSurface.blit(self.image[1], (self.position[0], self.position[1]))
        buttonText = bigFont.render(str(self.text), False, YELLOW)
        buttonTextSize = buttonText.get_size()
        windowSurface.blit(buttonText, (self.position[0] + (100 - (buttonTextSize[0] / 2)), self.position[1] + (50 - (buttonTextSize[1] / 2))))
        
        if mousePosition[0] > self.position[0] and mousePosition[0] < self.position[0] + 200 and mousePosition[1] > self.position[1] and mousePosition[1] < self.position[1] + 100: #Button is 200x100 px
            self.hovering = True
        else:
            self.hovering = False
        
        if self.hovering == True and pygame.mouse.get_pressed()[button]:
            return True
        else:
            return False

class Animation(object):
    def __init__(self, frameList, frameTime, lastFrameTime, currentFrame, position): #list with pictures, time in ms between frames, time the last frame was displayed, current list index, list
        self.frameList = frameList
        self.frameTime = frameTime
        self.lastFrameTime = lastFrameTime
        self.currentFrame = currentFrame
        self.position = position
    def render(self):
        if pygame.time.get_ticks() - self.lastFrameTime >= self.frameTime:
            self.currentFrame = self.currentFrame + 1
            self.lastFrameTime = pygame.time.get_ticks()
        try:
            windowSurface.blit(self.frameList[self.currentFrame], (self.position[0], self.position[1]))
        except IndexError:
            return 1
        return 0

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
smallFont = pygame.font.SysFont("Impact", 22)
bigFont = pygame.font.SysFont("Impact", 50)

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
score = 0

backgroundImg = pygame.image.load('background.png')
background1 = GameObject([0, 0], backgroundImg, None)
background2 = GameObject([0, -900], backgroundImg, None)

""""Game States"""
STARTGAME = 0
GAMEPLAY = 1
GAMEOVER = 2
GameState = GAMEPLAY

"""Button objects"""
#blStartGame = 
quitButton = Button([200, 600], "QUIT")
retryButton = Button([200, 705], "RETRY")

# -------------- Image and Music Loading --------------

"""Sprites"""
playerImage = pygame.image.load('Player_ship.png')
playerStretchedImage = pygame.transform.scale(playerImage, (PLAYERWIDTH * 4, PLAYERHEIGHT * 4))

laserImage = pygame.image.load('lasers.png')
laserStretchedImage = pygame.transform.scale(laserImage, (1 * 4, 3 * 4))

enemyImage = pygame.image.load('Enemy_Ship.png')
enemyStretchedImage = pygame.transform.scale(enemyImage, (21 * 5, 27 * 5))

lifeImage = pygame.image.load('life.png')
lifeImage = pygame.transform.scale(lifeImage, (18 * 3, 18 * 3))

gameOverIMG = pygame.image.load('GameOver.png')

"""Overlay"""
heatSurface = pygame.Surface((600, 900))
heatSurface.fill((255, 0, 0))

"""Animation lists"""
explosionList = [pygame.transform.scale(pygame.image.load('explosion0.png'), (21 * 4, 21 * 4)),
                 pygame.transform.scale(pygame.image.load('explosion1.png'), (21 * 4, 21 * 4)),
                 pygame.transform.scale(pygame.image.load('explosion2.png'), (21 * 4, 21 * 4)),
                 pygame.transform.scale(pygame.image.load('explosion3.png'), (21 * 4, 21 * 4)),
                 pygame.transform.scale(pygame.image.load('explosion4.png'), (21 * 4, 21 * 4)),
                 pygame.transform.scale(pygame.image.load('explosion5.png'), (21 * 4, 21 * 4)),
                 pygame.transform.scale(pygame.image.load('explosion6.png'), (21 * 4, 21 * 4))]

animationObjects = []

# -------------- Game Loop -------------- 
while True:
    
    # -------- Run first outside Gamestate system --------
    """Update loop specific variables"""
    loopTrack = loopTrack + 1
    frameTime = mainClock.tick(1000)
    currentTime = pygame.time.get_ticks()
    mousePosition = pygame.mouse.get_pos()
    
    """Background"""
    backgroundScrolling()

    # -------- Game state specific --------
    """Menu with a start button"""
    if GameState == STARTGAME:
        pass

    """Moving, shooting, enemies etc"""
    if GameState == GAMEPLAY:
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
                score = score + 1
            if enemy.position[1] > 910:
                enemyList.remove(enemy)
                lives = lives - 1
                difficulty = 10 + (1.6 * lives)
            enemy.position[1] = enemy.position[1] + distance(enemy.speed, frameTime)
            enemy.rect = pygame.Rect(enemy.position[0], enemy.position[1], 21 * 5, 27 * 5)
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
                    animationObjects.append(Animation(explosionList, 30, pygame.time.get_ticks(), 0, [int(enemy.position[0]) + 11, int(enemy.position[1])]))
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
            debugText = smallFont.render(str(debug), False, YELLOW) #text | antialiasing | color
            windowSurface.blit(debugText, (1, 1))

        # -------- Check Death --------
        if lives <= 0:
            lives = 0
            GameState = GAMEOVER

        # -------- Debugging --------
        """
        for laser in laserList:
            pygame.draw.rect(windowSurface, RED, laser.rect)
        for enemy in enemyList:
            pygame.draw.rect(windowSurface, GREEN, enemy.rect)
        """

    # -------- Run if the player has <0 lives left --------
    """Gameover Screen with try again button"""
    if GameState == GAMEOVER:
        # -------- Enemies finish their track --------
        for enemy in enemyList:
            enemy.position[1] = enemy.position[1] + distance(enemy.speed, frameTime)
            enemy.rect = pygame.Rect(enemy.position[0], enemy.position[1], 21 * 5, 27 * 5)
            enemy.render()
            enemy.renderHealth()

        # -------- Blitting GameOver images etc --------
        windowSurface.blit(gameOverIMG, (WINDOWWIDTH / 2 - 100, WINDOWHEIGHT / 3.5))

        scoreText = bigFont.render("Score: " + str(score), False, YELLOW)
        scoreTextSize = scoreText.get_size()
        windowSurface.blit(scoreText, ((WINDOWWIDTH / 2) - (scoreTextSize[0] / 2), 460))

        # -------- Handle Buttons --------
        if retryButton.doTasks(0) == True:
            GameState = GAMEPLAY
        if quitButton.doTasks(0) == True:
            quitgame()

    # -------- Run last outside GameState system --------
    """Handle Animations"""
    for animation in animationObjects:
        if animation.render() == 1:
            animationObjects.remove(animation)
    
    """Update display"""
    pygame.display.update()

    """Events"""
    for event in pygame.event.get():
        if event.type == KEYUP:
            if event.key == 284:
                showDebug = not showDebug
        if event.type == QUIT:
            quitgame()
