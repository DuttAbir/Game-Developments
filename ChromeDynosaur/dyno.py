import pygame as pg

# Player character class (Dinosaur)
class dyno(pg.sprite.Sprite):
    def __init__(self):
        # Initialize sprite parent class
        super(dyno, self).__init__()

        # Load running animation frames
        self.dyno_run_lst = [
            pg.image.load('ChromeDynosaur/Images/dino1.png').convert_alpha(),
            pg.image.load('ChromeDynosaur/Images/dino2.png').convert_alpha()
        ]
        
        # Load crouching animation frames
        self.dyno_crouch_lst = [
            pg.image.load('ChromeDynosaur/Images/dino_crouch1.png').convert_alpha(),
            pg.image.load('ChromeDynosaur/Images/dino_crouch2.png').convert_alpha()
        ]
        
        # Set initial image and collision mask
        self.img = self.dyno_run_lst[0]
        self.mask = pg.mask.from_surface(self.img)

        # Reset all movement and animation variables
        self.resetDyno()

        # Physics settings
        self.gravity = 10     # Downward acceleration
        self.jump = 250       # Jump force

    # Update function runs every frame
    def update(self, dt):
        # Check if down arrow key is pressed (crouch)
        keys = pg.key.get_pressed()
        if keys[pg.K_DOWN]:
            self.crouch = True
        else:
            self.crouch = False

        # If dinosaur is on the ground, play running/crouching animation
        if self.on_ground:
            # Change animation frame every few ticks
            if self.ani_counter == 5:

                # Switch between crouch and run animation
                if self.crouch:
                    self.img = self.dyno_crouch_lst[self.switch_img]
                    self.rect = pg.Rect(200, 220, 55, 30)  # Smaller hitbox when crouching
                else:
                    self.img = self.dyno_run_lst[self.switch_img]
                    self.rect = pg.Rect(200, 200, 43, 51)  # Normal running hitbox

                # Update collision mask to match new image
                self.mask = pg.mask.from_surface(self.img)

                # Toggle animation frame (0 ↔ 1)
                if self.switch_img == 0:
                    self.switch_img = 1
                else:
                    self.switch_img = 0

                # Reset animation counter
                self.ani_counter = 0

            # Increment animation counter
            self.ani_counter += 1

        else:
            # Apply gravity when in air
            self.y_vel += self.gravity * dt

            # Move dinosaur vertically
            self.rect.y += self.y_vel

            # Stop falling when reaching ground level
            if self.rect.y >= 200:
                self.on_ground = True
                self.rect.y = 200

    # Jump function triggered when spacebar is pressed
    def Jump(self, dt):
        if self.on_ground:
            # Apply upward velocity
            self.y_vel = -self.jump * dt
            self.on_ground = False

    # Reset dinosaur to starting state
    def resetDyno(self):
        self.rect = pg.Rect(200, 200, 43, 51)  # Starting position and size
        self.switch_img = 1    # Current animation frame index
        self.ani_counter = 0   # Animation timing counter
        self.crouch = False    # Crouch state
        self.on_ground = True  # Whether dinosaur is touching ground
        self.y_vel = 0         # Vertical velocity
