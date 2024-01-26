#imports
import pygame
import math

#Setter opp det essensielle
pygame.init()
screen = pygame.display.set_mode((768, 480)) # Setter skjermen til 500x500 piksler.
pygame.display.set_caption(r"Isak's Kjeller-eventyr")
clock = pygame.time.Clock()
running = True

#Klasse for spillerobjekt
class Spiller:
    #setter opp variabler/attributter for spiller
    def __init__(self):
        #alt som har med start å gjøre
        self.max_hp = 3
        self.hp = self.max_hp
        self.x = screen.get_width() / 2
        self.y = screen.get_height() / 2

        #alt som har med bevegelse og retning å gjøre
        self.retning = [0, 0]
        self.skyt_retning = [0, 0]

        #alt som har med utseende å gjøre
        self.size = 25
        self.color = 'black'
        
        #alt som har med diverse stats å gjøre
        self.speed = 6
        self.attackspeed = 3
        self.last_attack = 0
        self.facing_r = 1
        self.facing_u = 1

        #alt som har ,med å tegne spriten å gjøre
        self.sheet = sprite_sheet_image
        self.sprite_w = 24
        self.sprite_h = 24
        self.scale = 1.4

        self.sprite_face_left = (0, 0, 24 , 24)
        self.sprite_face_right = (25, 0, 48 , 24)
        self.sprite_face_up = (49, 0, 72 , 24)
        self.sprite_face_down =(73, 0, 96 , 24)
        self.TheSprite = (0, 0, 24 , 24)

    #funksjon for å tegne seg selv
    def draw(self):
        
        #displaye riktig sprite i forhold til retningen spiller ser
        if(self.facing_r == 1) and (self.facing_u == 0):
            self.TheSprite = (0, 0, 24 , 24)
        if(self.facing_r == -1) and (self.facing_u == 0):
            self.TheSprite = (72, 0, 96 , 24)
        if(self.facing_r == 0) and (self.facing_u == -1):
            self.TheSprite = (24, 0, 48 , 24)
        if(self.facing_r == 0) and (self.facing_u == 1):
            self.TheSprite = (48, 0, 72 , 24)
        self.rect = pygame.Rect(self.x - self.size / 2, self.y - self.size / 2, self.size, self.size) #rektangel som skal virke som hitboks
        pygame.draw.rect(screen, 'black', self.rect)
        
        #ordner selve bildet
        self.image = pygame.Surface((self.sprite_w, self.sprite_h)).convert_alpha()
        self.image.blit(self.sheet, (0, 0), self.TheSprite) #den siset paranteset (top_L_x, top_L_y, bottom_R_x, bottom_R_y) Hvor den henter piksler fra spritesheetet
        self.image = pygame.transform.scale(self.image, (self.sprite_w * self.scale, self.sprite_h * self.scale)) #lar deg skalere bildet etter ønske
        self.image.set_colorkey(self.color) #Fjerner alle piksler med denne fargen, fordi jeg velger svart må man velge en annen farge
        screen.blit(self.image, (self.x - self.sprite_w*self.scale / 2, self.y - self.sprite_h*self.scale / 2))


#klasse for magisk/prosjektil angrep
class Magic:
    def __init__(self, retning, x, y):
        self.damage = 1
        self.speed = 10
        self.retning = retning
        self.x = x
        self.y = y

    #funksjon for å oppdatere prosjektilet
    def update(self):
        pygame.draw.circle(screen, 'blue', (self.x, self.y), 8)
        if(self.retning[0] != 0) and (self.retning[1] != 0):
            self.x += self.retning[0] * self.speed / math.sqrt(2)
            self.y += self.retning[1] * self.speed / math.sqrt(2)
        else:
            self.x += self.retning[0] * self.speed
            self.y += self.retning[1] * self.speed


class Tileset(): #Klasse for å opprette 
    def __init__(self, tileset, r, l, u, d):
        """ Preset
        [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        """
        self.sheet = sprite_sheet_image
        self.tileset = tileset
        self.door_r = r #booleans for å sjekke om dørene er låst eller ikke
        self.door_l = l
        self.door_u = u
        self.door_d = d
        self.ground = (96, 0, 119, 24) #hvor i tilesheet man finner hver tile
        self.wall = (96, 24, 119, 48)
        self.door_locked = (96, 49, 119, 72)
        self.door_unlocked = (96, 73, 119, 96)

    def draw(self):
        wall_rects = []
        for row in range(len(self.tileset)):
            for col in range(len(self.tileset[row])):
                #bestemmer hvilken tile som skal plasseres
                if(self.tileset[row][col] == 0):
                    self.TheTile = self.ground
                if(self.tileset[row][col]) == 1:
                    self.TheTile = self.wall
                if(self.tileset[row][col]) == 2:
                    self.TheTile = self.door_locked

                image = pygame.Surface((24, 24)).convert_alpha()
                image.blit(self.sheet, (0, 0), self.TheTile) #den siset paranteset (top_L_x, top_L_y, bottom_R_x, bottom_R_y) Hvor den henter piksler fra spritesheetet
                image = pygame.transform.scale(image, (48, 48)) #lar deg skalere bildet etter ønske
                image.set_colorkey('BLACK') #Fjerner alle piksler med denne fargen, fordi jeg velger svart må man velge en annen farge
                screen.blit(image, (col*48, row*48))

                if self.get_tile_type(row, col) == 1:
                    wall_rects.append(pygame.Rect(self.get_tile_position(row, col), (48, 48)))
        return wall_rects
            
    def get_tile_type(self, row, col):
        return self.tileset[row][col]

    def get_tile_position(self, row, col):
        return col * 48, row * 48


