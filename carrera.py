import pygame
import sys
import math

# --- Constants ---
ANCHO_VENTANA = 800
ALTO_VENTANA = 600
FPS = 60
BLANCO = (255, 255, 255)

# --- Classes ---

class Jugador(pygame.sprite.Sprite):
    def __init__(self, imagen_coche, x, y):
        super().__init__()
        self.image = pygame.image.load(imagen_coche)
        self.image = pygame.transform.scale(self.image, (50, 25))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # Initial position (center of the screen).
        self.angulo = 0
        self.velocidad = 0
        self.velocidad_maxima = 10
        self.aceleracion = 0.2
        self.friccion = 0.1
        self.giro = 3
        self.imagenes = []
        self.imagen_actual = 0
        # Store original position (center of the screen)
        self.original_x = x
        self.original_y = y

        # Load rotated car images
        base_name = imagen_coche.split(".")[0]
        for i in range(0, 360, 45):
            try:
                imagen = pygame.image.load(f"{base_name}_{i}.png")
                imagen = pygame.transform.scale(imagen, (50, 25))
                self.imagenes.append(imagen)
            except FileNotFoundError:
                self.imagenes.append(self.image)

    def update(self):
        # --- Controls ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.velocidad += self.aceleracion
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.velocidad -= self.aceleracion  # Or could be reverse/brake
        else:
            # Friction (gradual deceleration)
            if self.velocidad > 0:
                self.velocidad -= self.friccion
            elif self.velocidad < 0:
                self.velocidad += self.friccion
            if abs(self.velocidad) < self.friccion:
                self.velocidad = 0

        self.velocidad = max(-self.velocidad_maxima, min(self.velocidad, self.velocidad_maxima))

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.angulo += self.giro
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.angulo -= self.giro

        self.angulo %= 360

        # Image selection
        if self.imagenes:
            self.imagen_actual = int((self.angulo + 22.5) % 360 // 45)
            if self.imagen_actual < len(self.imagenes):
                self.image = self.imagenes[self.imagen_actual]

        # ---  Keep the car centered  ---
        self.rect.center = (self.original_x, self.original_y)

        # --- Movement (SIMULATED - by moving the world) ---
        angulo_rad = math.radians(self.angulo)
        delta_x = self.velocidad * math.cos(angulo_rad)
        delta_y = -self.velocidad * math.sin(angulo_rad)

        return delta_x, delta_y


class Circuito:
    def __init__(self, imagen_ruta, inicio_x, inicio_y, escala=1.0):
        self.imagen = pygame.image.load(imagen_ruta)
        self.imagen_original = self.imagen  # Keep original
        self.ancho_original = self.imagen.get_width()
        self.alto_original = self.imagen.get_height()
        self.escala = escala  # Initial scale
        # DO NOT SCALE YET.  Scale later, in iniciar_carrera.
        self.ancho = self.ancho_original
        self.alto = self.alto_original
        self.superficie = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
        self.superficie.blit(self.imagen, (0, 0))
        self.superficie_rotada = self.superficie
        self.rect = self.superficie.get_rect()
        self.rect_rotado = self.rect
        # Store UNSCALED initial position.
        self.inicio_x = inicio_x
        self.inicio_y = inicio_y
        #World position
        self.x = 0
        self.y = 0

    def rotar(self, angulo, centro_x, centro_y):
        """Rotates the circuit around the *given center point*."""
        self.superficie_rotada = pygame.transform.rotate(self.superficie, angulo)
        self.rect_rotado = self.superficie_rotada.get_rect(center=(centro_x, centro_y))

    def dibujar(self, pantalla, camara_x, camara_y):
        """Draws the rotated circuit surface, offset by the camera."""
        pantalla.blit(self.superficie_rotada, (self.rect_rotado.x - camara_x, self.rect_rotado.y - camara_y))

    def escalar(self, escala):
        """Scales the circuit image and updates related attributes."""
        new_width = int(self.ancho_original * escala)
        new_height = int(self.alto_original * escala)
        self.superficie = pygame.Surface((new_width, new_height), pygame.SRCALPHA)
        scaled_image = pygame.transform.scale(self.imagen_original, (new_width, new_height))
        self.superficie.blit(scaled_image, (0, 0))

        self.ancho = new_width
        self.alto = new_height
        self.superficie_rotada = self.superficie  # Reset rotated surface to the scaled, unrotated surface
        self.rect = self.superficie.get_rect()
        self.rect_rotado = self.rect  # Reset after scaling
        # Scale the stored initial position *relative to the previous scale*.
        self.inicio_x = int(self.inicio_x * (escala / self.escala))
        self.inicio_y = int(self.inicio_y * (escala / self.escala))
        self.escala = escala # Update the stored scale.

    def update(self, delta_x, delta_y):
        # Move the circuit *opposite* to the car's intended movement.
        self.x -= delta_x
        self.y -= delta_y
        self.rect.x = int(self.x) #Update circuit position.
        self.rect.y = int(self.y)


def iniciar_carrera(nombre_carro, circuito_seleccionado):
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Carrera")
    reloj = pygame.time.Clock()

    # --- Load Resources ---
    if nombre_carro == "RB18 #11":
        imagen_carro = "statics/img/red bull.png"
    elif nombre_carro == "AMR22 #5":
        imagen_carro = "statics/img/Aston_Martin.png"
    elif nombre_carro == "SF21 #16":
        imagen_carro = "statics/img/Ferrari.png"
    elif nombre_carro == "MCL36 #3":
        imagen_carro = "statics/img/Mclaren.png"
    else:
        imagen_carro = "statics/img/red bull.png"  # Default

    # --- Create circuit and player ---
    # Get *unscaled* initial position from circuit data.  Use .get() for safety.
    circuito = Circuito(circuito_seleccionado['ruta'],
                        circuito_seleccionado.get('inicio_x', 0),  # Defaults if not found!
                        circuito_seleccionado.get('inicio_y', 0))
    # Player starts at screen center.
    jugador = Jugador(imagen_carro, ANCHO_VENTANA // 2, ALTO_VENTANA // 2)


    # --- Camera and Zoom ---
    camara_x = 0
    camara_y = 0
    zoom_level = 0.4  # Start zoomed in
    circuito.escalar(zoom_level)  # Scale *after* creating Circuito

    # --- Initial Camera Setup (CRITICAL) ---
    # *After* scaling, calculate initial camera position to center the track's start.
    camara_x = circuito.inicio_x - ANCHO_VENTANA // 2
    camara_y = circuito.inicio_y - ALTO_VENTANA // 2

    # --- Initial drawing BEFORE the sound ---
    pantalla.fill(BLANCO)
    circuito.dibujar(pantalla, camara_x, camara_y)  # Draw rotated/scaled circuit
    # Car is *always* drawn at the fixed center of the screen.
    pantalla.blit(jugador.image, (ANCHO_VENTANA // 2 - jugador.rect.width // 2,
                                    ALTO_VENTANA // 2 - jugador.rect.height // 2))
    pygame.display.flip()  # Update the display *before* the wait



    # --- Music and Sound Effects ---
    try:
        # Load and play the countdown sound *before* the music
        semaforo_sound = pygame.mixer.Sound("statics/music/semaforof1.mp3")  # Your countdown sound
        semaforo_sound.play()
        pygame.time.wait(int(semaforo_sound.get_length() * 1000))  # Wait for it to finish

        pygame.mixer.music.load("statics/music/opciones.mp3")  # Your race music
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)  # Loop
    except pygame.error as e:
        print(f"Error loading or playing sound/music: {e}")

    # --- Acceleration Sound Setup ---
    try:
        acelerar_sound = pygame.mixer.Sound("statics/music/acelerar.mp3")
        acelerar_sound.set_volume(0)  # Start silent
        acelerar_channel = pygame.mixer.find_channel() # Use a dedicated channel

    except pygame.error as e:
        print(f"Error loading acceleration sound: {e}")
        acelerar_sound = None  # Set to None if loading fails
        acelerar_channel = None

    playing_acceleration_sound = False  # Flag to manage sound state

    # --- Game Loop ---
    juego_activo = True
    while juego_activo:
        # --- Event Handling ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                juego_activo = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    juego_activo = False
                if evento.key == pygame.K_z:
                    zoom_level += 0.1
                    zoom_level = min(zoom_level, 2.0)
                    circuito.escalar(zoom_level)
                    jugador.rect.center = (ANCHO_VENTANA//2, ALTO_VENTANA//2) #Keep car centered
                    jugador.original_x = jugador.rect.centerx
                    jugador.original_y = jugador.rect.centery
                elif evento.key == pygame.K_x:
                    zoom_level -= 0.1
                    zoom_level = max(zoom_level, 0.2)
                    circuito.escalar(zoom_level)
                    jugador.rect.center = (ANCHO_VENTANA//2, ALTO_VENTANA//2) #Keep car centered.
                    jugador.original_x = jugador.rect.centerx
                    jugador.original_y = jugador.rect.centery

                # --- Sound control with key press/release ---
                if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                    if acelerar_channel and not playing_acceleration_sound:
                        acelerar_channel.play(acelerar_sound, loops=-1)  # Play looped
                        #acelerar_channel.set_pos(4.0)  # REMOVE THIS
                        playing_acceleration_sound = True


            elif evento.type == pygame.KEYUP:
                if (evento.key == pygame.K_UP or evento.key == pygame.K_w):
                    playing_acceleration_sound = False #Set to false, and manage in update.


        # --- Sound Volume Management (in the main loop!) ---
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and acelerar_sound:
            # Increase volume up to a maximum (e.g., 1.0)
            new_volume = min(acelerar_sound.get_volume() + 0.02, 1.0)
            acelerar_sound.set_volume(new_volume)
            # Check and loop sound
            if acelerar_channel and acelerar_channel.get_pos() / 1000 >= 20.0:
                #acelerar_channel.set_pos(4.0) # REMOVE THIS
                acelerar_sound.play(loops=-1, start=4.0)  # USE THIS

        elif not playing_acceleration_sound and acelerar_sound:  # Key released, and sound loaded
            # Decrease volume
            new_volume = max(acelerar_sound.get_volume() - 0.02, 0.0)
            acelerar_sound.set_volume(new_volume)
            if new_volume <= 0:
                if acelerar_channel:
                    acelerar_channel.stop()  # Stop the *channel*
            #else: # REMOVE THIS - No need to set position on release
            #    if acelerar_channel:
            #        acelerar_channel.set_pos(4.0)

        # --- Game Updates ---
        delta_x, delta_y = jugador.update()  # Get intended movement
        circuito.update(delta_x, delta_y) #Move the world
        circuito.rotar(jugador.angulo, ANCHO_VENTANA // 2, ALTO_VENTANA // 2) #Rotate around the center

        # --- Camera Update (Simplified) ---
        # Camera *always* centers on the rotated circuit's center.
        camara_x = circuito.rect_rotado.centerx - ANCHO_VENTANA // 2
        camara_y = circuito.rect_rotado.centery - ALTO_VENTANA // 2


        # --- Drawing ---
        pantalla.fill(BLANCO)  # White background
        circuito.dibujar(pantalla, camara_x, camara_y)  # Draw rotated/scaled circuit

        # Car is *always* drawn at the fixed center of the screen.
        pantalla.blit(jugador.image, (ANCHO_VENTANA // 2 - jugador.rect.width // 2,
                                        ALTO_VENTANA // 2 - jugador.rect.height // 2))

        pygame.display.flip()
        reloj.tick(FPS)

    pygame.quit()