#!/usr/bin/env python
"""
    Created By: Marcelo F. Gonzales
    
"""
import math 
import random 
import pythonGraph

from abc import (
    ABC as _ABC,
    abstractclassmethod as _abstractclassmethod)

# CONSTANTS
SCREEN_WIDTH = 1250
SCREEN_HEIGHT = 700
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

    @property
    def size(self):
        return self._size

    @property
    def coordinates(self):
        return self._coordinates

    @coordinates.setter
    def coordinates(self, coordinates):
        self._coordinates = coordinates

    def initialize(self, generate_new_scenario, terrain=None):
        if generate_new_scenario:
            if terrain:
                self.coordinates = (random.randint(terrain.ground_width, 
                    terrain.ground_width + (SCREEN_WIDTH - terrain.ground_width + 1)), 
                    SCREEN_HEIGHT - terrain.water_height - self.size[1] + 1)
                self.velocity = random.randint(Boat.MINIMUM_VELOCITY, Boat.MAXIMUM_VELOCITY)
        

    def draw(self):
        pythonGraph.draw_image("boat.png", self.coordinates[0], self.coordinates[1], self.size[0], self.size[1])


class Rocket:
    HEIGHT = 50
    WIDTH = 50
    def __init__(self) -> None:
        self.velocity = self.coordinates = (0, 0)
        self._size = (Rocket.WIDTH, Rocket.HEIGHT)

    @property
    def size(self):
        return self._size

    def initialize(self, generate_new_scenario, terrain=None):
        if generate_new_scenario:
            if terrain:
                self.coordinates = ((terrain.ground_width - self.size[0])// 2, 
                    SCREEN_HEIGHT - terrain.ground_height - self.size[1])
                self.velocity = (0, 0)

    def draw(self):
        pythonGraph.draw_image("rocket.png", self.coordinates[0], self.coordinates[1], self.size[0], self.size[1])


class RocketLandingSimulator:
    def __init__(self):
        pythonGraph.open_window(SCREEN_WIDTH, SCREEN_HEIGHT)
        pythonGraph.set_window_title(TITLE)
        self.terrain = Terrain()
        self.boat = Boat()
        self.rocket = Rocket()

    def initialize_simulation(self, generate_new_scenario):
        self.terrain.initialize(generate_new_scenario)
        self.boat.initialize(generate_new_scenario, terrain=self.terrain)
        self.rocket.initialize(generate_new_scenario, terrain=self.terrain)

    def erase_objects(self):
        pythonGraph.clear_window(pythonGraph.colors.BLACK)

    def draw_objects(self):
        self.terrain.draw()
        self.boat.draw()
        self.rocket.draw()

    def update_objects(self):
        pass

    def get_input(self):
        pass

    def is_simulation_over(self):
        return False

    def analyze_results(self):
        pass

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
                self.initialize_simulation(False)

            pythonGraph.update_window()


def main():
    rocket_simulator = RocketLandingSimulator()
    rocket_simulator.loop()


if __name__ == "__main__":
    main()