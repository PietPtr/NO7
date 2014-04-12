"""
Made by Pietdagamer
Art by Mark Allen
Music by Jasdoge (https://soundcloud.com/jasx)
"""

from __future__ import division
import pygame, sys, time, random, os, pickle
from pygame.locals import *

# -------------- Functions and Classes -------------- 

def restart():
    global playerX
    global laserList
    global enemyList
    global lastShotTime
    global lastCoolTime
    global lastSpawn
    global loopTrack
    global heat
    global overheat
    global collidingEnemies
    global lives
    global difficulty
    global score
    global showDebug
    global clicked
    playerX = 300
    laserList = []
    enemyList = []
    lastShotTime = pygame.time.get_ticks()
    lastCoolTime = pygame.time.get_ticks()
    lastSpawn = pygame.time.get_ticks()
    loopTrack = 0
    heat = 0
    overheat = False
    collidingEnemies = None
    lives = 3
    difficulty = 18
    score = 0
    showDebug = False
    clicked = False

def changeGameState(newState):
    global GameState
    restart()
    GameState = newState

def distance(speed, time):
    distance = time * speed
    return distance

def loadOptions():
    try:
        options = pickle.load(open("options.txt", "rb"))
    except IOError:
        options = [1.01, True]
        pickle.dump(options, open("options.txt", "wb"))
    return options

def saveOptions(options):
    try:
        pickle.dump(options, open("options.txt", "wb"))
        return True
    except:
        return False

def loadScores():
    try:
        scores = pickle.load(open("highscores.txt", "rb"))
    except IOError:
        scores = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        pickle.dump(scores, open("highscores.txt", "wb"))
    return scores

def saveScores(scores):
    try:
        pickle.dump(scores, open("highscores.txt", "wb"))
        return True
    except:
        return False

def musicText():
    global options
    if options[1] == True:
        return "ON"
    elif options[1] == False:
        return "OFF"

def changeMusic():
    options[1] = not options[1]
    saveOptions(options)
    return options

def difficultyText():
    global options
    if options[0] == 1.005:
        return "EASY"
    elif options[0] == 1.01:
        return "MEDIUM"
    elif options[0] == 1.03:
        return "HARD"

def changeDifficulty():
    if options[0] == 1.005:
        options[0] = 1.01
    elif options[0] == 1.01:
        options[0] = 1.03
    elif options[0] == 1.03:
        options[0] = 1.005
    saveOptions(options)
    return options

def backgroundScrolling():
    background1.position[1] = background1.position[1] + distance(1, frameTime)
    background2.position[1] = background2.position[1] + distance(1, frameTime)
    if background1.position[1] > 900:
        background1.position[1] = 0
        background2.position[1] = -900
    
    background1.render()
    background2.render()

def quitgame():
    pygame.quit()
    sys.exit()

def music(song):
    global musicStarted
    global options
    if musicStarted == False and options[1] == True:
        pygame.mixer.music.load(song + ".mp3")
        pygame.mixer.music.play(-1, 0.0)
        musicStarted = True
    if options[1] == False:
        pygame.mixer.music.stop()

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
    def __init__(self, position, text, function):   #position list [0, 0], list of two images: regular and hovering, boolean
        self.position = position
        self.text = text
        self.function = function
        self.image = [pygame.image.load('button.png'), pygame.image.load('buttonH.png')]
        self.hovering = False
    def doTasks(self):                              #Render button, check for hovering mouse and check for clicks
        global clicked
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

        if self.hovering == True and clicked == True:
            clicked = False
            self.function()
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
YELLOW = (100, 100, 100)

"""Constants"""
WINDOWWIDTH = 600
WINDOWHEIGHT = 900

PLAYERWIDTH = 21
PLAYERHEIGHT = 27

SHOOTDELAY = 100
BULLETSPEED = 1.7

EXPLODERESIZE = 5

"""Initiate pygame and set up quick access variable"""
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (700,40)

pygame.init()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0)
mainClock = pygame.time.Clock()
smallFont = pygame.font.SysFont("Impact", 22)
bigFont = pygame.font.SysFont("Impact", 44)

"""Other variables"""
restart()
musicStarted = False

options = loadOptions()
scores = loadScores()

""""Game States"""
GAMEMENU  =  0
GAMEPLAY  =  1
GAMEOVER  =  2
OPTIONS   =  3
HIGHSCORE =  4
GameState =  GAMEMENU

"""Objects"""
startButton = Button([200, 300], "START", lambda:changeGameState(GAMEPLAY))
optionButton = Button([200, 405], "OPTIONS", lambda:changeGameState(OPTIONS))
highScoreButton = Button([200, 510], "TOPSCORE", lambda:changeGameState(HIGHSCORE))

menuButton = Button([200, 510], "MENU", lambda:changeGameState(GAMEMENU))
quitButton = Button([200, 615], "QUIT", lambda:quitgame())
retryButton = Button([200, 405], "RETRY", lambda:changeGameState(GAMEPLAY))

