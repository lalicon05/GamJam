#imports
import pygame #importerer pygame
import math #importerer matte funksjoner
from pygame import mixer #import for musikk

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()

#Setter opp det essensielle
pygame.init()
screen = pygame.display.set_mode((768, 480)) # Setter skjermen til 500x500 piksler.
pygame.display.set_caption(r"Kjeller-eventyr") #navnet på spillet
clock = pygame.time.Clock()
running = True
Won = False

#Konstante variabler
spiller_mot_høyre = (0, 0, 24 , 24)
spiller_mot_venstre = (72, 0, 96 , 24)
spiller_oppover = (24, 0, 48 , 24)
spiller_nedover = (48, 0, 72 , 24)

#objekter / klasser ---------------------------------------------------------------------------------------------------------

#Klasse for spillerobjekt
class Spiller:
    #setter opp variabler/attributter for spiller
    def __init__(self):
        #alt som har med start å gjøre
        self.max_hp = 5
        self.hp = self.max_hp
        self.x = screen.get_width() / 2
        self.y = screen.get_height() / 2
        self.alive = True

        #alt som har med bevegelse og retning å gjøre
        self.retning = [0, 0]
        self.skyt_retning = [0, 0]

        #Ting for spillogikk
        self.time_since_damage = pygame.time.get_ticks()
        
        #alt som har med utseende å gjøre
        self.size = 25
        self.color = 'black'
        
        #alt som har med diverse stats å gjøre
        self.speed = 6
        self.attackspeed = 3
        self.last_attack = 0
        self.facing_right = 1
        self.facing_down = 1
        self.invincibility_time = 400

        #alt som har, med å tegne spriten å gjøre
        self.sheet = sprite_sheet_image
        self.sprite_width= 24
        self.sprite_heigth = 24
        self.scale = 1.4

        self.TheSprite = spiller_mot_høyre

        self.rect = pygame.Rect((self.x - self.size, self.y - self.size), (self.size, self.size))

    def damagecheck(self, angrep_liste, knockback, slowdown):
        if(time - self.time_since_damage > self.invincibility_time):
            self.speed = 6
        index = 0
        while index < len(angrep_liste):
            if self.rect.colliderect(angrep_liste[index].Rect):
                                
                self.x += -knockback * self.retning[0]
                self.y += -knockback * self.retning[1]
                if ((pygame.time.get_ticks() - self.time_since_damage) > self.invincibility_time):
                    self.hp -= angrep_liste[index].damage
                    self.speed *= slowdown
                    ouch_sound.play()
                    self.time_since_damage = pygame.time.get_ticks()
                #Hvis objektet i listen har attributten "alignment" så er den et prosjektil, og da skal den fjernes
                try:
                    angrep_liste[index].alignment
                    angrep_liste.pop(index)
                #Putter noe som ikke gjør noe i except 
                except: 
                    index = index
            index += 1
        
    
    def status(self):
        if self.hp <= 0:
            self.alive = False
            last_bgm = time
            gmover.play()
                
    #funksjon for å tegne seg selv
    def draw(self):
        
        #displaye riktig sprite i forhold til retningen spiller ser
        if(self.facing_right == 1) and (self.facing_down == 0):
            self.TheSprite = spiller_mot_høyre
        if(self.facing_right == -1) and (self.facing_down == 0):
            self.TheSprite = spiller_mot_venstre
        if(self.facing_right == 0) and (self.facing_down == -1):
            self.TheSprite = spiller_oppover
        if(self.facing_right == 0) and (self.facing_down == 1):
            self.TheSprite = spiller_nedover
        self.rect = pygame.Rect(self.x - self.size / 2, self.y - self.size / 2, self.size, self.size) #rektangel som skal virke som hitboks
        pygame.draw.rect(screen, 'black', self.rect)
        
        #ordner selve bildet
        self.image = pygame.Surface((self.sprite_width, self.sprite_heigth)).convert_alpha()
        self.image.blit(self.sheet, (0, 0), self.TheSprite) 
        self.image = pygame.transform.scale(self.image, (self.sprite_width* self.scale, self.sprite_heigth * self.scale)) #lar deg skalere bildet etter ønske
        self.image.set_colorkey(self.color) #Fjerner alle piksler med denne fargen, fordi jeg velger svart må man velge en annen farge
        screen.blit(self.image, (self.x - self.sprite_width*self.scale / 2, self.y - self.sprite_heigth*self.scale / 2))

