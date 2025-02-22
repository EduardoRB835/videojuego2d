import pygame
import time
import sys
import carrera_1_jugador  # Import the module
import carrera_2_jugadores

pygame.init()

# --- Configuraciones Iniciales ---
ancho_ventana = 800
alto_ventana = 600
ventana = pygame.display.set_mode((ancho_ventana, alto_ventana), pygame.RESIZABLE)
pygame.display.set_caption("Opciones")

# --- Música ---
pygame.mixer.music.load("statics/music/opciones.mp3")
pygame.mixer.music.set_volume(0.0)
pygame.mixer.music.play(-1)

# --- Transición ---
transicion_duracion = 3000
tiempo_inicio = pygame.time.get_ticks()  # Tiempo de inicio para la transición inicial

# --- Fuentes ---
fuente_titulo = pygame.font.Font("statics/fonts/PixelifySans-VariableFont_wght.ttf", 60)
fuente_botones = pygame.font.Font("statics/fonts/PixelifySans-VariableFont_wght.ttf", 40)
fuente_input = pygame.font.Font("statics/fonts/PixelifySans-VariableFont_wght.ttf", 32)
fuente_placeholder = pygame.font.Font("statics/fonts/PixelifySans-VariableFont_wght.ttf", 32)
fuente_nombre = pygame.font.Font("statics/fonts/PixelifySans-VariableFont_wght.ttf", 40)

# --- Superficie ---
superficie_opciones = pygame.Surface((ancho_ventana, alto_ventana), pygame.SRCALPHA)

# --- Colores ---
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
GRIS_CLARO = (200, 200, 200)
GRIS_OSCURO = (100, 100, 100)
GRIS_PLACEHOLDER = (170, 170, 170)
AZUL_RESALTADO = (0, 120, 215)
COLOR_FONDO = (20, 25, 35)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)

# --- Imagen de fondo ---
try:
    fondo = pygame.image.load("statics/img/F1-2.png")
    fondo = pygame.transform.scale(fondo, (ancho_ventana, alto_ventana))
    fondo = fondo.convert_alpha()
except FileNotFoundError:
    print("Error: No se encontró la imagen de fondo.")
    fondo = None

