import pygame
from constantes import *

# ------------------------ CLASES ----------------------------

class Fondo():
    def __init__(self):
        self.imagen = pygame.image.load("data\Game_background.png").convert()
        self.ALTO_FONDO = 800 
        self.fondo_1_coord_y = -100
        self.fondo_2_coord_y = self.fondo_1_coord_y - self.ALTO_FONDO
        self.speed_y_org = 7
        self.speed_y = self.speed_y_org

    def movimiento(self, objeto_pantalla):
        
        pantalla = objeto_pantalla

        # Impresion:
        pantalla.blit(self.imagen,(0, self.fondo_1_coord_y))
        pantalla.blit(self.imagen,(0, self.fondo_2_coord_y)) 

        # Desplazamiento:
        self.fondo_1_coord_y += self.speed_y   
        self.fondo_2_coord_y += self.speed_y 

        # Reposicionamiento fondo 1:
        if self.fondo_1_coord_y > -100:
            self.fondo_2_coord_y = self.fondo_1_coord_y - self.ALTO_FONDO

        # Reposicionamiento fondo 2:
        if self.fondo_2_coord_y > -100:
           self.fondo_1_coord_y = self.fondo_2_coord_y - self.ALTO_FONDO


class Jugador(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.coord_x = 278 
        self.coord_y = 560
        self.speed_x = 0
        self.speed_y = 0
        self.image = pygame.image.load("data\Jugador.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.hitbox = pygame.Rect(self.coord_x + 9, self.coord_y + 2, self.rect.width*0.775, self.rect.height*0.965)

    def movimiento(self):

        # Bloqueo el movimiento del jugador para que no se salga de la pantalla:
        if self.coord_x <= 0 and self.speed_x < 0:
            self.speed_x = 0
        if self.coord_x >= (ANCHO_PANTALLA-self.rect.width) and self.speed_x > 0:
            self.speed_x = 0    
        if self.coord_y <= 0 and self.speed_y < 0:
            self.speed_y = 0   
        if self.coord_y >= (ALTO_PANTALLA-self.rect.height) and self.speed_y > 0:
            self.speed_y = 0  

        # Desplazamiento e impresion:
        self.coord_x += self.speed_x
        self.coord_y += self.speed_y
        self.hitbox = pygame.Rect(self.coord_x + 9, self.coord_y + 2, self.rect.width*0.775, self.rect.height*0.965)
        


class Auto_enemigo(pygame.sprite.Sprite):

    def __init__(self, coord_x, coord_y, speed_y, imagen):
        super().__init__()
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.speed_y_org = speed_y
        self.speed_y = speed_y
        self.image = pygame.image.load(f"data\{imagen}").convert_alpha()
        self.rect = self.image.get_rect()
        self.hitbox = pygame.Rect(self.coord_x + 8.5, self.coord_y + 2, self.rect.width*0.792, self.rect.height*0.96)

    def movimiento(self):

        # Movimiento e impresion:
        self.coord_y += self.speed_y
        self.hitbox = pygame.Rect(self.coord_x + 8.5, self.coord_y + 2, self.rect.width*0.792, self.rect.height*0.96)
