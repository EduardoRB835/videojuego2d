import pygame
import sys
import circuitos

# --- Constantes ---
ANCHO_VENTANA = 800
ALTO_VENTANA = 600
COLOR_FONDO = (25, 25, 25)  # Gris más oscuro
COLOR_BOTON = (0, 119, 187)  # Azul más vibrante
COLOR_TEXTO_BOTON = (255, 255, 255)  # Blanco
COLOR_BORDE_SELECCIONADO = (255, 165, 0)  # Naranja
COLOR_SOMBRA = (15, 15, 15)  # Sombra más sutil
FPS = 60

class SelectorCarros:
    """Maneja la lógica de selección de carros y su visualización."""

    def __init__(self, carros):
        """Inicializa el selector."""
        self.carros = carros
        self.indice_actual = 0
        self.imagenes = []
        self.ancho_imagen = 240  # Imagen más grande
        self.alto_imagen = 120  # Imagen más grande
        self.cargar_imagenes()

        # Posiciones
        self.posicion_x = (ANCHO_VENTANA - self.ancho_imagen) // 2
        self.posicion_y = (ALTO_VENTANA - self.alto_imagen) // 2 - 80 # Subido

        # Flechas
        self.flecha_izquierda = self.cargar_imagen_pixel("statics/img/FlechaIzquierda.png", (45, 45))  # Flechas más grandes
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
        self.velocidad_desplazamiento = 20  # Más rápido
        self.direccion = 0

        # Botón de selección
        self.boton_seleccionar = pygame.Rect(ANCHO_VENTANA // 2 - 75, ALTO_VENTANA - 80, 150, 45)  # Botón más grande
        self.boton_sombra = pygame.Rect(ANCHO_VENTANA // 2 - 73, ALTO_VENTANA - 78, 150, 45) # Sombra ajustada
        self.carro_seleccionado = None

        # Título
        self.font_titulo = pygame.font.Font("statics/fonts/PixelifySans-VariableFont_wght.ttf", 56)  # Título más grande
        self.titulo_texto = self.font_titulo.render("Selecciona tu Monoplaza", True, (240, 240, 240)) # Texto más claro
        self.titulo_rect = self.titulo_texto.get_rect(center=(ANCHO_VENTANA // 2, 60)) # Posición ajustada

        # Fondo
        self.fondo = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA))
        self.crear_fondo()

        # --- Música ---
        pygame.mixer.init()  # Inicializa el módulo de sonido de Pygame
        self.musica_fondo = "statics/music/formula1.mp3"
        self.cargar_musica()


    def cargar_musica(self):
        """Carga y reproduce la música de fondo."""
        try:
            pygame.mixer.music.load(self.musica_fondo)
            pygame.mixer.music.set_volume(0.2)  # Ajusta el volumen (0.0 a 1.0), un poco más bajo
            pygame.mixer.music.play(-1)  # Reproduce en bucle (-1)
        except pygame.error as e:
            print(f"Error al cargar o reproducir la música: {e}")


    def crear_fondo(self):
        """Crea el fondo con un patrón sutil."""
        self.fondo.fill(COLOR_FONDO) # Color de fondo base.
        cuadricula = 40  # Cuadrícula más grande
        for x in range(0, ANCHO_VENTANA, cuadricula):
            for y in range(0, ALTO_VENTANA, cuadricula):
                rect = pygame.Rect(x, y, cuadricula, cuadricula)
                if (x // cuadricula + y // cuadricula) % 2 == 0:
                    pygame.draw.rect(self.fondo, (30, 30, 30), rect) #Cuadrados un poco mas oscuros.


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
        """Carga las imágenes de los carros."""
        for carro_data in self.carros:
            imagen = self.cargar_imagen_pixel(carro_data['ruta'], (self.ancho_imagen, self.alto_imagen))
            self.imagenes.append(imagen)

    def siguiente_carro(self):
        if not self.imagenes or self.direccion != 0: return
        self.direccion = -1
        self.desplazamiento_objetivo = -ANCHO_VENTANA

    def anterior_carro(self):
        if not self.imagenes or self.direccion != 0: return
        self.direccion = 1
        self.desplazamiento_objetivo = ANCHO_VENTANA

    def seleccionar_carro(self):
        self.carro_seleccionado = self.indice_actual
        nombre_carro = self.carros[self.indice_actual]['nombre']  # Obtén el nombre
        print(f"Carro seleccionado: {nombre_carro}")
        selector_circuitos, carro_seleccionado = circuitos.main(nombre_carro) #pasa el nombre
        indice_circuito = selector_circuitos.circuito_seleccionado
        circuito_elegido = selector_circuitos.circuitos[indice_circuito]


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

        # Título
        pantalla.blit(self.titulo_texto, self.titulo_rect)

        # Carros - Añadido borde a las imágenes
        imagen_actual = self.imagenes[self.indice_actual]
        rect_actual = imagen_actual.get_rect(
            topleft=(self.posicion_x + self.desplazamiento_actual * self.direccion, self.posicion_y)
        )
        pygame.draw.rect(pantalla, (50,50,50), rect_actual.inflate(8,8), 4) #Borde.
        pantalla.blit(imagen_actual, rect_actual)

        indice_siguiente = (self.indice_actual + self.direccion) % len(self.imagenes)
        imagen_siguiente = self.imagenes[indice_siguiente]
        rect_siguiente = imagen_siguiente.get_rect(topleft=(
            self.posicion_x + self.desplazamiento_actual * self.direccion + ANCHO_VENTANA * -self.direccion,
            self.posicion_y
        ))
        pygame.draw.rect(pantalla, (50,50,50), rect_siguiente.inflate(8,8), 4) #Borde.
        pantalla.blit(imagen_siguiente, rect_siguiente)


        # Flechas
        pantalla.blit(self.flecha_izquierda, self.rect_flecha_izq)
        pantalla.blit(self.flecha_derecha, self.rect_flecha_der)

        # Información del carro
        font = pygame.font.Font("statics/fonts/PixelifySans-VariableFont_wght.ttf", 26)  # Fuente más grande
        carro_actual_data = self.carros[self.indice_actual]

        # Nombre - Con sombreado
        nombre_texto = font.render(carro_actual_data['nombre'], True, (255, 255, 255))
        sombra_nombre = font.render(carro_actual_data['nombre'], True, COLOR_SOMBRA)
        nombre_rect = nombre_texto.get_rect(center=(ANCHO_VENTANA // 2, self.posicion_y + self.alto_imagen + 35))#ajuste
        pantalla.blit(sombra_nombre, (nombre_rect.x + 2, nombre_rect.y + 2))
        pantalla.blit(nombre_texto, nombre_rect)

        # Descripción - Con sombreado
        descripcion_texto = font.render(carro_actual_data['descripcion'], True, (220, 220, 220)) # Color más claro
        sombra_descripcion = font.render(carro_actual_data['descripcion'], True, COLOR_SOMBRA)
        descripcion_rect = descripcion_texto.get_rect(center=(ANCHO_VENTANA // 2, nombre_rect.bottom + 25)) # ajuste
        pantalla.blit(sombra_descripcion, (descripcion_rect.x + 2, descripcion_rect.y + 2))
        pantalla.blit(descripcion_texto, descripcion_rect)

        # Atributos - Con sombreado y mejor espaciado
        if 'atributos' in carro_actual_data:
            atributos = carro_actual_data['atributos']
            y_offset = descripcion_rect.bottom + 35 # Más espacio.
            for key, value in atributos.items():
                atributo_texto = font.render(f"{key.capitalize()}: {value}", True, (240, 240, 240)) # Color más claro
                sombra_atributo = font.render(f"{key.capitalize()}: {value}", True, COLOR_SOMBRA)
                atributo_rect = atributo_texto.get_rect(center=(ANCHO_VENTANA // 2, y_offset))
                pantalla.blit(sombra_atributo, (atributo_rect.x + 2, atributo_rect.y +2))
                pantalla.blit(atributo_texto, atributo_rect)

                y_offset += 30  # Más espacio entre atributos

        # Botón de selección - Estilo "Neumorphism"
        pygame.draw.rect(pantalla, COLOR_SOMBRA, self.boton_sombra, border_radius=12) #Bordes redondeados.
        pygame.draw.rect(pantalla, COLOR_BOTON, self.boton_seleccionar, border_radius=12) #Bordes redondeados.
        texto_boton = font.render("Seleccionar", True, COLOR_TEXTO_BOTON)
        texto_boton_rect = texto_boton.get_rect(center=self.boton_seleccionar.center)
        pantalla.blit(texto_boton, texto_boton_rect)

        # Resaltar si está seleccionado - Borde más grueso y naranja
        if self.carro_seleccionado == self.indice_actual:
            pygame.draw.rect(pantalla, COLOR_BORDE_SELECCIONADO, rect_actual.inflate(10, 10), 5)  # Borde más grueso


        pygame.display.flip()


# --- Funciones ---

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
                    selector.anterior_carro()
                elif selector.rect_flecha_der.collidepoint(evento.pos):
                    selector.siguiente_carro()
                elif selector.boton_seleccionar.collidepoint(evento.pos):
                    selector.seleccionar_carro()
                    return False  # Sale del selector al seleccionar
    return True

def main():
    """Función principal."""
    pygame.init()
    ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Selector de Carros")
    reloj = pygame.time.Clock()

    carros = [
        {
            'ruta': "statics/img/red bull.png",
            'nombre': "RB18 #11",
            'descripcion': "piloto: Checo Perez.",
            'atributos': {'Vel': 10, 'Ace': 8, 'Man': 8}
        },
        {
            'ruta': "statics/img/Aston_Martin.png",
            'nombre': "AMR22 #5",
            'descripcion': "piloto: Sebastian Vettel.",
            'atributos': {'Vel': 10, 'Ace': 9, 'Man': 4}
        },
        {
            'ruta': "statics/img/Ferrari.png",
            'nombre': "SF21 #16",
            'descripcion': "piloto: Charles Leclerc.",
            'atributos': {'Vel': 6, 'Ace': 8, 'Man': 7}
        },
        {
            'ruta': "statics/img/Mclaren.png",
            'nombre': "MCL36 #3",
            'descripcion': "piloto: Daniel Ricciardo.",
            'atributos': {'Vel': 6, 'Ace': 8, 'Man': 7}
        },
    ]

    selector = SelectorCarros(carros)
    juego_activo = True

    while juego_activo:
        juego_activo = manejar_eventos(selector)
        if not juego_activo: break  # Sale del bucle principal si se selecciona un carro
        selector.actualizar()
        selector.dibujar(ventana)
        reloj.tick(FPS)

    pygame.quit()
    # sys.exit() # Removido. No es necesario y puede causar problemas con la integración.


if __name__ == "__main__":
    main()