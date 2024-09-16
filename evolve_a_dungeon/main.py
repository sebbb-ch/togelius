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

WIN_WIDTH = 900     # 180 tiles across
WIN_HEIGHT = 600    # 120 tiles down
WIN_SCALE = 2
TILE_SIZE = 5

mac = True
if mac : WIN_SCALE = 1

# ASSETS =====================================

i_tile = pygame.image.load('./tile.png')
i_dirt = pygame.image.load('./dirt.png')
i_debug = pygame.image.load('./debug.png')

# HELPER DATA =====================================

display_window = pygame.display.set_mode((WIN_WIDTH * WIN_SCALE, WIN_HEIGHT * WIN_SCALE), 0, 32)
raw_window = pygame.Surface((WIN_WIDTH,WIN_HEIGHT))

clock = pygame.time.Clock()

frame_start = 0
frame_end = pygame.time.get_ticks()
dt = frame_end - frame_start

playing = True

# IMPORTANT : never forget to convert between pixels and tiles as needed

# HELPER FUNCTIONS =====================================

class Room() :
    def __init__(self, corner : tuple, dims : tuple) -> None:
        self.corner : tuple = corner    # in TILES - converted from px if needed
        self.dims   : tuple = dims      # in TILES - converted from px if needed

    def containsPoint(self, point : tuple) -> bool: 
        x_range = range(self.corner[0], self.corner[0] + self.dims[0])
        y_range = range(self.corner[1], self.corner[1] + self.dims[1])
        if (point[0] in x_range) and (point[1] in y_range) :
            return True
        return False

    # check the closest corner of the foreign room for containment in the self
    # closest corner is determined by cardinal direction
    def conflictsWith(self, room : 'Room') -> bool:
        # check for foreign room corner containment in self
        if self.containsPoint(room.corner) :
            return True
        # ================================
        relative_direction : str = ""
        if room.corner[1] < self.corner[1] :
            relative_direction += "N"
            if room.corner[0] < self.corner[0] :
                relative_direction += "W"
            else :
                relative_direction += "E"
        else :
            relative_direction += "S"
            if room.corner[0] < self.corner[0] :
                relative_direction += "W"
            else :
                relative_direction += "E"
        # ================================
        point = None
        if relative_direction == "NW" : # check foreign's bottom right corner for containment
            point = (room.corner[0] + room.dims[0], room.corner[1] + room.dims[1])
        if relative_direction == "NE" : # check foreign's bottom left corner for containment
            point = (room.corner[0], room.corner[1] + room.dims[1])
        if relative_direction == "SW" : # check foreign's top right corner for containment
            point = (room.corner[0] + room.dims[0], room.corner[1])
        # this should be superfluous!!!
        if relative_direction == "SE" : # check foreign's top left corner for containment
            point = (room.corner[0] + room.dims[0], room.corner[1] + room.dims[1])

        if self.containsPoint(point) :
            return True
        return False



# this is the "first level of translation" - we convert our notion of a room, and put it into code
# in this case, a top-left corner and a pair of dimensions are our notion of a room, and are easily put into code.
# tolerance - parameter to determine how many failed attempts at placing rooms are allowed before terminating loop
def generateGenotype(tolerance : int) -> list :
    x_rand = int(math.floor(random.randrange(int(WIN_WIDTH / 4), int((WIN_WIDTH  * 3) / 4))) / TILE_SIZE)
    y_rand = int(math.floor(random.randrange(int(WIN_HEIGHT / 4), int((WIN_HEIGHT  * 3) / 4))) / TILE_SIZE)
    
    central_room = Room(
        (x_rand, y_rand),
        (30, 30) # NOTE : 30x30 is the largest room size that doesn't cause bounding errors, given the size of the middle room
    )
 
    # TODO : any new room will need to be compared against every other room that already exists 
    # this is probably inefficient at first go, but fuck it we ball
    genotype : list[Room] = [central_room]

    for i in range(10) :
        x_dim = math.floor(random.randrange(10, 20))
        y_dim = math.floor(random.randrange(10, 20))
        x_corner = math.floor(random.randrange(1, int(WIN_WIDTH / TILE_SIZE) - x_dim))
        y_corner = math.floor(random.randrange(1, int(WIN_HEIGHT / TILE_SIZE) - y_dim))
        protoroom = Room((x_corner, y_corner), (x_dim, y_dim))
        print(len(genotype))
        # I KNOW MY MISTAKE - IT WAS ADDING DUPLICATE ROOMS!!!!
        # EVERY TIME A NON CONFLICT WAS ENCOUNTERED IT ADDED THE SAME ROOM
        safe = True
        for room in genotype :
            if room.conflictsWith(protoroom) :
                safe = False
                break
        
        if safe :
            genotype.append(protoroom)


    # NOTE : a certain allowance for overlapping square rooms could lead to more interesting shapes/rooms
    # t = tolerance
    # while t > 0 :
    #     x_dim = math.floor(random.randrange(10, 20))
    #     y_dim = math.floor(random.randrange(10, 20))
    #     x_corner = math.floor(random.randrange(1, int(WIN_WIDTH / TILE_SIZE) - x_dim))
    #     y_corner = math.floor(random.randrange(1, int(WIN_HEIGHT / TILE_SIZE) - y_dim))
    #     r = Room((x_corner, y_corner), (x_dim, y_dim))

    #     for room in genotype :
    #         if r.conflictsWith(room) :
    #             t -= 1
    #         else :
    #             genotype.append(r)
    
    return genotype

def outputPhenotype(genotype : list) :
    # each cell represents a 5x5 tile
    phenotype = [[0 for x in range(int(WIN_WIDTH / TILE_SIZE))] for y in range(int(WIN_HEIGHT / TILE_SIZE))]

    for room in genotype :        
        for i in range(room.dims[1]) : 
            for j in range(room.dims[0]) :
                phenotype[room.corner[1] + i][room.corner[0] + j] = 1

    return phenotype

# MAIN GAME LOOP =====================================

gene = generateGenotype(100)
phenotype = outputPhenotype(gene)

while playing:
    raw_window.fill((0,0,0))
    
    for event in pygame.event.get() :
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN : 
            if event.key == K_ESCAPE:
                playing = False

    # i and j represent the tile coord numbers - hence they need to be mutiplied by T_S
    for i in range(len(phenotype)) :
        for j in range(len(phenotype[0])) :
            if phenotype[i][j] == 0 :
                raw_window.blit(i_tile, pygame.Rect(j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            else :
                raw_window.blit(i_dirt, pygame.Rect(j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    scaled_window = pygame.transform.scale(raw_window, display_window.get_size())
    display_window.blit(scaled_window, (0,0))
    pygame.display.update()
    # ==============================
    frame_end = pygame.time.get_ticks()
    dt = frame_end - frame_start
    clock.tick(60)

pygame.quit()
sys.exit()
