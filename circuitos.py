import pygame
import sys
import carrera  # Import the carrera module

# --- Constants ---
ANCHO_VENTANA = 800
ALTO_VENTANA = 600
COLOR_FONDO = (25, 25, 25)
COLOR_BOTON = (0, 119, 187)
COLOR_TEXTO_BOTON = (255, 255, 255)
COLOR_BORDE_SELECCIONADO = (255, 165, 0)
COLOR_SOMBRA = (15, 15, 15)
FPS = 60

class SelectorCircuitos:
    def __init__(self, circuitos):
        """Inicializa el selector."""
        self.circuitos = circuitos
        self.indice_actual = 0
        self.imagenes = []
        self.ancho_imagen = 280
        self.alto_imagen = 168
        self.cargar_imagenes()

        # Posiciones
        self.posicion_x = (ANCHO_VENTANA - self.ancho_imagen) // 2
        self.posicion_y = (ALTO_VENTANA - self.alto_imagen) // 2 - 80

        # Flechas
        self.flecha_izquierda = self.cargar_imagen_pixel("statics/img/FlechaIzquierda.png", (45, 45))
        self.rect_flecha_izq = self.flecha_izquierda.get_rect(
            topleft=(20, ALTO_VENTANA // 2 - 22)
        )
        self.flecha_derecha = self.cargar_imagen_pixel("statics/img/FlechaDerecha.png", (45, 45))
        self.rect_flecha_der = self.flecha_derecha.get_rect(
            topleft=(ANCHO_VENTANA - 65, ALTO_VENTANA // 2 - 22)
        )

        # Animación
        self.desplazamiento_objetivo = 0
        self.desplazamiento_actual = 0
        self.velocidad_desplazamiento = 20
        self.direccion = 0

        # Botón de selección
        self.boton_seleccionar = pygame.Rect(ANCHO_VENTANA // 2 - 75, ALTO_VENTANA - 80, 150, 45)
        self.boton_sombra = pygame.Rect(ANCHO_VENTANA // 2 - 73, ALTO_VENTANA - 78, 150, 45)
        self.circuito_seleccionado = None
        self.nombre_carro = ""  # Initialize

        # Título
        self.font_titulo = pygame.font.Font("statics/fonts/PixelifySans-VariableFont_wght.ttf", 56)
        self.titulo_texto = self.font_titulo.render("Selecciona un Circuito", True, (240, 240, 240))
        self.titulo_rect = self.titulo_texto.get_rect(center=(ANCHO_VENTANA // 2, 60))

        # Fondo
        self.fondo = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA))
        self.crear_fondo()

        # Música
        pygame.mixer.init()
        self.musica_fondo = "statics/music/formula1.mp3"
        self.cargar_musica()

    def cargar_musica(self):
        """Carga y reproduce la música."""
        try:
            pygame.mixer.music.load(self.musica_fondo)
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"Error al cargar o reproducir la música: {e}")

    def crear_fondo(self):
        """Crea el fondo con un patrón sutil."""
        self.fondo.fill(COLOR_FONDO)
        cuadricula = 40
        for x in range(0, ANCHO_VENTANA, cuadricula):
            for y in range(0, ALTO_VENTANA, cuadricula):
                rect = pygame.Rect(x, y, cuadricula, cuadricula)
                if (x // cuadricula + y // cuadricula) % 2 == 0:
                    pygame.draw.rect(self.fondo, (30, 30, 30), rect)


    def cargar_imagen_pixel(self, ruta, tamano):
        """Carga y escala imágenes."""
        try:
            imagen = pygame.image.load(ruta)
            imagen = pygame.transform.scale(imagen, tamano)
            return imagen
        except FileNotFoundError:
            print(f"Error: No se encontró la imagen en {ruta}")
            sys.exit()

    def cargar_imagenes(self):
        """Carga las imágenes de los circuitos."""
        for circuito_data in self.circuitos:
            imagen = self.cargar_imagen_pixel(circuito_data['ruta'], (self.ancho_imagen, self.alto_imagen))
            self.imagenes.append(imagen)

    def siguiente_circuito(self):
        if not self.imagenes or self.direccion != 0: return
        self.direccion = -1
        self.desplazamiento_objetivo = -ANCHO_VENTANA

    def anterior_circuito(self):
        if not self.imagenes or self.direccion != 0: return
        self.direccion = 1
        self.desplazamiento_objetivo = ANCHO_VENTANA

    def seleccionar_circuito(self):
        self.circuito_seleccionado = self.indice_actual
        print(f"Circuito seleccionado: {self.circuitos[self.indice_actual]['nombre']}")
        # --- IMPORTANT ---
        carrera.iniciar_carrera(self.nombre_carro, self.circuitos[self.indice_actual])
        return  # Exit the circuit selector

    def actualizar(self):
        if not self.imagenes: return
        if self.desplazamiento_actual < self.desplazamiento_objetivo:
            self.desplazamiento_actual += self.velocidad_desplazamiento
        elif self.desplazamiento_actual > self.desplazamiento_objetivo:
            self.desplazamiento_actual -= self.velocidad_desplazamiento
        if abs(self.desplazamiento_objetivo - self.desplazamiento_actual) < self.velocidad_desplazamiento:
            self.desplazamiento_actual = 0
            self.desplazamiento_objetivo = 0
            self.indice_actual = (self.indice_actual + self.direccion) % len(self.imagenes)
            self.direccion = 0

    def dibujar(self, pantalla):
        if not self.imagenes: return

        # Dibuja el fondo
        pantalla.blit(self.fondo, (0, 0))

        # Mostrar el nombre del carro seleccionado
        font_carro = pygame.font.Font("statics/fonts/PixelifySans-VariableFont_wght.ttf", 32)
        texto_carro = font_carro.render(f"Carro: {self.nombre_carro}", True, (255, 255, 255))
        rect_carro = texto_carro.get_rect(center=(ANCHO_VENTANA // 2, 25))
        pantalla.blit(texto_carro, rect_carro)

        # Título
        pantalla.blit(self.titulo_texto, self.titulo_rect)

        # Circuitos
        imagen_actual = self.imagenes[self.indice_actual]
        rect_actual = imagen_actual.get_rect(
            topleft=(self.posicion_x + self.desplazamiento_actual * self.direccion, self.posicion_y)
        )
        pygame.draw.rect(pantalla, (50, 50, 50), rect_actual.inflate(8, 8), 4)
        pantalla.blit(imagen_actual, rect_actual)

        indice_siguiente = (self.indice_actual + self.direccion) % len(self.imagenes)
        imagen_siguiente = self.imagenes[indice_siguiente]
        rect_siguiente = imagen_siguiente.get_rect(topleft=(
            self.posicion_x + self.desplazamiento_actual * self.direccion + ANCHO_VENTANA * -self.direccion,
            self.posicion_y
        ))
        pygame.draw.rect(pantalla, (50, 50, 50), rect_siguiente.inflate(8, 8), 4)
        pantalla.blit(imagen_siguiente, rect_siguiente)


        # Flechas
        pantalla.blit(self.flecha_izquierda, self.rect_flecha_izq)
        pantalla.blit(self.flecha_derecha, self.rect_flecha_der)

        # Información del circuito
        font = pygame.font.Font("statics/fonts/PixelifySans-VariableFont_wght.ttf", 26)
        circuito_actual_data = self.circuitos[self.indice_actual]

        # Nombre
        nombre_texto = font.render(circuito_actual_data['nombre'], True, (255, 255, 255))
        sombra_nombre = font.render(circuito_actual_data['nombre'], True, COLOR_SOMBRA)
        nombre_rect = nombre_texto.get_rect(center=(ANCHO_VENTANA // 2, self.posicion_y + self.alto_imagen + 35))
        pantalla.blit(sombra_nombre, (nombre_rect.x + 2, nombre_rect.y + 2))
        pantalla.blit(nombre_texto, nombre_rect)

        # Descripción
        descripcion_texto = font.render(circuito_actual_data['descripcion'], True, (220, 220, 220))
        sombra_descripcion = font.render(circuito_actual_data['descripcion'], True, COLOR_SOMBRA)
        descripcion_rect = descripcion_texto.get_rect(center=(ANCHO_VENTANA // 2, nombre_rect.bottom + 25))
        pantalla.blit(sombra_descripcion, (descripcion_rect.x + 2, descripcion_rect.y + 2))
        pantalla.blit(descripcion_texto, descripcion_rect)

        # Atributos
        if 'atributos' in circuito_actual_data:
            atributos = circuito_actual_data['atributos']
            y_offset = descripcion_rect.bottom + 35
            for key, value in atributos.items():
                atributo_texto = font.render(f"{key.capitalize()}: {value}", True, (240, 240, 240))
                sombra_atributo = font.render(f"{key.capitalize()}: {value}", True, COLOR_SOMBRA)
                atributo_rect = atributo_texto.get_rect(center=(ANCHO_VENTANA // 2, y_offset))
                pantalla.blit(sombra_atributo, (atributo_rect.x+2, atributo_rect.y + 2))
                pantalla.blit(atributo_texto, atributo_rect)
                y_offset += 30

        # Botón de selección
        pygame.draw.rect(pantalla, COLOR_SOMBRA, self.boton_sombra, border_radius=12)
        pygame.draw.rect(pantalla, COLOR_BOTON, self.boton_seleccionar, border_radius=12)

        texto_boton = font.render("Seleccionar", True, COLOR_TEXTO_BOTON)
        texto_boton_rect = texto_boton.get_rect(center=self.boton_seleccionar.center)
        pantalla.blit(texto_boton, texto_boton_rect)

        # Resaltar si está seleccionado
        if self.circuito_seleccionado == self.indice_actual:
            pygame.draw.rect(pantalla, COLOR_BORDE_SELECCIONADO, rect_actual.inflate(10, 10), 5)

        pygame.display.flip()

def manejar_eventos(selector):
    """Maneja los eventos."""
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                return False
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                if selector.rect_flecha_izq.collidepoint(evento.pos):
                    selector.anterior_circuito()
                elif selector.rect_flecha_der.collidepoint(evento.pos):
                    selector.siguiente_circuito()
                elif selector.boton_seleccionar.collidepoint(evento.pos):
                    selector.seleccionar_circuito()
                    return False  # Exit after selection
    return True

def main(nombre_carro):
    """Función principal para la selección de circuitos."""
    pygame.init()
    ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Selector de Circuitos")
    reloj = pygame.time.Clock()

    # --- CIRCUIT DATA (NOW WITH STARTING POSITIONS) ---
    circuitos = [
        {
            'ruta': "statics/img/pista1.png",
            'nombre': "Bharain",
            'descripcion': "Un circuito para Novatos.",
            'atributos': {'Curvas': 4, 'Longitud': '3.337 km'},
            'inicio_x': 395,  # Use the value you found
            'inicio_y': 815   # Use the value you found
        },
        {
            'ruta': "statics/img/pista2.png",
            'nombre': "Imola",
            'descripcion': "Un circuito rápido y fluido.",
            'atributos': {'Curvas': 6, 'Longitud': '5.891 km'},
            'inicio_x': 591,  # Example: Replace with actual values
            'inicio_y': 1062
        },
        {
            'ruta': "statics/img/pista3.png",
            'nombre': "Monza",
            'descripcion': "Circuito con cambios de elevación.",
            'atributos': {'Curvas': 14, 'Longitud': '4.309 km'},
            'inicio_x': 216,  # Example: Replace with actual values
            'inicio_y': 817
        },
    ]
    # --- End of circuit data ---

    selector = SelectorCircuitos(circuitos)
    selector.nombre_carro = nombre_carro
    juego_activo = True

    while juego_activo:
        juego_activo = manejar_eventos(selector)
        if not juego_activo:
            break

        selector.actualizar()
        selector.dibujar(ventana)
        reloj.tick(FPS)

    pygame.quit()
    return selector, nombre_carro

if __name__ == "__main__":
    main("Coche Demo")  # This only runs if you run circuitos.py directly