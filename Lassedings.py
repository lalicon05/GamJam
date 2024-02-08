import pygame

#setter opp det essensielle for spillet
pygame.init()
screen = pygame.display.set_mode((800*1.2, 450*1.2)) # Setter skjermen til 500x500 piksler.
clock = pygame.time.Clock()
running = True

sprite_sheet_image = pygame.image.load("spritesheet.png").convert_alpha()


#lager objekter -----------------------------------------------------------------------
class Player:
    def __init__(self):
        #alt basic som settes opp
        self.pos = [0, 0]
        self.mappos = [0, 0]
        self.size = 24
        self.rect = pygame.Rect(0 - self.size / 2, 0 - self.size / 2, self.size, self.size)
        self.sheet = sprite_sheet_image

        self.speed = 3

        self.right = (0, 0, 24 , 24)
        self.left = (72, 0, 24 , 24)
        self.up = (24, 0, 24 , 24)
        self.down = (48, 0, 24 , 24)
        #retning
        self.facing = self.right

        #hvor stor spiller sprite skal være
        self.scale = 2
        self.rect = pygame.Rect(self.mappos[0] - self.size * self.scale / 2, self.mappos[1] - self.size * self.scale / 2, self.size * self.scale, self.size * self.scale)

    #funksjon for å tegne spiller
    def draw(self):
        self.image = pygame.Surface((24 * self.scale, 24*self.scale)).convert_alpha()
        self.image.blit(self.sheet, (0, 0), self.facing)
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.image.set_colorkey('BLACK')
        screen.blit(self.image, (screen.get_width() / 2, screen.get_height() / 2))

class Npc:
    def __init__(self, x, y):
        self.size = 48
        self.x = x
        self.y = y
        self.rect = pygame.Rect(100 + x - self.size / 2, 100 + y - self.size / 2, self.size, self.size)
        self.color = ("blue")
    
    def draw(self):
        self.x = player.pos[0]
        self.y = player.pos[1]
        self.rect = pygame.Rect(100 + self.x - self.size / 2, 100 + self.y - self.size / 2, self.size, self.size)
        pygame.draw.rect(screen, self.color, self.rect)


#lager objekter ---------------------------------------
player = Player()
gertrude = Npc(player.pos[0], player.pos[1])

while running:
    # Avslutter løkken
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()

    if(keys[pygame.K_a]):
        player.facing = player.left
        player.pos[0] += player.speed
    if(keys[pygame.K_d]):
        player.facing = player.right
        player.pos[0] -= player.speed
    if(keys[pygame.K_s]):
        player.facing = player.down
        player.pos[1] -= player.speed
    if(keys[pygame.K_w]):
        player.facing = player.up
        player.pos[1] += player.speed




    # Fyller skjermen med hvit farge
    screen.fill("white")

    
    

    Player.draw(player)
    Npc.draw(gertrude)
    # Oppdaterer hele skjermen
    pygame.display.flip()

    # Forsikrer at spillet kjører i maksimalt 60 FPS.
    clock.tick(60)

# Avslutter spillet
pygame.quit()