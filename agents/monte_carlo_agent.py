from agents.agent import Agent
import numpy as np
import matplotlib.pyplot as plt
from random import randint, shuffle
from config import *



class MonteCarlo(Agent):

    def __init__(self, state, print_out=False):
        self.state = state
        self.move_sim = MONTE_CARLO_SAMPLES  # The number of moves to simulate
        self.print_out = print_out
        self.priority = 5  # The priority to give simulations that intersect hits


    def monte_carlo(self, out_path=""):
        simulations = []

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
            plt.imshow(sim_state.get_board() * 5, cmap='bwr', interpolation=None)
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
            if self.print_out:
                print(self.state)
        else:
            self.state.miss(x, y)



class SimulationBoard():
    def __init__(self, state):
        self.size = state.width
        self.width = state.width
        self.higth = state.higth
        self.board = np.zeros((state.width, state.higth), dtype=np.int8)

        self.square_states = {0: '.',
                              1: '~',
                              2: 'X'}
        self.inv_square_states = {v: k for k, v in self.square_states.items()}
        self.state = state

    def get_board(self, copy=False):
        if copy:
            return self.board.copy()
        else:
            return self.board

    def simulate_ship(self):

        # Select a random ship length we haven't destroyed yet and place it onto the board in a valid locatipn
        # self.ships.sort(key=lambda s:s.hp, reverse=False)
        # #shuffle(self.ships)
        # for s in self.ships:
        #     if not s.sunk():
        #         length = s.size
        shuffle(SHIPS)
        length = SHIPS[0]

        #length = self.attack_board.defense_board.available_ships[index]
        ship_cord = self.state.add(length)
        if ship_cord == None:
            sim_board = self.get_board(copy=True)
            sim_board[sim_board != self.inv_square_states['X']] = 0
            return sim_board, 0

        # Check if the ship intersects an existing hit. If it does, we want to emphasise it to the algorithm
        sim_board = self.get_board(copy=True)
        intersect = 0
        for x,y in ship_cord:
            sim_board[x][y] = 2
            if self.state.overlap(x,y):
                intersect += 1
            
        if intersect == length:
            intersect = 0

        # Make sure to remove all non-ship squares to avoid messing with frequencies
        sim_board[sim_board != self.inv_square_states['X']] = 0

        return sim_board, intersect  # Return tuple with True if intersect, False if not

    # Reset the simulation
    def update(self, state):
        self.state = state
        for x in range(self.width):
            for y in range(self.higth):
                c = state.map[x][y]
                if c == ".":
                    self.board[x][y] = 0
                elif c == "~":
                    self.board[x][y] = 1
                elif c == "X":
                    self.board[x][y] = 2
                elif c == "*":
                    self.board[x][y] = 3
                else:
                    raise "cant create one_hot"