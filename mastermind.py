#!/usr/bin/python3

import pygame
import random

width = 1280
height = 720 

#need 10 rows, 4 col wide
square_size = int(height/11)
y_start = square_size
x_start = int((width - 4*square_size)/2)

c_radius = int(square_size*.45)

colors = "black white yellow blue red green".split(" ")
secret_answer = random.choices(colors, k=4)

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

PinCon = SpriteContainer

class TextCon(SpriteContainer):
    def __init__(self):
        self.all_sprites = []
        self.sprite_rows = [] 


#these will be stored in the square container for convience 
class TextSq(Sprite):
    def __init__(self, color, fnt, x1, y1):
        self.color = color
        self.fnt = fnt 
        self.text = ""
        self.x1 = x1
        self.y1 = y1

    def draw(self):
        if self.text != "":
            txt = self.fnt.render(self.text, True, self.color)
            # rect = txt.get_rect()
            # rect.x = self.x1
            # rect.y = self.y1
            screen.blit(txt, (self.x1, self.y1))
            

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

    def draw(self):
        pygame.draw.circle(screen, self.color, self.rect.center, c_radius)
        


# pygame setup
pygame.init()
pygame.display.set_caption("MasterMind")
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True


fnt = pygame.font.Font(size=65)

#want to be fancy and make an icon here. 
#icon should be 32 x 32
icon = pygame.Surface((32,32))

icon_fnt = pygame.font.Font(size=32)
t0 = icon_fnt.render("M", 1, "black")
t1 = icon_fnt.render("M", 1, "white")
tx = icon_fnt.render("MM", 1, "black")
w = tx.get_width()
h = tx.get_height()
t0x = int((32-w)/2)
t0x = 0
t0y = int((32-h)/2)
t1x = t0.get_width() - 3

icon.fill("black")
cx = 8
for i in "blue yellow green red".split(" "):
    r = pygame.draw.circle(icon, i, (cx, 16), 16)
    cx += 8
    
icon.blit(t0, (t0x, t0y))
icon.blit(t1, (t1x, t0y))
pygame.display.set_icon(icon)


#setup initial sprites
grid_squares = GridSquareCon()
text_squares = TextCon()

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
    
    cx += square_size
    c_row = []
    for color in ["black", "white"]: 
        cx += square_size
        ctxt = TextSq(color, fnt, cx, cy)
        text_squares.add(ctxt)
        c_row.append(ctxt)
    text_squares.sprite_rows.append(c_row)
    
    cy += square_size

#grid_squares.sprite_rows[9][0].set_pin("blue")

#setup pin prototypes
pins = PinCon()

cy = height - 7 * square_size
cx = x_start - 5 - square_size
for c in "black white yellow blue red green".split(" "):
    r = pygame.Rect(cx, cy, square_size, square_size)
    cp = Pin(r, c)
    pins.add(cp)    
    cy += square_size

row_idx = len(grid_squares.sprite_rows) - 1 
floating_pin = None
finished = False
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    check_row = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not finished:
            (x,y) = pygame.mouse.get_pos()
            for p in pins.all_sprites:
                if p.rect.collidepoint(x, y):
                    color = p.color
                    rect = pygame.Rect(0,0,square_size,square_size)
                    floating_pin = Pin(rect, color)
        elif event.type == pygame.MOUSEBUTTONUP and floating_pin and not finished:
            for cgs in grid_squares.sprite_rows[row_idx]:
                if cgs.rect.collidepoint(pygame.mouse.get_pos()):
                    cgs.color = floating_pin.color 
                    cgs.circle = True
                    check_row = True 

            floating_pin = None

    if check_row:
        decr = True
        for i in grid_squares.sprite_rows[row_idx]:
            if i.circle == False: 
                decr = False

        #test how close the guess is
        if decr:
            user_answer = [i.color for i in grid_squares.sprite_rows[row_idx]]
            ###### was working here
            ### need to test the font yet.
            (black, white) = text_squares.sprite_rows[row_idx]
            black_cnt = 0 
            white_cnt = 0
            prune_list_user = []
            prune_list_answer = []  
            for i in range(0,4):
                if user_answer[i] == secret_answer[i]:
                    black_cnt += 1
                else:
                    prune_list_answer.append(secret_answer[i])
                    prune_list_user.append(user_answer[i])
            
            if black_cnt == 4:
                finished = "win" 
            black.text = str(black_cnt)

            for i in prune_list_user:
                if i in prune_list_answer:
                    white_cnt += 1 
                    prune_list_answer.remove(i)
        
            white.text = str(white_cnt)



        if decr and row_idx > 0:
            row_idx -=1 
        elif decr:
            if not finished:
                finished = "loss"
            print("Game done")



    # fill the screen with a color to wipe away anything from last frame
    screen.fill("gray64")

    # RENDER YOUR GAME HERE
    if not finished:     
        grid_squares.update()
        pins.update()
        if floating_pin:
            floating_pin.rect.center = pygame.mouse.get_pos()


    grid_squares.draw()
    pins.draw()
    text_squares.draw()
    if floating_pin:
        floating_pin.draw()

    if finished:
        cx = x_start
        for i in secret_answer:
            r = pygame.Rect(cx, 2, square_size, square_size)
            pygame.draw.circle(screen, i, r.center, c_radius)
            cx += square_size
        
        cfnt = pygame.font.Font(size=65*2)
        if finished == "win":
            cc = "blue"
        else:
            cc = "red"
        ctxt = cfnt.render(finished, True, cc)
        screen.blit(ctxt, (20, int(height/2)))

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(30)  # limits FPS to 60

pygame.quit()