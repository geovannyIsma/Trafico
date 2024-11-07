from configuracion import VERDE, ROJO, FACTOR_VELOCIDAD


class Semaforo:
    def __init__(self, duracion_luz_verde, duracion_luz_roja):
        self.temporizador = 0
        self.duracion_luz_verde = duracion_luz_verde
        self.duracion_luz_roja = duracion_luz_roja
        self.direccion_actual = "NORTE"
        self.luces = {"NORTE": VERDE, "SUR": ROJO, "ESTE": ROJO, "OESTE": ROJO}
        self.direcciones = ["NORTE", "SUR", "ESTE", "OESTE"]

    def actualizar(self):
        self.temporizador += 1 * FACTOR_VELOCIDAD
        if self.temporizador > self.duracion_luz_verde:
            # Cambiar al siguiente semáforo en verde y el resto en rojo
            self.temporizador = 0
            indice_actual = self.direcciones.index(self.direccion_actual)
            indice_siguiente = (indice_actual + 1) % len(self.direcciones)
            self.direccion_actual = self.direcciones[indice_siguiente]

            # Asignar luces
            for direccion in self.direcciones:
                self.luces[direccion] = VERDE if direccion == self.direccion_actual else ROJO