# --- Título ---
texto_titulo = fuente_titulo.render("Opciones", True, BLANCO)
sombra_titulo = fuente_titulo.render("Opciones", True, NEGRO)
rect_titulo = texto_titulo.get_rect(center=(ancho_ventana // 4, 100))
rect_sombra_titulo = sombra_titulo.get_rect(topleft=(rect_titulo.left + 3, rect_titulo.top + 3))

# --- Función para crear botones (reutilizable) ---
def crear_boton(texto, fuente, color_texto, color_fondo, x, y, ancho, alto):
    texto_boton = fuente.render(texto, True, color_texto)
    rect_boton = pygame.Rect(x, y, ancho, alto)
    superficie_boton = pygame.Surface((rect_boton.width, rect_boton.height), pygame.SRCALPHA)
    pygame.draw.rect(superficie_boton, color_fondo, (0, 0, rect_boton.width, rect_boton.height), border_radius=15)
    superficie_boton.blit(texto_boton, (rect_boton.width // 2 - texto_boton.get_width() // 2,
                                        rect_boton.height // 2 - texto_boton.get_height() // 2))
    return superficie_boton, rect_boton

# --- Posicionamiento de los botones ---
x_botones = 50
y_inicial = 270
ancho_boton = 400
alto_boton = 60
espacio_entre_botones = 20

# --- Botones ---
boton_carrera_rapida, rect_carrera_rapida = None, None
boton_trayectoria, rect_trayectoria = None, None
boton_volver, rect_volver = None, None
botones_visibles = False

# --- Caja de texto (input) ---
ancho_input = 350
alto_input = 45
x_input = 0
y_input = 0
rect_input = pygame.Rect(x_input, y_input, ancho_input, alto_input)
color_input_activo = AZUL_RESALTADO
color_input_inactivo = GRIS_CLARO
color_texto_input = BLANCO
placeholder = "Ingresa tu nombre"
texto_ingresa_nombre = fuente_botones.render("Ingresa tu nombre:", True, BLANCO)
rect_ingresa_nombre = None

input_activo = False
texto_input = ""
max_caracteres = 15

# --- Botón Guardar ---
boton_guardar, rect_boton_guardar = crear_boton("Guardar", fuente_botones, BLANCO, GRIS_OSCURO, 0, 0, 160, alto_input * 1.6)

# --- Superficie y Rect para mostrar el nombre ---
superficie_nombre = None
rect_nombre = None

# --- Funciones de Pantallas con Transición---
import pygame
import sys  # Import sys

def pantalla_carrera_rapida(num_jugadores=None):  # Añadimos el parámetro opcional
    transicion_entrada()

    # --- Cargar la imagen de fondo ---
    try:
        fondo_carrera = pygame.image.load("statics/img/F1 pixel art.png")
        fondo_carrera = pygame.transform.scale(fondo_carrera, (ancho_ventana, alto_ventana))
        fondo_carrera = fondo_carrera.convert()
    except FileNotFoundError:
        print("Error: No se encontró la imagen de fondo para Carrera Rápida.")
        fondo_carrera = None

    # --- Textos ---
    titulo = fuente_titulo.render("Carrera Rápida", True, BLANCO)
    rect_titulo = titulo.get_rect(center=(ancho_ventana // 2, 100))

    texto_multijugador = fuente_botones.render("Multijugador:", True, BLANCO)
    rect_multijugador = texto_multijugador.get_rect(center=(ancho_ventana // 2, 250))

    # --- Botones (mejorados) ---
    def crear_boton_mejorado(texto, fuente, color_texto, color_fondo, color_borde, x, y, ancho, alto, radio_borde=15):
        """Crea un botón con borde."""
        texto_boton = fuente.render(texto, True, color_texto)
        rect_boton = pygame.Rect(x, y, ancho, alto)
        superficie_boton = pygame.Surface((rect_boton.width, rect_boton.height), pygame.SRCALPHA)
        # Borde
        pygame.draw.rect(superficie_boton, color_borde, (0, 0, rect_boton.width, rect_boton.height), border_radius=radio_borde)
        # Fondo (más pequeño para que se vea el borde)
        pygame.draw.rect(superficie_boton, color_fondo, (4, 4, rect_boton.width - 8, rect_boton.height - 8), border_radius=radio_borde)

        superficie_boton.blit(texto_boton, (rect_boton.width // 2 - texto_boton.get_width() // 2,
                                            rect_boton.height // 2 - texto_boton.get_height() // 2))
        return superficie_boton, rect_boton

    # --- Botones Jugadores (más grandes) ---
    ancho_boton_jugador = 300
    alto_boton_jugador = 75
    boton_1_jugador, rect_1_jugador = crear_boton_mejorado("1 Jugador", fuente_botones, BLANCO, GRIS_OSCURO, NEGRO, 0, 0, ancho_boton_jugador, alto_boton_jugador)
    boton_2_jugadores, rect_2_jugadores = crear_boton_mejorado("2 Jugadores", fuente_botones, BLANCO, GRIS_OSCURO, NEGRO, 0, 0, ancho_boton_jugador, alto_boton_jugador)

    # Calcula el ancho total y centra (ajustado)
    espacio_entre_botones = 30
    ancho_total_botones = rect_1_jugador.width + rect_2_jugadores.width + espacio_entre_botones
    rect_1_jugador.center = ((ancho_ventana - ancho_total_botones) // 2 + rect_1_jugador.width // 2, 350)
    rect_2_jugadores.center = ((ancho_ventana - ancho_total_botones) // 2 + rect_1_jugador.width + espacio_entre_botones + rect_2_jugadores.width // 2, 350)



    # --- Botón Volver (mejorado) ---
    boton_volver, rect_volver = crear_boton_mejorado("Volver", fuente_botones, BLANCO, GRIS_OSCURO, NEGRO, 0, 0, 150, 50)
    rect_volver.center = (ancho_ventana // 2, 500)

    # --- Bucle principal de ESTA pantalla ---
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # Importante: Regresa al menú principal

            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect_1_jugador.collidepoint(event.pos):
                    print("1 Jugador seleccionado")
                    import carrera_1_jugador  # Importa el módulo
                    carrera_1_jugador.main()   # Ejecuta su función principal
                    return # Importante regresar

                elif rect_2_jugadores.collidepoint(event.pos):
                    print("2 Jugadores seleccionado")
                    import carrera_2_jugadores  # Importa el módulo
                    carrera_2_jugadores.main()   # Ejecuta su función principal.
                    return # Importante regresar

                elif rect_volver.collidepoint(event.pos):
                    return  # Volver al menú principal

            #Resaltado de boton (mejorado)
            if event.type == pygame.MOUSEMOTION:
                # 1 Jugador (actualizado)
                if rect_1_jugador.collidepoint(event.pos):
                    boton_1_jugador, rect_1_jugador = crear_boton_mejorado("1 Jugador", fuente_botones, BLANCO, GRIS_CLARO, AZUL_RESALTADO, rect_1_jugador.x, rect_1_jugador.y, ancho_boton_jugador, alto_boton_jugador)
                else:
                    boton_1_jugador, rect_1_jugador = crear_boton_mejorado("1 Jugador", fuente_botones, BLANCO, GRIS_OSCURO, NEGRO, rect_1_jugador.x, rect_1_jugador.y, ancho_boton_jugador, alto_boton_jugador)
                rect_1_jugador.center = ((ancho_ventana - ancho_total_botones) // 2 + rect_1_jugador.width // 2, 350)

                # 2 Jugadores (actualizado)
                if rect_2_jugadores.collidepoint(event.pos):
                    boton_2_jugadores, rect_2_jugadores = crear_boton_mejorado("2 Jugadores", fuente_botones, BLANCO, GRIS_CLARO, AZUL_RESALTADO, rect_2_jugadores.x, rect_2_jugadores.y, ancho_boton_jugador, alto_boton_jugador)
                else:
                    boton_2_jugadores, rect_2_jugadores = crear_boton_mejorado("2 Jugadores", fuente_botones, BLANCO, GRIS_OSCURO, NEGRO, rect_2_jugadores.x, rect_2_jugadores.y, ancho_boton_jugador, alto_boton_jugador)
                rect_2_jugadores.center = ((ancho_ventana - ancho_total_botones) // 2 + rect_1_jugador.width + espacio_entre_botones + rect_2_jugadores.width // 2, 350)



                if rect_volver.collidepoint(event.pos):
                    boton_volver, rect_volver = crear_boton_mejorado("Volver", fuente_botones, BLANCO, GRIS_CLARO,AZUL_RESALTADO, rect_volver.x, rect_volver.y, 150, 50)
                    rect_volver.center = (ancho_ventana // 2, 500)
                else:
                    boton_volver, rect_volver = crear_boton_mejorado("Volver", fuente_botones, BLANCO, GRIS_OSCURO, NEGRO, rect_volver.x, rect_volver.y, 150, 50)
                    rect_volver.center = (ancho_ventana // 2, 500)



        # --- Dibujado ---
        if fondo_carrera:
            ventana.blit(fondo_carrera, (0, 0))
        ventana.blit(titulo, rect_titulo)
        ventana.blit(texto_multijugador, rect_multijugador)
        ventana.blit(boton_1_jugador, rect_1_jugador)
        ventana.blit(boton_2_jugadores, rect_2_jugadores)
        ventana.blit(boton_volver, rect_volver)
        pygame.display.flip()
        
        
def pantalla_modo_trayectoria():
    transicion_entrada()  # Llama a la función de transición
    ventana.fill(AZUL)
    texto = fuente_titulo.render("Hola mundo2", True, BLANCO)
    rect = texto.get_rect(center=(ancho_ventana // 2, alto_ventana // 2))
    ventana.blit(texto, rect)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

def transicion_entrada():
    """Realiza la transición de entrada (fundido desde negro)."""
    superficie_transicion = pygame.Surface((ancho_ventana, alto_ventana))
    superficie_transicion.fill(NEGRO)
    for alfa in range(0, 256, 10):  # Aumenta la transparencia gradualmente
        superficie_transicion.set_alpha(alfa)
        ventana.blit(superficie_transicion, (0, 0))
        pygame.display.flip()
        pygame.time.delay(20)  # Controla la velocidad de la transición


def actualizar_posiciones(ancho_ventana, alto_ventana):
    global x_input, y_input, rect_input, rect_ingresa_nombre, boton_guardar, rect_boton_guardar, x_botones, y_inicial, rect_titulo, rect_sombra_titulo, superficie_nombre, rect_nombre, boton_carrera_rapida, rect_carrera_rapida, boton_trayectoria, rect_trayectoria, boton_volver, rect_volver

    rect_titulo = texto_titulo.get_rect(center=(ancho_ventana // 4, alto_ventana // 5))
    rect_sombra_titulo = sombra_titulo.get_rect(topleft=(rect_titulo.left + 3, rect_titulo.top + 3))

    if not botones_visibles:
        x_input = (ancho_ventana - ancho_input - 160 - 30) // 2
        y_input = alto_ventana // 2 - alto_input // 2
        rect_input = pygame.Rect(x_input, y_input, ancho_input, alto_input)
        rect_ingresa_nombre = texto_ingresa_nombre.get_rect(midbottom=(x_input + ancho_input // 2, y_input - 5))
        boton_guardar, rect_boton_guardar = crear_boton(
            "Guardar", fuente_botones, BLANCO, GRIS_OSCURO,
            x_input + ancho_input + 30, y_input, 160, alto_input * 1.6
        )
    else:
        x_botones = (ancho_ventana - ancho_boton) // 2
        y_inicial = alto_ventana // 2

        if superficie_nombre is None:
            superficie_nombre = fuente_nombre.render(texto_input, True, BLANCO)
        rect_nombre = superficie_nombre.get_rect(center=(ancho_ventana // 2, y_inicial - 60))

        boton_carrera_rapida, rect_carrera_rapida = crear_boton(
            "Carrera Rápida", fuente_botones, BLANCO, GRIS_OSCURO,
            x_botones, y_inicial, ancho_boton, alto_boton
        )
        boton_trayectoria, rect_trayectoria = crear_boton(
            "Modo Trayectoria", fuente_botones, BLANCO, GRIS_OSCURO,
            x_botones, y_inicial + alto_boton + espacio_entre_botones, ancho_boton, alto_boton
        )
        boton_volver, rect_volver = crear_boton(
            "Salir del Juego", fuente_botones, BLANCO, GRIS_OSCURO,
            x_botones, y_inicial + 2 * (alto_boton + espacio_entre_botones), ancho_boton, alto_boton
        )


# --- Bucle principal ---
pantalla_completa = False
ejecutando = True

actualizar_posiciones(ancho_ventana, alto_ventana)

while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

        if evento.type == pygame.MOUSEMOTION and botones_visibles:
            if rect_carrera_rapida.collidepoint(evento.pos):
                boton_carrera_rapida, rect_carrera_rapida = crear_boton("Carrera Rápida", fuente_botones, BLANCO, GRIS_CLARO, rect_carrera_rapida.x, rect_carrera_rapida.y, ancho_boton, alto_boton)
            else:
                boton_carrera_rapida, rect_carrera_rapida = crear_boton("Carrera Rápida", fuente_botones, BLANCO, GRIS_OSCURO, rect_carrera_rapida.x, rect_carrera_rapida.y, ancho_boton, alto_boton)

            if rect_trayectoria.collidepoint(evento.pos):
                boton_trayectoria, rect_trayectoria = crear_boton("Modo Trayectoria", fuente_botones, BLANCO, GRIS_CLARO, rect_trayectoria.x, rect_trayectoria.y, ancho_boton, alto_boton)
            else:
                boton_trayectoria, rect_trayectoria = crear_boton("Modo Trayectoria", fuente_botones, BLANCO, GRIS_OSCURO, rect_trayectoria.x, rect_trayectoria.y, ancho_boton, alto_boton)

            if rect_volver.collidepoint(evento.pos):
                boton_volver, rect_volver = crear_boton("Salir del Juego", fuente_botones, BLANCO, GRIS_CLARO, rect_volver.x, rect_volver.y, ancho_boton, alto_boton)
            else:
                boton_volver, rect_volver = crear_boton("Salir del Juego", fuente_botones, BLANCO, GRIS_OSCURO, rect_volver.x, rect_volver.y, ancho_boton, alto_boton)

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if not botones_visibles:
                if rect_input.collidepoint(evento.pos):
                    input_activo = not input_activo
                else:
                    input_activo = False

                if rect_boton_guardar.collidepoint(evento.pos) and texto_input.strip():
                    print(f"Nombre guardado: {texto_input}")
                    botones_visibles = True
                    superficie_nombre = fuente_nombre.render(texto_input, True, BLANCO)
                    actualizar_posiciones(ancho_ventana, alto_ventana)

            elif botones_visibles:
                if rect_carrera_rapida.collidepoint(evento.pos):
                    print("¡Has seleccionado Carrera Rápida!")
                    pantalla_carrera_rapida()  # Llama a la función de la pantalla

                elif rect_trayectoria.collidepoint(evento.pos):
                    print("¡Has seleccionado Modo Trayectoria!")
                    pantalla_modo_trayectoria()  # Llama a la función de la pantalla

                elif rect_volver.collidepoint(evento.pos):
                    print("Salir")
                    pygame.quit()
                    sys.exit()

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                print("Saliendo por ESC")
                pygame.quit()
                sys.exit()
            if evento.key == pygame.K_f:
                pantalla_completa = not pantalla_completa
                if pantalla_completa:
                    ventana = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    ventana = pygame.display.set_mode((ancho_ventana, alto_ventana), pygame.RESIZABLE)
                actualizar_posiciones(ancho_ventana, alto_ventana)

            if input_activo:
                if evento.key == pygame.K_BACKSPACE:
                    texto_input = texto_input[:-1]
                elif len(texto_input) < max_caracteres and evento.unicode.isalnum():
                    texto_input += evento.unicode

        if evento.type == pygame.VIDEORESIZE:
            if not pantalla_completa:
                ancho_ventana, alto_ventana = evento.size
                ventana = pygame.display.set_mode((ancho_ventana, alto_ventana), pygame.RESIZABLE)
                superficie_opciones = pygame.Surface((ancho_ventana, alto_ventana), pygame.SRCALPHA)
                if fondo:
                    fondo = pygame.transform.scale(fondo, (ancho_ventana, alto_ventana))
                actualizar_posiciones(ancho_ventana, alto_ventana)

    # --- Lógica de transición de la música ---
    tiempo_transcurrido = pygame.time.get_ticks() - tiempo_inicio
    progreso = min(1.0, tiempo_transcurrido / transicion_duracion)
    nuevo_volumen = progreso
    pygame.mixer.music.set_volume(nuevo_volumen)

    # --- Dibujado de la escena principal ---
    superficie_opciones.fill((0, 0, 0, 0))  # Fondo transparente
    if fondo:
        fondo_con_transparencia = fondo.copy()
        fondo_con_transparencia.set_alpha(int(progreso * 255))
        superficie_opciones.blit(fondo_con_transparencia, (0, 0))
    else:
        superficie_opciones.fill(COLOR_FONDO)

    superficie_opciones.blit(sombra_titulo, rect_sombra_titulo)
    superficie_opciones.blit(texto_titulo, rect_titulo)

    if not botones_visibles:
        superficie_opciones.blit(texto_ingresa_nombre, rect_ingresa_nombre)
        color_input = color_input_activo if input_activo else color_input_inactivo
        pygame.draw.rect(superficie_opciones, color_input, rect_input, border_radius=10)
        pygame.draw.rect(superficie_opciones, NEGRO, rect_input.inflate(-4, -4), border_radius=8)

        if texto_input:
            superficie_texto = fuente_input.render(texto_input, True, color_texto_input)
        else:
            superficie_texto = fuente_placeholder.render(placeholder, True, GRIS_PLACEHOLDER)
        superficie_opciones.blit(superficie_texto, (rect_input.x + 10, rect_input.y + rect_input.height // 2 - superficie_texto.get_height() // 2))
        superficie_opciones.blit(boton_guardar, rect_boton_guardar)
    else:
        superficie_opciones.blit(superficie_nombre, rect_nombre)
        superficie_opciones.blit(boton_carrera_rapida, rect_carrera_rapida)
        superficie_opciones.blit(boton_trayectoria, rect_trayectoria)
        superficie_opciones.blit(boton_volver, rect_volver)


    alfa = int(progreso * 255)
    superficie_opciones.set_alpha(alfa)
    ventana.blit(superficie_opciones, (0, 0))
    pygame.display.flip()

pygame.quit()