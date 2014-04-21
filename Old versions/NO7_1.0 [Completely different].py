"""
Made by Pietdagamer
Music by Jasdoge
"""

import pygame, sys, time, random, os, pickle
from pygame.locals import *

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (700,40)

# set up pygame
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
mainClock = pygame.time.Clock()

WINDOWWIDTH = 600
WINDOWHEIGHT = 900

windowBackground = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32) #always 0 and 32
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32) #always 0 and 32
pygame.display.set_caption('Shoot in Spyce')

#Program states: Menu, Gameplay, Dead
MENU = 1
STARTGAME = 2
GAMEPLAY = 3
DEAD = 4
OPTIONS = 5
HIGHSCORES = 6
GameState = MENU
#End states

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 201, 0)

PLAYERWIDTH = 21
PLAYERHEIGHT = 27

LASERWIDTH = 21
LASERHEIGHT = 3

ENEMYWIDTH = 180
ENEMYHEIGHT = 180

try:
    scoreList = pickle.load(open('scores.dat', 'rb'))
except IOError:
    scoreList = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    pickle.dump(scoreList, open('scores.dat', 'wb'))

try:
    options = pickle.load(open('options.dat', 'rb'))
except IOError:
    options = [True, 50]
    pickle.dump(options, open('options.daat', 'wb'))

scoreTextList = []

speed = 1
flySpeed = 0

gameOver = False

x1 = WINDOWWIDTH / 2 - ((PLAYERWIDTH * 4) / 2)
animation = 1
shot = False
turnleft = False
turnright = False
showDebug = False
generationNeeded = True
animatePlayer = True
moveRunway = False
animation = False
hoverOverYes = False
hoverOverNo = False
musicLooped = True
playmusicLooped = True
renderingToDo = True
musicOn = options[0]  #moet nog met pickle gedaan worden!
difficulty = options[1] #ook pickle. 
laserX = x1
bulletTracker = 0
frame = 0
score = 0
randX_animation = 0
enemyDist_animation = 0
playerDistance = 900 + PLAYERHEIGHT * 4
runwayDistance = 0
endScoreList = []

basicFont = pygame.font.SysFont(None, 23)

background = pygame.image.load('background.png')

player = pygame.Rect(x1, (WINDOWWIDTH / 2) - (PLAYERWIDTH / 2), x1 + PLAYERHEIGHT * 4, (WINDOWWIDTH / 2) + (PLAYERWIDTH / 2))
playerImage = pygame.image.load('Player_ship.png')
playerStretchedImage = pygame.transform.scale(playerImage, (PLAYERWIDTH * 4, PLAYERHEIGHT * 4))

playerImageLeft = pygame.image.load('shipLeft.png')
playerImageRight = pygame.image.load('shipRight.png')
playerStretchedImageLeft = pygame.transform.scale(playerImageLeft, (PLAYERWIDTH * 4, PLAYERHEIGHT * 4))
playerStretchedImageRight = pygame.transform.scale(playerImageRight, (PLAYERWIDTH * 4, PLAYERHEIGHT * 4))

laserImage = pygame.image.load('lasers.png')
laserRect = laserImage.get_rect()
laserStretchedImage = pygame.transform.scale(laserImage, (21 * 4, 3 * 4))

explosionList = [pygame.image.load('explosion0.png'), pygame.image.load('explosion1.png'), pygame.image.load('explosion2.png'), pygame.image.load('explosion3.png'), pygame.image.load('explosion4.png'), pygame.image.load('explosion5.png'), pygame.image.load('explosion6.png')] 
explosionLargeList = [pygame.transform.scale(explosionList[0], (17 * 6, 17 * 6)), pygame.transform.scale(explosionList[1], (17 * 6, 17 * 6)), pygame.transform.scale(explosionList[2], (17 * 6, 17 * 6)), pygame.transform.scale(explosionList[3], (17 * 6, 17 * 6)), pygame.transform.scale(explosionList[4], (17 * 6, 17 * 6)), pygame.transform.scale(explosionList[5], (17 * 6, 17 * 6)), pygame.transform.scale(explosionList[6], (17 * 6, 17 * 6))]

