#!/usr/bin/env python
"""
    Created By: Marcelo F. Gonzales

"""
import random 
import pythonGraph

# CONSTANTS
SCREEN_WIDTH = 1250
SCREEN_HEIGHT = 700
TEXT_SIZE = 20
TEXT_LOCATION_X = 0
TEXT_LOCATION_Y = 0
TITLE = "Rocket Simulator"


class Terrain:
    MIN_GROUND_WIDTH = 100
    MIN_GROUND_HEIGHT = 100
    MIN_WATER_HEIGHT = 50
    SCREEN_WIDTH_FACTOR = .20
    SCREEN_HEIGHT_FACTOR = .30

    def __init__(self) -> None:
        self.ground_width = self.ground_height = self.water_height = None
        self.terrain_height = []

    def initialize(self, generate_new_scenario):
        if generate_new_scenario:
            ground_width_max = round(Terrain.SCREEN_WIDTH_FACTOR * SCREEN_WIDTH)
            self.ground_width = random.randint(Terrain.MIN_GROUND_WIDTH, ground_width_max)
            self.ground_height = random.randint(Terrain.MIN_GROUND_HEIGHT, round(Terrain.SCREEN_HEIGHT_FACTOR * SCREEN_HEIGHT))
            self.water_height = random.randint(Terrain.MIN_WATER_HEIGHT, self.ground_height)
            for _ in range(self.ground_width + 1):
                self.terrain_height.append(self.ground_height)

            for _ in range(self.ground_width, SCREEN_WIDTH + 1):
                self.terrain_height.append(self.water_height)

    def draw(self):
        for i in range(self.ground_width + 1):
            for j in range(SCREEN_HEIGHT, SCREEN_HEIGHT - self.ground_height + 1, -1):
                pythonGraph.draw_pixel(i, j, pythonGraph.colors.GREEN)

        for i in range(SCREEN_WIDTH - self.ground_width + 1):
            for j in range(SCREEN_HEIGHT, SCREEN_HEIGHT - self.water_height + 1, -1):
                pythonGraph.draw_pixel(i + self.ground_width + 1, j, pythonGraph.colors.BLUE)



class Boat:
    HEIGHT = 25
    WIDTH = 80
    MINIMUM_VELOCITY = -5
    MAXIMUM_VELOCITY = 5
    def __init__(self) -> None:
        self._coordinates = (0, 0)
        self._size = (Boat.WIDTH, Boat.HEIGHT)
        self.velocity = 0
        self.terrain_location = None

    @property
    def size(self):
        return self._size

    @property
    def coordinates(self):
        return self._coordinates

    @coordinates.setter
    def coordinates(self, coordinates):
        self._coordinates = coordinates

    def initialize(self, terrain=None):
        if terrain:
            self.coordinates = (random.randint(terrain.ground_width, 
                (SCREEN_WIDTH - terrain.ground_width)), 
                SCREEN_HEIGHT - terrain.water_height - self.size[1] + 1)
            self.velocity = random.randint(Boat.MINIMUM_VELOCITY, Boat.MAXIMUM_VELOCITY)
            while self.velocity == 0:
                self.velocity = random.randint(Boat.MINIMUM_VELOCITY, Boat.MAXIMUM_VELOCITY)
            self.terrain_location = terrain.ground_width
        

    def draw(self):
        pythonGraph.draw_image("boat.png", self.coordinates[0], self.coordinates[1], self.size[0], self.size[1])

    def update(self):
        self.coordinates = (self.coordinates[0] + self.velocity, self.coordinates[1])
        if self.coordinates[0] + self.size[0] >= SCREEN_WIDTH:
            self.velocity *= -1
        if self.terrain_location:
            if self.coordinates[0] <= self.terrain_location:
                self.velocity *= -1