#Klasse for fiender
class Fiende():
    def __init__(self, type, koordinater, skade):

        """
        type : alternativer('basic', 'cucumber', 'ranged')
        """
        
        self.speed = 2
        self.can_shoot = False
        self.can_move = False
        self.size = 40
        self.start_koordinater = list(koordinater)
        self.koordinater = list(koordinater)
        self.Rect = pygame.Rect(koordinater, (self.size, self.size))
        self.hp = 3
        self.damage = skade
        self.type = type
        self.retning = [0, 0]
        self.last_shoot = 0

        self.sheet = sprite_sheet_image
        self.image = pygame.Surface((24, 24)).convert_alpha()

        if (self.type == 'basic'):
            self.can_move = True
            self.basic_enemy_sheet = (0, 24, 24, 48)
            self.image.blit(self.sheet, (0, 0), self.basic_enemy_sheet)
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
            self.image.set_colorkey('BLACK')
        elif (self.type == 'ranged'):
            self.can_shoot = True
            self.basic_enemy_sheet = (72, 24, 96, 24)
            self.image.blit(self.sheet, (0, 0), self.basic_enemy_sheet)
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
            self.image.set_colorkey('BLACK')
        

    #funksjon for å skyte
    def shoot(self):
        if self.can_shoot:
            if(time - self.last_shoot > 1000):
                fiende_prosjektiler.append(Magi(self.retning, self.koordinater[0] + self.size/2, self.koordinater[1] + self.size/2, 1))
                self.last_shoot = time
                
    def move(self):
        if self.can_move:
            self.koordinater[0] += self.speed * self.retning[0]
            self.koordinater[1] += self.speed * self.retning[1]
            self.Rect = pygame.Rect(tuple(self.koordinater), (self.size, self.size))
    
    #funksjon for å sjekke om den tar skade
    def damage_check(self, prosjektil_liste):
        #Her bruker jeg en while løkke fordi jeg ønsker å endre lengden på listen underveis
        index = 0
        while index < len(prosjektil_liste):
            if (self.Rect.colliderect(prosjektil_liste[index].Rect)):
                self.hp -= prosjektil_liste[index].damage
                prosjektil_liste.pop(index)
                b_fx.play()
            index += 1
            
    def alive(self):
        if self.hp <= 0:
            return False
        return True

    def finn_retning(self, mål):
        vektor = pygame.math.Vector2(mål.x - self.koordinater[0], mål.y - self.koordinater[1])
        self.retning = list([vektor.normalize()[0], vektor.normalize()[1]])
        
    def draw(self):
        screen.blit(self.image, self.koordinater)
        pygame.draw.rect(screen, 'red', (self.koordinater[0] - 8, self.koordinater[1] - 13, 55, 6))
        pygame.draw.rect(screen, 'green', (self.koordinater[0] - 8, self.koordinater[1] - 13, (55/3) * self.hp, 6))
    
