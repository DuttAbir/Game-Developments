# Import required libraries
import pygame as pg     # Game development library
import sys              # For exiting the program
import time as t        # Used for time delta calculation
from dyno import dyno   # Player character class
from bird import bird   # Flying obstacle class
from tree import tree   # Ground obstacle class
import random as rd     # For random obstacle spawning

# Initialize pygame
pg.init()

class Game:
    def __init__(self):
        # Screen dimensions
        self.width = 600
        self.height = 300

        # Create game window and clock for FPS control
        self.sc = pg.display.set_mode((self.width, self.height))
        self.clk = pg.time.Clock()

        # Load scrolling ground images
        self.ground = pg.image.load('ChromeDynosaur/Images/ground.png').convert_alpha()
        self.gnd_rect = self.ground.get_rect(center=(300, 250))

        self.ground2 = pg.image.load('ChromeDynosaur/Images/ground.png').convert_alpha()
        self.gnd2_rect = self.ground2.get_rect(center=(900, 250))

        # Load font and create score display
        self.font = pg.font.Font('ChromeDynosaur/Fonts/font.ttf', 20)
        self.score_dis = self.font.render("Score : 0", True, (0,0,0))
        self.score_dis_rect = self.score_dis.get_rect(center=(500, 20))

        # Restart message display
        self.restart_dis = self.font.render("Restart Game", True, (0,0,0))
        self.restart_dis_rect = self.score_dis.get_rect(center=(300, 150))

        # Create player character
        self.dyno = dyno()

        # Game state variables
        self.lost = False           # Tracks if the player lost
        self.bg_speed = 250         # Background scrolling speed
        self.spawn_counter = 0      # Counter for spawning enemies
        self.spawn_time = 80        # Time interval between spawns
        self.score = 0              # Player score
        self.ene_grp = pg.sprite.Group()  # Group to hold enemy sprites

        # Load sound effects
        self.dead_sfx = pg.mixer.Sound('ChromeDynosaur/Sounds/dead.mp3')
        self.point_sfx = pg.mixer.Sound('ChromeDynosaur/Sounds/points.mp3')
        self.jump_sfx = pg.mixer.Sound('ChromeDynosaur/Sounds/jump.mp3')

    # Check collision between player and enemies
    def collison_check(self):
        if pg.sprite.spritecollide(self.dyno, self.ene_grp, False, pg.sprite.collide_mask):
            self.gameOver()

    # Trigger game over state
    def gameOver(self):
        self.lost = True
        self.dead_sfx.play()

    # Reset game variables to restart
    def restart(self):
        self.lost = False
        self.score = 0
        self.spawn_counter = 0
        self.bg_speed = 250
        self.score_dis = self.font.render("Score : 0", True, (0,0,0))

        # Reset player state
        self.dyno.resetDyno()

        # Remove all enemies
        for ene in self.ene_grp:
            ene.deleteSelf()

    # Main game loop
    def GameLoop(self):
        prev_time = t.time()  # Store previous frame time

        while True:
            # Calculate delta time (time between frames)
            now_time = t.time()
            dt = now_time - prev_time
            prev_time = now_time

            # Handle user input/events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                # Spacebar controls jumping or restarting
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    if not self.lost:
                        self.dyno.Jump(dt)
                        self.jump_sfx.play()
                    else:
                        self.restart()

            # Clear screen with white background
            self.sc.fill((255,255,255))

            if not self.lost:
                # Move scrolling ground
                self.gnd_rect.x -= int(self.bg_speed * dt)
                self.gnd2_rect.x -= int(self.bg_speed * dt)

                # Reset ground position when off-screen
                if self.gnd_rect.right < 0:
                    self.gnd_rect.x = 600
                if self.gnd2_rect.right < 0:
                    self.gnd2_rect.x = 600

                # Update score over time
                self.score += 0.1
                self.score_dis = self.font.render(f"Score : {int(self.score)}", True, (0,0,0))

                # Update player and enemies
                self.dyno.update(dt)
                self.ene_grp.update(dt)

                # Spawn enemies randomly after interval
                if self.spawn_counter == self.spawn_time:
                    if rd.randint(0,1) == 1:
                        self.ene_grp.add(bird(self.ene_grp, self.bg_speed))
                    else:
                        self.ene_grp.add(tree(self.ene_grp, self.bg_speed))
                    self.spawn_counter = 0

                self.spawn_counter += 1

                # Increase game speed every 50 points
                if int(self.score) % 50 == 0:
                    self.bg_speed += 5
                    for ene in self.ene_grp:
                        ene.setSpeed(self.bg_speed)

                # Play score sound every 100 points
                if int(self.score + 1) % 100 == 0:
                    self.point_sfx.play()

                # Draw player and enemies
                self.sc.blit(self.dyno.img, self.dyno.rect)
                for ene in self.ene_grp:
                    self.sc.blit(ene.img, ene.rect)

                # Check for collisions
                self.collison_check()

            else:
                # Show restart message if game over
                self.sc.blit(self.restart_dis, self.restart_dis_rect)

            # Draw ground and score
            self.sc.blit(self.ground, self.gnd_rect)
            self.sc.blit(self.ground2, self.gnd2_rect)
            self.sc.blit(self.score_dis, self.score_dis_rect)

            # Update screen and maintain 60 FPS
            pg.display.update()
            self.clk.tick(60)

# Create game instance and start loop
game = Game()
game.GameLoop()