class Rocket:
    HEIGHT = 50
    WIDTH = 50
    THRUSTER_HEIGHT = 50
    THRUSTER_WIDTH = 50
    def __init__(self) -> None:
        self.velocity = self.coordinates = (0, 0)
        self._size = (Rocket.WIDTH, Rocket.HEIGHT)
        self.boosting = True
        self.thrust_up = self.thrust_right = self.thrust_left = 0.0
        self.acceleration = 0.15 #Acceleration due to gravity
        self.terrain_location = None
        self._fuel_consumed = 0

    @property
    def size(self):
        return self._size

    @property
    def fuel_consumed(self):
        return self._fuel_consumed

    @fuel_consumed.setter
    def fuel_consumed(self, fuel_consumed):
        self._fuel_consumed = fuel_consumed

    def initialize(self, terrain=None):
        self.boosting = True
        if terrain:
            self.coordinates = ((terrain.ground_width - self.size[0]) // 2, 
                SCREEN_HEIGHT - terrain.ground_height - self.size[1])
            self.velocity = (0, 0)
            self.terrain_location = terrain.ground_width

    def draw(self):
        pythonGraph.draw_image("rocket.png", self.coordinates[0], self.coordinates[1], self.size[0], self.size[1])
        if self.thrust_up:
            pythonGraph.draw_image("thruster.png", self.coordinates[0], self.coordinates[1] + (self.size[1] // 2 + 13)
                                    , Rocket.THRUSTER_WIDTH, Rocket.THRUSTER_HEIGHT)
        if self.thrust_left:
            pythonGraph.draw_image("thruster.png", self.coordinates[0] + (self.size[0] // 3 - 5), self.coordinates[1]
                                    + (self.size[1] // 2 + 13), Rocket.THRUSTER_WIDTH, Rocket.THRUSTER_HEIGHT)
        if self.thrust_right:
            pythonGraph.draw_image("thruster.png", self.coordinates[0] - (self.size[0] // 3 - 5), self.coordinates[1] 
                                    + (self.size[1] // 2 + 13), Rocket.THRUSTER_WIDTH, Rocket.THRUSTER_HEIGHT)

    def update(self):
        velocity_x, velocity_y = self.velocity
        coordinates_x, coordinates_y = self.coordinates
        if self.boosting:
            self.thrust_up = self.thrust_right = self.thrust_left = 0.0
            if self.coordinates[1] + self.size[1] > SCREEN_HEIGHT // 2:
                self.thrust_up = 0.35
            else:
                self.thrust_right = 0.25
            if self.terrain_location:
                if self.coordinates[0] > self.terrain_location:
                    self.boosting = False
        velocity_y = velocity_y - self.thrust_up + self.acceleration
        velocity_x += self.thrust_right
        velocity_x += self.thrust_left
        coordinates_x += velocity_x
        coordinates_y += velocity_y
        self.velocity = (velocity_x, velocity_y)
        self.coordinates = (coordinates_x, coordinates_y)


class RocketLandingSimulator:
    NUM_RUNS = 5
    def __init__(self):
        pythonGraph.open_window(SCREEN_WIDTH, SCREEN_HEIGHT)
        pythonGraph.set_window_title(TITLE)
        self.terrain = Terrain()
        self.boat = Boat()
        self.rocket = Rocket()
        self.max_score = 0
        self.time_elapsed = 0
        self.crashes = 0
        self.landings = 0
        self.current_run = 0

    def initialize_simulation(self, generate_new_scenario):
        self.time_elapsed = 0
        self.rocket.fuel_consumed = 0
        self.terrain.initialize(generate_new_scenario)
        self.boat.initialize(terrain=self.terrain)
        self.rocket.initialize(terrain=self.terrain)

    def erase_objects(self):
        pythonGraph.clear_window(pythonGraph.colors.BLACK)

    def draw_objects(self):
        self.terrain.draw()
        self.boat.draw()
        self.rocket.draw()
        self.draw_hud()
        self.time_elapsed += 1

    def draw_hud(self):
        pythonGraph.draw_text(f"Max Score: {self.max_score}", TEXT_LOCATION_X, TEXT_LOCATION_Y, pythonGraph.colors.WHITE, TEXT_SIZE)
        pythonGraph.draw_text(f"Time Elapsed: {self.time_elapsed}", TEXT_LOCATION_X, TEXT_LOCATION_Y+TEXT_SIZE, pythonGraph.colors.WHITE, TEXT_SIZE)
        pythonGraph.draw_text(f"Fuel Consumed: {self.rocket.fuel_consumed:.2f}", TEXT_LOCATION_X, TEXT_LOCATION_Y+2*TEXT_SIZE, pythonGraph.colors.WHITE, TEXT_SIZE)
        pythonGraph.draw_text(f"X Velocity: {self.rocket.velocity[0]:.2f}", TEXT_LOCATION_X, TEXT_LOCATION_Y+3*TEXT_SIZE, pythonGraph.colors.WHITE, TEXT_SIZE)
        pythonGraph.draw_text(f"Y Velocity: {self.rocket.velocity[1]:.2f}", TEXT_LOCATION_X, TEXT_LOCATION_Y+4*TEXT_SIZE, pythonGraph.colors.WHITE, TEXT_SIZE)
        pythonGraph.draw_text(f"Crashes: {self.crashes} Landings: {self.landings}", TEXT_LOCATION_X, TEXT_LOCATION_Y+5*TEXT_SIZE, pythonGraph.colors.WHITE, TEXT_SIZE)

    def update_objects(self):
        self.boat.update()
        self.rocket.update()

    def get_input(self):
        self.rocket.thrust_up = self.rocket.thrust_left = self.rocket.thrust_right = 0
        if not self.rocket.boosting:
            if pythonGraph.key_down("up"):
                self.rocket.thrust_up = 0.35
                self.rocket.fuel_consumed += 0.35
            if pythonGraph.key_down("right"):
                self.rocket.thrust_right = 0.5
                self.rocket.fuel_consumed += 0.5
            if pythonGraph.key_down("left"):
                self.rocket.thrust_left = -0.5
                self.rocket.fuel_consumed += 0.5

    def is_simulation_over(self):
        if not self.rocket.boosting:
            left_side_of_rocket = self.rocket.coordinates[0] 
            right_side_of_rocket = self.rocket.coordinates[0] + self.rocket.size[0]
            if left_side_of_rocket < 0:
                return True
            if right_side_of_rocket > SCREEN_WIDTH:
                return True
            for i in range(round(left_side_of_rocket), round(right_side_of_rocket) + 1):
                height = self.terrain.terrain_height[i]
                if SCREEN_HEIGHT - height < self.rocket.coordinates[1] + self.rocket.size[1] - 10:
                    return True
        return False

    def analyze_results(self):
        boat_left_side = self.boat.coordinates[0]
        boat_right_side = self.boat.coordinates[0] + self.boat.size[0]
        rocket_left_side = self.rocket.coordinates[0]
        rocket_right_side = self.rocket.coordinates[0] + self.rocket.size[0]
        if boat_left_side <= rocket_left_side and boat_right_side >= rocket_right_side:
            self.max_score += 100
            self.landings += 1
        else:
            self.max_score -= 100
            self.crashes += 1

    def loop(self):
        self.initialize_simulation(True)
        while pythonGraph.window_not_closed():
            if not self.is_simulation_over():
                self.erase_objects()
                self.draw_objects()
                self.get_input()
                self.update_objects()
            else:
                self.analyze_results()
                self.current_run += 1
                if self.current_run == RocketLandingSimulator.NUM_RUNS:
                    self.initialize_simulation(True)
                    self.current_run = 0
                else:
                    self.initialize_simulation(False)
            pythonGraph.update_window()


def main():
    try:
        rocket_simulator = RocketLandingSimulator()
        rocket_simulator.loop()
    except KeyboardInterrupt:
        print("CTRL-C: Exit Program")


if __name__ == "__main__":
    main()