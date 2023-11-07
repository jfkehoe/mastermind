import pygame
import random

width = 1280
height = 720 

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


# pygame setup
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True

#setup initial sprites
all_sprite_con = SpriteContainer()

dummy_sprite = Sprite()
all_sprite_con.add(dummy_sprite)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("gray64")

    # RENDER YOUR GAME HERE
    all_sprite_con.upate()

    all_sprite_con.draw()

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()