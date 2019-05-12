import numpy as np
import matplotlib.pyplot as plt
from random import randint, shuffle
from config import *

class SimulationBoard():
    def __init__(self, state):
        self.size = state.width
        self.width = state.width
        self.higth = state.higth
        self.board = np.zeros((state.width, state.higth), dtype=np.int8)

        self.square_states = {0: '.',
                              1: '~',
                              2: 'X', 
                              3: '*'}
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
        length = 2
        for s in SHIPS:
            if s > 1 and s < self.state.tiles_left:
                length = SHIPS[0]

        # if self.state.ships_left == 1:
        #     length = max(2,self.state.tiles_left)

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