backButton = Button([200, 615], "BACK", lambda:changeGameState(GAMEMENU))
musicButton = Button([200, 300], musicText(), lambda:changeMusic())
difficultyButton = Button([200, 405], difficultyText(), lambda:changeDifficulty())

backgroundImg = pygame.image.load('background.png')
background1 = GameObject([0, 0], backgroundImg, None)
background2 = GameObject([0, -900], backgroundImg, None)

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

logo = pygame.image.load('logo.png')

gameOverIMG = pygame.image.load('GameOver.png')

"""Overlay"""
heatSurface = pygame.Surface((600, 900))
heatSurface.fill((255, 0, 0))

"""Animation lists"""
explosionList = [pygame.transform.scale(pygame.image.load('explosion0.png'), (21 * EXPLODERESIZE, 21 * EXPLODERESIZE)),
                 pygame.transform.scale(pygame.image.load('explosion1.png'), (21 * EXPLODERESIZE, 21 * EXPLODERESIZE)),
                 pygame.transform.scale(pygame.image.load('explosion2.png'), (21 * EXPLODERESIZE, 21 * EXPLODERESIZE)),
                 pygame.transform.scale(pygame.image.load('explosion3.png'), (21 * EXPLODERESIZE, 21 * EXPLODERESIZE)),
                 pygame.transform.scale(pygame.image.load('explosion4.png'), (21 * EXPLODERESIZE, 21 * EXPLODERESIZE)),
                 pygame.transform.scale(pygame.image.load('explosion5.png'), (21 * EXPLODERESIZE, 21 * EXPLODERESIZE)),
                 pygame.transform.scale(pygame.image.load('explosion6.png'), (21 * EXPLODERESIZE, 21 * EXPLODERESIZE)),
                 pygame.transform.scale(pygame.image.load('explosion7.png'), (21 * EXPLODERESIZE, 21 * EXPLODERESIZE)),
                 pygame.transform.scale(pygame.image.load('explosion8.png'), (21 * EXPLODERESIZE, 21 * EXPLODERESIZE)),]

animationObjects = []

laserSound = pygame.mixer.Sound('shot.wav')

