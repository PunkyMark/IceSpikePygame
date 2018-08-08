import pygame, os
from pygame.locals import *
import random
import time

pygame.init()

os.environ['SDL_VIDEO_WINDOW_POS'] = str(0) + "," + str(0)

infoObject = pygame.display.Info()
display_width = infoObject.current_w
display_height = infoObject.current_h

FPS = 27

pixelpos_list = 0

rain_y_catch_pos = 1170
rain_y_dis_pos = 1189

amount_Rain = 1

score_y = 20
score_x = 380
score_int = 0


def score(score):
    score_text = font.render(str(score), True, black)
    fake_win.blit(score_text, [score_x, score_y])


black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)

colors = [green, red, yellow, blue, white]
rain_x_pos = [100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400, 425, 450, 475, 500, 525, 550, 575, 600, 625, 650, 675, 700]
rain_y_pos = [20, -20, -60, -100, -140, -200, -260, -300]

win = pygame.display.set_mode((800, 1280))
fake_win = win.copy()
pygame.display.set_caption("Ice Spike")
listValue = 0

walkRight = [pygame.image.load('snowball90.png'), pygame.image.load('snowball180.png'), pygame.image.load('snowball270.png')]

walkLeft = [pygame.image.load('snowball270.png'), pygame.image.load('snowball180.png'), pygame.image.load('snowball90.png')]

still_ball = pygame.image.load('snowball.png')

homebg = pygame.image.load('home2.png')

homeButton = pygame.image.load('homeButton.png')

pauseButton = pygame.image.load('pauseButton.png')

restartButton = pygame.image.load('restartButton.png')

gameoverbg = pygame.image.load('gameover.png')

pixelpos = [pygame.image.load('50p.png'), pygame.image.load('100p.png'),
            pygame.image.load('200p.png'), pygame.image.load('250p.png'),
            pygame.image.load('300p.png')]

playButton = pygame.image.load('playbutton.png')
quitButton = pygame.image.load('quitbutton.png')
arrowLeft = pygame.image.load('arrowleftT.png')
arrowRight = pygame.image.load('arrowrightT.png')
hyperIce = pygame.image.load('HYPERICE LOGO.png')

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 160)
text_x = 430
text_y = 230


def message_to_screen(msg, color):
    screen_text = font.render(msg, True, color)
    fake_win.blit(screen_text, [text_x, text_y])


