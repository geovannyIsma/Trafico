import random
from Semaforo import Semaforo
from configuracion import *
from vehiculo import Vehiculo

class SimulacionTrafico:
    def __init__(self, tasa_aparicion, duracion_luz_verde, duracion_luz_roja):
        self.carriles = {direccion: [] for direccion in ["NORTE", "SUR", "ESTE", "OESTE"]}
        self.semaforo = Semaforo(duracion_luz_verde, duracion_luz_roja)
        self.tasa_aparicion = tasa_aparicion
        self.tiempos_espera = {direccion: [] for direccion in ["NORTE", "SUR", "ESTE", "OESTE"]}
        self.tiempo_actual = 0
        self.contador_vehiculos = {direccion: 0 for direccion in ["NORTE", "SUR", "ESTE", "OESTE"]}  # Contador de vehículos

    def generar_vehiculo(self):
        if random.randint(0, 1800 // random.randint(*self.tasa_aparicion) // FACTOR_VELOCIDAD) == 0:
            direccion = random.choice(["NORTE", "SUR", "ESTE", "OESTE"])
            if not self.carriles[direccion] or self.distancia_al_ultimo_vehiculo(direccion) > 50:
                self.carriles[direccion].append(Vehiculo(direccion, self.tiempo_actual))
                self.contador_vehiculos[direccion] += 1  # Aumentar el contador al generar un vehículo

    def distancia_al_ultimo_vehiculo(self, direccion):
        if not self.carriles[direccion]:
            return float('inf')
        ultimo_vehiculo = self.carriles[direccion][-1]
        if direccion == "NORTE":
            return ALTURA - ultimo_vehiculo.rect.y
        elif direccion == "SUR":
            return ultimo_vehiculo.rect.y
        elif direccion == "ESTE":
            return ultimo_vehiculo.rect.x
        elif direccion == "OESTE":
            return ANCHO - ultimo_vehiculo.rect.x

    def mover_vehiculos(self):
        for direccion, vehiculos in self.carriles.items():
            for i, vehiculo in enumerate(vehiculos):
                if self.debe_detenerse(vehiculo, i, vehiculos):
                    continue
                self.ajustar_velocidad(vehiculo, vehiculos, i)
                vehiculo.mover()
                if vehiculo.esta_en_interseccion():
                    vehiculo.en_interseccion = True
                if self.esta_fuera_de_limites(vehiculo):
                    if vehiculo.tiempo_espera is None:
                        vehiculo.tiempo_espera = self.tiempo_actual - vehiculo.tiempo_llegada
                        self.tiempos_espera[vehiculo.direccion].append(vehiculo.tiempo_espera)
                    vehiculos.remove(vehiculo)

    def ajustar_velocidad(self, vehiculo, vehiculos, indice):
        if indice > 0:
            vehiculo_previo = vehiculos[indice - 1]
            distancia = self.calcular_distancia(vehiculo, vehiculo_previo)
            if distancia < 60:
                vehiculo.velocidad = max(0, min(VELOCIDAD_BASE_VEHICULO * (1 + (50 - distancia) / 50), VELOCIDAD_BASE_VEHICULO * 2))
            else:
                vehiculo.velocidad = VELOCIDAD_BASE_VEHICULO

    def debe_detenerse(self, vehiculo, indice, vehiculos):
        luz = self.semaforo.luces[vehiculo.direccion]
        if vehiculo.en_interseccion:
            return False

        if indice > 0:
            vehiculo_previo = vehiculos[indice - 1]
            distancia = self.calcular_distancia(vehiculo, vehiculo_previo)
            if distancia < 60:
                return True

        if luz == ROJO:
            return self.verificar_linea_de_parada(vehiculo)

        return False

    def verificar_linea_de_parada(self, vehiculo):
        lineas_parada = {"NORTE": ALTURA // 2 + 100, "SUR": ALTURA // 2 - 100,
                         "ESTE": ANCHO // 2 - 100, "OESTE": ANCHO // 2 + 100}
        if vehiculo.direccion == "NORTE" and vehiculo.rect.y <= lineas_parada["NORTE"]:
            return True
        elif vehiculo.direccion == "SUR" and vehiculo.rect.bottom >= lineas_parada["SUR"]:
            return True
        elif vehiculo.direccion == "ESTE" and vehiculo.rect.right >= lineas_parada["ESTE"]:
            return True
        elif vehiculo.direccion == "OESTE" and vehiculo.rect.x <= lineas_parada["OESTE"]:
            return True
        return False

    def calcular_distancia(self, vehiculo, vehiculo_previo):
        if vehiculo.direccion in ["NORTE", "SUR"]:
            return abs(vehiculo.rect.y - vehiculo_previo.rect.y)
        elif vehiculo.direccion in ["ESTE", "OESTE"]:
            return abs(vehiculo.rect.x - vehiculo_previo.rect.x)

    def esta_fuera_de_limites(self, vehiculo):
        return (vehiculo.rect.y < -TAMANO_VEHICULO[1] or vehiculo.rect.y > ALTURA or
                vehiculo.rect.x < -TAMANO_VEHICULO[0] or vehiculo.rect.x > ANCHO)

    def actualizar(self):
        self.tiempo_actual += 1 * FACTOR_VELOCIDAD
        self.semaforo.actualizar()
        self.generar_vehiculo()
        self.mover_vehiculos()

        if self.tiempo_actual >= DURACION_SIMULACION:
            self.mostrar_resultados()
            pygame.quit()
            exit()

    def mostrar_resultados(self):
        tiempos_promedio_espera = self.calcular_tiempos_promedio_espera()
        for direccion, tiempo_promedio in tiempos_promedio_espera.items():
            contador_vehiculos = self.contador_vehiculos[direccion]
            print(f"{direccion}: Tiempo promedio de espera: {tiempo_promedio:.2f}s, Vehículos: {contador_vehiculos}")

    def calcular_tiempos_promedio_espera(self):
        tiempos_promedio = {}
        for direccion, tiempos in self.tiempos_espera.items():
            if tiempos:
                tiempos_promedio[direccion] = sum(tiempos) / len(tiempos)
            else:
                tiempos_promedio[direccion] = 0
        return tiempos_promedio

    def dibujar(self):
        ventana.fill(BLANCO)
        pygame.draw.rect(ventana, GRIS, (ANCHO // 2 - 100, 0, 200, ALTURA))  # Carril vertical
        pygame.draw.rect(ventana, GRIS, (0, ALTURA // 2 - 100, ANCHO, 200))  # Carril horizontal

        # Dibujar vehículos
        for direccion, vehiculos in self.carriles.items():
            for vehiculo in vehiculos:
                pygame.draw.rect(ventana, AZUL, vehiculo.rect)

        # Dibujar semáforos
        for direccion, color in self.semaforo.luces.items():
            x, y = (ANCHO // 2 - 150, ALTURA // 2 + 120) if direccion == "NORTE" else \
                (ANCHO // 2 + 120, ALTURA // 2 - 150) if direccion == "SUR" else \
                    (ANCHO // 2 - 150, ALTURA // 2 - 150) if direccion == "ESTE" else \
                        (ANCHO // 2 + 120, ALTURA // 2 + 120)
            pygame.draw.rect(ventana, color, (x, y, 30, 30))

        # Indicadores de tiempo promedio de espera
        tiempos_promedio_espera = self.calcular_tiempos_promedio_espera()
        posiciones_direcciones = {
            "NORTE": (ANCHO // 2 - 60, ALTURA // 2 + 150),
            "SUR": (ANCHO // 2 - 60, ALTURA // 2 - 200),
            "ESTE": (ANCHO // 2 + 150, ALTURA // 2 - 30),
            "OESTE": (ANCHO // 2 - 200, ALTURA // 2 - 30)
        }
        for direccion, pos in posiciones_direcciones.items():
            tiempo_promedio = tiempos_promedio_espera[direccion]
            contador_vehiculos = self.contador_vehiculos[direccion]  # Obtener el contador de vehículos
            superficie_texto = fuente.render(f"{direccion}: {tiempo_promedio:.2f}s, Vehículos: {contador_vehiculos}", True, NEGRO)
            ventana.blit(superficie_texto, pos)

        pygame.display.flip()
