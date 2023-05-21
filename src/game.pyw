import pygame, sys
from clases import *
from funciones import *
from constantes import *

pygame.init()

# ----------------------- CONFIGURACION -------------------------
pantalla = pygame.display.set_mode((ANCHO_PANTALLA,ALTO_PANTALLA))
pygame.display.set_caption("HIGHWAY RACE")

# OCULTAR EL PUNTERO DEL MOUSE:
pygame.mouse.set_visible(False)

# Clock:
clock = pygame.time.Clock()

# -------------------------- MUSICA ----------------------------
pygame.mixer.music.load("data\Musica.wav")
pygame.mixer.music.play(-1)

# ------------------ VARIABLES DEL JUEGO -------------------------
game_over = False
score = 0
high_score = 0
acumulador_tiempo_pasado_partidas_pasadas = 0

#------------------------- LISTAS DE SPRITES -------------------------
lista_todos_los_sprites = pygame.sprite.Group()
lista_enemigos = pygame.sprite.Group()

# -------------------- INSTANCIAMIENTO DE LOS OBJETOS -----------------------------

# Fondo:
fondo = Fondo()

# Jugador:
jugador = Jugador()
lista_todos_los_sprites.add(jugador)

#------------------------- GENERACION DE EVENTOS -------------------------
generacion_enemigos =  pygame.USEREVENT + 1
tiempo_generacion_enemigos_original = 1300
pygame.time.set_timer(generacion_enemigos, tiempo_generacion_enemigos_original, 1)


# ---------------------- BUCLE PRINCIPAL --------------------------------
while True:

    # CRONOMETRO
    tiempo_pasado_partida_actual = round(pygame.time.get_ticks()/1000) - acumulador_tiempo_pasado_partidas_pasadas
    
    # ACTUALIZACION DEL PUNTAJE:
    score = 2*tiempo_pasado_partida_actual    


    # ------------------ AUMENTO PROGRESIVO DE LA DIFICULTAD -----------------------------
    incremento_velocidad = 0.02*tiempo_pasado_partida_actual

    # Limito el incremento de velocidad para que sea jugable
    if incremento_velocidad < 1:
        
        # Reduzco la frecuencia de generacion de enemigos:
        nuevo_tiempo_generacion_enemigos = tiempo_generacion_enemigos_original - round(tiempo_generacion_enemigos_original*incremento_velocidad*0.39) 

        # Aumento la velocidad de dezplazamiento de los enemigos:
        for enemigo in lista_enemigos:
            enemigo.speed_y = enemigo.speed_y_org + enemigo.speed_y_org * incremento_velocidad 

        # Aumento la velocidad de dezplazamiento del fondo:
        fondo.speed_y = fondo.speed_y_org + fondo.speed_y_org * incremento_velocidad 

    # -------------------------------- CHEQUEO EVENTOS -----------------------------------
    for evento in pygame.event.get():
    
        # Configuracion del cierre de la ventana:
        if evento.type == pygame.QUIT:
            sys.exit()

        # Asocio el movimiento del jugador con los eventos del teclado:
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador.speed_x = -4.7
            if evento.key == pygame.K_RIGHT: 
                jugador.speed_x = 4.7
            if evento.key == pygame.K_UP:
                jugador.speed_y = -1.5
            if evento.key == pygame.K_DOWN: 
                jugador.speed_y = 3

        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT:
                jugador.speed_x = 0
            if evento.key == pygame.K_RIGHT: 
                jugador.speed_x = 0  
            if evento.key == pygame.K_UP:
                jugador.speed_y = 0
            if evento.key == pygame.K_DOWN: 
                jugador.speed_y = 0   

        # Generacion de enemigos:
        if evento.type == generacion_enemigos:
            
            enemigo = generar_enemigos(Auto_enemigo)
            lista_enemigos.add(enemigo)
            lista_todos_los_sprites.add(enemigo)
            pygame.time.set_timer(generacion_enemigos, nuevo_tiempo_generacion_enemigos, 1)

    # -------------------------- IMPRESION DE IMAGENES ----------------------

    # Impresion y movimiento del fondo:
    fondo.movimiento(pantalla)

    # Impresion sprites:    
    impresion_sprites(pantalla, lista_todos_los_sprites)

    # Impresion puntaje:
    impresion_puntaje(pantalla, score, high_score)

    # Actualizo la pantalla:
    pygame.display.flip()   


    # ----------------------------- COLISIONES --------------------------------

    for enemigo in lista_enemigos:
        if enemigo.hitbox.colliderect(jugador.hitbox):
            
            # Muestro la explosion en lugar del jugador:
            pygame.mixer.Sound("data\Explosion_sfx.wav").play()
            jugador.image = pygame.image.load("data\Explosion.png").convert_alpha()
            jugador.coord_x = jugador.coord_x - 15
            fondo.movimiento(pantalla)   
            impresion_sprites(pantalla, lista_todos_los_sprites)
            impresion_puntaje(pantalla, score, high_score)
            pygame.display.flip()  

            game_over = True



    # ----------------------------- GAME OVER --------------------------------- 
    if game_over == True:

        # Fin de la partida:

        # Puntaje:
        if score > high_score:
            high_score = score
        score = 0    

        # Reseteo el reloj de partida:
        acumulador_tiempo_pasado_partidas_pasadas += tiempo_pasado_partida_actual       

        # Mensaje de game over:
        mensaje_game_over = pygame.font.SysFont("Verdana", 55).render("GAME OVER", True, (201,20,14))
        pantalla.blit(mensaje_game_over,((ANCHO_PANTALLA - mensaje_game_over.get_width())/2, 250))
        pygame.display.flip()

        # Paro la musica:
        pygame.mixer.music.fadeout(2000)

        # Paro unos segundos el programa para que se vea el mensaje:
        pygame.time.delay(2500)

        # Reseteo la frecuencia de generacion de enemigos:
        pygame.event.clear(generacion_enemigos)
        pygame.time.set_timer(generacion_enemigos, tiempo_generacion_enemigos_original, 1)

        # Vacio las listas de sprites:
        lista_todos_los_sprites.empty()
        lista_enemigos.empty()

        # Vuelvo a crear al objeto jugador:
        jugador = Jugador()
        lista_todos_los_sprites.add(jugador)

        # Reseteo la musica:
        pygame.mixer.music.play(-1, 0, 1500)

        # Devuelvo la variable game over a False:
        game_over = False

    # -------------------------- CONTROL DE FRAMES ----------------------------
    clock.tick(FPS)
           