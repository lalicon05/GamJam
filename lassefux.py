#imports needed libraries
import pygame

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
        self.world_x = 0
        self.world_y = 0

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

#object for the world
class World:
    def __init__(self):
        #list of rects that will act as terrain in the world
        self.terrain = [] 

    def draw(self):
        for terr_part in range(len(self.terrain)):
            self.temp_rect = self.terrain[terr_part]



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
world1 = World()

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
            if(player.map_x) < ((screen.get_width() / 2) + 75):
                player.map_x += player.movespeed
            else:
                player.world_x += player.movespeed

        if(keys[pygame.K_a]):
            #movement to the left
            if(player.map_x) > ((screen.get_width() / 2) - 75):
                player.map_x -= player.movespeed
            else:
                player.world_x -= player.movespeed

        if(keys[pygame.K_w]):
            #movement up
            if(player.map_y) > ((screen.get_height() / 2) - 75):
                player.map_y -= player.movespeed
            else:
                player.world_y -= player.movespeed

    if(keys[pygame.K_s]):
        #movement down
        if(player.map_y) < ((screen.get_height() / 2) + 75):
            player.map_y += player.movespeed
        else:
            player.world_y += player.movespeed


    #fyller skjermen med hvit
    screen.fill('white')

    #updates the player
    player.update()

    #draws the player
    player.draw()


    draw_text(f"player.x: {player.x}  player.y: {player.y}", text_font_small, 'black', 120, screen.get_height() - 15)
    #flips the diaplay
    pygame.display.flip()
    #makes the time move
    clock.tick(60)

#quits the game if the loop is exited
pygame.quit()