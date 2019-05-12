from lib.world import World
from lib.state import State
from lib.ship import Ship
from agents.random_agent import RandomAgent
from agents.vidar_agent import HuntTarget
from agents.vidar_agent import HuntTargetParity
from agents.monte_carlo_agent import MonteCarlo
from agents.monte_carlo_sinc_agent import MonteCarloSinc
from util.evaluvate import bench, run
from config import *



if __name__ == "__main__":
    agents = [RandomAgent, HuntTarget, HuntTargetParity, MonteCarlo, MonteCarloSinc]
    print("Benshmarking with", BENCHMARK, "games")
    for agent in agents:
        print("{:.2f} moves: {}".format(bench(agent, BENCHMARK), agent.__name__ ))