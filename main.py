# EVOLVE PLAYABLE DUNGEONS FOR AN IMAGINARY ROGUELIKE
# PHENOTYPE : 2D MATRICES
#     each cell is a free space, wall, starting point, exit, monster, treasure
#     other types of stuff: traps, teleporters, doors, keys
# EXPLORE DIFFERENT CONTENT REPRESENTATIONS AND QUALITY MEASURES

# REMEMBER: the pillars at work here are:
#     a search algorithm
#     a content representation
#     an evaluation function
# ==============================================================
import pygame
import pygame, json, random, glob, ast, sys, os, math
from pygame.locals import *

WIN_WIDTH = 900
WIN_HEIGHT = 600
WIN_SCALE = 2

TILE_SIZE = 5
# 180 tiles across
# 120 tiles down

# ASSETS =====================================

i_tile = pygame.image.load('./tile.png')
i_dirt = pygame.image.load('./dirt.png')

# HELPER DATA =====================================

display_window = pygame.display.set_mode((WIN_WIDTH * WIN_SCALE, WIN_HEIGHT * WIN_SCALE), 0, 32)
raw_window = pygame.Surface((WIN_WIDTH,WIN_HEIGHT))

clock = pygame.time.Clock()

frame_start = 0
frame_end = pygame.time.get_ticks()
dt = frame_end - frame_start

playing = True

# each cell is a free space, wall, starting point, exit, monster, or treasure
    # walls and free spaces make up rooms
        # rooms are dictated by 1) a top left corner 2) dimensions
    # within those rooms we can place the monsters and treasure
    # two walls are replaced with an entrance and an exit
    # the rooms are connected ******** this one is important - how are they connected? in order? or as a complete graph? ************
gene = {
    'walls' : [],
    'rooms' : []
}

# HELPER FUNCTIONS =====================================

# I have a random room being generated at different points of the map. 
# My current connundrum is: how do I get other rooms to spawn as well that don't conflict with each other

class Room() :
    def __init__(self, corner : tuple, dims : tuple) -> None:
        self.corner : tuple = corner
        self.dims   : tuple = dims

def generateGenotype() -> list :
    # a room is a pair of coordinates and a pair of dimensions 

    # GENERATE ENTRANCE ROOM
    # decide which quadrant
    entry_quad = random.randrange(0,3)
    exit_quad = (entry_quad + 2) % 4
    quads = {
        0 : Room((0, 0), (90, 60)) ,
        1 : Room((int((WIN_WIDTH / 2) / TILE_SIZE), 0), (90, 60)) ,
        2 : Room((int((WIN_WIDTH / 2) / TILE_SIZE), int((WIN_HEIGHT / 2) / TILE_SIZE)), (90, 60)) ,
        3 : Room((0, int((WIN_HEIGHT / 2) / TILE_SIZE)), (90, 60)) 
    }

    # place a room of any size somewhere in the middle rectangle
    x_rand = math.floor(random.randrange(225, 775) / 10) * 10
    y_rand = math.floor(random.randrange(150, 450) / 10) * 10

    entry_room = Room(
        (int(x_rand / TILE_SIZE), int(y_rand / TILE_SIZE)),
        (20, 10)
    )

    return [entry_room]

# IMPORTANT : never forget to convert between pixels and tiles as needed

# right now, the genotype that is getting passed in is a list of Room objects
# where 0 is the top left corner and 1 is the dimensions spanning from that corner
def outputPhenotype(genotype : list) :
    # each cell represents a 5x5 tile
    phenotype = [[0 for x in range(int(WIN_WIDTH / TILE_SIZE))] for y in range(int(WIN_HEIGHT / TILE_SIZE))]
    
    for room in genotype :        
        for i in range(room.dims[1]) : 
            for j in range(room.dims[0]) :
                phenotype[room.corner[1] + i][room.corner[0] + j] = 1


    return phenotype

# MAIN GAME LOOP =====================================

gene = generateGenotype()
fein = outputPhenotype(gene)

while playing:
    raw_window.fill((0,0,0))
    
    for event in pygame.event.get() :
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN : 
            if event.key == K_ESCAPE:
                playing = False



    for i in range(len(fein)) :
        for j in range(len(fein[0])) :
            if fein[i][j] == 0 :
                # pygame.draw.rect(raw_window, (0,200,0), pygame.Rect(j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                raw_window.blit(i_tile, pygame.Rect(j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            else :
                # pygame.draw.rect(raw_window, (0,200,0), pygame.Rect(j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                raw_window.blit(i_dirt, pygame.Rect(j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # pygame.draw.rect(raw_window, (0,0,100), pygame.Rect(225, 150, 450, 300))

    scaled_window = pygame.transform.scale(raw_window, display_window.get_size())
    display_window.blit(scaled_window, (0,0))
    pygame.display.update()
    # ==============================
    frame_end = pygame.time.get_ticks()
    dt = frame_end - frame_start
    clock.tick(60)

pygame.quit()
sys.exit()