# -------------- Game Loop -------------- 
while True:
    
    # -------- Run first outside Gamestate system --------
    """Update loop specific variables"""
    loopTrack = loopTrack + 1
    frameTime = mainClock.tick(1000)
    FPS = mainClock.get_fps()
    currentTime = pygame.time.get_ticks()
    mousePosition = pygame.mouse.get_pos()
    
    """Background"""
    backgroundScrolling()

    """Events"""
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                clicked = True
        if event.type == KEYUP:
            if event.key == 284:
                showDebug = not showDebug
        if event.type == QUIT:
            quitgame()


    # -------- Game state specific --------
    """Menu with a start button"""
    if GameState == GAMEMENU:
        music("launchpad")
        
        windowSurface.blit(logo, (200, 150))
        
        quitButton.doTasks()
        if startButton.doTasks() == True:
            musicStarted = False
        optionButton.doTasks()
        highScoreButton.doTasks()

    """Display 10 highest scores"""
    if GameState == HIGHSCORE:
        windowSurface.blit(logo, (200, 150))
        
        backButton.doTasks()
        
        for i in range (1, 11):
            HighScoreText = smallFont.render(str(i) + '. ' + str(scores[len(scores) - i]), True, YELLOW)
            windowSurface.blit(HighScoreText, (270, 240 + (30 * i)))

    """Options"""
    if GameState == OPTIONS:
        music("launchpad")
        windowSurface.blit(logo, (200, 150))

        musicOptionText = bigFont.render("MUSIC", False, YELLOW)
        difficultyOptionText = bigFont.render("DIFFICULTY", False, YELLOW)
        windowSurface.blit(musicOptionText, (200 - musicOptionText.get_size()[0], 300 + (50 - (musicOptionText.get_size()[1] / 2))))
        windowSurface.blit(difficultyOptionText, (200 - difficultyOptionText.get_size()[0], 405 + (50 - (difficultyOptionText.get_size()[1] / 2))))

        musicButton.text = musicText()
        musicButton.doTasks()
        difficultyButton.text = difficultyText()
        difficultyButton.doTasks()
        backButton.doTasks()
        
    """Moving, shooting, enemies etc"""
    if GameState == GAMEPLAY:
        music("ToTheMoon")
        # -------- Render Lives --------
        for i in range(0, lives + 1):
            windowSurface.blit(lifeImage, (WINDOWWIDTH - 18 * 3 * i, WINDOWHEIGHT - 18 * 3))

        # -------- Movement -------- 
        mouseX = pygame.mouse.get_pos()[0] - PLAYERWIDTH * 2
        if playerX != pygame.mouse.get_pos()[0] - PLAYERWIDTH * 2:
            if int(playerX) > int(pygame.mouse.get_pos()[0] - PLAYERWIDTH * 2):
                playerX = playerX - distance(1, frameTime)
            elif int(playerX) < int(pygame.mouse.get_pos()[0] - PLAYERWIDTH * 2):
                playerX = playerX + distance(1, frameTime)
        else:
            windowSurface.blit(playerStretchedImage, (playerX, 770))
        windowSurface.blit(playerStretchedImage, (playerX, 770))

        # -------- Enemies --------
        """Keep list filled with enemies and check for overlapping enemies"""
        if difficulty < 7:
            difficulty = 7
        if currentTime - lastSpawn >= 1100:
            lastSpawn = pygame.time.get_ticks()
            randomX = random.randint(0, WINDOWWIDTH - 21 * 5)
            randomY = random.randint(-700, -300)
            enemyList.append(Enemy(loopTrack, 100, [randomX, randomY], enemyStretchedImage, pygame.Rect(randomX, randomY, 21 * 5, 27 * 5), random.choice([4, 5, 6, 7, 10]) / difficulty))
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
                difficulty = difficulty / 1.005
                score = score + 1
            if enemy.position[1] > 910:
                enemyList.remove(enemy)
                lives = lives - 1
            if enemy.speed > 0.6:
                enemy.speed = 0.6
            if enemy.speed < 0.1:
                enemy.speed = 0.1
            enemy.position[1] = enemy.position[1] + distance(enemy.speed, frameTime)
            enemy.rect = pygame.Rect(enemy.position[0], enemy.position[1], 21 * 5, 27 * 5)
            enemy.render()
            enemy.renderHealth()

        # -------- Shooting Conditions and Overheating -------- 
        if currentTime - lastShotTime >= SHOOTDELAY  and (pygame.mouse.get_pressed()[0] == True or pygame.key.get_pressed()[32] == True):
            if overheat == False:
                if options[1] == True:
                    laserSound.play()
                laserList.append(GameObject([int(playerX) + 4, 826], laserStretchedImage, pygame.Rect(int(playerX), 826, 4, 3 * 4)))
                laserList.append(GameObject([int(playerX) + PLAYERWIDTH * 4 - 8, 826], laserStretchedImage, pygame.Rect(int(playerX), 826, 4, 3 * 4)))
                lastShotTime = pygame.time.get_ticks()
                heat = heat + (frameTime * (FPS / 80))
        if pygame.time.get_ticks() - lastCoolTime >= 10:
            heat = heat - (frameTime * (FPS / 1000))
            lastCoolTime = pygame.time.get_ticks()

        if heat <= 0:
            heat = 0
            overheat = False                       #< Cheat mode!
        elif heat > 100:
            heat = 100
            overheat = True                        #< Cheat mode!

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
                    halfexplosion = int(21 * EXPLODERESIZE / 2)
                    animationObjects.append(Animation(explosionList, 30, pygame.time.get_ticks(), 0, [random.randint(int(enemy.position[0]) - halfexplosion, int(enemy.position[0]) + 21 * 5), int(enemy.position[1]) + random.randint(0, 27 * 5) - halfexplosion]))
                elif laser.collision(enemy.rect) == False:
                    hasHit = False
            try:
                laser.render()
                laser.position[1] = laser.position[1] - int(distance(1.7, frameTime))
                if laser.position[1] < -10:
                    laserList.remove(laser)
            except:
                pass
            
        # -------- Check Death --------
        if lives <= 0:
            lives = 0
            GameState = GAMEOVER
            
            scores.append(score)
            scores = sorted(scores)

            saveScores(scores)
        # -------- Debugging --------
        """
        for laser in laserList:
            pygame.draw.rect(windowSurface, RED, laser.rect)
        for enemy in enemyList:
            pygame.draw.rect(windowSurface, GREEN, enemy.rect)
        """

        """Simulate slower computers:"""
        """
        for i in range(0, 5):
            print i
        """

    """Gameover Screen with try again button"""
    if GameState == GAMEOVER:
        # -------- Enemies finish their track --------
        for enemy in enemyList:
            enemy.position[1] = enemy.position[1] + distance(enemy.speed, frameTime)
            enemy.rect = pygame.Rect(enemy.position[0], enemy.position[1], 21 * 5, 27 * 5)
            enemy.render()
            enemy.renderHealth()

        # -------- Blitting GameOver images etc --------
        windowSurface.blit(gameOverIMG, (WINDOWWIDTH / 2 - 100, 200))

        scoreText = bigFont.render("Score: " + str(score), False, YELLOW)
        scoreTextSize = scoreText.get_size()
        windowSurface.blit(scoreText, ((WINDOWWIDTH / 2) - (scoreTextSize[0] / 2), 350))

        # -------- Handle Buttons --------
        retryButton.doTasks()
        quitButton.doTasks()
        if menuButton.doTasks() == True:
            musicStarted = False

    # -------- Debug text -------- 
    if showDebug == True:
        try:
            debug = FPS
        except:
            debug = "Loading"
        debugText = smallFont.render(str(debug), False, YELLOW) #text | antialiasing | color
        windowSurface.blit(debugText, (1, 1))

    # -------- Run last outside GameState system --------
    """"reset variables"""
    clicked = False
    
    """Handle Animations"""
    for animation in animationObjects:
        if animation.render() == 1:
            animationObjects.remove(animation)
    
    """Update display"""
    pygame.display.update()
