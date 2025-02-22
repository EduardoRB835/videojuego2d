import pygame
import math
import subprocess
import sys
import threading  # Importante: Importar el módulo threading

# Inicializar Pygame
pygame.init()

# Dimensiones de la ventana
ancho_ventana = 800
alto_ventana = 600
ventana = pygame.display.set_mode((ancho_ventana, alto_ventana))

# Título de la ventana
pygame.display.set_caption("Fórmula 1 - Edición Pixel 2025")

# Cargar la imagen de fondo
fondo = pygame.image.load("statics/img/F1 pixel art.png").convert()  # Reemplaza con la ruta correcta

# Escalar la imagen de fondo a las dimensiones de la ventana
fondo = pygame.transform.scale(fondo, (ancho_ventana, alto_ventana))

# --- Fuentes personalizadas ---
fuente_titulo = pygame.font.Font("statics/fonts/PixelifySans-VariableFont_wght.ttf", 90)  # Reemplaza si usas otra fuente
fuente_carga = pygame.font.Font("statics/fonts/PixelifySans-VariableFont_wght.ttf", 36)
fuente_bienvenida = pygame.font.Font("statics/fonts/PixelifySans-VariableFont_wght.ttf", 72)
fuente_boton = pygame.font.Font("statics/fonts/PixelifySans-VariableFont_wght.ttf", 48)

# Definir el nombre del juego
nombre_juego = "Fórmula 1 - Edición Pixel 2025"

