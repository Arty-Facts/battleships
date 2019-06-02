from agents.agent import Agent
import numpy as np
import matplotlib.pyplot as plt
from random import randint, shuffle
from config import *
from lib.simulation_board import SimulationBoard
# Inspired by DataSnaek from https://github.com/DataSnaek/battleships_ai

class MonteCarlo(Agent):

    def __init__(self, state, print_out=False):
        self.state = state
        self.move_sim = MONTE_CARLO_SAMPLES  # The number of moves to simulate
        self.print_out = print_out
        self.priority = MONTE_CARLO_PRIORITY  # The priority to give simulations that intersect hits



    def monte_carlo(self, out_path=""):
        simulations = []
        if self.state.tiles_left == 1:
            self.priority *= 2

        sim_state = SimulationBoard(self.state)
        for i in range(self.move_sim):
            sim_state.update(self.state)
            brd, intersect = sim_state.simulate_ship()

            # If we intersect a hit, take into account priority and overlap
            if intersect:
                for i in range(self.priority):
                    for i in range(intersect):
                        simulations.append(brd)
            simulations.append(brd)

        # Mean the ship simulations down the stacked axis to calculate percentages
        simulations = np.array(simulations)
        percentages = np.mean(simulations, axis=0)

        # Output a heatmap if specified
        if HEAT_MAP:
            fig = plt.figure(figsize=(8, 8))
            fig.add_subplot(1, 2, 1)
            plt.imshow(percentages, cmap='hot', interpolation='nearest')
            fig.add_subplot(1, 2, 2)
            plt.imshow(sim_state.get_board() * 10, cmap='bwr', interpolation=None)
            plt.savefig("heatmap/out")
            plt.close(fig)

        return percentages

    def next_tile(self):
        probs = self.monte_carlo()

        x, y = np.unravel_index(probs.argmax(), probs.shape)
        while not self.state.free(x, y):
            probs[x, y] = 0
            x, y = np.unravel_index(probs.argmax(), probs.shape)
        return x, y


    def result(self, x, y, hit, sinc):
        if hit:
            self.state.hit(x, y)
            self.state.tiles_left -= 1
            if self.print_out:
                print(self.state)
        else:
            self.state.miss(x, y)

