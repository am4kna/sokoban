import pygame
from pygame.locals import *
import time

# Configure your parameters
capture_interval = 5  # seconds between frames

pygame.init()

screen_width = 1040
screen_height = 720

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')

tile_size= 80
# Load images
bg_img = pygame.image.load('img/floor.png')
bg_img =pygame.transform.scale(bg_img , (screen_width, screen_height))

def draw_grid():
    for line in range(0, 15):
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))

class World():
    def __init__(self, data):
        self.tile_list = []

        # Load images
        wall_img = pygame.image.load('img/wall.png')
        floor_img = pygame.image.load('img/floor.png')
        storage_img = pygame.image.load('img/storage.png')
        box_img = pygame.image.load('img/box.png')
        boxTarget_img = pygame.image.load('img/boxTarget.png')
        robotTarget_img = pygame.image.load('img/playerTarget.png')
        player_img = pygame.image.load('img/player.png')  # Assuming you have an image for the player

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                img = None
                img_rect = None
                
                if tile == 'O':  # Wall (Obstacle)
                    img = pygame.transform.scale(wall_img, (tile_size, tile_size))
                    
                elif tile == ' ':  # Empty space
                    img = pygame.transform.scale(floor_img, (tile_size, tile_size))
                
                elif tile == 'S':  # Target space (Storage)
                    img = pygame.transform.scale(storage_img, (tile_size, tile_size))
                    
                elif tile == 'B':  # Box (Block)
                    img = pygame.transform.scale(box_img, (tile_size, tile_size))
                    
                elif tile == '.':  # Player on a target space
                    img = pygame.transform.scale(robotTarget_img, (tile_size, tile_size))
                    
                elif tile == '*':  # Box on a target space
                    img = pygame.transform.scale(boxTarget_img, (tile_size, tile_size))
                    
                elif tile == 'R':  # Player (Robot)
                    img = pygame.transform.scale(player_img, (tile_size, tile_size))
                
                # Set the image position and add to the tile list
                if img is not None:
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    self.tile_list.append((img, img_rect))
                
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])




world_data = [
            ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
            ['O', ' ', ' ', ' ', ' ', 'O', 'O', 'O', 'S', ' ', ' ', ' ', 'O'],
            ['O', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'O'],
            ['O', ' ', ' ', ' ', ' ', 'O', 'O', 'O', ' ', ' ', ' ', ' ', 'O'],
            ['O', ' ', ' ', ' ', ' ', 'O', 'O', 'O', ' ', ' ', ' ', '*', 'O'],
            ['O', 'R', ' ', ' ', ' ', 'O', 'O', 'O', ' ', 'S', ' ', ' ', 'O'],
            ['O', ' ', ' ', ' ', ' ', 'O', 'O', 'O', ' ', ' ', ' ', ' ', 'O'],
            ['O', ' ', ' ', ' ', ' ', 'O', 'O', 'O', ' ', 'S', ' ', '*', 'O'],
            ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']
            
]
world_data2 = [
            ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
            ['O', ' ', ' ', ' ', ' ', 'O', 'O', 'O', 'S', ' ', ' ', ' ', 'O'],
            ['O', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', 'O'],
            ['O', ' ', ' ', ' ', ' ', 'O', 'O', 'O', ' ', ' ', ' ', ' ', 'O'],
            ['O', ' ', ' ', ' ', ' ', 'O', 'O', 'O', ' ', ' ', ' ', '*', 'O'],
            ['O', ' ', ' ', ' ', ' ', 'O', 'O', 'O', ' ', '.', ' ', ' ', 'O'],
            ['O', ' ', ' ', ' ', ' ', 'O', 'O', 'O', ' ', ' ', ' ', ' ', 'O'],
            ['O', ' ', ' ', ' ', ' ', 'O', 'O', 'O', ' ', '*', ' ', '*', 'O'],
            ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']
]

def update_world(world_data):
    world = World(world_data) 
    world.draw() 

last_update_time = pygame.time.get_ticks()  # Start the timer

run = True
while run:
    screen.blit(bg_img, (0, 0))
    update_world(world_data)
    #draw_grid()
	
    current_time = pygame.time.get_ticks()
    if current_time - last_update_time >= 2000:
        world_data = world_data2 
        last_update_time = current_time  # Reset the timer


    for event in pygame.event.get():
	    if event.type == pygame.QUIT:
		    run = False
    pygame.display.update()

pygame.quit()