# Renderizar el nombre del juego
texto_nombre = fuente_titulo.render(nombre_juego, True, (255, 255, 255))
texto_nombre = pygame.transform.scale(texto_nombre, (texto_nombre.get_width() // 2, texto_nombre.get_height() // 2))
rect_texto = texto_nombre.get_rect()
rect_texto.center = (ancho_ventana // 2, alto_ventana // 2)

# Variables para el ondeamiento
amplitud = 0.02
frecuencia = 0.01
desfase = 0

# Variables para la transición del texto
tiempo_inicio = pygame.time.get_ticks()
transicion_completada = False

# Cargar la música
pygame.mixer.music.load("statics/music/formula1.mp3") # Reemplaza con la ruta correcta
pygame.mixer.music.set_volume(1.0)  # Volumen inicial

# --- Pantalla de carga ---
carrito_original = pygame.image.load("statics/img/N1 F1.png").convert_alpha() # Reemplaza con la ruta correcta

# Escalado ANTIALIASADO del carrito
carrito = pygame.transform.smoothscale(carrito_original, (carrito_original.get_width() * 2, carrito_original.get_height() * 2))


texto_carga = fuente_carga.render("CARGANDO...", True, (255, 255, 255))
rect_texto_carga = texto_carga.get_rect()
rect_texto_carga.center = (ancho_ventana // 2, alto_ventana - 50)
distancia_al_texto = 118
carrito_x = rect_texto_carga.left - distancia_al_texto - carrito.get_width()
posicion_final_carrito = rect_texto_carga.right + distancia_al_texto
distancia_carrito = posicion_final_carrito - carrito_x
velocidad_carrito = distancia_carrito / 5000
tiempo_inicio_carga = pygame.time.get_ticks()
puntos = []

# Variable para la rotación del neumático
angulo_rotacion = 0

cargando = True
while cargando:
    # Manejar eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            cargando = False
            ejecutando = False  # Salir del bucle principal también

    # Calcular el tiempo transcurrido en la pantalla de carga
    tiempo_transcurrido_carga = pygame.time.get_ticks() - tiempo_inicio_carga

    # Si han pasado 5 segundos, salir de la pantalla de carga
    if tiempo_transcurrido_carga > 5000:
        cargando = False

    # Mover el carrito
    carrito_x += velocidad_carrito  # Usar la velocidad calculada
    # Verificar si el carrito ha llegado a la posición final
    if carrito_x > posicion_final_carrito:
        carrito_x = rect_texto_carga.left - distancia_al_texto - carrito.get_width()  # Reiniciar posición

    # Rotar el carrito (neumático) - Usar rotación ANTIALIASADA
    angulo_rotacion -= velocidad_carrito * 5 # Ajusta la velocidad de rotación aquí
    carrito_rotado = pygame.transform.rotozoom(carrito, angulo_rotacion, 1)  # Usamos rotozoom con escala 1
    rect_carrito_rotado = carrito_rotado.get_rect(center = (carrito_x + carrito.get_width() // 2, rect_texto_carga.y - carrito.get_height() // 2 - 20))


    # Agregar un punto a la lista, ajustando la posición vertical.  Usamos el centro del carrito rotado.
    puntos.append((rect_carrito_rotado.centerx, rect_carrito_rotado.centery))
    if len(puntos) > 100:  # Ajustar la longitud del rastro de puntos
        puntos.pop(0)

    # Dibujar la pantalla de carga
    ventana.fill((0, 0, 0))  # Rellenar la pantalla con negro

    # Dibujar los puntos
    for punto in puntos:
        pygame.draw.circle(ventana, (255, 255, 255), punto, 3)

    # Dibujar el carrito rotado
    ventana.blit(carrito_rotado, rect_carrito_rotado)
    ventana.blit(texto_carga, rect_texto_carga)

    # Actualizar la pantalla
    pygame.display.flip()

# --- Fin de la pantalla de carga ---


# Reproducir la música en bucle
pygame.mixer.music.play(-1)

# Variables para controlar la aparición de los mensajes
mostrar_bienvenida = False
mostrar_correr = False
tiempo_bienvenida = 0

# Inicializar las posiciones de los mensajes
rect_bienvenida = pygame.Rect(0, alto_ventana, 0, 0)
rect_correr = pygame.Rect(0, alto_ventana, 0, 0)

# --- Botón COMENZAR ---
mostrar_boton = False
parpadeo_boton = False  # Flag para controlar el estado de parpadeo
tiempo_parpadeo = 0
num_parpadeos = 0
boton_visible = True  # Controla si el botón se dibuja o no
texto_boton = fuente_boton.render("COMENZAR", True, (255, 255, 255))
rect_boton = texto_boton.get_rect()
rect_boton.center = (ancho_ventana // 2, alto_ventana - 100)

# --- Variables para la transición a la siguiente pantalla ---
transicionando = False
alpha = 0  #  alpha para la superficie de desvanecimiento
# Volumen al final de la transición.
volumen_final = 0
transicion_duracion = 3000  # Duración de la transición en milisegundos (3 segundos)
tiempo_inicio_transicion = 0


# --- Función para ejecutar el otro archivo ---
def ejecutar_otro_archivo():
    try:
        # --- Ejecutar opciones.py en un hilo separado ---
        hilo_opciones = threading.Thread(target=ejecutar_opciones)
        hilo_opciones.start()

    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el otro archivo: {e}")
    except FileNotFoundError:
        print("Error: No se encontró el archivo 'opciones.py'.")

def ejecutar_opciones():
    """Función que se ejecutará en el hilo separado."""
    subprocess.run([r"c:/videojuego2d/.venv/Scripts/python.exe", "opciones.py"], check=True)



# Bucle principal del juego
ejecutando = True
while ejecutando:
    # Manejar eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        # --- Detectar clic en el botón ---
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if rect_boton.collidepoint(evento.pos) and mostrar_boton and boton_visible:
                transicionando = True  # Iniciar la transición
                tiempo_inicio_transicion = pygame.time.get_ticks() # Guarda el tiempo de inicio


    # --- Lógica de la transición ---
    if transicionando:
        # Calcular el tiempo transcurrido desde el inicio de la transición
        tiempo_transcurrido = pygame.time.get_ticks() - tiempo_inicio_transicion

        # Calcular el progreso de la transición (0.0 a 1.0)
        progreso = min(1.0, tiempo_transcurrido / transicion_duracion)

        # Calcular el alpha basado en el progreso.
        alpha = int(progreso * 255)

        # Disminuir el volumen gradualmente
        nuevo_volumen = 1.0 - progreso # El volumen disminuye linealmente
        pygame.mixer.music.set_volume(nuevo_volumen)

        if progreso >= 1.0:  # La transición ha terminado
            pygame.mixer.music.stop() # Detener la musica por completo

            # --- CERRAR la ventana y SALIR del script actual ANTES de ejecutar el otro archivo---
            pygame.quit()
            ejecutar_otro_archivo()  # Llama a la función para ejecutar el otro archivo (en un hilo)
            sys.exit() # Importantisimo


    # Calcular el tiempo transcurrido (para el movimiento del título)
    tiempo_transcurrido = pygame.time.get_ticks() - tiempo_inicio

    # Si han pasado 5 segundos y la transición no se ha completado
    if tiempo_transcurrido > 5000 and not transicion_completada:
        # Mover el texto hacia arriba lentamente
        rect_texto.y -= 1

        # Si el texto llega a la posición final, marcar la transición como completada
        # y activar la aparición del mensaje de bienvenida
        if rect_texto.top <= 20:
            transicion_completada = True
            mostrar_bienvenida = True
            tiempo_bienvenida = pygame.time.get_ticks()

            # Definir el mensaje de bienvenida
            texto_bienvenida = fuente_bienvenida.render("¡Bienvenido, piloto!", True, (255, 255, 0))
            rect_bienvenida = texto_bienvenida.get_rect()
            rect_bienvenida.center = (ancho_ventana // 2, alto_ventana)

            # Definir el mensaje "Es hora de correr!"
            texto_correr = fuente_bienvenida.render("¡Es hora de correr!", True, (255, 255, 0))
            rect_correr = texto_correr.get_rect()
            rect_correr.center = (ancho_ventana // 2, alto_ventana)

    # Si se debe mostrar el segundo mensaje y han pasado 4 segundos desde que apareció el primero
    if mostrar_bienvenida and pygame.time.get_ticks() - tiempo_bienvenida > 4000:
        mostrar_correr = True

    # Mover los mensajes hacia arriba
    if mostrar_bienvenida:
        rect_bienvenida.y -= 1
        if rect_bienvenida.centery < alto_ventana // 2 - 50:
            rect_bienvenida.centery = alto_ventana // 2 - 50

    if mostrar_correr:
        rect_correr.y -= 1
        if rect_correr.centery < alto_ventana // 2 + 50:
            rect_correr.centery = alto_ventana // 2 + 50

    # Controlar la aparición del botón (y su parpadeo)
    if mostrar_correr and rect_correr.centery == alto_ventana // 2 + 50 and not mostrar_boton:
        mostrar_boton = True
        tiempo_parpadeo = pygame.time.get_ticks()  # Iniciar el conteo para el parpadeo
        parpadeo_boton = True  # Activar el parpadeo

    if parpadeo_boton:
        if pygame.time.get_ticks() - tiempo_parpadeo > 500:  # Alternar cada 500 ms
            boton_visible = not boton_visible
            num_parpadeos += 1
            tiempo_parpadeo = pygame.time.get_ticks()  # Reiniciar el temporizador

        if num_parpadeos >= 6:  # 6 cambios = 3 parpadeos
            parpadeo_boton = False  # Detener el parpadeo
            boton_visible = True  # Asegurar que el botón quede visible

    # Crear una nueva superficie para la imagen ondeada
    fondo_ondeado = pygame.Surface((ancho_ventana, alto_ventana))

    for x in range(ancho_ventana):
        factor_escala = 1 + amplitud * math.sin(frecuencia * pygame.time.get_ticks() + desfase + x * 0.1)
        factor_escala = abs(factor_escala)
        porcion_fondo = pygame.Surface((1, alto_ventana))
        porcion_fondo.blit(fondo, (0, 0), (x, 0, 1, alto_ventana))
        porcion_escalada = pygame.transform.scale(porcion_fondo, (1, int(alto_ventana * factor_escala)))
        fondo_ondeado.blit(porcion_escalada, (x, (alto_ventana - porcion_escalada.get_height()) // 2))

    # --- Dibujado (solo si NO estamos en transición) ---
    if not transicionando:
        ventana.blit(fondo_ondeado, (0, 0))
        ventana.blit(texto_nombre, rect_texto)

        if mostrar_bienvenida:
            ventana.blit(texto_bienvenida, rect_bienvenida)

        if mostrar_correr:
            ventana.blit(texto_correr, rect_correr)

        if mostrar_boton and boton_visible:
            pygame.draw.rect(ventana, (255, 255, 255), rect_boton, 2)
            ventana.blit(texto_boton, rect_boton)

    # --- Aplicar superficie de desvanecimiento ---
    if transicionando:
        superficie_transicion = pygame.Surface((ancho_ventana, alto_ventana))
        superficie_transicion.set_alpha(alpha)  # Usamos el alpha calculado
        superficie_transicion.fill((0, 0, 0))  # Rellenar de negro
        ventana.blit(superficie_transicion, (0, 0))

    pygame.display.flip()

# Salir de Pygame (esto solo se ejecutará si `ejecutando` es False)
pygame.quit()