class Ball(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 10
        self.walkCount = 0
        self.still_ball = True
        self.left = False
        self.right = False


    def draw(self, fake_win):
        if self.walkCount + 1 >= 9:
            self.walkCount = 0

        if self.left:
            fake_win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1

        elif self.right:
            fake_win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1

        elif self.still_ball:
            fake_win.blit(still_ball, (self.x, self.y))

        pygame.display.update()


class Rain(object):
    def __init__(self, x, y, radius, color):
        self.y = random.choice(rain_y_pos)
        self.x = random.choice(rain_x_pos)
        self.radius = radius
        self.color = random.choice(colors)
        self.vel = 15

    def draw(self, fake_win):
        pygame.draw.circle(fake_win, self.color, (self.x, self.y), self.radius)


def redrawGameWindow():
    fake_win.blit(pixelpos[pixelpos_list], (0, 0))
    score(score_int)
    for rain in rains:
        rain.draw(fake_win)
    ball.draw(fake_win)
    fake_win.blit(pauseButton, (800 - 118, 25))
    fake_win.blit(arrowLeft, (40, 1200))
    fake_win.blit(arrowRight, (685, 1200))
    pygame.display.update()

def isOverArrowLeft(pos, display_width, display_height):
    newSizeArrowLeft = (display_width * (40 / 800), display_height * (1200 / 1280))
    newWidthArrowLeft = 80 / (40 / newSizeArrowLeft[0])
    newHeightArrowLeft = 65 / (1200 / newSizeArrowLeft[1])
    if pos[0] > newSizeArrowLeft[0] and pos[0] < newSizeArrowLeft[0] + newWidthArrowLeft:
        if pos[1] > newSizeArrowLeft[1] and pos[1] < newSizeArrowLeft[1] + newHeightArrowLeft:
            return True
    return False

def isOverArrowRight(pos, display_width, display_height):
    newSizeArrowRight = (display_width * (685 / 800), display_height * (1200 / 1280))
    newWidthArrowRight = 80 / (685 / newSizeArrowRight[0])
    newHeightArrowRight = 65 / (1200 / newSizeArrowRight[1])
    if pos[0] > newSizeArrowRight[0] and pos[0] < newSizeArrowRight[0] + newWidthArrowRight:
        if pos[1] > newSizeArrowRight[1] and pos[1] < newSizeArrowRight[1] + newHeightArrowRight:
            return True
    return False

def isOverPlay(pos, display_width, display_height):
    newSizePlay = (display_width * (212 / 800), display_height * (845 / 1280))
    newWidthPlay = 364 / (212 / newSizePlay[0])
    newHeightPlay = 364 / (845 / newSizePlay[1])
    if pos[0] > newSizePlay[0] and pos[0] < newSizePlay[0] + newWidthPlay:
        if pos[1] > newSizePlay[1] and pos[1] < newSizePlay[1] + newHeightPlay:
            return True
    return False

def isOverQuit(pos, display_width, display_height):
    newSizeQuit = (display_width * (22 / 800), display_height * (25 / 1280))
    newWidthQuit = 96 / (22 / newSizeQuit[0])
    newHeightQuit = 96 / (25 / newSizeQuit[1])
    if pos[0] > newSizeQuit[0] and pos[0] < newSizeQuit[0] + newWidthQuit:
        if pos[1] > newSizeQuit[1] and pos[1] < newSizeQuit[1] + newHeightQuit:
            return True
    return False

def isOverHomeButton(pos, display_width, display_height):
    newSizeHomeButton = (display_width * (22 / 800), display_height * (25 / 1280))
    newWidthHomeButton = 96 / (22 / newSizeHomeButton[0])
    newHeightHomeButton = 96 / (25 / newSizeHomeButton[1])
    if pos[0] > newSizeHomeButton[0] and pos[0] < newSizeHomeButton[0] + newWidthHomeButton:
        if pos[1] > newSizeHomeButton[1] and pos[1] < newSizeHomeButton[1] + newHeightHomeButton:
            return True
    return False

def isOverPause(pos, display_width, display_height):
    newSizePause = (display_width * (682 / 800), display_height * (25 / 1280))
    newWidthPause = 96 / (682 / newSizePause[0])
    newHeightPause = 96 / (25 / newSizePause[1])
    if pos[0] > newSizePause[0] and pos[0] < newSizePause[0] + newWidthPause:
        if pos[1] > newSizePause[1] and pos[1] < newSizePause[1] + newHeightPause:
            return True
    return False

def isOverRestart(pos, display_width, display_height):
    newSizeRestart = (display_width * (212 / 800), display_height * (845 / 1280))
    newWidthRestart = 364 / (212 / newSizeRestart[0])
    newHeightRestart = 364 / (845 / newSizeRestart[1])
    if pos[0] > newSizeRestart[0] and pos[0] < newSizeRestart[0] + newWidthRestart:
        if pos[1] > newSizeRestart[1] and pos[1] < newSizeRestart[1] + newHeightRestart:
            return True
    return False

# mainloop
ball = Ball(400, 1150, 80, 80)
gameExit = False
rains = []

startScreen = True
homeScreen = True
gameOver = False

while not gameExit:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
            homeScreen = False
            gameOver = False
        if event.type == VIDEORESIZE:
            screen = pygame.display.set_mode([display_width, display_height], RESIZABLE)

    while startScreen:
        fake_win.blit(hyperIce, (0, 0))
        win.blit(pygame.transform.scale(fake_win, [display_width, display_height]), (0, 0))
        pygame.display.update()
        time.sleep(2)
        startScreen = False

    while homeScreen:
        del rains[:]
        rain_y_catch_pos = 1170
        rain_y_dis_pos = 1189
        score_y = 20
        score_x = 380
        ball.x = 400
        ball.y = 1150
        amount_Rain = 1
        fake_win.blit(homebg, (0, 0))
        fake_win.blit(playButton, (212, 1280 - 435))
        fake_win.blit(quitButton, (22, 25))
        win.blit(pygame.transform.scale(fake_win, [display_width, display_height]), (0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            if isOverPlay(pos, display_width, display_height):
                if click[0] == 1:
                    homeScreen = False
                    gameOver = False
                    gameExit = False
                    score_int = 0
            if event.type == pygame.QUIT:
                gameExit = True
                gameOver = False
                homeScreen = False
                score_int = 0
            if isOverQuit(pos, display_width, display_height):
                if click[0] == 1:
                    gameExit = True
                    gameOver = False
                    homeScreen = False
                    score_int = 0
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.K_q:
                    gameExit = True
                    gameOver = False
                    homeScreen = False
                    score_int = 0
            if event.type == VIDEORESIZE:
                screen = pygame.display.set_mode([display_width, display_height], RESIZABLE)

    for rain in rains:
        click = pygame.mouse.get_pressed()
        pos = pygame.mouse.get_pos()
        rain.y += rain.vel
        if rain.y > rain_y_catch_pos and rain.y <= rain_y_dis_pos and rain.x >= ball.x and rain.x < (ball.x + ball.width):
          if rain.color == white:
            score_int += 1
            amount_Rain += 1
          if rain.color != white:
            pixelpos_list += 1
            ball.y -= 240
            rain_y_dis_pos -= 240
            rain_y_catch_pos -= 240
          if ball.y <= 300:
            gameExit = False
            homeScreen = False
            gameOver = True
        elif rain.y > rain_y_dis_pos:
            rains.pop(rains.index(rain))

    if len(rains) < amount_Rain:
        rains.append(Rain(random.choice(rain_x_pos), (random.choice(rain_y_pos)), 10, (random.choice(colors))))

    click = pygame.mouse.get_pressed()
    pos = pygame.mouse.get_pos()

    if isOverArrowLeft(pos, display_width, display_height) and click[0] == 1 and ball.x > ball.vel + 65:
        ball.x -= ball.vel
        ball.left = True
        ball.right = False
        ball.still_ball = False

    else:
        ball.right = False
        ball.left = False
        ball.still_ball = True
        ball.walkCount = 0

    if isOverArrowRight(pos, display_width, display_height) and click[0] == 1 and ball.x < 800 - ball.width - ball.vel - 65:
        ball.x += ball.vel
        ball.right = True
        ball.left = False
        ball.still_ball = False

    else:
        ball.right = False
        ball.left = False
        ball.still_ball = True
        ball.walkCount = 0

    redrawGameWindow()

    win.blit(pygame.transform.scale(fake_win, [display_width, display_height]), (0, 0))
    pygame.display.update()

    while gameOver:
        del rains[:]
        powerUp = 0
        rain_y_catch_pos = 1170
        rain_y_dis_pos = 1189
        score_y = 550
        score_x = 370
        ball.y = 1150
        ball.x = 400
        amount_Rain = 1
        fake_win.blit(gameoverbg, (0, 0))
        fake_win.blit(restartButton, (212, 1280 - 435))
        fake_win.blit(homeButton, (800 - 118, 25))
        score(score_int)
        win.blit(pygame.transform.scale(fake_win, [display_width, display_height]), (0, 0))
        pygame.display.update()
        time.sleep(0.1)
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            if isOverHomeButton(pos, display_width, display_height):
                if click[0] == 1:
                    gameOver = False
                    gameExit = False
                    homeScreen = True
                    pixelpos_list = 0
                    score_y = 20
                    score_x = 380
                    score_int = 0
            if event.type == pygame.QUIT:
                gameExit = True
                gameOver = False
                homeScreen = False
                score_int = 0
                score_y = 20
                score_x = 220
                pixelpos_list = 0
            click = pygame.mouse.get_pressed()
            if isOverRestart(pos, display_width, display_height):
                if click[0] == 1:
                    homeScreen = False
                    gameOver = False
                    gameExit = False
                    pixelpos_list = 0
                    score_y = 20
                    score_x = 380
                    score_int = 0
            if event.type == VIDEORESIZE:
                screen = pygame.display.set_mode([display_width, display_height], RESIZABLE)

    if isOverPause(pos, display_width, display_height):
        if click[0] == 1:
            FPS = 10
            pause = True
            while pause:
                click = pygame.mouse.get_pressed()
                pos = pygame.mouse.get_pos()
                fake_win.blit(gameoverbg, (0, 0))
                fake_win.blit(homeButton, (22, 25))
                fake_win.blit(playButton, (212, 1280 - 435))
                win.blit(pygame.transform.scale(fake_win, [display_width, display_height]), (0, 0))
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameExit = True
                        homeScreen = False
                        gameOver = False
                    if event.type == VIDEORESIZE:
                        screen = pygame.display.set_mode([display_width, display_height], RESIZABLE)
                    if isOverHomeButton(pos, display_width, display_height):
                        if click[0] == 1:
                            time.sleep(1)
                            gameOver = False
                            gameExit = False
                            homeScreen = True
                            FPS = 27
                            pause = False
                            pixelpos_list = 0
                            score_y = 20
                            score_x = 380
                            score_int = 0
                    if isOverPlay(pos, display_width, display_height):
                        if click[0] == 1:
                            gameOver = False
                            gameExit = False
                            homeScreen = False
                            FPS = 27
                            pause = False

pygame.quit()
