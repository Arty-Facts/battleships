from ML.nn_agent import NN_Agent
from lib.world import World
from lib.state import State
from lib.ship import Ship
from config import *
from time import time
from random import shuffle
import torch

_size = 10
_ships = 6

def ships_left(ships):
    for s in ships:
        if not s.sunk():
            return True
    return False

def launch(world, ships):
    shuffle(ships)
    #ships.sort(key=lambda s:s.hp, reverse=False)
    for s in ships:
        world.add(s)

def run(world, agent):
    ships = [Ship(i) for i in SHIPS]
    launch(world, ships)
    counter = 0
    while(ships_left(ships) and counter < 2*(WORLD_SIZE_X*WORLD_SIZE_Y)):
        counter += 1
        x,y = agent.next_tile()
        hit = world.shot(x,y)
        agent.result(hit)
    #print(agent.state)
    return counter

def bench(network, n):
    res = []
    targets = []
    for x in range(WORLD_SIZE_X):
        for y in range(WORLD_SIZE_Y):
            targets.append((x,y))
    
    for i in range(n):
        world = World(WORLD_SIZE_X, WORLD_SIZE_Y)
        state = State(WORLD_SIZE_X, WORLD_SIZE_Y)
        agent = NN_Agent(state, network, targets)
        res.append(run(world, agent))

    return sum(res)/len(res)
        


if __name__ == "__main__":
    raise"not a script"
