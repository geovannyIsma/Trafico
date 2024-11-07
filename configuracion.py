import pygame

pygame.init()

FACTOR_VELOCIDAD = 1

# Constantes de configuración
ANCHO, ALTURA = 1080, 720
TAMANO_VEHICULO = (20, 40)
VELOCIDAD_BASE_VEHICULO = 8 * FACTOR_VELOCIDAD # Velocidad base del vehículo
TASA_APARICION_PICO = (20, 40)  # Vehículos por minuto en horas pico
TASA_APARICION_FUERA_PICO = (10, 25)  # Vehículos por minuto en horas no pico
TIEMPO_PASO_VEHICULO = 2  # Tiempo que tarda cada vehículo en cruzar la intersección

# Tiempos de los semáforos en segundos
TIEMPO_LUZ_VERDE_PICO = 20 * 30
TIEMPO_LUZ_ROJA_PICO = 40 * 30
TIEMPO_LUZ_VERDE_FUERA_PICO = 30 * 30
TIEMPO_LUZ_ROJA_FUERA_PICO = 30 * 30

# Colores
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
GRIS = (50, 50, 50)
AZUL = (0, 0, 255)
NEGRO = (0, 0, 0)

# Tiempo total de simulación (en segundos)
DURACION_SIMULACION = 60 * 3600  # 60 minutos

# Inicializar ventana
ventana = pygame.display.set_mode((ANCHO, ALTURA))
pygame.display.set_caption("Simulación de Tráfico en Intersección")
fuente = pygame.font.Font(None, 24)