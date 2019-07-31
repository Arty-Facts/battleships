from lib.world import World
from lib.state import State
from lib.ship import Ship
from agents.Qlerning_agent import QlergningAgent
from random import shuffle
from util.evaluvate import bench, run
from config import *


        
def main():
    state = State(WORLD_SIZE_X,WORLD_SIZE_Y)
    agent = QlergningAgent(state, print_out=False)
    for i in range(1_000_000):
        world = World(WORLD_SIZE_X,WORLD_SIZE_Y)
        state = State(WORLD_SIZE_X,WORLD_SIZE_Y)
        agent.state = state
        counter = run(world, agent)
        if i%100 == 0:
            agent.save()
        print("Done in", counter, "moves", "at iteration", i)
     
def eval_agent():
    counter = bench(QlergningAgent, 10 )
    print("\nGames", 10 ,"avg in", counter, "moves")

if __name__ == "__main__":
    #eval_agent()
    main()
    
