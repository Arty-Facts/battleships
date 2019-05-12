from lib.world import World
from lib.state import State
from lib.ship import Ship
from agents.random_agent import RandomAgent
from agents.vidar_agent import HuntTarget
from agents.vidar_agent import HuntTargetParity
from agents.monte_carlo_agent import MonteCarlo
from agents.monte_carlo_sinc_agent import MonteCarloSinc
from random import shuffle
from util.evaluvate import bench, run
from config import *


        
def main():
    world = World(WORLD_SIZE,WORLD_SIZE)
    state = State(WORLD_SIZE,WORLD_SIZE)
    agent = MonteCarloSinc(state, True)
    counter = run(world, agent)
    print("Done in", counter, "moves")
     


if __name__ == "__main__":
    main()