button = pygame.image.load('buttonTemplate.png')
buttonS = pygame.image.load('buttonTemplateSmall.png')
buttonHover = pygame.image.load('buttonHoverTemplate.png')
buttonHoverS = pygame.image.load('buttonHoverTemplateSmall.png')
yesText = pygame.image.load('yes.png')
noText = pygame.image.load('no.png')
highScoresText = pygame.image.load('high scores.png')
playText = pygame.image.load('play.png')
quitText = pygame.image.load('quit.png')
optionsText = pygame.image.load('options.png')
backText = pygame.image.load('back.png')
logoPNG = pygame.image.load('logo.png')
gameOverPNG = pygame.image.load('GameOver.png')
enemy1 = pygame.image.load('Enemy_Ship_2.png')
runway = pygame.image.load('Runway_1.png')
difficultyBG = pygame.image.load('sliderBG.png')
difficultyFG = pygame.image.load('sliderFG.png')
musicOnPNG = pygame.image.load('musicOn.png')
musicOffPNG = pygame.image.load('musicOff.png')

enemyList = [enemy1]

laserSound = pygame.mixer.Sound('shot.wav')

Clock =  pygame.time.Clock()

def distance(speed, time):
    distance = time * speed
    return distance

def movePlayer(x1, frameTime):
    global laserX
    turnleft = False
    turnright = False
    if pygame.key.get_pressed()[97]:
        x1 = x1 - distance(speed * 1.2, frameTime)
        turnleft = True
        if shot == False:
            laserX = x1
    if pygame.key.get_pressed()[100]:
        x1 = x1 + distance(speed * 1.2, frameTime)
        turnright = True
        if shot == False:
            laserX = x1
    if pygame.key.get_pressed()[100] == False and pygame.key.get_pressed()[97] == False:
        if shot == False:
            laserX = x1

    if turnleft == False and turnright == False:
        windowSurface.blit(playerStretchedImage, (x1, WINDOWHEIGHT - PLAYERHEIGHT * 4 - 50, x1 + 100, WINDOWHEIGHT - 50))
    elif turnleft == True:
        windowSurface.blit(playerStretchedImageLeft, (x1, WINDOWHEIGHT - PLAYERHEIGHT * 4 - 50, x1 + 100, WINDOWHEIGHT - 50))
        turnleft = False
    elif turnright == True:
        windowSurface.blit(playerStretchedImageRight, (x1, WINDOWHEIGHT - PLAYERHEIGHT * 4 - 50, x1 + 100, WINDOWHEIGHT - 50))
        turnright = False

    return x1

def shootLaser(bulletTracker, frameTime, laserX):
    windowBackground.blit(laserStretchedImage, (laserX, WINDOWHEIGHT - 110 - bulletTracker, 84, 12))
    bulletTracker = bulletTracker + distance(speed * 2, frameTime)
    global laserRect
    laserRect = pygame.Rect(laserX, WINDOWHEIGHT - 110 - bulletTracker, 84, 12)
    #pygame.draw.rect(windowSurface, RED, (laserX, WINDOWHEIGHT - 110 - bulletTracker, 84, 12))
    if bulletTracker >= WINDOWHEIGHT - 110:
        bulletTracker = 0
        global shot
        shot = False
        laserRect = pygame.Rect(-1000,-1000,-1001,-1001)
    return bulletTracker

def moveBG(bgDist):
    bgDist = distance(speed, frameTime) + bgDist

    if bgDist - WINDOWHEIGHT > 0:
            bgDist = 0

    windowBackground.blit(background, (0, bgDist, WINDOWWIDTH, WINDOWHEIGHT + bgDist))
    windowBackground.blit(background, (0, bgDist - WINDOWHEIGHT, WINDOWWIDTH, bgDist))

    return bgDist    

