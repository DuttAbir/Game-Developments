import pygame as pg

# Bird enemy class (flying obstacle)
class bird(pg.sprite.Sprite):
    def __init__(self, ene_grp, mv_speed):
        # Initialize parent Sprite class
        super(bird, self).__init__()

        # Load bird animation frames (wing flapping)
        self.img_lst = [
            pg.image.load('ChromeDynosaur/Images/bird1.png').convert_alpha(),
            pg.image.load('ChromeDynosaur/Images/bird2.png').convert_alpha()
        ]

        # Set initial image and collision mask
        self.img = self.img_lst[0]
        self.mask = pg.mask.from_surface(self.img)

        # Starting position (right side of screen)
        self.rect = pg.Rect(600, 180, 42, 31)

        # Animation control variables
        self.ani_counter = 0     # Counts frames between animation switches
        self.img_switch = 1      # Tracks which animation frame to show

        # Movement speed (same as background speed)
        self.speed = mv_speed

        # Store reference to enemy group
        self.grp = ene_grp

    # Update runs every frame
    def update(self, dt):
        # Handle wing-flapping animation
        if self.ani_counter == 10:
            self.img = self.img_lst[self.img_switch]

            # Toggle animation frame (0 ↔ 1)
            if self.img_switch == 0:
                self.img_switch = 1
            else:
                self.img_switch = 0

            # Reset animation counter
            self.ani_counter = 0

        # Increase animation counter each frame
        self.ani_counter += 1

        # Move bird left across the screen
        self.rect.x -= self.speed * dt

        # Remove bird if it moves off-screen
        if self.rect.right < 0:
            self.deleteSelf()

    # Update movement speed (used when game speeds up)
    def setSpeed(self, mv_speed):
        self.speed = mv_speed

    # Remove bird from sprite group and memory
    def deleteSelf(self):
        self.kill()   # Removes sprite from all groups
        del self      # Deletes object from memory
