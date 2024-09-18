import pygame
import pygame, json, random, glob, ast, sys, os, math
from pygame.locals import *

WIN_WIDTH = 900     # 180 tiles across
WIN_HEIGHT = 600    # 120 tiles down
WIN_SCALE = 2
TILE_SIZE = 5

mac = False
if mac : WIN_SCALE = 1

# ASSETS =====================================

i_tile = pygame.image.load('../res/tile.png')
i_dirt = pygame.image.load('../res/dirt.png')
i_debug = pygame.image.load('../res/debug.png')

# HELPER DATA =====================================

display_window = pygame.display.set_mode((WIN_WIDTH * WIN_SCALE, WIN_HEIGHT * WIN_SCALE), 0, 32)
raw_window = pygame.Surface((WIN_WIDTH,WIN_HEIGHT))

clock = pygame.time.Clock()

frame_start = 0
frame_end = pygame.time.get_ticks()
dt = frame_end - frame_start

playing = True

# MAIN GAME LOOP =====================================

while playing:
    raw_window.fill((0,0,0))
    
    for event in pygame.event.get() :
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN : 
            if event.key == K_ESCAPE:
                playing = False


    scaled_window = pygame.transform.scale(raw_window, display_window.get_size())
    display_window.blit(scaled_window, (0,0))
    pygame.display.update()
    # ==============================
    frame_end = pygame.time.get_ticks()
    dt = frame_end - frame_start
    clock.tick(60)

pygame.quit()
sys.exit()