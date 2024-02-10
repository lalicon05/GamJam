#imports needed libraries
import pygame
import random
import math

#setting up the essentials -------------------------------------------------------------------------------------------------
pygame.init() #
screen = pygame.display.set_mode((800, 450))
pygame.display.set_caption(r"Lassefux")
clock = pygame.time.Clock()
running = True


in_world = True

#objects -------------------------------------------------------------------------------------------------------------
class Player:
    def __init__(self):
        #position on the screen
        self.map_x = screen.get_width() / 2
        self.map_y = screen.get_height() / 2

        #position in the world
        self.world_x = 1000
        self.world_y = 1000

        #players absolute pos in the world
        self.x = self.map_x + self.world_x
        self.y = self.map_y + self.world_y

        self.movespeed = 3

        #players size
        self.size = 40

    #function to draw the player
    def draw(self):
        pygame.draw.rect(screen, 'blue', self.rect)

    #function to update the player
    def update(self):
        self.rect = pygame.Rect(self.map_x - self.size / 2, self.map_y - self.size / 2, self.size, self.size)
        self.x = self.map_x + self.world_x
        self.y = self.map_y + self.world_y

#object for terrain
class Terrain:
    def __init__(self, x : int, y : int, x_size : int, y_size : int):

        #where in the world
        self.base_x = x
        self.base_y = y
        self.x = x
        self.y = y

        #size of terrain rect
        self.x_size = x_size
        self.y_size = y_size

        #creates the rectangle for the object
        self.rect = pygame.Rect(self.base_x - (self.x_size / 2), self.base_y - (self.y_size / 2), self.x_size, self.y_size)
        #randomly selects a color for terrain rect
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    #function to draw this terrain rect
    def draw(self):
        self.rect = pygame.Rect(self.x - player.world_x - (self.x_size / 2), self.y - player.world_y - (self.y_size / 2), self.x_size, self.y_size)
        pygame.draw.rect(screen, self.color, self.rect)

    def reset(self):
        #function to call when resetting the world
        self.x = self.base_x
        self.y = self.base_y