#klasse for magisk/prosjektil angrep
class Magi:
    def __init__(self, retning, x, y, alignment):
        self.alignment = alignment
        self.damage = 1
        self.speed = 10
        self.retning = retning
        self.x = x
        self.y = y
        

        self.Rect = pygame.Rect(self.x - 6, self.y - 6, 12, 12)

        self.sheet = sprite_sheet_image
        #Spiller sitt prosjektil
        if alignment == 0:
            self.sprite = (0, 48, 24, 72)
        #Fiende sitt prosjektil
        if alignment == 1:
            self.sprite = (24, 48, 48, 72)

        self.image = pygame.Surface((24, 24)).convert_alpha()
        self.image.blit(self.sheet, (0, 0), self.sprite)
        self.image = pygame.transform.scale(self.image, (18, 18))
        self.image.set_colorkey('BLACK')

    #funksjon for å oppdatere prosjektilet
    def update(self):
        if(self.retning[0] != 0) and (self.retning[1] != 0):
            self.x += self.retning[0] * self.speed / math.sqrt(2)
            self.y += self.retning[1] * self.speed / math.sqrt(2)
        else:
            self.x += self.retning[0] * self.speed
            self.y += self.retning[1] * self.speed
        #pygame.draw.circle(screen, 'blue', (self.x, self.y), 8)
        self.Rect = pygame.Rect(self.x - 8, self.y - 8, 16, 16)
        screen.blit(self.image, (self.x - 9, self.y - 9))



class Tileset(): #Klasse for å opprette ett tileset knyttet til ett rom
    def __init__(self, tileset, room_coords, enemy_list):
        self.sheet = sprite_sheet_image #laster inn sprite -sheet
        self.tileset = tileset #

        self.room_coords = (room_coords)
        self.door_r = False #booleans for å velge hvilke dører ett rom skal inneholde
        self.door_l = False
        self.door_u = False
        self.door_d = False

        self.ground = (96, 0, 119, 24) #hvor i tilesheet man finner hver tile
        self.wall = (96, 24, 119, 48) 
        self.door_locked = (96, 49, 119, 72)
        self.door_unlocked = (96, 72, 119, 96)

        #Data om fiender
        self.cleared = False
        self.starting_enemy_list = enemy_list[:]
        self.enemy_list = enemy_list
        self.wall_rects = []
    
    def check_if_empty(self):
        if len(self.enemy_list) == 0:
            self.cleared = True
    
    def get_room_coords(self):
        return self.room_coords
    
    def get_door_rects(self):
        return self.door_rects 

    def place_doors(self, room_list):
        self.door_r = False #booleans for å velge hvilke dører ett rom skal inneholde
        self.door_l = False
        self.door_u = False
        self.door_d = False

        for rom in range(len(room_list)):
            #sjekker rom til høyre (rommene[room_index].room_coords) == (active_coords[0] + 1,active_coords[1])
            if(self.room_coords[0] + 1, self.room_coords[1]) == (room_list[rom].room_coords):
                self.door_r = True
            #sjekker rom til venstre
            if(self.room_coords[0] - 1, self.room_coords[1]) == (room_list[rom].room_coords):
                self.door_l = True
            #sjekker rom nedover
            if(self.room_coords[0], self.room_coords[1] - 1) == (room_list[rom].room_coords):
                self.door_d = True
            #sjekker rom oppover
            if(self.room_coords[0], self.room_coords[1] + 1) == (room_list[rom].room_coords):
                self.door_u = True

    def draw(self):
        self.wall_rects = [] #liste over alle vegger
        self.door_rects = []

        

        for row in range(len(self.tileset)):
            for col in range(len(self.tileset[row])):
                #bestemmer hvilken tile som skal plasseres
                if(self.tileset[row][col] == 0):
                    self.TheTile = self.ground
                if(self.tileset[row][col]) == 1:
                    self.TheTile = self.wall
                if(self.tileset[row][col]) == 2:
                    self.TheTile = self.door_locked
                if(self.tileset[row][col]) == 3:
                    self.TheTile = self.door_unlocked

                if(col == 0) or (col == 15): #sørger for at alle kanter er vegger
                    self.tileset[row][col] = 1
                    self.TheTile = self.wall
                if(row == 0) or (row == 9):
                    self.tileset[row][col] = 1
                    self.TheTile = self.wall


                if self.door_r and col == len(self.tileset[0]) - 1 and row == len(self.tileset) // 2: #sjekker hvilke dører ett rom skal inneholde
                    self.tileset[row][col] = 3
                    self.TheTile = self.door_unlocked
                if self.door_l and col == 0 and row == len(self.tileset) // 2:
                    self.tileset[row][col] = 3
                    self.TheTile = self.door_unlocked
                if self.door_d and col == len(self.tileset[0]) // 2 and row == len(self.tileset) - 1:
                    self.tileset[row][col] = 3
                    self.TheTile = self.door_unlocked
                if self.door_u and col == len(self.tileset[1]) // 2 and row == 0:
                    self.tileset[row][col] = 3
                    self.TheTile = self.door_unlocked



                image = pygame.Surface((24, 24)).convert_alpha() #ett surface å tegne spriten til veggen på
                image.blit(self.sheet, (0, 0), self.TheTile) #den siset paranteset (top_L_x, top_L_y, bottom_R_x, bottom_R_y) Hvor den henter piksler fra spritesheetet
                image = pygame.transform.scale(image, (48, 48)) #lar deg skalere bildet etter ønske
                image.set_colorkey('BLACK') #Fjerner alle piksler med denne fargen, fordi jeg velger svart må man velge en annen farge
                screen.blit(image, (col*48, row*48))


                if self.get_tile_type(row, col) == 3:
                    self.door_rects.append(pygame.Rect(self.get_tile_position(row, col), (48, 48)))

                if self.get_tile_type(row, col) == 1: #hvis tile er en vegg, legg til i liste over vegger
                    self.wall_rects.append(pygame.Rect(self.get_tile_position(row, col), (48, 48)))

            for i in self.enemy_list:
                i.draw()

        return self.wall_rects #returnerer vegger slik at man kan kollidere med de

    def get_tile_type(self, row, col): #returnerer type tile
        return self.tileset[row][col]
    
    def get_walls(self):
        return self.wall_rects

    def get_tile_position(self, row, col): #henter posisjon til tile
        return col * 48, row * 48

