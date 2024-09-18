# 1) binary space partitioning
# 2) agent based generation
# 3) cellular automata
# ============================================
import pygame
import pygame, json, random, glob, ast, sys, os, math
from pygame.locals import *

WIN_WIDTH = 900     # 180 tiles across
WIN_HEIGHT = 600    # 120 tiles down
WIN_SCALE = 2
TILE_SIZE = 5

mac = True
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

# HELPER FUNCTIONS =====================================


class Room() :
    def __init__(self, corner : tuple, dims : tuple) -> None:
        self.corner : tuple = corner    # in TILES - converted from px if needed
        self.dims   : tuple = dims      # in TILES - converted from px if needed

    # given the self as the root node, return a list of the list of leaf nodes obtained from
    # applying a BSP to it
    def bsp(self, depth) -> list:
        # 1) set current node as a BSP node
        # 2) if it can be partitioned, split it and repeat
        # 3) if not, return a flag saying so
        pass

# NOTE: in theory, the room here should be interchangeable with whatever this gets pasted into
class BTreeNode() :
    def __init__(self, room : Room) -> None:
        self.room = room
        # NOTE: is there any merit to having this be a list? this would be necessary for more than two children
        self.left = None
        self.right = None

# if we were to think in terms of geno/pheno type here, the genotype would be the 
# list of leaf nodes, which basically translates to the same list of rooms we had b4

# with this in mind, my goal is to pass in the whole space to something, and from that
# to be able to get a list of rooms

def generateGenotype() -> list :
    # 1) set the whole space as a room
    root = Room((0,0), (WIN_WIDTH / TILE_SIZE, WIN_HEIGHT / TILE_SIZE)) 
    # 2) partition it
    room_layout = root.bsp()
    # 3) boom
    return room_layout


def outputPhenotype(genotype : list) -> list:
    # each cell represents a 5x5 tile
    phenotype : list[list[int]] = [[0 for x in range(int(WIN_WIDTH / TILE_SIZE))] for y in range(int(WIN_HEIGHT / TILE_SIZE))]

    for room in genotype :        
        for i in range(room.dims[1]) : 
            for j in range(room.dims[0]) :
                phenotype[room.corner[1] + i][room.corner[0] + j] = 1

    # NOTE: temporarily adding note on the top left corners of rooms
    for room in genotype :
        phenotype[room.corner[1]][room.corner[0]] = 2
        phenotype[room.corner[1] + room.dims[1] - 1][room.corner[0] + room.dims[0] - 1] = 2

    return phenotype

genotype = generateGenotype()
# phenotype = outputPhenotype(genotype)

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