#object for the world
class World:
    def __init__(self, worldnr: int, chunk_size: int):
        self.terrain = []
        self.sheet = pygame.image.load('lassefux1.png').convert_alpha()
        self.this_world = worldnr
        self.chunk_size = chunk_size
        self.current_chunk_x = 0
        self.current_chunk_y = 0

        with open("world" + str(self.this_world) + ".txt", "w") as file:
            for y in range(200):
                for x in range(200):
                    file.write(str(random.randint(0, 1)))
                file.write('\n')
            file.close()

    def create_background(self):
        self.tile1 = (0, 0, 24, 24)
        self.tile2 = (24, 0, 48, 24)
        with open("world" + str(self.this_world) + ".txt", "r") as file:
            self.lines = file.readlines()
        file.close()

    def update_chunk_position(self):
        self.current_chunk_x = int(player.x / self.chunk_size)
        self.current_chunk_y = int(player.y / self.chunk_size)

    def draw(self):
        self.update_chunk_position()

        # Calculate the visible range of chunks based on the screen size
        visible_chunk_x_start = max(0, self.current_chunk_x - screen.get_width() // (2 * self.chunk_size) - 1)
        visible_chunk_x_end = min(len(self.lines[0]), visible_chunk_x_start + screen.get_width() // self.chunk_size + 2)
        visible_chunk_y_start = max(0, self.current_chunk_y - screen.get_height() // (2 * self.chunk_size) - 1)
        visible_chunk_y_end = min(len(self.lines), visible_chunk_y_start + screen.get_height() // self.chunk_size + 3)

        for y in range(visible_chunk_y_start, visible_chunk_y_end):
            for x in range(visible_chunk_x_start, visible_chunk_x_end):
                image = pygame.Surface((24, 24)).convert_alpha()
                if self.lines[y][x] == '0':
                    image.blit(self.sheet, (0, 0), self.tile1)
                else:
                    image.blit(self.sheet, (0, 0), self.tile2)

                image = pygame.transform.scale(image, (72, 72))
                image.set_colorkey('BLACK')
                screen.blit(image, (x * 72 - player.world_x, y * 72 - player.world_y))

        for terr_part in range(len(self.terrain)):
            self.terrain[terr_part].draw()






#functions ----------------------------------------------------------------------------------------------------------

#function to draw text
text_font_small = pygame.font.SysFont("Arial", 14) # liten tekst
text_font_medium = pygame.font.SysFont("Arial", 36) # Medium tekst
text_font_large = pygame.font.SysFont("Arial", 48) # Stor tekst
#Function to draw text
def draw_text(text : str, font : pygame.font.Font, text_col : pygame.Color, x : int, y : int): #Funksjon som brukes for å lage tekst.
    img = font.render(text, True, text_col)
    tekst_rect = img.get_rect(center=(x, y))
    screen.blit(img, tekst_rect)

#creates objects---------------------------------------------------------------------------------------------------------

#creates the player
player = Player()

#creates world 1
world1 = World(0, 72)
world1.terrain.append(Terrain(100, 90, 50, 50))
world1.terrain.append(Terrain(200, 120, 80, 50))
world1.terrain.append(Terrain(100, 450, 50, 70))
world1.terrain.append(Terrain(300, 150, 50, 50))
world1.terrain.append(Terrain(200, -100, 50, 50))

world1.create_background()


#runs the game --------------------------------------------------------------------------------------------------
while running:
    #quits the game if user closes the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    #inputs -----------------------------------------------------------------
    keys = pygame.key.get_pressed()

    #game logic ------------------------------------------------------------------------------------------------------------------------------------
    if in_world:
        if(keys[pygame.K_d]):
            #movement to the right
            if(keys[pygame.K_w]) or (keys[pygame.K_s]):
                if(player.map_x) < ((screen.get_width() / 2) + 10):
                    player.map_x += player.movespeed / math.sqrt(2)
                else:
                    player.world_x += player.movespeed / math.sqrt(2)
            else:
                if(player.map_x) < ((screen.get_width() / 2) + 10):
                    player.map_x += player.movespeed
                else:
                    player.world_x += player.movespeed

        if(keys[pygame.K_a]):
            #movement to the left
            if(keys[pygame.K_w]) or (keys[pygame.K_s]):
                if(player.map_x) > ((screen.get_width() / 2) - 10):
                    player.map_x -= player.movespeed / math.sqrt(2)
                else:
                    player.world_x -= player.movespeed / math.sqrt(2)
            else:
                if(player.map_x) > ((screen.get_width() / 2) - 10):
                    player.map_x -= player.movespeed
                else:
                    player.world_x -= player.movespeed

        if(keys[pygame.K_w]):
            #movement up
            if(keys[pygame.K_a]) or (keys[pygame.K_d]):
                if(player.map_y) > ((screen.get_height() / 2) - 10):
                    player.map_y -= player.movespeed / math.sqrt(2)
                else:
                    player.world_y -= player.movespeed / math.sqrt(2)
            else:
                if(player.map_y) > ((screen.get_height() / 2) - 10):
                    player.map_y -= player.movespeed
                else:
                    player.world_y -= player.movespeed

    if(keys[pygame.K_s]):
        #movement down
        if(keys[pygame.K_a]) or (keys[pygame.K_d]):
            if(player.map_y) < ((screen.get_height() / 2) + 10):
                player.map_y += player.movespeed / math.sqrt(2)
            else:
                player.world_y += player.movespeed / math.sqrt(2)
        else:
            if(player.map_y) < ((screen.get_height() / 2) + 10):
                player.map_y += player.movespeed
            else:
                player.world_y += player.movespeed


#gameloop --------------------------------------------------------------------------------------------------------
                
    screen.fill('white')

    #updates the player
    player.update()

    #draws the world
    world1.draw()

    #draws the player
    player.draw()


    draw_text(f"player.x: {round(player.x)}  player.y: {round(player.y)}", text_font_small, 'black', 120, screen.get_height() - 15)
    draw_text(f"fps : {round(clock.get_fps())}", text_font_small, 'black', 30, 20)
    #flips the diaplay
    pygame.display.flip()
    #makes the time move
    clock.tick(60)

#quits the game if the loop is exited
pygame.quit()