#laster spritesheet
sprite_sheet_image = pygame.image.load('spritesheet.png').convert_alpha()

#Laster Game-over skjerm
game_over_img = pygame.image.load('sad_fog.jpg').convert_alpha()


rommene = [] #liste over rom
rommene.append(Tileset([
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], #legger til rom i listen
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
                ], (0, 0), [Fiende('basic',(100, 100), 1), Fiende('basic',(650, 400), 1)]))
rommene.append(Tileset([
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
                ], (-1, 0), [Fiende('basic',(500, 100), 1), Fiende('basic',(500, 400), 1),Fiende('ranged', (300, 100), 1), Fiende('ranged', (100, 150), 1), Fiende('ranged', (100, 200), 1), Fiende('ranged', (100, 250), 1), Fiende('ranged', (400, 350), 1)]))
rommene.append(Tileset([
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
                ], (1, 1), [Fiende('basic',(100, 100), 1), Fiende('ranged',(400, 100), 1)]))
rommene.append(Tileset([
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
                ], (1, 0), [Fiende('basic',(500, 400), 1), Fiende('ranged',(200, 100), 1)]))
rommene.append(Tileset([
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
                ], (0, -1), [Fiende('basic',(300, 300), 1), Fiende('ranged',(100, 100), 1), Fiende('ranged',(100, 200), 1), Fiende('ranged',(100, 300), 1), Fiende('ranged',(600, 100), 1), Fiende('ranged',(600, 200), 1), Fiende('ranged',(600, 300), 1), Fiende('ranged',(600, 350), 1)]))
rommene.append(Tileset([
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
                ], (0, -2), [Fiende('basic',(400, 250), 1), Fiende('ranged',(100, 100), 1), Fiende('ranged',(600, 100), 1)]))
rommene.append(Tileset([
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
                ], (0, 1), [Fiende('basic',(100, 100), 1)]))


