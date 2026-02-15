import random as rd
import sys
import pygame
from pygame.locals import *

FPS = 32
SCREENWIDTH = 380
SCREENHEIGHT = 400

SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))

GROUND_Y = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}

PLAYER = "Flappy Bird/gallery/images/flappy_bird.png"
BACKGROUND = "Flappy Bird/gallery/images/background.png"
PIPE = "Flappy Bird/gallery/images/pipe.png"

numbers_list = [pygame.image.load("Flappy Bird/gallery/images/numbers/0-number-png.png").convert_alpha(),
        pygame.image.load("Flappy Bird/gallery/images/numbers/1-number-png.png").convert_alpha(),
        pygame.image.load("Flappy Bird/gallery/images/numbers/2-number-png.png").convert_alpha(),
        pygame.image.load("Flappy Bird/gallery/images/numbers/3-number-png.png").convert_alpha(),
        pygame.image.load("Flappy Bird/gallery/images/numbers/4-number-png.png").convert_alpha(),
        pygame.image.load("Flappy Bird/gallery/images/numbers/5-number-png.png").convert_alpha(),
        pygame.image.load("Flappy Bird/gallery/images/numbers/6-number-png.png").convert_alpha(),
        pygame.image.load("Flappy Bird/gallery/images/numbers/7-number-png.png").convert_alpha(),
        pygame.image.load("Flappy Bird/gallery/images/numbers/8-number-png.png").convert_alpha(),
        pygame.image.load("Flappy Bird/gallery/images/numbers/9-number-png.png").convert_alpha()]

for i in range (0,10):
    numbers_list[i] = pygame.transform.scale(numbers_list[i], (40, 40))

def welcome():
    player_x = int(SCREENWIDTH/5)
    player_y = int((SCREENHEIGHT - GAME_SPRITES["player"].get_height())/2)

    intro_x = int(SCREENWIDTH - GAME_SPRITES["intro"].get_width())/2
    intro_y = int(SCREENHEIGHT*0.13)

    base_x = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0,0))
                SCREEN.blit(GAME_SPRITES['player'], (player_x, player_y))
                SCREEN.blit(GAME_SPRITES['intro'], (intro_x, intro_y))
                SCREEN.blit(GAME_SPRITES['base'], (base_x, GROUND_Y))

                pygame.display.update()
                FPS_CLOCK.tick(FPS)
          
def maingame():
    score = 0
    player_x = int(SCREENWIDTH/5)
    player_y = int((SCREENHEIGHT - GAME_SPRITES["player"].get_height())/2)

    base_x = 0

    newPipe1= getRandomPipe()
    newPipe2= getRandomPipe()

    upperPipes = [
        {'x' : SCREENWIDTH + 200, 'y' : newPipe1[0]['y']},
        {'x' : SCREENWIDTH + 200 +(SCREENWIDTH/2), 'y' : newPipe2[0]['y']},
    ]
 
    lowerPipes = [
        {'x' : SCREENWIDTH + 200, 'y' : newPipe1[1]['y']},
        {'x' : SCREENWIDTH + 200 +(SCREENWIDTH/2), 'y' : newPipe2[1]['y']},
    ]
        
    pipeVelx = -4 
    playerVely = -9
    playerMaxvely = 10
    playerMinvely = -8
    playerAccy = 1

    playerflapvel  = -8
    playerfalpped = False

    while True :
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    if player_y > 0:
                        playerVely = playerflapvel
                        playerfalpped = True
                        GAME_SOUNDS['wing'].play()
        crashTest = isCollide(player_x, player_y, upperPipes, lowerPipes)

        if crashTest:
            return

        playerMidPos = player_x + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos +4:
                score += 1
                print(f"Your score is {score}")
                GAME_SOUNDS['point'].play() 
 
        if playerVely < playerMaxvely and not playerfalpped:
            playerVely += playerAccy

        if playerfalpped:
            playerfalpped = False

        playerHeight  = GAME_SPRITES['player'].get_height()
        player_y = player_y + min(playerVely , GROUND_Y - player_y - playerHeight)

        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelx
            lowerPipe['x'] += pipeVelx

        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0]) 
            lowerPipes.append(newpipe[1])

        if upperPipes[0]['x'] < -(GAME_SPRITES['pipe'][0].get_width()):
            upperPipes.pop(0)
            lowerPipes.pop(0)


        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

 
        SCREEN.blit(GAME_SPRITES['base'], (base_x, GROUND_Y))
        SCREEN.blit(GAME_SPRITES['player'], (player_x, player_y))

        
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digits in myDigits:
            width += GAME_SPRITES['numbers'][digits].get_width()

        x_offset = (SCREENWIDTH - width)/2

        for digits in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digits], (x_offset, SCREENHEIGHT*0.12))
            x_offset += GAME_SPRITES['numbers'][digits].get_width()
        

        pygame.display.update()
        FPS_CLOCK.tick(FPS)

def isCollide(player_x, player_y, upperPipes, lowerPipes):
    if player_y > GROUND_Y - 25 - 25 or player_y <0:
        GAME_SOUNDS['hit'].play()
        return True

    for pipe in upperPipes:
        pipe_height = GAME_SPRITES['pipe'][0].get_height()
        if (player_y < pipe_height + pipe['y'] and abs(player_x - pipe['x']) + 135 < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True
    for pipe in lowerPipes:
        if (player_y + GAME_SPRITES['player'].get_height() > pipe['y'] and abs(player_x - pipe['x']) + 135 < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        pass
    return  False

def getRandomPipe():
     pipeHeight = GAME_SPRITES['pipe'][0].get_height()
     offset = SCREENHEIGHT/3
     y2 = offset + rd.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 0.8 * offset))
     pipeX = SCREENWIDTH+10
     y1 = pipeHeight - y2 + offset
 
     pipe = [
         {'x': pipeX, 'y' : -y1}, 
         {'x': pipeX, 'y' : y2}
    ]
    
     return pipe

if __name__ == "__main__":
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    pygame.display.set_caption("FLAPPY BIRD by Xavier")
    GAME_SPRITES['numbers'] =( 
        numbers_list[0],
        numbers_list[1],
        numbers_list[2],
        numbers_list[3],
        numbers_list[4],
        numbers_list[5],
        numbers_list[6],
        numbers_list[7],
        numbers_list[8],
        numbers_list[9],
    )

    GAME_SPRITES['intro'] = pygame.image.load("Flappy Bird/gallery/images/intro.png").convert_alpha()
    GAME_SPRITES['intro'] = pygame.transform.scale(GAME_SPRITES['intro'], (400, 400))
    GAME_SPRITES['base'] = pygame.image.load("Flappy Bird/gallery/images/flappy-bird-ground.png").convert_alpha()
    GAME_SPRITES['pipe'] = ( 
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
        pygame.image.load(PIPE).convert_alpha()
        )
    
    GAME_SOUNDS['die'] = pygame.mixer.Sound("Flappy Bird/gallery/sounds/sfx_die.wav")
    GAME_SOUNDS['hit'] = pygame.mixer.Sound("Flappy Bird/gallery/sounds/sfx_hit.wav")
    GAME_SOUNDS['point'] = pygame.mixer.Sound("Flappy Bird/gallery/sounds/sfx_point.wav")
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound("Flappy Bird/gallery/sounds/sfx_swoosh.wav")
    GAME_SOUNDS['wing'] = pygame.mixer.Sound("Flappy Bird/gallery/sounds/sfx_wing.wav")

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()
    GAME_SPRITES['player'] = pygame.transform.scale(GAME_SPRITES['player'], (40, 40))

    
    
    while True:
        welcome()
        maingame()