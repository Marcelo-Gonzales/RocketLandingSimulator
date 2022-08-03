#!/usr/bin/env python

import math
import random
import pythonGraph

# CONSTANTS
WINDOW_WIDTH = 1250
WINDOW_HEIGHT = 700
TITLE = "Rocket Simulator"


class RocketLandingSimulator:
    def __init__(self):
        pythonGraph.open_window(WINDOW_WIDTH, WINDOW_HEIGHT)
        pythonGraph.set_window_title(TITLE)

    def initialize_simulation(self, generate_new_scenario):
        pass

    def erase_objects(self):
        pass

    def draw_objects(self):
        pass

    def update_objects(self):
        pass

    def get_input(self):
        pass

    def is_simulation_over(self):
        pass

    def analyze_results(self):
        pass

    def loop(self):
        while pythonGraph.window_not_closed():
            if self.is_simulation_over() == False:
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