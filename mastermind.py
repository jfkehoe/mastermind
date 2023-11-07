import pygame
import random

width = 1280
height = 720 

#need 10 rows, 4 col wide
square_size = int(height/11)
y_start = square_size
x_start = int((width - 4*square_size)/2)

c_radius = int(square_size*.45)

class SpriteContainer():
    def __init__(self):
        self.all_sprites = []

    def add(self, sprite):
        self.all_sprites.append(sprite)

    def update(self):
        for i in self.all_sprites:
            i.update()
    
    def draw(self):
        for i in self.all_sprites:
            i.draw()

class Sprite():
    def __init__(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass

class GridSquareCon(SpriteContainer):
    def __init__(self):
        self.all_sprites = []
        self.sprite_rows = [] 

class PinCon(SpriteContainer):
    pass

class GridSquare(Sprite):
    def __init__(self):
        self.rect = None
        self.circle = False

    def set_pin(self, color):
        self.color = color
        self.circle = True

    def draw(self):
        pygame.draw.rect(screen, "black", self.rect, width=2)
        if self.circle:
            pygame.draw.circle(screen, self.color, self.rect.center, c_radius)

class Pin(Sprite):
    def __init__(self, rect, color):
        self.rect = rect
        self.color = color

    def draw():
        pygame.draw.circle(screen, self.color, self.rect.center, c_radius)



# pygame setup
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True

#setup initial sprites
grid_squares = GridSquareCon()

cy = y_start 
for yi in range(9,-1,-1):
    c_row = [] 
    cx = x_start
    for xi in range(0,4):
        c_gs = GridSquare()
        grid_squares.add(c_gs)
        c_row.append(c_gs)
        r = pygame.Rect(cx,cy,square_size,square_size)
        c_gs.rect = r 
        cx += square_size
    grid_squares.sprite_rows.append(c_row)
    cy += square_size

grid_squares.sprite_rows[9][0].set_pin("blue")


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("gray64")

    # RENDER YOUR GAME HERE
    grid_squares.update()

    grid_squares.draw()
    
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()