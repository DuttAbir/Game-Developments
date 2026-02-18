import pygame as pg
from pygame.math import Vector2
import sys
import random as rd

pg.init()

title_font = pg.font.Font(None, 50)
score_font = pg.font.Font(None, 30)
cell_size = 30
cell_num = 20

offset = 60


class Food:
    def __init__(self, snake_body):
        self.pos = self.rendom_food_pos(snake_body)

    def draw(self):
        food_rect = pg.Rect(offset+self.pos.x*cell_size, offset+self.pos.y*cell_size, cell_size, cell_size)
        sc.blit(food_img, food_rect)

    def random_cell(self):
        x = rd.randint(0, cell_num-1)
        y = rd.randint(0, cell_num-1)
        return Vector2(x,y)

    def rendom_food_pos(self, snake_body):
        pos  = self.random_cell()
        while pos in snake_body:
            pos = self.random_cell()

        return pos
    
class Snake:
    def __init__(self):
        self.body = [Vector2(6,9), Vector2(5,9), Vector2(4,9)]
        self.dir = Vector2(1,0)
        self.add_part = False
        self.eat_sound = pg.mixer.Sound('Snake_Game/sfx/eat.mp3')
        self.wallHit_sound = pg.mixer.Sound('Snake_Game/sfx/fail.mp3')

    def draw(self):
        for part in self.body:
            part_rect = (offset+part.x * cell_size, offset+part.y*cell_size, cell_size, cell_size)
            pg.draw.rect(sc, (0,0,0), part_rect, 0,7)

    def update_pos(self):
        self.body.insert(0, self.body[0]+self.dir)
        if self.add_part == True: 
            self.add_part = False
        else:    
            self.body = self.body[:-1]

    def reset(self):
        self.body = [Vector2(6,9), Vector2(5,9), Vector2(4,9)]
        self.dir = Vector2(1,0)
        self.add_part = False

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.pause = False
        self.score = 0


    def draw(self):
        self.food.draw()
        self.snake.draw()
    
    def update(self):
        if not self.pause:
            self.snake.update_pos()
            self.foodCollison()
            self.edgeCollison()
            self.tailCollison()

    def foodCollison(self):
        if self.snake.body[0] == self.food.pos:
            self.food.pos = self.food.rendom_food_pos(self.snake.body)
            self.snake.add_part = True
            self.score+=1
            self.snake.eat_sound.play()

    def edgeCollison(self):
        if self.snake.body[0].x == cell_num or self.snake.body[0].x == -1:
            self.gameOver()
        if self.snake.body[0].y == cell_num or self.snake.body[0].y == -1:
            self.gameOver()

    def tailCollison(self):
        tailPart = self.snake.body[1:]
        if self.snake.body[0] in tailPart:
            self.gameOver()

    def gameOver(self):
        self.snake.reset()
        self.food.pos = self.food.rendom_food_pos(self.snake.body)
        self.pause = True
        self.score = 0
        self.snake.wallHit_sound.play()

sc = pg.display.set_mode((2*offset+cell_size*cell_num,2*offset+cell_size*cell_num))

pg.display.set_caption("Snake Game")
icon = pg.image.load('Snake_Game/graphics/snake_icon.png')
pg.display.set_icon(icon)

clk = pg.time.Clock()

game = Game()

food_img = pg.image.load('Snake_Game/graphics/food.png').convert_alpha()
food_img = pg.transform.scale(food_img, (cell_size, cell_size))

SNAKE_UPDATE = pg.USEREVENT
pg.time.set_timer(SNAKE_UPDATE, 200)

while True:
    for event in pg.event.get():
        if event.type == SNAKE_UPDATE:
            game.update()
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if game.pause:
                game.pause = False
            if event.key == pg.K_UP and game.snake.dir != Vector2(0,1):
                game.snake.dir = Vector2(0,-1)
            if event.key == pg.K_DOWN and game.snake.dir != Vector2(0,-1):
                game.snake.dir = Vector2(0,1)
            if event.key == pg.K_LEFT and game.snake.dir != Vector2(1,0):
                game.snake.dir = Vector2(-1,0)
            if event.key == pg.K_RIGHT and game.snake.dir != Vector2(-1,0):
                game.snake.dir = Vector2(1,0)
        
    sc.fill((173, 204, 96))
    pg.draw.rect(sc, (0,0,0), (offset-5, offset-5, cell_size*cell_num +10, cell_size*cell_num+10),5)
    game.draw()
    title = title_font.render("Snake Game", True, (255,0,0))
    score_place = score_font.render(str(game.score), True, (255,0,0))
    sc.blit(title, (((cell_num*cell_size)/2)-offset, 20))
    sc.blit(score_place, (offset-5, offset+cell_num*cell_size+10))
    pg.display.update()
    clk.tick(60)