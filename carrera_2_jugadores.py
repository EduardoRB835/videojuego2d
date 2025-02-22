import pygame
import sys

# --- Constantes ---
ANCHO_VENTANA = 800
ALTO_VENTANA = 600
COLOR_FONDO = (20, 25, 35)

# --- Inicialización de Pygame ---
pygame.init()
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Carrera 2 Jugadores")
reloj = pygame.time.Clock()


def main():
    """Función principal del juego de 2 jugadores."""
    juego_terminado = False

    while not juego_terminado:
        # --- Manejo de Eventos ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                juego_terminado = True
            if evento.type == pygame.KEYDOWN: # Agrego el manejo del ESC
                if evento.key == pygame.K_ESCAPE:
                    juego_terminado = True


        # --- Dibujado (solo fondo) ---
        ventana.fill(COLOR_FONDO)
        pygame.display.flip()

        # --- Control de FPS ---
        reloj.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()