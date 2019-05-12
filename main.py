from lib.world import World
from lib.state import State
from lib.ship import Ship
from agents.random_agent import RandomAgent
from agents.vidar_agent import HuntTarget
from agents.vidar_agent import HuntTargetParity
from agents.monte_carlo_agent import MonteCarlo
from random import shuffle
from util.evaluvate import bench, run
from config import *


        
def main():
    world = World(WORLD_SIZE,WORLD_SIZE)
    state = State(WORLD_SIZE,WORLD_SIZE)
    agent = MonteCarlo(state, True)

    counter = run(world, agent)
    print("Done in", counter, "moves")
     


if __name__ == "__main__":
    #main()
    agents = [RandomAgent, HuntTarget, HuntTargetParity, MonteCarlo]
    print("Benshmarking with", BENCHMARK, "games")
    for agent in agents:
        print("{:.2f} moves: {}".format(bench(agent, BENCHMARK), agent.__name__ ))