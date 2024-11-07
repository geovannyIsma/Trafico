from configuracion import GREEN, RED, SPEED_MULTIPLIER


class TrafficLight:
    def __init__(self, green_light_duration, red_light_duration):
        self.timer = 0
        self.green_light_duration = green_light_duration
        self.red_light_duration = red_light_duration
        self.current_direction = "NORTH"
        self.lights = {"NORTH": GREEN, "SOUTH": RED, "EAST": RED, "WEST": RED}
        self.directions = ["NORTH", "SOUTH", "EAST", "WEST"]

    def update(self):
        self.timer += 1 * SPEED_MULTIPLIER
        if self.timer > self.green_light_duration:
            # Cambiar al siguiente semáforo en verde y el resto en rojo
            self.timer = 0
            current_index = self.directions.index(self.current_direction)
            next_index = (current_index + 1) % len(self.directions)
            self.current_direction = self.directions[next_index]

            # Asignar luces
            for direction in self.directions:
                self.lights[direction] = GREEN if direction == self.current_direction else RED