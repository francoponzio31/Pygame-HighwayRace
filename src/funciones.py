import pygame, random

def generar_enemigos(clase_auto):

    carril = random.randint(1,4)   

    if carril == 1:
        imagen = random.randint(1,4)
        enemigo = clase_auto(41,-500,8.4, f"Coche_enemigo_{imagen}.png")
                    
    elif carril == 2:
        imagen = random.randint(1,4)
        enemigo = clase_auto(151,-500,8, f"Coche_enemigo_{imagen}.png")

    elif carril == 3:
        imagen = random.randint(5,8)
        enemigo = clase_auto(267,-500,4.5, f"Coche_enemigo_{imagen}.png")

    elif carril == 4:
        imagen = random.randint(5,8)
        enemigo = clase_auto(382,-500,3.3, f"Coche_enemigo_{imagen}.png")

    return enemigo


def impresion_puntaje(objeto_pantalla, score, high_score):

    fuente_puntaje = pygame.font.SysFont("Verdana", 15)

    # score:     
    impresion_score = fuente_puntaje.render( f"Score: {score}", True, (230,230,230))
    objeto_pantalla.blit(impresion_score, (24, 2))

    # High score:
    impresion_highscore = fuente_puntaje.render( f"High Score: {high_score}", True, (230,230,230))
    objeto_pantalla.blit(impresion_highscore, (24, 20))     


def impresion_sprites(objeto_pantalla, lista_sprites):

    for sprite in lista_sprites:
        sprite.movimiento()
        objeto_pantalla.blit(sprite.image,(sprite.coord_x,sprite.coord_y))  
        
        if sprite.coord_y > 1000:
            sprite.kill() 