#Funksjoner-------------------------------------------------------------------------------------------------------
#dreper fiender hvis de er døde
def fiende_fjerner(fiende_liste):
    #Bruker while løkke fordi jeg endrer listen underveis
    index = 0
    while index < len(fiende_liste):
        if not fiende_liste[index].alive():
            fiende_liste.pop(index)
        index += 1

#fonts og størrelse til tekst
text_font_small = pygame.font.SysFont("Arial", 24) # liten tekst
text_font_medium = pygame.font.SysFont("Arial", 36) # Medium tekst
text_font_large = pygame.font.SysFont("Arial", 48) # Stor tekst
#Funksjon for å skrive tekst enklere
def draw_text(text : str, font : pygame.font.Font, text_col : pygame.Color, x : int, y : int): #Funksjon som brukes for å lage tekst.
    img = font.render(text, True, text_col)
    tekst_rect = img.get_rect(center=(x, y))
    screen.blit(img, tekst_rect)


#Funksjon for å kunne tegne enhver del av sheetet
def get_image(sheet, width, height, scale, color):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), (0, 0, 24 , 24)) #den siset paranteset (top_L_x, top_L_y, bottom_R_x, bottom_R_y) Hvor den henter piksler fra spritesheetet
    image = pygame.transform.scale(image, (width * scale, height * scale)) #lar deg skalere bildet etter ønske
    image.set_colorkey(color) #Fjerner alle piksler med denne fargen, fordi jeg velger svart må man velge en annen farge
    return image

#spiller kollidere med vegg
def wall_collision(new_x, new_y):
    #sjekker om spiller kollidere på x-akse
    player_rect_x = pygame.Rect(new_x - spiller.size / 2, spiller.y - spiller.size / 2, spiller.size, spiller.size)
    wall_rects_x = rommene[active_room].draw()  # Henter vegg tiles fra rommet for å kollidere med de

    collision_detected_x = False

    for wall_rect_x in wall_rects_x:
        if player_rect_x.colliderect(wall_rect_x): #sjekker om spiller kolliderer med vegg på x-akse
            new_x = spiller.x #flytter ikke spiller videre
            collision_detected_x = True 

    # sjekker om kolliderer på y-aksen
    player_rect_y = pygame.Rect(spiller.x - spiller.size / 2, new_y - spiller.size / 2, spiller.size, spiller.size)
    wall_rects_y = rommene[active_room].draw()  # Get the rectangles representing walls along the y-axis

    collision_detected_y = False

    for wall_rect_y in wall_rects_y:
        if player_rect_y.colliderect(wall_rect_y): #sjekker om spiller kolliderer med vegg på y-akse
            new_y = spiller.y #Hindrer spiller i å bevege seg videre
            collision_detected_y = True

    if not collision_detected_x:
        spiller.x = new_x #beveger seom vanlig om det ikke er en kollisjon langs x-akse

    if not collision_detected_y:
        spiller.y = new_y #Beveger seg som vanlig om det ikke er en kollisjon langs y-akse

#sjekker om spiller er på en dør
def door_handle(player_rect, door_rects):
    for door_rect in door_rects:
        if door_rect.contains(player_rect):
            return True
    return False

#Sjekker hvilken dør spilleren er ved
def which_door(playerx, playery):
    if (playerx > (screen.get_width() - 96)):
        return 'r'
    if (playerx < (96)):
        return 'l'
    if (playery > (screen.get_height() - 96)):
        return 'd'
    if (playery < (96)):
        return 'u'
    else:
        return "no door"

#funksjon for å sjekke om det er ett rom i en retning og legger til en dør/vegg ut i fra resultatet
def check_neighbor_rooms():
    room_pos = rommene[active_room].room_coords
    r = False
    #sjekker om det er ett rom til høyre
    for room in range(len(rommene)):
        if(rommene[room].room_coords == (room_pos[0] + 1, room_pos[1])):
            rommene[room].tileset[6][15] == 3
            r = True
        if r != True:
            rommene[room].tileset[6][15] == 1


