from agents.agent import Agent
import numpy as np
import matplotlib.pyplot as plt
from random import randint, shuffle
from config import *
from lib.simulation_board import SimulationBoard
from agents.monte_carlo_agent import MonteCarlo


class MonteCarloSinc(MonteCarlo):

    def __init__(self, state, print_out=False):
        super().__init__(state, print_out)


    def result(self, x, y, hit, sinc):
        if hit:
            if sinc:
                self.state.sinc(x, y)
                self.state.ships_left -= 1
            else:
                self.state.hit(x, y)
                self.state.tiles_left -= 1
            if self.print_out:
                print(self.state)
        else:
            self.state.miss(x, y)