#fonts og størrelse til tekst
text_font_s = pygame.font.SysFont("Arial", 24) # liten tekst
text_font_m = pygame.font.SysFont("Arial", 36) # Medium tekst
text_font_l = pygame.font.SysFont("Arial", 48) # Stor tekst
#Funksjon for å skrive tekst enklere
def draw_text(text : str, font : pygame.font.Font, text_col : pygame.Color, x : int, y : int): #Funksjon som brukes for å lage tekst.
    img = font.render(text, True, text_col)
    tekst_rect = img.get_rect(center=(x, y))
    screen.blit(img, tekst_rect)

#laster spritesheet
sprite_sheet_image = pygame.image.load('spritesheet.png').convert_alpha()
#Funksjon for å kunne tegne enhver del av sheetet
def get_image(sheet, width, height, scale, color):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), (0, 0, 24 , 24)) #den siset paranteset (top_L_x, top_L_y, bottom_R_x, bottom_R_y) Hvor den henter piksler fra spritesheetet
    image = pygame.transform.scale(image, (width * scale, height * scale)) #lar deg skalere bildet etter ønske
    image.set_colorkey(color) #Fjerner alle piksler med denne fargen, fordi jeg velger svart må man velge en annen farge
    return image




#Lager objekter
spiller = Spiller()
prosjektiler = []

rom_1 = Tileset([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]], False, False, False, False)

#Kjører spillet
while running:
    # Avslutter løkken
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #Får ett input
    keys = pygame.key.get_pressed()

    spiller.retning = [0, 0]
    spiller.skyt_retning = [0, 0]

    #Inputs
    if keys[pygame.K_d] and (spiller.x + spiller.speed) < screen.get_width():
        spiller.retning[0] += 1
        spiller.skyt_retning[0] = 1
        spiller.facing_r = 1
        spiller.facing_u = 0

    if(keys[pygame.K_a]) and ((spiller.x - spiller.speed) > 0): 
        spiller.retning[0] -= 1
        spiller.skyt_retning[0] = -1
        spiller.facing_r = -1
        spiller.facing_u = 0

    if(keys[pygame.K_s]) and((spiller.y + spiller.speed) < screen.get_height()):
        spiller.retning[1] += 1
        spiller.skyt_retning[1] = 1
        spiller.facing_r = 0
        spiller.facing_u = 1

    if(keys[pygame.K_w]) and ((spiller.y - spiller.speed) > 0): 
        spiller.retning[1] -= 1
        spiller.skyt_retning[1] = -1
        spiller.facing_r = 0
        spiller.facing_u = -1

    if(keys[pygame.K_SPACE]):
        if(time - spiller.last_attack) > ((1 / spiller.attackspeed)*1000):
            if(spiller.retning != [0, 0]):
                spiller.skyt_retning = [spiller.retning[0], spiller.retning[1]]
                prosjektiler.append(Magic(spiller.skyt_retning, spiller.x, spiller.y))
                spiller.last_attack = time
            else:
                spiller.skyt_retning = [spiller.facing_r, spiller.facing_u]
                prosjektiler.append(Magic(spiller.skyt_retning, spiller.x, spiller.y))
                spiller.last_attack = time



    if spiller.retning[0] != 0 and spiller.retning[1] != 0:
        new_x = spiller.x + spiller.retning[0] * spiller.speed / math.sqrt(2)
        new_y = spiller.y + spiller.retning[1] * spiller.speed / math.sqrt(2)
    else:
        new_x = spiller.x + spiller.retning[0] * spiller.speed
        new_y = spiller.y + spiller.retning[1] * spiller.speed

    player_rect_x = pygame.Rect(new_x - spiller.size / 2, spiller.y - spiller.size / 2, spiller.size, spiller.size)
    wall_rects_x = rom_1.draw()  # Get the rectangles representing walls along the x-axis

    collision_detected_x = False

    for wall_rect_x in wall_rects_x:
        if player_rect_x.colliderect(wall_rect_x):
            # If there is a collision, prevent the player from moving along the x-axis
            new_x = spiller.x
            collision_detected_x = True

    # Check for collisions with walls along the y-axis
    player_rect_y = pygame.Rect(spiller.x - spiller.size / 2, new_y - spiller.size / 2, spiller.size, spiller.size)
    wall_rects_y = rom_1.draw()  # Get the rectangles representing walls along the y-axis

    collision_detected_y = False

    for wall_rect_y in wall_rects_y:
        if player_rect_y.colliderect(wall_rect_y):
            # If there is a collision, prevent the player from moving along the y-axis
            new_y = spiller.y
            collision_detected_y = True

    if not collision_detected_x:
        spiller.x = new_x

    if not collision_detected_y:
        spiller.y = new_y

    rom_1.draw()

    #oppdaterer alle prosjektiler
    for prosjektil in prosjektiler:
        if(prosjektil.retning == [0, 0]):
            prosjektiler.pop(prosjektiler.index(prosjektil))
        prosjektil.update()

    #tegner spiller i sin posisjon
    spiller.draw()


    # Oppdaterer hele skjermen
    pygame.display.flip()

    # Forsikrer at spillet kjører i maksimalt 60 FPS.
    time = pygame.time.get_ticks()
    clock.tick(60)

# Avslutter spillet
pygame.quit()