bgDist = 0
enemyDist = 0
loopTrack = 0
bulletTracker = 0
while True:
    mousePosition = pygame.mouse.get_pos()
    mouseMovement = pygame.mouse.get_rel()
    frameTime = mainClock.tick(70)
    if musicOn == False:
        pygame.mixer.music.stop()
        musicLooped = True
    if GameState == MENU:
        if musicLooped == True:
            if musicOn == True:
                pygame.mixer.music.load("Launchpad.mp3")
                pygame.mixer.music.play(-1, 0.0)
            musicLooped = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                pygame.mixer.quit()
                sys.exit()
        
        bgDist = moveBG(bgDist)

        windowSurface.blit(logoPNG, (200, 100))
        windowSurface.blit(button, (200, 300))
        windowSurface.blit(button, (200, 405))
        windowSurface.blit(button, (200, 510))
        windowSurface.blit(button, (200, 615))
        windowSurface.blit(runway, (0, WINDOWHEIGHT - 200))

        for i in range(0, 4):
            if mousePosition[0] > 200 and mousePosition[0] < 400 and mousePosition[1] > (300 + (i * 105)) and mousePosition[1] < (400 + (i * 105)):
                windowSurface.blit(buttonHover, (200, (300 + (i * 105))))
                if i == 0 and pygame.mouse.get_pressed()[0] == 1:
                    musicLooped = True
                    GameState = STARTGAME
                if i == 1 and pygame.mouse.get_pressed()[0] == 1:
                    GameState = HIGHSCORES
                if i == 2 and pygame.mouse.get_pressed()[0] == 1:
                    GameState = OPTIONS
                if i == 3 and pygame.mouse.get_pressed()[0] == 1:
                    print "quit"
                    pygame.quit()
                    pygame.mixer.quit()
                    sys.exit()

        windowSurface.blit(playText, (200, 300))
        windowSurface.blit(highScoresText, (200, 405))
        windowSurface.blit(optionsText, (200, 510))
        windowSurface.blit(quitText, (200, 615))

        if animation == True:
            if frame == 7:
                frame = 0
                animation = False
            if animation == True:
                
                windowSurface.blit(explosionLargeList[frame], (x1, WINDOWHEIGHT - PLAYERHEIGHT * 4 - 50, x1 + 100, WINDOWHEIGHT - 50))
        
        if animation == True and loopTrack % 5 == 0:
            frame = frame + 1

    if GameState == HIGHSCORES:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP and mousePosition[0] > 200 and mousePosition[0] < 400 and mousePosition[1] > (300 + (3 * 105)) and mousePosition[1] < (400 + (3 * 105)):
                GameState = MENU
                renderingToDo = True
            if event.type == QUIT:
                pygame.quit()
                pygame.mixer.quit()
                sys.exit()
        bgDist = moveBG(bgDist)
        
        windowSurface.blit(logoPNG, (200, 100))
        windowSurface.blit(runway, (0, WINDOWHEIGHT - 200))
        windowSurface.blit(button, (200, 615))

        if mousePosition[0] > 200 and mousePosition[0] < 400 and mousePosition[1] > (300 + (3 * 105)) and mousePosition[1] < (400 + (3 * 105)):
            windowSurface.blit(buttonHover, (200, (300 + (3 * 105))))
            
        windowSurface.blit(backText, (200, 615))

        #read pickle list, sort on highest, for loop and blit on respective coords in regular anitaliased font.
        scoreList = pickle.load(open("scores.dat", "rb"))
        sortedScoreList = sorted(scoreList)
        #print sortedScoreList
        scoreList = sortedScoreList

        if renderingToDo == True:
            for i in range (1, 11):
                #print str(i) + '. ' + str(sortedScoreList[len(sortedScoreList) - i])
                HighScoreText = basicFont.render(str(i) + '. ' + str(sortedScoreList[len(sortedScoreList) - i]), True, YELLOW)
                windowSurface.blit(HighScoreText, (270, 240 + (30 * i)))

    if GameState == OPTIONS:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP and mousePosition[0] > 200 and mousePosition[0] < 400 and mousePosition[1] > 345 and mousePosition[1] < 400:
                musicOn = not musicOn
                print musicOn
            if event.type == MOUSEBUTTONUP and mousePosition[0] > 200 and mousePosition[0] < 400 and mousePosition[1] > (300 + (3 * 105)) and mousePosition[1] < (400 + (3 * 105)):
                GameState = MENU
                options[0] = musicOn
                options[1] = difficulty
                pickle.dump(options, open('options.dat', 'wb'))
                print options
                renderingToDo = True
            if event.type == QUIT:
                pygame.quit()
                pygame.mixer.quit()
                sys.exit()
        bgDist = moveBG(bgDist)
        
        windowSurface.blit(logoPNG, (200, 100))
        windowSurface.blit(runway, (0, WINDOWHEIGHT - 200))
        windowSurface.blit(button, (200, 615))
        windowSurface.blit(difficultyBG, (200, 400))
        windowSurface.blit(buttonS, (200, 345))

        if mousePosition[0] > 200 and mousePosition[0] < 400 and mousePosition[1] > (300 + (3 * 105)) and mousePosition[1] < (400 + (3 * 105)):
            windowSurface.blit(buttonHover, (200, (300 + (3 * 105))))
        elif mousePosition[0] > 200 and mousePosition[0] < 400 and mousePosition[1] > 345 and mousePosition[1] < 395:
            windowSurface.blit(buttonHoverS, (200, 345))

        windowSurface.blit(backText, (200, 615))
        if musicOn == True:
            windowSurface.blit(musicOnPNG, (200, 345))
            
        elif musicOn == False:
            windowSurface.blit(musicOffPNG, (200, 345))

        windowSurface.blit(difficultyFG, (difficulty + 200, 400))

        if pygame.mouse.get_pressed()[0] == 1 and mousePosition[0] > difficulty + 200 - 8 and mousePosition[0] < difficulty + 200 + 20 and mousePosition[1] > 400 and mousePosition[1] < 450:
            difficulty = difficulty + mouseMovement[0]
            if difficulty < 4:
                difficulty = 4
            elif difficulty > 186:
                difficulty = 186
            print difficulty

    if GameState == STARTGAME:
        if musicLooped == True:
            if musicOn == True:
                pygame.mixer.music.load("ToTheMoon.mp3")
                pygame.mixer.music.play(-1, 0.0)
                musicLooped = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                pygame.mixer.quit()
                sys.exit()

        bgDist = moveBG(bgDist)
        
        if playerDistance < 900 - 150:
            animatePlayer = False
            GameState = GAMEPLAY

        if animatePlayer == True:
            playerDistance = playerDistance - distance(0.3, frameTime)
            runwayDistance = runwayDistance + distance(0.3, frameTime)
            
            windowSurface.blit(runway, (0, WINDOWHEIGHT - 200 + runwayDistance))
            windowSurface.blit(playerStretchedImage, (x1, playerDistance, PLAYERWIDTH * 4, PLAYERHEIGHT * 4 ))
    
    if GameState == GAMEPLAY:
        enemyDist = distance((speed * 0.5) + flySpeed, frameTime) + enemyDist

        if enemyDist - WINDOWHEIGHT > 0:
            enemyDist = -300
            generationNeeded = True
            scoreList.append(score)
            pickle.dump(scoreList, open('scores.dat', 'wb'))
            print scoreList
            GameState = DEAD

        bgDist = moveBG(bgDist)

        if generationNeeded == True:
            for enemy in enemyList:
                randX = random.randint(-90 ,WINDOWWIDTH -90)
            enemyDist = -300
            generationNeeded = False

        windowSurface.blit(enemy, (randX, enemyDist, 180, 180))
        enemyRect = pygame.Rect(randX, enemyDist, 180, 180)
        #pygame.draw.rect(windowSurface, GREEN, (randX, enemyDist, 180, 180))
        
        #print str(enemyRect) + " - " + str(laserRect) + " - " + str(laserRect.colliderect(enemyRect))
        #print str(randX) + " - " + str(randX + 180) + " - "

        if showDebug == True:
            getFPS = mainClock.get_fps()
            debug = "FPS: " + str(int(getFPS)) + " - " + str(laserRect.colliderect(enemyRect))
            fpsText = basicFont.render(str(debug), True, YELLOW)
            windowSurface.blit(fpsText, (1, 1))
        
        scoreText = basicFont.render("Score: " + str(score), True, YELLOW)
        windowSurface.blit(scoreText, (1, 880))
        
        x1 = movePlayer(x1, frameTime)

        if shot == True:
            bulletTracker = shootLaser(bulletTracker, frameTime, laserX)

        if x1 > WINDOWWIDTH:
            x1 = PLAYERWIDTH * -4
        elif x1 < PLAYERWIDTH * -4:
            x1 = WINDOWWIDTH

        #collision
        #"""
        if laserRect.colliderect(enemyRect) == True:
            shot = False
            generationNeeded = True
            bulletTracker = 0
            laserRect = pygame.Rect(-1000,-1000,-1001,-1001)
            flySpeed = flySpeed + (difficulty * 0.001)
            animation = True
            #animation coords to remember
            randX_animation = randX
            enemyDist_animation = enemyDist
            score = score + 1
            print score
        else:
            zero = 0
        #"""
        #end collision

        if animation == True:
            if frame == 6:
                frame = 0
                animation = False
            if animation == True:
                windowSurface.blit(explosionLargeList[frame], (randX_animation + (90 - (17 * 3)), enemyDist_animation, 180, 180))
            
        if animation == True and loopTrack % 2 == 0:
            frame = frame + 1


        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == 13:
                    if shot == False:
                        if musicOn == True:
                            laserSound.play()
                    shot = True
            if event.type == KEYUP:
                if event.key == 284:
                    showDebug = not showDebug
            if event.type == QUIT:
                pygame.quit()
                pygame.mixer.quit()
                sys.exit()

    if GameState == DEAD:
        animation = True
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                if event.button == 1 and mousePosition[0] > 197 and mousePosition[0] < 397 and mousePosition[1] > 450 and mousePosition[1] < 550:
                    print "Click"
                    x1 = WINDOWWIDTH / 2 - ((PLAYERWIDTH * 4) / 2)
                    animation = 1
                    shot = False
                    turnleft = False
                    turnright = False
                    showDebug = False
                    generationNeeded = True
                    animatePlayer = True
                    moveRunway = False
                    animation = False
                    hoverOverYes = False
                    hoverOverNo = False
                    laserX = x1
                    bulletTracker = 0
                    frame = 0
                    score = 0
                    randX_animation = 0
                    enemyDist_animation = 0
                    playerDistance = 900 + PLAYERHEIGHT * 4
                    runwayDistance = 0
                    flySpeed = 0
                    musicLooped = True
                    GameState = STARTGAME
                if event.button == 1 and mousePosition[0] > 197 and mousePosition[0] < 397 and mousePosition[1] > 555 and mousePosition[1] < 655:
                    x1 = WINDOWWIDTH / 2 - ((PLAYERWIDTH * 4) / 2)
                    animation = 1
                    shot = False
                    turnleft = False
                    turnright = False
                    showDebug = False
                    generationNeeded = True
                    animatePlayer = True
                    moveRunway = False
                    animation = False
                    hoverOverYes = False
                    hoverOverNo = False
                    laserX = x1
                    bulletTracker = 0
                    frame = 0
                    score = 0
                    randX_animation = 0
                    enemyDist_animation = 0
                    playerDistance = 900 + PLAYERHEIGHT * 4
                    runwayDistance = 0
                    flySpeed = 0
                    musicLooped = True
                    GameState = MENU
            if event.type == QUIT:
                pygame.quit()
                pygame.mixer.quit()
                sys.exit()

        bgDist = moveBG(bgDist)

        windowSurface.blit(gameOverPNG, (200, 200))

        if animation == True:
            if frame == 7:
                frame = 0
                animation = False
            if animation == True:
                
                windowSurface.blit(explosionLargeList[frame], (x1, WINDOWHEIGHT - PLAYERHEIGHT * 4 - 50, x1 + 100, WINDOWHEIGHT - 50))
        
        if animation == True and loopTrack % 5 == 0:
            frame = frame + 1

        windowSurface.blit(button, (197, 555))
        windowSurface.blit(button, (197, 450))

        if mousePosition[0] > 197 and mousePosition[0] < 397 and mousePosition[1] > 450 and mousePosition[1] < 550:
            windowSurface.blit(buttonHover, (197, 450))
        elif mousePosition[0] > 197 and mousePosition[0] < 397 and mousePosition[1] > 555 and mousePosition[1] < 655:
            windowSurface.blit(buttonHover, (197, 555))
            

        windowSurface.blit(yesText, (267, 470))
        windowSurface.blit(noText,(282, 575))

        scoreText = basicFont.render("Score: " + str(score), True, YELLOW)
        windowSurface.blit(scoreText, (270, 375))
        playAgainText = basicFont.render("Play again?", True, YELLOW)
        windowSurface.blit(playAgainText, (260, 400))

    pygame.display.update()
    loopTrack = loopTrack + 1
