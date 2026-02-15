import pygame
import random as rd
import math as m
from pygame import mixer

pygame.init()

sc = pygame.display.set_mode((800,600))

bg = pygame.image.load('SpaceInvader_v1/Images/space.jpg')
bg = pygame.transform.scale(bg, (800,600))

pygame.display.set_caption("Sapce Invaders")

icon = pygame.image.load('SpaceInvader_v1/Images/ufo.png')
pygame.display.set_icon(icon)


playerImg = pygame.image.load('SpaceInvader_v1/Images/spaceship.png')
playerImg = pygame.transform.scale(playerImg, (64, 64))
playerX = 370
playerY = 480

playerX_change = 0


monsterImg = []
monsterX =[]
monsterY =[]
monsterXchange = []
monsterYchange = []

monsterCount = 5
for i in range(monsterCount):
    Img = pygame.image.load('SpaceInvader_v1/Images/monster.png')
    monsterImg.append(pygame.transform.scale(Img, (64, 64)))
    monsterX.append(rd.randint(0,735))
    monsterY.append(rd.randint(50, 150))
    monsterXchange.append(0.1)
    monsterYchange.append(40)

BulletImg = pygame.image.load('SpaceInvader_v1/Images/bullet.png')
BulletImg = pygame.transform.scale(BulletImg, (32,32))
BulletX = 0
BulletY = 480
BulletXchange = 0
BulletYchange = 0.5
BulletState = 'ready'


score = 0
font = pygame.font.Font('SpaceInvader_v1/Fonts/Game Of Squids.ttf', 32)
textX = 10
textY = 10

GOfont = pygame.font.Font('SpaceInvader_v1/Fonts/Game Of Squids.ttf', 64)

def showScore(x,y):
    score_val = font.render("Score : " + str(score), True, (255,255,255))
    sc.blit(score_val, (x,y))

def gameOverText():
    GOscore_val = GOfont.render("Game Over", True, (255,0,0))
    sc.blit(GOscore_val, (180, 200))

def player(x,y):
    sc.blit(playerImg, (x, y))

def monster(x,y,i):
    sc.blit(monsterImg[i], (x,y))

def fire(x,y):
    global BulletState
    BulletState = 'fire'
    sc.blit(BulletImg, (x+16,y+10))

def hit(monsterX, monsterY, BulletX, BulletY):
    d = m.sqrt((m.pow(monsterX-BulletX,2))+(m.pow(monsterY-BulletY,2)))
    if d < 25:
        return True
    else:
        return False

run = True

while run:

    sc.fill((25,50,50))
    sc.blit(bg, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3

            if event.key == pygame.K_SPACE:
                if BulletState == 'ready':
                    bulletSound  = mixer.Sound('SpaceInvader_v1/Sounds/shoot.wav')
                    bulletSound.play()
                    BulletX = playerX
                    fire(BulletX, BulletY)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
        

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(monsterCount):

        if monsterY[i] > 440:
            for j in range(monsterCount):
                monsterY[j] = 2000
            gameOverText()
            break
        monsterX[i] += monsterXchange[i]
        if monsterX[i] <= 0:
            monsterXchange[i] = 0.1
            monsterY[i] += monsterYchange[i]
        elif monsterX[i] >= 736:
            monsterXchange[i] = -0.1
            monsterY[i] += monsterYchange[i]

        collide = hit(monsterX[i], monsterY[i], BulletX, BulletY)
        if collide:
            CollisionSound  = mixer.Sound('SpaceInvader_v1/Sounds/explosion.wav')
            CollisionSound.play()
            BulletY = 480
            BulletState = 'ready'
            score += 1
            # print(score)
            monsterX[i] = rd.randint(0,735)
            monsterY[i] = rd.randint(50, 150)

        monster(monsterX[i], monsterY[i], i)

    if BulletY<=0:
        BulletY=480
        BulletState = 'ready'

    if BulletState == 'fire':
        fire(BulletX, BulletY)
        BulletY -= BulletYchange

    
    player(playerX, playerY)
    showScore(textX, textY)
    pygame.display.update()