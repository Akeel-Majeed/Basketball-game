#---------------------------basketball.py--------------------------------------#
#by Akeel Majeed

#import libraries
import random
import math
import pygame
from pygame import mixer
from tkinter import *
import tkinter.messagebox

#initilise the game
pygame.init()

def message_box():

    """displays an into message for game"""

    root = Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    tkinter.messagebox.showinfo("Basketball Game", "Welcome to my Game!\nYou control the hoop!\nYour job is to catch the basketball and avoid the bomb!")
    try:
        root.destroy()
    except:
        pass

#background sound
mixer.music.load('resources/crowd.wav')
mixer.music.play(-1)

#settting up screen, logo
screen = pygame.display.set_mode((600, 800))
pygame.display.set_caption("Basketball game! By Akeel Majeed")

logo = pygame.image.load('resources/basketball.png')
pygame.display.set_icon(logo)

background = pygame.image.load('resources/brickwall.png')

#player
player_img = pygame.image.load('resources/hoop.png')
px = 300
py = 600
ps = 15
pw = 64
ph = 64

def draw_player(x, y):

    """blits player onto screen"""

    screen.blit(player_img, (x, y))

#enemy
enemy_img = pygame.image.load('resources/bomb.png')
ex = random.randint(0, 550)
ey = 50
es = 10
ew = 32
ew = 32

#enemy == bomb
def draw_enemy(x, y):

    """blits enemy onto screen"""

    screen.blit(enemy_img, (x, y))

#basketball
ball_img = pygame.image.load('resources/basketball.png')
bx = random.randint(0, 550)
by = 50
bs = 10
bw = 32
bh = 32

def draw_ball(x, y):

    """displays basketball onto screen"""

    screen.blit(ball_img, (x, y))

def collision_check(px, py, a, b):

    """checks for a collision between two points"""

    distance = math.sqrt(math.pow(px - a, 2) + (math.pow(py - b, 2)))
    if distance < 27:
        return True
    else:
        return False

#timekeeping variables
score = 0
clock = pygame.time.Clock()
time_elapsed = 0

#x and y values to blit time elapsed and score/game over texts
TX = 10
TY = 10
GOX = 300
GOY = 400
font = pygame.font.Font('freesansbold.ttf', 16)
game_over_font = pygame.font.Font('freesansbold.ttf', 32)

def show_score(x, y):

    """displays score on screen"""

    dis_score = font.render("Score : " + str(score), True, (255, 255, 255))
    screen.blit(dis_score, (x, y))

def game_over(x, y):

    """displays a game over message if player has lost"""

    game_over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over_text, (x, y))

#show intro message
message_box()

#main game loop
run = True
while run:

#sound effects
    bomb_effect = mixer.Sound('resources/explosion.wav')
    swish_effect = mixer.Sound('resources/swish.wav')

#time delay
    pygame.time.delay(100)

#display background
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

#movement mechanics
    key = pygame.key.get_pressed()

    if key[pygame.K_LEFT] and px > ps:
        px -= ps
    if key[pygame.K_RIGHT] and px < 600 - pw - ps   :
        px += ps
    if key[pygame.K_UP] and py > ps:
        py -= ps
    if key[pygame.K_DOWN] and py < 800 - ph - ps:
        py += ps

#display sprites
    draw_player(px, py)
    draw_ball(bx, by)
    draw_enemy(ex, ey)

#makes ball and bomb and obstacles fall
    by += bs
    ey += es

#collision check (ball) and playing swish sound effect
    caught_ball = collision_check(px, py, bx, by)
    if caught_ball:
        swish_effect.play(1)
        bx = random.randint(0, 550)
        by = -25
        bs += 1
        score += 1
    elif not caught_ball and by >= 800:
        game_over(GOX, GOY)
        print("Game Over!\nscore:", score, "\nThanks for playing!")
        run = False

#collision check (bomb) and playing explosion sound effect
    caught_bomb = collision_check(px, py, ex, ey)
    if caught_bomb:
        bomb_effect.play(2)
        game_over(GOX, GOY)
        print("Game Over!\nscore:", score, "\nThanks for playing!")
        run = False

#blits bomb back to top if player has successfully avoided bomb
    if ey > 800:
        ex = random.randint(0, 550)
        ey = -25

#updating the time elapsed on screen
    curr_time = clock.tick()/1000.0
    time_elapsed += curr_time
    display_clock = math.trunc(time_elapsed)
    clock_text = font.render("Time elapsed: " + str(display_clock), True, (255, 255, 255))
    screen.blit(clock_text, (460, 10))

#displaying and updating the player's score
    show_score(TX, TY)

    pygame.display.update()
