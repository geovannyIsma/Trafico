from Trafico_simulacion import TrafficSimulation
from configuracion import *

# Función para mostrar el menú de selección de caso de prueba
def show_menu():
    menu_running = True
    selected_option = None

    # Opciones de menú con diferentes configuraciones de prueba
    test_cases = {
        "Caso 1: Hora pico": (SPAWN_RATE_PEAK, GREEN_LIGHT_TIME_PEAK, RED_LIGHT_TIME_PEAK),
        "Caso 2: Hora no pico": (SPAWN_RATE_OFF_PEAK, GREEN_LIGHT_TIME_OFF_PEAK, RED_LIGHT_TIME_OFF_PEAK),
        "Caso 3: Ajuste de semáforo según tráfico": (None, None, None)
    }

    # Definir el tamaño de la ventana del menú
    window.fill(WHITE)

    while menu_running:
        window.fill(WHITE)

        # Título del menú
        title_surface = font.render("Selecciona un caso de prueba", True, BLACK)
        window.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, HEIGHT // 4))

        # Dibujar opciones de menú
        for i, (text, _) in enumerate(test_cases.items()):
            option_surface = font.render(text, True, BLACK)
            window.blit(option_surface, (WIDTH // 2 - option_surface.get_width() // 2, HEIGHT // 2 + i * 50))

        pygame.display.flip()

        # Manejar eventos del menú
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_option = "Caso 1: Hora pico"
                    menu_running = False
                elif event.key == pygame.K_2:
                    selected_option = "Caso 2: Hora no pico"
                    menu_running = False
                elif event.key == pygame.K_3:
                    selected_option = "Caso 3: Ajuste de semáforo según tráfico"
                    menu_running = False

    # Retornar la configuración del caso de prueba seleccionado
    return test_cases[selected_option]

def main():
    clock = pygame.time.Clock()

    # Mostrar menú y obtener configuración
    spawn_rate, green_light_duration, red_light_duration = show_menu()

    # Si es "Caso 3: Ajuste de semáforo según tráfico", se manejará por separado en la simulación
    if spawn_rate is None:  # Significa que es el caso de ajuste dinámico
        spawn_rate = (10, 25)  # Tasa de aparición por defecto
        green_light_duration = GREEN_LIGHT_TIME_OFF_PEAK
        red_light_duration = RED_LIGHT_TIME_OFF_PEAK

    # Crear simulación con los parámetros seleccionados
    simulation = TrafficSimulation(spawn_rate, green_light_duration, red_light_duration)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        simulation.update()
        simulation.draw()
        clock.tick(60 * SPEED_MULTIPLIER)

    pygame.quit()

# Ejecutar simulación
if __name__ == "__main__":
    main()