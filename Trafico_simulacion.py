import random
from Semaforo import TrafficLight
from configuracion import *
from vehiculo import Vehicle

class TrafficSimulation:
    def __init__(self, spawn_rate, green_light_duration, red_light_duration):
        self.lanes = {direction: [] for direction in ["NORTH", "SOUTH", "EAST", "WEST"]}
        self.traffic_light = TrafficLight(green_light_duration, red_light_duration)
        self.spawn_rate = spawn_rate
        self.wait_times = {direction: [] for direction in ["NORTH", "SOUTH", "EAST", "WEST"]}
        self.current_time = 0
        self.vehicle_count = {direction: 0 for direction in ["NORTH", "SOUTH", "EAST", "WEST"]}  # Contador de vehículos

    def spawn_vehicle(self):
        if random.randint(0, 1800 // random.randint(*self.spawn_rate) // SPEED_MULTIPLIER) == 0:
            direction = random.choice(["NORTH", "SOUTH", "EAST", "WEST"])
            if not self.lanes[direction] or self.distance_to_last_vehicle(direction) > 50:
                self.lanes[direction].append(Vehicle(direction, self.current_time))
                self.vehicle_count[direction] += 1  # Aumentar el contador al generar un vehículo

    def distance_to_last_vehicle(self, direction):
        if not self.lanes[direction]:
            return float('inf')
        last_vehicle = self.lanes[direction][-1]
        if direction == "NORTH":
            return HEIGHT - last_vehicle.rect.y
        elif direction == "SOUTH":
            return last_vehicle.rect.y
        elif direction == "EAST":
            return last_vehicle.rect.x
        elif direction == "WEST":
            return WIDTH - last_vehicle.rect.x

    def move_vehicles(self):
        for direction, vehicles in self.lanes.items():
            for i, vehicle in enumerate(vehicles):
                if self.should_stop(vehicle, i, vehicles):
                    continue
                self.adjust_speed(vehicle, vehicles, i)
                vehicle.move()
                if vehicle.is_in_intersection():
                    vehicle.in_intersection = True
                if self.is_out_of_bounds(vehicle):
                    if vehicle.wait_time is None:
                        vehicle.wait_time = self.current_time - vehicle.arrival_time
                        self.wait_times[vehicle.direction].append(vehicle.wait_time)
                    vehicles.remove(vehicle)

    def adjust_speed(self, vehicle, vehicles, index):
        if index > 0:
            prev_vehicle = vehicles[index - 1]
            distance = self.calculate_distance(vehicle, prev_vehicle)
            if distance < 60:
                vehicle.speed = max(0, min(BASE_VEHICLE_SPEED * (1 + (50 - distance) / 50), BASE_VEHICLE_SPEED * 2))
            else:
                vehicle.speed = BASE_VEHICLE_SPEED

    def should_stop(self, vehicle, index, vehicles):
        light = self.traffic_light.lights[vehicle.direction]
        if vehicle.in_intersection:
            return False

        if index > 0:
            prev_vehicle = vehicles[index - 1]
            distance = self.calculate_distance(vehicle, prev_vehicle)
            if distance < 60:
                return True

        if light == RED:
            return self.check_stop_line(vehicle)

        return False

    def check_stop_line(self, vehicle):
        stop_lines = {"NORTH": HEIGHT // 2 + 100, "SOUTH": HEIGHT // 2 - 100,
                      "EAST": WIDTH // 2 - 100, "WEST": WIDTH // 2 + 100}
        if vehicle.direction == "NORTH" and vehicle.rect.y <= stop_lines["NORTH"]:
            return True
        elif vehicle.direction == "SOUTH" and vehicle.rect.bottom >= stop_lines["SOUTH"]:
            return True
        elif vehicle.direction == "EAST" and vehicle.rect.right >= stop_lines["EAST"]:
            return True
        elif vehicle.direction == "WEST" and vehicle.rect.x <= stop_lines["WEST"]:
            return True
        return False

    def calculate_distance(self, vehicle, prev_vehicle):
        if vehicle.direction in ["NORTH", "SOUTH"]:
            return abs(vehicle.rect.y - prev_vehicle.rect.y)
        elif vehicle.direction in ["EAST", "WEST"]:
            return abs(vehicle.rect.x - prev_vehicle.rect.x)

    def is_out_of_bounds(self, vehicle):
        return (vehicle.rect.y < -VEHICLE_SIZE[1] or vehicle.rect.y > HEIGHT or
                vehicle.rect.x < -VEHICLE_SIZE[0] or vehicle.rect.x > WIDTH)

    def update(self):
        self.current_time += 1 * SPEED_MULTIPLIER
        self.traffic_light.update()
        self.spawn_vehicle()
        self.move_vehicles()

        if self.current_time >= SIMULATION_DURATION:
            self.display_results()
            pygame.quit()
            exit()

    def display_results(self):
        avg_wait_times = self.calculate_average_wait_times()
        for direction, avg_time in avg_wait_times.items():
            vehicle_count = self.vehicle_count[direction]
            print(f"{direction}: Tiempo promedio de espera: {avg_time:.2f}s, Vehículos: {vehicle_count}")

    def calculate_average_wait_times(self):
        average_wait_times = {}
        for direction, times in self.wait_times.items():
            if times:
                average_wait_times[direction] = sum(times) / len(times)
            else:
                average_wait_times[direction] = 0
        return average_wait_times

    def draw(self):
        window.fill(WHITE)
        pygame.draw.rect(window, GRAY, (WIDTH // 2 - 100, 0, 200, HEIGHT))  # Carril vertical
        pygame.draw.rect(window, GRAY, (0, HEIGHT // 2 - 100, WIDTH, 200))  # Carril horizontal

        # Dibujar vehículos
        for direction, vehicles in self.lanes.items():
            for vehicle in vehicles:
                pygame.draw.rect(window, BLUE, vehicle.rect)

        # Dibujar semáforos
        for direction, color in self.traffic_light.lights.items():
            x, y = (WIDTH // 2 - 150, HEIGHT // 2 + 120) if direction == "NORTH" else \
                (WIDTH // 2 + 120, HEIGHT // 2 - 150) if direction == "SOUTH" else \
                    (WIDTH // 2 - 150, HEIGHT // 2 - 150) if direction == "EAST" else \
                        (WIDTH // 2 + 120, HEIGHT // 2 + 120)
            pygame.draw.rect(window, color, (x, y, 30, 30))

        # Indicadores de tiempo promedio de espera
        avg_wait_times = self.calculate_average_wait_times()
        directions_positions = {
            "NORTH": (WIDTH // 2 - 60, HEIGHT // 2 + 150),
            "SOUTH": (WIDTH // 2 - 60, HEIGHT // 2 - 200),
            "EAST": (WIDTH // 2 + 150, HEIGHT // 2 - 30),
            "WEST": (WIDTH // 2 - 200, HEIGHT // 2 - 30)
        }
        for direction, pos in directions_positions.items():
            avg_time = avg_wait_times[direction]
            vehicle_count = self.vehicle_count[direction]  # Obtener el contador de vehículos
            text_surface = font.render(f"{direction}: {avg_time:.2f}s, Vehículos: {vehicle_count}", True, BLACK)
            window.blit(text_surface, pos)

        pygame.display.flip()
