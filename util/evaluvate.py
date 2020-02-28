import matplotlib.pyplot as plt
import numpy as np
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
    m = 60
    for i in range(n):
        print(i+1, "out of", n, "latest round", moves, " "*10, end="\r")
        world = World(WORLD_SIZE_X,WORLD_SIZE_Y)
        state = State(WORLD_SIZE_X,WORLD_SIZE_Y)
        agent = agent_class(state)
        moves = run(world, agent)
        if m < moves:
            print()
            print(moves)
            print(state)
            m = moves
        if m >= 80:
            m = 70
        res.append(moves)

    return sum(res)/len(res)


def plotLearning(x, scores, epsilons, filename, lines=None):
    fig=plt.figure()
    ax=fig.add_subplot(111, label="1")
    ax2=fig.add_subplot(111, label="2", frame_on=False)

    ax.plot(x, epsilons, color="C0")
    ax.set_xlabel("Game", color="C0")
    ax.set_ylabel("Epsilon", color="C0")
    ax.tick_params(axis='x', colors="C0")
    ax.tick_params(axis='y', colors="C0")

    N = len(scores)
    running_avg = np.empty(N)
    for t in range(N):
	    running_avg[t] = np.mean(scores[max(0, t-20):(t+1)])

    ax2.scatter(x, running_avg, color="C1")
    #ax2.xaxis.tick_top()
    ax2.axes.get_xaxis().set_visible(False)
    ax2.yaxis.tick_right()
    #ax2.set_xlabel('x label 2', color="C1")
    ax2.set_ylabel('Score', color="C1")
    #ax2.xaxis.set_label_position('top')
    ax2.yaxis.set_label_position('right')
    #ax2.tick_params(axis='x', colors="C1")
    ax2.tick_params(axis='y', colors="C1")

    if lines is not None:
        for line in lines:
            plt.axvline(x=line)

    plt.savefig(filename)
if __name__ == "__main__":
    raise"not a script"