#Laster inn lyder
bgm = pygame.mixer.Sound('musiiic.mp3') #importerer lydfilen for bakgrunnsmusikk
bgm.set_volume(0.2) #halvverer volumet
bmg_delay = 17500
last_bgm = pygame.time.get_ticks()
bgm.play()

gmover = pygame.mixer.Sound('gameover.mp3')
gmover.set_volume(1)

s_fx = pygame.mixer.Sound('shoot.mp3') #importerer lydfilen for skyting
s_fx.set_volume(2)

b_fx = pygame.mixer.Sound('boom.mp3')
b_fx.set_volume(0.25)

ouch_sound = pygame.mixer.Sound('classic_hurt.mp3')
ouch_sound.set_volume(0.5)

#Lager objekter -------------------------------------------------------------------------------------
spiller = Spiller()
spiller_prosjektiler = []
fiende_prosjektiler = []

last_door = 0
enter = False
active_room = 0

active_coords = (0, 0)
rommene[active_room].draw()
rommene[active_room].place_doors(rommene)

new_room = False

time = 0


#Kjører spillet -------------------------------------------------------------
while running:
    if spiller.alive and (not Won):
        if(time - last_bgm >= bmg_delay): #spiller av musikken
            bgm.play()
            last_bgm = time

        # Avslutter løkken
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
        #tar inn inputs
        keys = pygame.key.get_pressed()

        spiller.retning = [0, 0]
        spiller.skyt_retning = [0, 0]


        #Inputs
        if keys[pygame.K_d] and (spiller.x + spiller.speed) < screen.get_width() - 16:
            spiller.retning[0] += 1
            spiller.skyt_retning[0] = 1
            spiller.facing_right = 1
            spiller.facing_down = 0

        if(keys[pygame.K_a]) and ((spiller.x - spiller.speed) > 16): 
            spiller.retning[0] -= 1
            spiller.skyt_retning[0] = -1
            spiller.facing_right = -1
            spiller.facing_down = 0

        if(keys[pygame.K_s]) and((spiller.y + spiller.speed) < screen.get_height() - 16):
            spiller.retning[1] += 1
            spiller.skyt_retning[1] = 1
            spiller.facing_right = 0
            spiller.facing_down = 1

        if(keys[pygame.K_w]) and ((spiller.y - spiller.speed) > 16): 
            spiller.retning[1] -= 1
            spiller.skyt_retning[1] = -1
            spiller.facing_right = 0
            spiller.facing_down = -1
        
        if(keys[pygame.K_ESCAPE]):
            spiller.alive = False
            gmover.play()

        if(keys[pygame.K_SPACE]): #angriper 
            if(time - spiller.last_attack) > ((1 / spiller.attackspeed)*1000): #sjekker om man prøver å skyte før cooldown er over
                if(spiller.retning != [0, 0]):
                    spiller.skyt_retning = [spiller.retning[0], spiller.retning[1]]
                    spiller_prosjektiler.append(Magi(spiller.skyt_retning, spiller.x, spiller.y, 0))
                    spiller.last_attack = time
                    s_fx.play()
                else:
                    spiller.skyt_retning = [spiller.facing_right, spiller.facing_down]
                    spiller_prosjektiler.append(Magi(spiller.skyt_retning, spiller.x, spiller.y, 0))
                    spiller.last_attack = time
                    s_fx.play()

        if(keys[pygame.K_RETURN]):
            enter = True

        if spiller.retning[0] != 0 and spiller.retning[1] != 0: #fikse hastighetsproblemet med å bevege seg diagonalt
            new_x = spiller.x + spiller.retning[0] * spiller.speed / math.sqrt(2)
            new_y = spiller.y + spiller.retning[1] * spiller.speed / math.sqrt(2)
        else:
            new_x = spiller.x + spiller.retning[0] * spiller.speed
            new_y = spiller.y + spiller.retning[1] * spiller.speed

        if new_room: #Sjekker
            active_coords = rommene[active_room].get_room_coords()
            new_room = False



        wall_collision(new_x, new_y) #sjekker om spiller kolliderer med vegger og korrigerer bevegelse deretter
        rommene[active_room].draw() #tegner rommet
        spiller.damagecheck(rommene[active_room].enemy_list, 30, 0.2)
        spiller.damagecheck(fiende_prosjektiler, 10, 0.8)
        spiller.status()
        for x in rommene[active_room].enemy_list:
            x.damage_check(spiller_prosjektiler)
            x.finn_retning(spiller)
            x.move()
            x.shoot()
        fiende_fjerner(rommene[active_room].enemy_list)
        rommene[active_room].check_if_empty()
        #tegner spiller i sin posisjon
        spiller.draw()


        #sjekker om man er i en dør mens man trykker enter
        if(enter == True) and (door_handle(spiller.rect, rommene[active_room].get_door_rects())):
            if time - last_door >= 1000: 
                if(which_door(new_x, new_y) == 'r'):
                    for room_index in range(len(rommene)):
                        if(rommene[room_index].room_coords) == (active_coords[0] + 1,active_coords[1]):
                            active_room = room_index
                            print(rommene[active_room].room_coords)
                            spiller.x = 32
                            spiller.y = spiller.y
                            rommene[room_index].place_doors(rommene)
                            new_room = True
                if(which_door(new_x, new_y) == 'l'):
                    for room_index in range(len(rommene)):
                        if(rommene[room_index].room_coords) == (active_coords[0] - 1,active_coords[1]):
                            active_room = room_index
                            print(rommene[active_room].room_coords)
                            spiller.x = screen.get_width() - 32
                            spiller.y = spiller.y
                            rommene[room_index].place_doors(rommene)
                            new_room = True
                if(which_door(new_x, new_y) == 'u'):
                    for room_index in range(len(rommene)):
                        if(rommene[room_index].room_coords) == (active_coords[0],active_coords[1] + 1):
                            active_room = room_index
                            print(rommene[active_room].room_coords)
                            spiller.x = spiller.x
                            spiller.y = screen.get_height() - 32
                            rommene[room_index].place_doors(rommene)
                            new_room = True
                if(which_door(new_x, new_y) == 'd'):
                    for room_index in range(len(rommene)):
                        if(rommene[room_index].room_coords) == (active_coords[0],active_coords[1] - 1):
                            active_room = room_index
                            print(rommene[active_room].room_coords)
                            spiller.x = spiller.x
                            spiller.y = 32
                            rommene[room_index].place_doors(rommene)
                            new_room = True
                last_door = time
            enter = False

        #oppdaterer alle spiller_prosjektiler
        for prosjektil in spiller_prosjektiler:
            prosjektil.update() #oppdaterer spiller_prosjektiler
            for wall in rommene[active_room].get_walls(): #sjekker om prosjektilet kolliderer med en vegg
                if pygame.Rect.colliderect(prosjektil.Rect, wall):
                    try:
                        spiller_prosjektiler.pop(spiller_prosjektiler.index(prosjektil))
                        b_fx.play()
                    except:
                        print("did not")

            if prosjektil.x < 0 or prosjektil.x > screen.get_width(): #sletter hvis spiller_prosjektiler går utenfor skjermen på sidene
                spiller_prosjektiler.pop(spiller_prosjektiler.index(prosjektil))
                b_fx.play()
            if prosjektil.y < 0 or prosjektil.y > screen.get_height(): #fjerner prosjektilet hvis det går over eller under skjermen
                spiller_prosjektiler.pop(spiller_prosjektiler.index(prosjektil))
                b_fx.play()

            if(prosjektil.retning == [0, 0]): #fjerner spiller_prosjektiler som står stille
                spiller_prosjektiler.pop(spiller_prosjektiler.index(prosjektil))
            
        for prosjektil in fiende_prosjektiler:
            prosjektil.update() #oppdaterer fiende_prosjektiler
            for wall in rommene[active_room].get_walls(): #sjekker om prosjektilet kolliderer med en vegg
                if pygame.Rect.colliderect(prosjektil.Rect, wall):
                    try:
                        fiende_prosjektiler.pop(fiende_prosjektiler.index(prosjektil))
                        b_fx.play()
                    except:
                        print("did not")

            if prosjektil.x < 0 or prosjektil.x > screen.get_width(): #sletter hvis fiende_prosjektiler går utenfor skjermen på sidene
                fiende_prosjektiler.pop(fiende_prosjektiler.index(prosjektil))
                b_fx.play()
            if prosjektil.y < 0 or prosjektil.y > screen.get_height(): #fjerner prosjektilet hvis det går over eller under skjermen
                fiende_prosjektiler.pop(fiende_prosjektiler.index(prosjektil))
                b_fx.play()

            if(prosjektil.retning == [0, 0]): #fjerner fiende_prosjektiler som står stille
                fiende_prosjektiler.pop(fiende_prosjektiler.index(prosjektil))

        #tegner health bar
        pygame.draw.rect(screen, 'green', (3, 30, spiller.hp * 20, 9))
        draw_text(f"Health: {spiller.hp}", text_font_small, 'white', 40, 17)

        # Oppdaterer hele skjermen
        pygame.display.flip()

        enter = False

        # Forsikrer at spillet kjører i maksimalt 60 FPS.
        time = pygame.time.get_ticks()
        clock.tick(60)
    elif Won:
        print("Du vant")
    
    
    else:
        bgm.set_volume(0)
        gmover.set_volume(1)
        if(time - last_bgm > 6000): #spiller av musikken
            gmover.play()
            last_bgm = time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

        keys = pygame.key.get_pressed()

        if(keys[pygame.K_RETURN]):
            pygame.mixer.quit()
            pygame.mixer.pre_init(44100, -16, 2, 512)
            mixer.init()
            
            gmover.set_volume(0)

            bgm.set_volume(0.3)
            last_bgm = time
            bgm.play()

            for x in rommene:
                x.cleared = False
                x.enemy_list = x.starting_enemy_list[:]
            
            for x in rommene:
                for y in x.enemy_list:
                    y.hp = 3
                    y.koordinater = y.start_koordinater[:]
                    y.Rect = pygame.Rect(tuple(y.koordinater), (y.size, y.size))

            last_door = 0
            enter = False
            active_room = 0

            spiller.alive = True
            spiller.hp = spiller.max_hp
            spiller.x = screen.get_width() / 2
            spiller.y = screen.get_height() / 2
            spiller.retning = [0, 0]
            spiller.skyt_retning = [0, 0]
            spiller.size = 25
            spiller.speed = 6
            spiller.attackspeed = 3


            active_coords = (0, 0)
            rommene[active_room].draw()
            rommene[active_room].place_doors(rommene)

            new_room = False

            time = 0



        #ordner selve bildet
        image = pygame.Surface((screen.get_width(), screen.get_height())).convert_alpha()
        image.blit(game_over_img, (0, 0), (0, 100, game_over_img.get_width(), game_over_img.get_height())) #den siset paranteset (top_L_x, top_L_y, bottom_R_x, bottom_R_y) Hvor den henter piksler fra spritesheetet
        image = pygame.transform.scale(image, (screen.get_width() + 100, screen.get_height())) #lar deg skalere bildet etter ønske
        #image.set_colorkey(self.color) #Fjerner alle piksler med denne fargen, fordi jeg velger svart må man velge en annen farge
        screen.blit(image, (0, 0))

        draw_text("Game Over!", text_font_large, 'white', screen.get_width() / 2, screen.get_height() / 2)
        draw_text(r"Press Enter to restart", text_font_small, 'white', screen.get_width() / 2, screen.get_height() / 1.7)

        pygame.display.flip()

        time = pygame.time.get_ticks()
        clock.tick(60)

# Avslutter spillet
pygame.quit()