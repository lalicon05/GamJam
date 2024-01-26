#imports
print("Bean")
import pygame
import math

#Setter opp det essensielle
pygame.init()
screen = pygame.display.set_mode((800, 500)) # Setter skjermen til 500x500 piksler.
clock = pygame.time.Clock()
running = True

#Klasse for spillerobjekt
class Spiller:
    def __init__(self):
        self.max_hp = 3
        self.hp = self.max_hp
        self.x = screen.get_width() / 2
        self.y = screen.get_height() / 2
        self.retning = [0, 0]
        self.size = 25
        self.color = 'darkolivegreen3'
        self.speed = 6
        
    #funksjon for å tegne seg selv
    def draw(self):
        self.rect = pygame.Rect(self.x - self.size / 2, self.y - self.size / 2, self.size, self.size)
        pygame.draw.rect(screen, self.color, self.rect)

class Magic:
    def __init__(self, x, y):
        self.damage = 1
        self.speed = 10
        self.direction = [x, y]


#fonts og størrelse til tekst
text_font_s = pygame.font.SysFont("Arial", 24) # liten tekst
text_font_m = pygame.font.SysFont("Arial", 36) # Medium tekst
text_font_l = pygame.font.SysFont("Arial", 48) # Stor tekst

#Funksjon for å skrive tekst enklere
def draw_text(text : str, font : pygame.font.Font, text_col : pygame.Color, x : int, y : int): #Funksjon som brukes for å lage tekst.
    img = font.render(text, True, text_col)
    tekst_rect = img.get_rect(center=(x, y))
    screen.blit(img, tekst_rect)

#Lager objekter
spiller = Spiller()

#Kjører spillet
while running:
    # Avslutter løkken
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #Får ett input
    keys = pygame.key.get_pressed()

    spiller.retning = [0, 0]

    if(keys[pygame.K_d]) and((spiller.x) < screen.get_width()):
        spiller.retning[0] += 1
    if(keys[pygame.K_a]) and ((spiller.x) > 0): 
        spiller.retning[0] -= 1
    if(keys[pygame.K_s]) and((spiller.y) < screen.get_height()):
        spiller.retning[1] += 1
    if(keys[pygame.K_w]) and ((spiller.y) > 0): 
        spiller.retning[1] -= 1


    if(spiller.retning[0] != 0) and (spiller.retning[1] != 0):
        spiller.x += spiller.retning[0] * spiller.speed / math.sqrt(2)
        spiller.y += spiller.retning[1] * spiller.speed / math.sqrt(2)
    else:
        spiller.x += spiller.retning[0] * spiller.speed
        spiller.y += spiller.retning[1] * spiller.speed
    

    # Fyller skjermen med hvit farge
    screen.fill("hotpink4")

    spiller.draw()

    # Oppdaterer hele skjermen
    pygame.display.flip()

    # Forsikrer at spillet kjører i maksimalt 60 FPS.
    clock.tick(60)

# Avslutter spillet
pygame.quit()