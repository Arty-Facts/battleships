from agents.vidar_agent import HuntTargetParity
from lib.world import World
from lib.state import State
from lib.ship import Ship
from config import *
from time import time
from random import shuffle
import torch

def ships_left(ships):
    for s in ships:
        if not s.sunk():
            return True
    return False

def launch(world, ships):
    shuffle(ships)
    #ships.sort(key=lambda s:s.size, reverse=False)
    for s in ships:
        world.add(s)

def run(world, agent):
    ships = [Ship(i) for i in SHIPS]
    launch(world, ships)
    counter = 0
    while(ships_left(ships) or counter > 2*(WORLD_SIZE_X*WORLD_SIZE_Y)):
        counter += 1
        x,y = agent.next_tile()
        hit, sinc = world.shot(x,y)
        agent.result(x,y,hit, sinc)
    return counter

def bench(agent_class, n):
    res = []
    moves = 100
    for i in range(n):
        print(i+1, "out of", n, "latest round", moves, " "*10, end="\r")
        world = World(WORLD_SIZE_X,WORLD_SIZE_Y)
        state = State(WORLD_SIZE_X,WORLD_SIZE_Y)
        agent = agent_class(state)
        moves = run(world, agent)
        res.append(moves)

    return sum(res)/len(res)


if __name__ == "__main__":
    raise"not a script"