import pygame as pg
import random as rd

# Tree enemy class (ground obstacle)
class tree(pg.sprite.Sprite):
    def __init__(self, ene_grp, mv_speed):
        # Initialize parent Sprite class
        super(tree, self).__init__()

        # Load multiple tree images into a list
        # This allows random variation in tree appearance
        self.img_lst = []
        for i in range(1, 6):
            self.img_lst.append(
                pg.image.load(f'ChromeDynosaur/Images/trees/tree{i}.png').convert_alpha()
            )

        # Randomly choose one tree image
        self.img = self.img_lst[rd.randint(0, 4)]

        # Create collision mask from image (for accurate collision detection)
        self.mask = pg.mask.from_surface(self.img)

        # Set starting position (right side of screen)
        self.rect = pg.Rect(600, 210, 50, 50)

        # Movement speed (matches background scrolling speed)
        self.speed = mv_speed

        # Store reference to enemy sprite group
        self.grp = ene_grp

    # Update runs every frame
    def update(self, dt):
        # Move tree left across the screen
        self.rect.x -= self.speed * dt

        # Delete tree when it goes off-screen
        if self.rect.right < 0:
            self.deleteSelf()

    # Update speed when game speed increases
    def setSpeed(self, mv_speed):
        self.speed = mv_speed

    # Remove tree from sprite groups and memory
    def deleteSelf(self):
        self.kill()   # Removes sprite from all groups
        del self      # Deletes object from memory
