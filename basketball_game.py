#---------------------------basketball.py--------------------------------------#
#by Akeel Majeed

#import libraries
import random
import math
import pygame

#initilise the game
pygame.init()

#for messagebox
from tkinter import *
import tkinter.messagebox

def message_box():
    root = Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    tkinter.messagebox.showinfo("Basketball Game", "Welcome to my Game!\nYou control the hoop!\nYour job is to catch the basketball and avoid the bomb!")
    try:
        root.destroy()
    except:
        pass

#for the tunes
from pygame import mixer

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

#displays player
def draw_player(x, y):
    screen.blit(player_img, (x, y))

#enemy
enemy_img = pygame.image.load('resources/bomb.png')
ex = random.randint(0, 550)
ey = 50
es = 10
ew = 32
ew = 32

#displays enemy
def draw_enemy(x, y):
    screen.blit(enemy_img, (x, y))

#basketball
ball_img = pygame.image.load('resources/basketball.png')
bx = random.randint(0, 550)
by = 50
bs = 10
bw = 32
bh = 32

#displays basketball
def draw_ball(x, y):
    screen.blit(ball_img, (x, y))

#collision checker function (27 == 1cm)
def collision_check(px, py, a, b):
    distance = math.sqrt(math.pow(px - a, 2) + (math.pow(py - b, 2)))
    if distance < 27:
        return True
    else:
        return False

#displays score and timer on screen
score = 0
clock = pygame.time.Clock()
time_elapsed = 0

tx = 10
ty = 10
gox = 300
goy = 400
font = pygame.font.Font('freesansbold.ttf', 16)
game_over_font = pygame.font.Font('freesansbold.ttf', 32)

def show_score(x, y):
    dis_score = font.render("Score : " + str(score), True, (255, 255, 255))
    screen.blit(dis_score, (x, y))

def game_over(x, y):
    game_over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over_text, (x, y))

#show intro
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

#collision checker (ball) and playing swish sound effect
    collision_check1 = collision_check(px, py, bx, by)
    if collision_check1:
        swish_effect.play(1)
        bx = random.randint(0, 550)
        by = -25
        bs += 1
        score += 1
    elif collision_check1 == False and by >= 800:
        game_over(gox, goy)
        print("Game Over!\nscore:", score, "\nThanks for playing!")
        run = False

#collision check (bomb) and playing explosion sound effect
    collison_check2 = collision_check(px, py, ex, ey)
    if collison_check2:
        bomb_effect.play(2)
        game_over(gox, goy)
        print("Game Over!\nscore:", score, "\nThanks for playing!")
        run = False

#when ball and bomb hits floor goes to top again
    if by > 800:
        bx = random.randint(0, 550)
        by = -25

    if ey > 800:
        ex = random.randint(0, 550)
        ey = -25

#updating score and clock on screen

    curr_time = clock.tick()/1000.0
    time_elapsed += curr_time
    display_clock = math.trunc(time_elapsed)
    clock_text = font.render("Time elapsed: " + str(display_clock), True, (255, 255, 255))
    screen.blit(clock_text, (460, 10))
    show_score(tx, ty)

    pygame.display.update()
