import pygame

pygame.init()

SPEED_MULTIPLIER = 20

# Constantes de configuración
WIDTH, HEIGHT = 1080, 720
VEHICLE_SIZE = (20, 40)
BASE_VEHICLE_SPEED = 8 * SPEED_MULTIPLIER # Velocidad base del vehículo
SPAWN_RATE_PEAK = (20, 40)  # Vehículos por minuto en horas pico
SPAWN_RATE_OFF_PEAK = (10, 25)  # Vehículos por minuto en horas no pico
VEHICLE_PASS_TIME = 2  # Tiempo que tarda cada vehículo en cruzar la intersección

# Tiempos de los semáforos en segundos teniendo en cuenta el speed multiplier
GREEN_LIGHT_TIME_PEAK = 20 * 30
RED_LIGHT_TIME_PEAK = 40 * 30
GREEN_LIGHT_TIME_OFF_PEAK = 30 * 30
RED_LIGHT_TIME_OFF_PEAK = 30 * 30

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (50, 50, 50)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Tiempo total de simulación (en segundos)
SIMULATION_DURATION = 60 * 3600  # 60 minutos

# Inicializar ventana
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulación de Tráfico en Intersección")
font = pygame.font.Font(None, 24)