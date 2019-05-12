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
    while(ships_left(ships) or counter > 2*(WORLD_SIZE**2)):
        counter += 1
        x,y = agent.next_tile()
        hit = world.shot(x,y)
        agent.result(x,y,hit, False)
    return counter

def bench(agent_class, n):
    res = []
    for i in range(n):
        print(i+1, "out of", n, end="\r")
        world = World(WORLD_SIZE,WORLD_SIZE)
        state = State(WORLD_SIZE,WORLD_SIZE)
        agent = agent_class(state)
        res.append(run(world, agent))

    return sum(res)/len(res)


if __name__ == "__main__":
    raise"not a script"