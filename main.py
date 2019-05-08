from lib.world import World
from lib.state import State
from lib.ship import Ship
from agents.random_agent import RandomAgent
from agents.vidar_agent import HuntTarget
from agents.vidar_agent import HuntTargetParity
from random import shuffle


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
    while(ships_left(ships)):
        counter += 1
        x,y = agent.next_tile()
        hit = world.shot(x,y)
        agent.result(hit)
    return counter
        
def main():
    world = World(_size,_size)
    print(world)
    state = State(_size,_size)
    agent = HuntTargetParity(state, True)

    counter = run(world, agent)
    print("Done in", counter, "moves")


def bench(agent_class, n):
    res = []
    for i in range(n):
        world = World(_size,_size)
        state = State(_size,_size)
        agent = agent_class(state)
        res.append(run(world, agent))

    return sum(res)/len(res)
        


if __name__ == "__main__":
    #main()

    print(bench(RandomAgent, 100000))