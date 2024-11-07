import pygame

from configuracion import BASE_VEHICLE_SPEED, VEHICLE_SIZE, WIDTH, HEIGHT

class Vehicle:
    def __init__(self, direction, arrival_time):
        self.direction = direction
        self.rect = self.create_rect(direction)
        self.in_intersection = False
        self.speed = BASE_VEHICLE_SPEED
        self.arrival_time = arrival_time
        self.wait_time = None

    def create_rect(self, direction):
        if direction == "NORTH":
            return pygame.Rect(WIDTH // 2 - 30, HEIGHT, *VEHICLE_SIZE)
        elif direction == "SOUTH":
            return pygame.Rect(WIDTH // 2 + 10, 0, *VEHICLE_SIZE)
        elif direction == "EAST":
            return pygame.Rect(0, HEIGHT // 2 - 30, *VEHICLE_SIZE[::-1])
        elif direction == "WEST":
            return pygame.Rect(WIDTH, HEIGHT // 2 + 10, *VEHICLE_SIZE[::-1])

    def move(self):
        if self.direction == "NORTH":
            self.rect.y -= self.speed
        elif self.direction == "SOUTH":
            self.rect.y += self.speed
        elif self.direction == "EAST":
            self.rect.x += self.speed
        elif self.direction == "WEST":
            self.rect.x -= self.speed

    def is_in_intersection(self):
        return (WIDTH // 2 - 100 < self.rect.centerx < WIDTH // 2 + 100 and
                HEIGHT // 2 - 100 < self.rect.centery < HEIGHT // 2 + 100)
