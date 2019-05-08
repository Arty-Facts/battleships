from ML.neural_tagger_trainer import train_neural
from agents.nn_agent import NN_Agent
from agents.vidar_agent import HuntTargetParity
from lib.world import World
from lib.state import State
from lib.ship import Ship
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
    ships = [Ship(i) for i in range(2,_ships)]
    ships.append(Ship(3))
    launch(world, ships)
    counter = 0
    while(ships_left(ships) and counter < 2*(_size**2)):
        counter += 1
        x,y = agent.next_tile()
        hit = world.shot(x,y)
        agent.result(hit)
    print(agent.state)
    return counter

def bench(network, n):
    res = []
    targets = []
    for x in range(_size):
        for y in range(_size):
            targets.append((x,y))
    
    for i in range(n):
        world = World(_size,_size)
        state = State(_size,_size)
        agent = NN_Agent(state, network, targets)
        res.append(run(world, agent))

    return sum(res)/len(res)
        
def main():
    start = time()
    network = train_neural(HuntTargetParity ,State , World, Ship ,_size, _ships, n=1)
    print("training Done in {:.2} min".format((time() - start)*60))
    bench(network, 10)

if __name__ == "__main__":
    main()