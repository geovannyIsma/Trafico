from Trafico_simulacion import SimulacionTrafico
from configuracion import *

# Función para mostrar el menú de selección de caso de prueba
def mostrar_menu():
    menu_activo = True
    opcion_seleccionada = None

    # Opciones de menú con diferentes configuraciones de prueba
    casos_prueba = {
        "Caso 1: Hora pico": (TASA_APARICION_PICO, TIEMPO_LUZ_VERDE_PICO, TIEMPO_LUZ_ROJA_FUERA_PICO),
        "Caso 2: Hora no pico": (TASA_APARICION_FUERA_PICO, TIEMPO_LUZ_VERDE_FUERA_PICO, TIEMPO_LUZ_ROJA_FUERA_PICO),
        "Caso 3: Ajuste de semáforo según tráfico": (None, None, None)
    }

    # Definir el tamaño de la ventana del menú
    ventana.fill(BLANCO)

    while menu_activo:
        ventana.fill(BLANCO)

        # Título del menú
        titulo = fuente.render("Selecciona un caso de prueba", True, NEGRO)
        ventana.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, ALTURA // 4))

        # Dibujar opciones de menú
        for i, (texto, _) in enumerate(casos_prueba.items()):
            opcion = fuente.render(texto, True, NEGRO)
            ventana.blit(opcion, (ANCHO // 2 - opcion.get_width() // 2, ALTURA // 2 + i * 50))

        pygame.display.flip()

        # Manejar eventos del menú
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    opcion_seleccionada = "Caso 1: Hora pico"
                    menu_activo = False
                elif evento.key == pygame.K_2:
                    opcion_seleccionada = "Caso 2: Hora no pico"
                    menu_activo = False
                elif evento.key == pygame.K_3:
                    opcion_seleccionada = "Caso 3: Ajuste de semáforo según tráfico"
                    menu_activo = False

    # Retornar la configuración del caso de prueba seleccionado
    return casos_prueba[opcion_seleccionada]

def principal():
    reloj = pygame.time.Clock()

    # Mostrar menú y obtener configuración
    tasa_aparicion, duracion_luz_verde, duracion_luz_roja = mostrar_menu()

    # Si es "Caso 3: Ajuste de semáforo según tráfico", se manejará por separado en la simulación
    if tasa_aparicion is None:  # Significa que es el caso de ajuste dinámico
        tasa_aparicion = (10, 25)  # Tasa de aparición por defecto
        duracion_luz_verde = TIEMPO_LUZ_VERDE_FUERA_PICO
        duracion_luz_roja = TIEMPO_LUZ_ROJA_FUERA_PICO

    # Crear simulación con los parámetros seleccionados
    simulacion = SimulacionTrafico(tasa_aparicion, duracion_luz_verde, duracion_luz_roja)
    ejecutando = True

    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

        simulacion.actualizar()
        simulacion.dibujar()
        reloj.tick(60 * FACTOR_VELOCIDAD)

    pygame.quit()

# Ejecutar simulación
if __name__ == "__main__":
    principal()