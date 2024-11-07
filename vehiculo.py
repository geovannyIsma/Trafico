import pygame

from configuracion import VELOCIDAD_BASE_VEHICULO, TAMANO_VEHICULO, ANCHO, ALTURA

class Vehiculo:
    def __init__(self, direccion, tiempo_llegada):
        self.direccion = direccion
        self.rect = self.crear_rect(direccion)
        self.en_interseccion = False
        self.velocidad = VELOCIDAD_BASE_VEHICULO
        self.tiempo_llegada = tiempo_llegada
        self.tiempo_espera = None

    def crear_rect(self, direccion):
        if direccion == "NORTE":
            return pygame.Rect(ANCHO // 2 - 30, ALTURA, *TAMANO_VEHICULO)
        elif direccion == "SUR":
            return pygame.Rect(ANCHO // 2 + 10, 0, *TAMANO_VEHICULO)
        elif direccion == "ESTE":
            return pygame.Rect(0, ALTURA // 2 - 30, *TAMANO_VEHICULO[::-1])
        elif direccion == "OESTE":
            return pygame.Rect(ANCHO, ALTURA // 2 + 10, *TAMANO_VEHICULO[::-1])

    def mover(self):
        if self.direccion == "NORTE":
            self.rect.y -= self.velocidad
        elif self.direccion == "SUR":
            self.rect.y += self.velocidad
        elif self.direccion == "ESTE":
            self.rect.x += self.velocidad
        elif self.direccion == "OESTE":
            self.rect.x -= self.velocidad

    def esta_en_interseccion(self):
        return (ANCHO // 2 - 100 < self.rect.centerx < ANCHO // 2 + 100 and
                ALTURA // 2 - 100 < self.rect.centery < ALTURA // 2 + 100)